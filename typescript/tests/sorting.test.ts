import { quicksort } from '../src/sorting/quicksort';
import { mergesort } from '../src/sorting/mergesort';

describe('Sorting Algorithms', () => {
  const unsorted = [5, 2, 9, 1, 5, 6];
  const sorted = [1, 2, 5, 5, 6, 9];

  describe('Quicksort', () => {
    test('should sort an unsorted array', () => {
      expect(quicksort(unsorted)).toEqual(sorted);
    });

    test('should handle empty array', () => {
      expect(quicksort([])).toEqual([]);
    });

    test('should handle large input', () => {
      const largeArr = Array.from({ length: 1000 }, () => Math.floor(Math.random() * 1000));
      const result = quicksort(largeArr);
      const expected = [...largeArr].sort((a, b) => a - b);
      expect(result).toEqual(expected);
    });
  });

  describe('Mergesort', () => {
    test('should sort an unsorted array', () => {
      expect(mergesort(unsorted)).toEqual(sorted);
    });

    test('should handle empty array', () => {
      expect(mergesort([])).toEqual([]);
    });
  });
});
