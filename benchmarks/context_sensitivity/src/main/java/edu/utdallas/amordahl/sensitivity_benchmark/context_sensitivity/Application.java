package edu.utdallas.amordahl.sensitivity_benchmark.context_sensitivity;

public class Application {
    public static void main(String[] args) {
        Application a = new Application();
        a.createA();
        a.createB();
    }

    private void createA() {
        A a = new A();
        intermediate(a);
    }

    private void createB() {
        B b = new B();
        intermediate(b);
    }

    /**
     * edu.utdallas.amordahl.sensitivity_benchmark.context_sensitivty.A correctly-implemented context-sensitive analysis would
     * differentiate the target of this call site based on the caller.
     * edu.utdallas.amordahl.sensitivity_benchmark.context_sensitivty.A context-insensitive analysis would simply say that the target
     * can call both edu.utdallas.amordahl.sensitivity_benchmark.context_sensitivty.A.foo and edu.utdallas.amordahl.sensitivity_benchmark.context_sensitivty.B.foo.
     * @param hf
     */
    private void intermediate(HasFoo hf) {
        hf.foo();
    }


}

