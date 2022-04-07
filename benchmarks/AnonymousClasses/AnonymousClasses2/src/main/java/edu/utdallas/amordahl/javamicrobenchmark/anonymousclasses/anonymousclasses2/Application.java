package edu.utdallas.amordahl.javamicrobenchmark.anonymousclasses.anonymousclasses2;

import java.util.function.Function;
import java.util.function.Supplier;

public class Application {
    public static void main(String[] args) {
        System.out.println(getGreeting(new Supplier<String>() {
            @Override
            public String get() {
                return Application.getStandardGreeting();
            }
        }));
    }

    public static String getGreeting(Supplier<String> greetingGenerator) {
        return greetingGenerator.get();
    }

    public static String getStandardGreeting() {
        return "Hello, everybody!";
    }

}
