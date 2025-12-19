"""
Sorting algorithms with step-by-step visualization
Each function is a generator that yields steps for visualization
"""
from typing import List, Generator, Tuple, Any


def insertion_steps(arr: List[int]) -> Generator[Tuple[str, ...], None, None]:
    """
    Insertion sort with step-by-step visualization
    Yields: (step_type, *args, current_array)
    """
    a = list(arr)
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        yield ("key", i, list(a))
        while j >= 0 and a[j] > key:
            yield ("compare", j, j + 1, list(a))
            a[j + 1] = a[j]
            yield ("shift", j + 1, list(a))
            j -= 1
        a[j + 1] = key
        yield ("insert", j + 1, list(a))
    yield ("done", list(a))


def bubble_steps(arr: List[int]) -> Generator[Tuple[str, ...], None, None]:
    """
    Bubble sort with step-by-step visualization
    Yields: (step_type, *args, current_array)
    """
    a = list(arr)
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            yield ("compare", j, j + 1, list(a))
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                yield ("swap", j, j + 1, list(a))
    yield ("done", list(a))


def selection_steps(arr: List[int]) -> Generator[Tuple[str, ...], None, None]:
    """
    Selection sort with step-by-step visualization
    Yields: (step_type, *args, current_array)
    """
    a = list(arr)
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield ("compare", min_idx, j, list(a))
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            yield ("swap", i, min_idx, list(a))
    yield ("done", list(a))


def merge_steps(arr: List[int]) -> Generator[Tuple[str, ...], None, None]:
    """
    Merge sort with step-by-step visualization
    Yields: (step_type, *args, current_array)
    """
    a = list(arr)
    n = len(a)
    curr_size = 1
    while curr_size < n:
        left_start = 0
        while left_start < n - 1:
            mid = min(left_start + curr_size - 1, n - 1)
            right_end = min(left_start + 2 * curr_size - 1, n - 1)
            yield ("merge", left_start, mid, right_end, list(a))
            temp = [0] * (right_end - left_start + 1)
            i = left_start
            j = mid + 1
            k = 0
            while i <= mid and j <= right_end:
                yield ("compare", i, j, list(a))
                if a[i] <= a[j]:
                    temp[k] = a[i]
                    i += 1
                else:
                    temp[k] = a[j]
                    j += 1
                k += 1
            while i <= mid:
                temp[k] = a[i]
                i += 1
                k += 1
            while j <= right_end:
                temp[k] = a[j]
                j += 1
                k += 1
            for m in range(len(temp)):
                a[left_start + m] = temp[m]
            yield ("merged", left_start, right_end, list(a))
            left_start += 2 * curr_size
        curr_size *= 2
    yield ("done", list(a))


def quick_steps(arr: List[int]) -> Generator[Tuple[str, ...], None, None]:
    """
    Quick sort with step-by-step visualization
    Yields: (step_type, *args, current_array)
    """
    a = list(arr)
    
    def qs(a, l, r):
        if l >= r:
            return
        pivot = a[r]
        i = l
        for j in range(l, r):
            yield ("compare", j, r, list(a))
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                yield ("swap", i, j, list(a))
                i += 1
        a[i], a[r] = a[r], a[i]
        yield ("swap", i, r, list(a))
        yield from qs(a, l, i - 1)
        yield from qs(a, i + 1, r)
    
    yield from qs(a, 0, len(a) - 1)
    yield ("done", a)
