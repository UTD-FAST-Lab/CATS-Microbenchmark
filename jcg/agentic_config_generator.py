import os
import json
from pathlib import Path

import argparse


def get_main_class(project: str, TESTCASE_PATH: str):


    conf_path = TESTCASE_PATH / project / "jcg.conf"

    with open(conf_path) as f:
        data = json.load(f)

    return data['main']



def main():


    parser = argparse.ArgumentParser(description="agentic config generator")
    parser.add_argument("--framework", required=True, help="Framework to analyze ()")
    parser.add_argument("--algorithm", required=True, help="Algorithm to use (e.g., Class Hierarchy Analysis)")

    args = parser.parse_args()

    BASE_PATH = Path(__file__).parent.parent
    TEST_CASE_PATH = BASE_PATH / 'programs'
    bench = 'cats'

    # with open(BASE_PATH / 'missed_projects.txt', 'r') as f:
    #     data = [line.strip() for line in f]


    # missed = []
    # for line in data:
    #     missed.append(line.split(',')[0].strip())


    configs = []
    missed = 0
    # programs = [program for program in os.listdir(TEST_CASE_PATH) if program not in missed]
    
    for program in os.listdir(TEST_CASE_PATH):

        # skip if boundaries.json does not exist or it is empty
        boundaries_path = TEST_CASE_PATH / program / "boundary" / args.framework / args.algorithm / "boundaries.json"
        if not boundaries_path.exists() or boundaries_path.stat().st_size == 0:
            print(f"Skipping {program} because boundaries.json is missing or empty.")
            missed += 1
            continue
        
        program_jar_path = TEST_CASE_PATH / program / f"{program}.jar"
        main_class = get_main_class(program, TEST_CASE_PATH)

        config =  {
            "program_name":    program,
            "target_program":  f"../programs/{bench}/{program}",
            "sa_tool_name":    args.framework,
            "sa_algorithm":    args.algorithm,
            "sa_tool":         f"../tools/{args.framework.lower()}",
            "boundaries_file": f"../input_data/{bench}/{program}/{args.framework}/{args.algorithm}/boundaries.json",
            "main_class": main_class,
            "program_jar_path": f"../programs/{bench}/{program}/{program}.jar"
        }

        configs.append(config)
        
    data = {'analyses' : configs}
    
    print(f"Generated config for {len(configs)} programs. Skipped {missed} programs due to missing or empty boundaries.json.")
    
    with open(BASE_PATH / 'jcg' / f'pipeline_config_{bench}_{args.framework}_{args.algorithm}.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    main()