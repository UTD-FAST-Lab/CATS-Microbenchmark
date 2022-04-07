package edu.utdallas.amordahl.javamicrobenchmark.callsitesensitivity.callsitesensitivity1;

public class A implements HasFoo {
    public void foo() {
        System.out.println("Calling from A");
    }
}
