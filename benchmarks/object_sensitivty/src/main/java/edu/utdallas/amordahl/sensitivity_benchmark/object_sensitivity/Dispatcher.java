package edu.utdallas.amordahl.sensitivity_benchmark.object_sensitivity;

public class Dispatcher {
    private final HasFoo a;

    public Dispatcher(HasFoo a) {
        this.a = a;
    }

    public void callFoo() {
        this.a.foo();
    }
}
