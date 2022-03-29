package edu.utdallas.amordahl.sensitivity_benchmark.object_sensitivity;

public class Application {
    public static void main(String[] args) {
        Dispatcher d1 = new Dispatcher(new A());
        Dispatcher d2 = new Dispatcher(new B());
        d1.callFoo();
        d2.callFoo();
    }
}
