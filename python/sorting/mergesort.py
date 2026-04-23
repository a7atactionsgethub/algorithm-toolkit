"""
Mergesort
Time Complexity: O(n log n)
Space Complexity: O(n)

Description:
A stable, divide-and-conquer sorting algorithm. It divides the array into halves,
recursively sorts them, and then merges the sorted halves.

Use when:
- Stable sorting is required.
- Predictable performance is needed.
"""

def mergesort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    l = r = 0
    
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
            
    result.extend(left[l:])
    result.extend(right[r:])
    return result

if __name__ == "__main__":
    test_arr = [38, 27, 43, 3, 9, 82, 10]
    sorted_arr = mergesort(test_arr)
    assert sorted_arr == [3, 9, 10, 27, 38, 43, 82]
    print("Python Mergesort: All tests passed!")
