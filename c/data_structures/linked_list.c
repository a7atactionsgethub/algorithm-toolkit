/**
 * Singly Linked List
 * Time Complexity:
 * - Access/Search: O(n)
 * - Insertion/Deletion (Head): O(1)
 * Space Complexity: O(n)
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

typedef struct Node {
    int value;
    struct Node* next;
} Node;

typedef struct LinkedList {
    Node* head;
    int size;
} LinkedList;

LinkedList* createList() {
    LinkedList* list = (LinkedList*)malloc(sizeof(LinkedList));
    list->head = NULL;
    list->size = 0;
    return list;
}

void append(LinkedList* list, int value) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->value = value;
    newNode->next = NULL;

    if (list->head == NULL) {
        list->head = newNode;
    } else {
        Node* current = list->head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = newNode;
    }
    list->size++;
}

void freeList(LinkedList* list) {
    Node* current = list->head;
    while (current != NULL) {
        Node* next = current->next;
        free(current);
        current = next;
    }
    free(list);
}

int main() {
    LinkedList* ll = createList();
    append(ll, 1);
    append(ll, 2);
    append(ll, 3);

    assert(ll->size == 3);
    assert(ll->head->value == 1);
    assert(ll->head->next->value == 2);
    assert(ll->head->next->next->value == 3);

    printf("C Linked List: All tests passed!\n");
    freeList(ll);
    return 0;
}
