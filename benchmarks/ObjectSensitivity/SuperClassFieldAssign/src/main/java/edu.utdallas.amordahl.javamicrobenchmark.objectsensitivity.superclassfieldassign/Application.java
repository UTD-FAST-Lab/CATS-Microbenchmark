package edu.utdallas.amordahl.javamicrobenchmark.objectsensitivity.superclassfieldassign;

public class Application {
    public static void main(String[] args) {
        Y y = new Y();
        Z z = new Z();
        B b = new B(y);
        C c = new C(c);

        b.m();
        c.m();
    }
}
