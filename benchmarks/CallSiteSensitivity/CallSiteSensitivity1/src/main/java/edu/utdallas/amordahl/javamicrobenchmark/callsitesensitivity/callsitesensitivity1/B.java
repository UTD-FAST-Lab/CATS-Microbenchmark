package edu.utdallas.amordahl.javamicrobenchmark.callsitesensitivity.callsitesensitivity1;

public class B implements HasFoo{
    public void foo() {
        System.out.println("Calling from B");
    }
}
