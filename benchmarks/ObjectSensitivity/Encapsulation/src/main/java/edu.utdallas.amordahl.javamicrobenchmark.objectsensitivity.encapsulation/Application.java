package edu.utdallas.amordahl.javamicrobenchmark.objectsensitivity.encapsulation;

public class Application {
    public static void main(String[] args) {
        A a1 = new A();
        A a2 = new A();
        B b1 = new B();
        B b2 = new B();

        b1.setA(a1);
        b2.setA(a2);
    }
}
