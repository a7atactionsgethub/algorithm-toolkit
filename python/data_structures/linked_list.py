"""
Singly Linked List
Time Complexity:
- Access/Search: O(n)
- Insertion/Deletion (Head): O(1)
Space Complexity: O(n)

Description:
A linear data structure where elements are not stored in contiguous memory.
Each node contains a value and a pointer to the next node.
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

if __name__ == "__main__":
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]
    print("Python Linked List: All tests passed!")
