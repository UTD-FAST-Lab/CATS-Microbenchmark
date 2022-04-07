package edu.utdallas.amordahl.javamicrobenchmark.objectsensitivity.objectsensitivity1;

public class Dispatcher {
    private final HasFoo a;

    public Dispatcher(HasFoo a) {
        this.a = a;
    }

    public void callFoo() {
        this.a.foo();
    }
}
