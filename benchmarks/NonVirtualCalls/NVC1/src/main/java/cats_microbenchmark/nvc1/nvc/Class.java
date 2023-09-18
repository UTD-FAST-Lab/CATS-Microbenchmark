// nvc/Class.java
package cats_microbenchmark.nvc1.nvc;

//import lib.annotations.callgraph.DirectCall;

class Class {

    public static void method(){ /* do something*/}
    public static void method(int param){ /* do something*/}

//    @DirectCall(name = "method", line = 12, resolvedTargets = "Lnvc/Class;")
    public static void main(String[] args){
        Class.method();
    }
}
