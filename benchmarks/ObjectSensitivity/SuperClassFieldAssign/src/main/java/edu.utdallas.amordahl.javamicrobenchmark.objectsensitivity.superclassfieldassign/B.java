package edu.utdallas.amordahl.javamicrobenchmark.objectsensitivity.superclassfieldassign;

public class B extends A {
    X f;

    B (X xb) {
        super(xb);
    }

    void m() {
        X xb = this.f;
        xb.n();
    }
}