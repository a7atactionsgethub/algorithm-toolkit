"""
Binary Search
Time Complexity: O(log n)
Space Complexity: O(1)

Description:
Searches for a target value within a sorted array by repeatedly dividing the search interval in half.

Use when:
- Array is sorted.

Avoid when:
- Array is unsorted.
"""

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

if __name__ == "__main__":
    # Quick test
    test_arr = [1, 3, 5, 7, 9, 11]
    assert binary_search(test_arr, 7) == 3
    assert binary_search(test_arr, 1) == 0
    assert binary_search(test_arr, 10) == -1
    print("Python Binary Search: All tests passed!")
