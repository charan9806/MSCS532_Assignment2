from __future__ import annotations
from typing import List
import random

def quicksort(arr: List[int]) -> List[int]:

    # If the list is empty or just has one thing, it's already sorted. Easy!
    if len(arr) <= 1:
        return arr

    # Grab a random number from the list to use as our "splitter."
    pivot = random.choice(arr)

    # Break the list into three piles: smaller than the splitter, equal to it, and bigger.
    # This way duplicates usually don't mess us up.
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Now, sort the smaller pile and the bigger pile, then glue them all back together.
    return quicksort(left) + mid + quicksort(right)


def mergesort(arr: List[int]) -> List[int]:

    # Same deal: if it's super short, it's already good to go.
    if len(arr) <= 1:
        return arr

    # Split the list right down the middle.
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])

    # Put the two sorted halves back together into one big sorted list.
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    # Take two lists that are already sorted and zip them together into one.
    merged = []
    i, j = 0, 0

    # Keep looking at the front of both lists and pick the smaller one to add next.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # If there's anything left over in either pile, just tack it on the end.
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


