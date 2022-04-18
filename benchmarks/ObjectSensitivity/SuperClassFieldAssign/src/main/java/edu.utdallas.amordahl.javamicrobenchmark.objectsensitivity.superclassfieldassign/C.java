package edu.utdallas.amordahl.javamicrobenchmark.objectsensitivity.superclassfieldassign;

public class C extends A {
    X f;

    C (X xc) {
        super(xc);
    }

    void m() {
        X xc = this.f;
        xc.n();
    }
}