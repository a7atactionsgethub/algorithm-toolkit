/**
 * Singly Linked List
 * 
 * A linear data structure where elements are not stored in contiguous memory locations.
 * 
 * Time Complexity:
 * - Access: O(n)
 * - Search: O(n)
 * - Insertion (at head): O(1)
 * - Deletion (at head): O(1)
 * 
 * Use when:
 * - Frequent insertions and deletions are required.
 * - Dynamic size is needed without pre-allocation.
 * 
 * Avoid when:
 * - Random access is required.
 * - Memory overhead of pointers is a concern.
 */

class LinkedListNode<T> {
  constructor(public value: T, public next: LinkedListNode<T> | null = null) {}
}

export class LinkedList<T> {
  private head: LinkedListNode<T> | null = null;
  private size: number = 0;

  /**
   * Add an element to the front of the list.
   */
  prepend(value: T): void {
    this.head = new LinkedListNode(value, this.head);
    this.size++;
  }

  /**
   * Add an element to the end of the list.
   */
  append(value: T): void {
    const newNode = new LinkedListNode(value);
    if (!this.head) {
      this.head = newNode;
    } else {
      let current = this.head;
      while (current.next) {
        current = current.next;
      }
      current.next = newNode;
    }
    this.size++;
  }

  /**
   * Remove the first occurrence of a value.
   */
  remove(value: T): boolean {
    if (!this.head) return false;

    if (this.head.value === value) {
      this.head = this.head.next;
      this.size--;
      return true;
    }

    let current = this.head;
    while (current.next && current.next.value !== value) {
      current = current.next;
    }

    if (current.next) {
      current.next = current.next.next;
      this.size--;
      return true;
    }

    return false;
  }

  toArray(): T[] {
    const arr: T[] = [];
    let current = this.head;
    while (current) {
      arr.push(current.value);
      current = current.next;
    }
    return arr;
  }

  getSize(): number {
    return this.size;
  }
}
