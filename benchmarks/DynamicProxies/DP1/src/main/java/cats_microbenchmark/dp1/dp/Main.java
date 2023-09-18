// dp/Main.java
package cats_microbenchmark.dp1.dp;

//import lib.annotations.callgraph.IndirectCall;

public class Main {
//    @IndirectCall(
//            name = "bar", returnType = Object.class, parameterTypes = Object.class, line = 17,
//            resolvedTargets = "Ldp/FooImpl;"
//    )
//    @IndirectCall(
//            name = "invoke", returnType = Object.class, parameterTypes = {Object.class, Method.class, Object[].class}, line = 17,
//            resolvedTargets = "Ldp/DebugProxy;"
//    )
    public static void main(String[] args) {
        Foo foo = (Foo) DebugProxy.newInstance(new FooImpl());
        foo.bar(null);
    }
}


