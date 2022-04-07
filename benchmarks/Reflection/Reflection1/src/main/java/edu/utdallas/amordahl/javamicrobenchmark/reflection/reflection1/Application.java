package edu.utdallas.amordahl.javamicrobenchmark.reflection.reflection1;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Application {
    public static void main(String[] args) {
        Application a = new Application();
        a.printGreeting();
    }

    public void printGreeting() {
        try {
            Class clazz = Class.forName("edu.utdallas.amordahl.javamicrobenchmark.reflection.reflection1.ReflectionTarget");
            Constructor ct = clazz.getConstructor();
            Method getGreeting = clazz.getMethod("getGreeting");
            System.out.println(getGreeting.invoke(ct.newInstance()));
        } catch (ClassNotFoundException | NoSuchMethodException cnfe) {
            System.out.println("Could not find reflection target.");
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
    }

}
