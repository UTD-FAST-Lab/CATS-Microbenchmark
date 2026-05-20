import argparse
import os
import subprocess
import sys
import json
import shutil
from pathlib import Path
import re
from typing import Optional, List, Dict
from datetime import datetime


config = {
    "BASE_DIR": Path("/20TB/mohammad/benchmarks/CATS-Microbenchmark"),
    "UID": os.getuid(),
    "GID": os.getgid(),
    "TESTCASE_PATH": Path("/20TB/mohammad/benchmarks/CATS-Microbenchmark/programs"),
    "STATICCG_TIMEOUT": "350m",  
    "STATICCG_MEMORY": "400G", 
    "STATICCG_CONTAINER": "staticcg_container",
    "DYNAMICCG_CONTAINER": "dyncg_container",
    "BOUNDARY_CONTAINER": "boundary_container",
    "JCG_IMAGE": "jcg_image",
}


def static_callgraph(framework: str, algo: str, project: str):
    """Generate static call graph"""
    build_jcg_image()
    
    staticcg_path = config["TESTCASE_PATH"] / project / "staticcg"
    temp_dir = config["TESTCASE_PATH"] / project
    os.makedirs(staticcg_path, exist_ok=True)

    mounts = [
        (str(temp_dir), "/repo", True),

        (str(config["TESTCASE_PATH"] / project / "jcg.conf"), f"/jcg-conf/{project}.conf", True),
        (str(staticcg_path), "/staticcg", False),
    ]
    
    cmd = [
        config["STATICCG_TIMEOUT"],
        config["STATICCG_MEMORY"],
        "runMain", "Evaluation",
        "--input", "/jcg-conf/",
        "--output", "/staticcg",
        "--adapter", framework,
        "--algorithm-prefix", algo,
        "--project-prefix", project,
        "--debug"
    ]
    
    docker_remove(config["STATICCG_CONTAINER"])
    docker_run(config["STATICCG_CONTAINER"], config["JCG_IMAGE"], mounts, cmd)


def dynamic_callgraph(project: str):
    """Generate dynamic call graph for a specific experiment directory"""
    build_jcg_image()
    
    dyncg_path = config["TESTCASE_PATH"] / project / "dyncg"
    temp_dir = config["TESTCASE_PATH"] / project
    os.makedirs(dyncg_path, exist_ok=True)

    mounts = [
        (str(temp_dir), "/repo", True),

        (str(config["TESTCASE_PATH"] / project / "jcg.conf"), f"/jcg-conf/{project}.conf", True),
        (str(dyncg_path), "/dyncg", False),
    ]
    
    cmd = [
        config["STATICCG_TIMEOUT"],
        config["STATICCG_MEMORY"],
        "runMain", "Evaluation",
        "--input", "/jcg-conf/",
        "--output", "/dyncg",
        "--adapter", "Dynamic",
        "--algorithm-prefix", "Dynamic",
        "--project-prefix", project,
        "--debug"
    ]
    
    docker_remove(config["DYNAMICCG_CONTAINER"])
    docker_run(config["DYNAMICCG_CONTAINER"], config["JCG_IMAGE"], mounts, cmd)


def boundary_generation(framework: str, algo: str, project: str):
    """Generate boundary call graph for a specific experiment directory"""
    
    build_jcg_image()
    
    dyncg_path = config["TESTCASE_PATH"] / project / "dyncg" / project / "Dynamic" / "Dynamic"
    staticcg_path = config["TESTCASE_PATH"] / project / "staticcg" / project / framework / algo
    boundary_path = config["TESTCASE_PATH"] / project / "boundary" / framework / algo

    # if os.path.exists(boundary_path / "boundaries.json"):
    #     return  # Boundary already generated, skip

    if not os.path.exists(dyncg_path / "cg.json"):
        try:
            dynamic_callgraph(project)
        except Exception as e:
            print(f"Error occurred while generating dynamic call graph for {project}: {e}")


    if not os.path.exists(dyncg_path / "cg.json"):
        return (1, "dynamic")


    if not os.path.exists(staticcg_path / "cg.json"):
        try:
            static_callgraph(framework, algo, project)
        except Exception as e:
            print(f"Error occurred while generating static call graph for {project} with {framework} and {algo}: {e}")

    if not os.path.exists(staticcg_path / "cg.json"):
        return (1, f"static-{framework}-{algo}")


    os.makedirs(boundary_path, exist_ok=True)

    mainClass = get_main_class(project)
    
    mounts = [
        (str(dyncg_path), "/dynamiccg", True),
        (str(staticcg_path), "/staticcg", True),
        (str(boundary_path), "/output", False),
    ]
    
    cmd = [
        config["STATICCG_TIMEOUT"],
        config["STATICCG_MEMORY"],
        "runMain", "CompareCGs",
        "--input1", "/staticcg/cg.json",
        "--input2", "/dynamiccg/cg.json",
        "--mainClass", mainClass,
        "--output", "/output",
        "--showPrecisionRecall", "all",
        "--showBoundaries",
        "--nonStrict"
    ]
    
    docker_remove(config["BOUNDARY_CONTAINER"])
    try:
        docker_run(config["BOUNDARY_CONTAINER"], config["JCG_IMAGE"], mounts, cmd)
    except Exception as e:
        print(f"Error occurred while generating boundary call graph for {project}: {e}")

    return (0, "success")


def project_build(project: str):
    """Build a project"""
    build_cmd = ["mvn", "clean", "package", "-DskipTests"]
    run_command(build_cmd, cwd=config["TESTCASE_PATH"] / project / "target")

def docker_remove(container: str):
    """Remove a Docker container"""
    run_command(["docker", "rm", "-f", container], check=False)


def run_command(cmd: List[str], cwd: Optional[Path] = None, 
                capture_output: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command"""
    print(f"Running: {' '.join(str(c) for c in cmd)}")
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        check=check
    )

def docker_run(name: str, image: str, mounts: List[tuple], 
                cmd: Optional[List[str]] = None, entrypoint: Optional[str] = None,
                interactive: bool = True, redirect_output: Optional[Path] = None,
                env: Optional[Dict[str, str]] = None, tee_output: bool = False):
    """Run a Docker container"""
    docker_cmd = ["docker", "run"]
    
    if interactive:
        docker_cmd.append("-it")
    
    docker_cmd.extend(["--name", name])

    if env:
        for key, value in env.items():
            docker_cmd.extend(["-e", f"{key}={value}"])
    
    for source, target, readonly in mounts:
        mount_str = f"type=bind,source={source},target={target}"
        if readonly:
            mount_str += ",readonly"
        docker_cmd.extend(["--mount", mount_str])
    
    if entrypoint:
        docker_cmd.extend(["--entrypoint", entrypoint])
    
    docker_cmd.append(image)
    
    if cmd:
        docker_cmd.extend(cmd)
    
    if redirect_output:
        if tee_output:
            # Use tee to show output AND save to file
            tee_cmd = " ".join([str(c) for c in docker_cmd]) + f" 2>&1 | tee {redirect_output}"
            subprocess.run(tee_cmd, shell=True)
        else:
            # Just redirect to file
            with open(redirect_output, "w") as f:
                subprocess.run(docker_cmd, stdout=f, stderr=subprocess.STDOUT)
    else:
        run_command(docker_cmd)

def build_jcg_image():
    """Build JCG Docker image"""
    context = config["BASE_DIR"] / "jcg"
    dockerfile = context / "Dockerfile"
    build_args = {
        "UID": config["UID"],
        "GID": config["GID"]
    }
    docker_build(config["JCG_IMAGE"], dockerfile, context, build_args)
    

def docker_build(tag: str, dockerfile: Path, context: Path, 
                    build_args: Optional[dict] = None, output: Optional[Path] = None):
        """Build a Docker image"""
        cmd = ["docker", "build", f"--tag={tag}"]
        
        if build_args:
            for key, value in build_args.items():
                cmd.extend(["--build-arg", f"{key}={value}"])
        
        if output:
            cmd.extend(["--output", str(output)])
        
        cmd.extend(["-f", str(dockerfile), str(context)])
        run_command(cmd)



def extract_main_class(src_dir):
    """
    Find a class with a main method in src_dir.
    Returns fully qualified class name or None.
    """
    MAIN_CLASS_CANDIDATES = {"Main", "Demo", "Class"}

    for dirpath, _, filenames in os.walk(src_dir):
        for file in filenames:
            if not file.endswith(".java"):
                continue

            class_name = file[:-5]

            if class_name not in MAIN_CLASS_CANDIDATES:
                continue

            file_path = os.path.join(dirpath, file)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Check for main method
            if "public static void main" not in content:
                continue

            # Extract package
            match = re.search(r'package\s+([\w\.]+);', content)
            if match:
                package = match.group(1)
                return f"{package}.{class_name}"
            else:
                return class_name  # default package

    return None


def create_jcg_conf(project: str, main_class: str):
    """Create a jcg.conf file for a project"""
    conf_content = {
        "name": project,
        "target": f"/repo/{project}.jar",
        "main": main_class,   # <-- added this
        "java": 8,
        "jvm_args": ["-Djava.library.path=/repo/"],
        "cp": [{
            "path": f"/repo/{project}.jar"
        }]
    }

    conf_path = config["TESTCASE_PATH"] / project / "jcg.conf"

    with open(conf_path, "w") as f:
        json.dump(conf_content, f, indent=4)


def get_main_class(project: str):


    conf_path = config["TESTCASE_PATH"] / project / "jcg.conf"

    with open(conf_path) as f:
        data = json.load(f)

    return data['main']


def collect_jars(root_dir, output_base="programs"):
    if not os.path.exists(root_dir):
        raise ValueError(f"Root directory does not exist: {root_dir}")

    os.makedirs(output_base, exist_ok=True)

    for dirpath, _, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) != "target":
            continue

        project_root = Path(dirpath).parent
        src_dir = project_root / "src"

        for file in filenames:
            if not file.endswith(".jar"):
                continue

            jar_path = os.path.join(dirpath, file)
            jar_name = os.path.splitext(file)[0]

            dest_dir = os.path.join(output_base, jar_name)
            os.makedirs(dest_dir, exist_ok=True)

            dest_path = os.path.join(dest_dir, file)
            shutil.copy2(jar_path, dest_path)

            print(f"Copied: {jar_path} -> {dest_path}")

            # 🔍 Find main class
            main_class = None
            if src_dir.exists():
                main_class = extract_main_class(src_dir)

            if main_class is None:
                print(f"[WARNING] No main class found for {jar_name}")
                continue

            # 🧾 Create config
            create_jcg_conf(jar_name, main_class)


def main():
    parser = argparse.ArgumentParser(description="JCG Runner")
    parser.add_argument("--framework", required=False, help="Framework to analyze ()")
    parser.add_argument("--algorithm", required=False, help="Algorithm to use (e.g., Class Hierarchy Analysis)")
    parser.add_argument("--project", required=False, help="Project name (must match test case directory)")
    parser.add_argument("--type", required=True, choices=["static", "dynamic", "boundary"], help="Type of call graph to generate")
    
    args = parser.parse_args()

    if not os.path.exists(config["TESTCASE_PATH"]):
        collect_jars(config["BASE_DIR"] / "benchmarks" , output_base=config["TESTCASE_PATH"])
     
    if args.project:
        projects = [args.project]
    else:
        projects = os.listdir(config["TESTCASE_PATH"])

    for project in projects:
        args.project = project   

        if args.type == "static":
            if not args.framework or not args.algorithm:
                print("Error: --framework and --algorithm are required for static call graph generation")
                sys.exit(1)
            static_callgraph(args.framework, args.algorithm, args.project)
        elif args.type == "dynamic":
            dynamic_callgraph(args.project)

        elif args.type == "boundary":
            code , text = boundary_generation(args.framework, args.algorithm, args.project)

            if code == 1:
                with open(config["BASE_DIR"] / "missed_projects.txt", "a") as f:
                    f.write(project + "," + text + "\n")

if __name__ == "__main__":
    main()