package edu.utdallas.amordahl.javamicrobenchmark.anonymousclasses.anonymousclasses1;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public class Application {
    public static void main(String[] args) {
        // Create an array of integers.
        List<Integer> intList = new ArrayList<>();
        Random random = new Random();
        while (intList.size() < 10)
            intList.add(random.nextInt());

        // Anonymous class to reverse sort.
        intList.sort(new Comparator<Integer>() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return Application.compareInts(o1, o2);
            }
        });

        System.out.println(String.format("Sorted list is %s", intList));
    }

    public static int compareInts(Integer o1, Integer o2) {
        return o2.compareTo(o1);
    }
}
