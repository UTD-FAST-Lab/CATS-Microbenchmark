package edu.utdallas.amordahl.sensitivity_benchmark.call_site_sensitivity;

public class A implements HasFoo {
    public void foo() {
        System.out.println("Calling from A");
    }
}
