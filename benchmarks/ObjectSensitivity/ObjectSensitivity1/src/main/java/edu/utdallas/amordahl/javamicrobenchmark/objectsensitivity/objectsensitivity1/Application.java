package edu.utdallas.amordahl.javamicrobenchmark.objectsensitivity.objectsensitivity1;

public class Application {
    public static void main(String[] args) {
        Dispatcher d1 = new Dispatcher(new A());
        Dispatcher d2 = new Dispatcher(new B());
        d1.callFoo();
        d2.callFoo();
    }
}
