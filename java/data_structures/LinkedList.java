package data_structures;

import java.util.ArrayList;
import java.util.List;

/**
 * Singly Linked List
 * Time Complexity:
 * - Access/Search: O(n)
 * - Insertion/Deletion (Head): O(1)
 * Space Complexity: O(n)
 */
public class LinkedList<T> {

    private static class Node<T> {
        T value;
        Node<T> next;

        Node(T value) {
            this.value = value;
        }
    }

    private Node<T> head;
    private int size;

    public void append(T value) {
        Node<T> newNode = new Node<>(value);
        if (head == null) {
            head = newNode;
        } else {
            Node<T> current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        size++;
    }

    public List<T> toList() {
        List<T> list = new ArrayList<>();
        Node<T> current = head;
        while (current != null) {
            list.add(current.value);
            current = current.next;
        }
        return list;
    }

    public static void main(String[] args) {
        LinkedList<Integer> ll = new LinkedList<>();
        ll.append(1);
        ll.append(2);
        ll.append(3);
        assert ll.toList().equals(List.of(1, 2, 3));
        System.out.println("Java Linked List: All tests passed!");
    }
}
