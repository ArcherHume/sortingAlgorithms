#!/usr/bin/env python
""" 
This file contains the logic/methods for the sorting algorithms.

This is a library file and cannot be run directly.

To add a new sorting algorithm, simply add a new function with the @algorithm_wrapper decorator taking array and delay as a parameter.

Please Note: These files are greatly overdocumented, this is because this is to be used as an educational tool, it should be understandable with zero python knowledge.
"""


import time


__author__ = "Archer Hume"
__copyright__ = "Copyright (C) 2022 Archer Hume"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Archer Hume"
__email__ = "archer@hume.email"
__status__ = "Development"

__algorithms__ = [] # This is a list that will contain all of the algorithms.


def algorithm_wrapper(func): # This is a decorator that will add the algorithm to the list of algorithms.
    """Decorator that will add the algorithm to the list of algorithms.

    Args:
        func (function): The algorithm to be added.
    """
    __algorithms__.append(func) # Add the algorithm to the list of algorithms.


@algorithm_wrapper # @ symbol assigns the decorator to the function.
def selection(sorting_array, delay):
    """ Selection sort algorithm. """
    STORED_LENGTH = len(sorting_array) # Length is stored to reduce the amount of times the length is calculated (Slows down algorithm to call len() often).
    
    for array_index in range(STORED_LENGTH): # For each element in the array...
        minimum_index = array_index # Set the minimum index to the current index.
        for search_index in range(array_index + 1, STORED_LENGTH): # For each element after the current array index...
            if sorting_array[search_index] < sorting_array[minimum_index]: # If the current element is less than the current minimum...
                minimum_index = search_index # Set the minimum index to the current index.
        # Swap the minimum index with the current index.
        sorting_array[array_index], sorting_array[minimum_index] = sorting_array[minimum_index], sorting_array[array_index]
        # Sleep for specified delay.
        if delay: time.sleep(delay)


@algorithm_wrapper
def selection_recursive(sorting_array, delay):
    """ Recursive selection sort algorithm. 
    
    DISCLAIMER: Due to the nature of the algorithm (recursion), it becomes unstable with large arrays.        
    """
    STORED_LENGTH = len(sorting_array) # Length is stored to reduce the amount of times the length is calculated (Slows down algorithm to call len() often).
    
    def _sort(item_index):
        """Nested function used to sort the array, recursive.
        Args:
            item_index (int): First index of unsorted section.
        """
        # If the item index is greater than the length of the array (Out of bounds), kill function.
        if item_index >= STORED_LENGTH: return
        
        minimum_index = item_index # Set the minimum index to the current index.
        for search_index in range(item_index + 1, STORED_LENGTH): # For each element after the current array index...
            if sorting_array[search_index] < sorting_array[minimum_index]: # If the current element is less than the current minimum...
                minimum_index = search_index # Set the minimum index to the current index.
        
        # Swap the minimum index with the current index.
        sorting_array[item_index], sorting_array[minimum_index] = sorting_array[minimum_index], sorting_array[item_index]
        # Sleep for specified delay.
        if delay: time.sleep(delay)
        
        # Recursively call the sort function with the next index.
        _sort(item_index+1)
    
    # Start the recursive sort function.
    _sort(0)


@algorithm_wrapper
def bubble(sorting_array, delay):
    """ Bubble sorting algorithm. """
    STORED_LENGTH = len(sorting_array) # Length is stored to reduce the amount of times the length is calculated (Slows down algorithm to call len() often).
    
    for _ in sorting_array: # For each element in the array (Index not used so it is assigned to underscore)...
        for search_index in range(STORED_LENGTH - 1): # For each element after the current item index...
            if sorting_array[search_index] > sorting_array[search_index + 1]: # If the current element is greater than the next element...
                # Swap the current element with the next element.
                sorting_array[search_index], sorting_array[search_index + 1] = sorting_array[search_index + 1], sorting_array[search_index]
        # Sleep for specified delay.
        if delay: time.sleep(delay)


@algorithm_wrapper
def quick_sort(sorting_array, delay):
    """ Quick sort algorithm. """
    
    def _quickSort(array, start, end):
        """Nested function used to sort the array, recursive.
        Args:
            array (array): Array to be sorted.
            start (int): First index of unsorted section.
            end (int): Last index of unsorted section.
        """
        if start >= end: return # If the start index is greater than or equal to the end index, kill function.
        
        # Set the pivot to the first element in the array.
        pivot = partition(array, start-1, end)
        # Run the quick sort algorithm on the left side of the pivot.
        _quickSort(array, start, pivot - 1)
        # Run the quick sort algorithm on the right side of the pivot.
        _quickSort(array, pivot + 1, end)
    
    def partition(array, start, end):
        """ Nested function used to partition & sort the array.
        Args:
            array (array): Array to be sorted.
            start (int): First index of unsorted section.
            end (int): Last index of unsorted section.
        Returns:
            int: Index of the pivot.
        """
        
        pivot = array[end] # Set the pivot to the last element in the array.
        
        for search_index in range(start+1, end): # For each element in the array (between start and end)...
            if array[search_index] <= pivot: # If the current element is less than or equal to the pivot...
                start += 1 # Increment the start index.
                array[start], array[search_index] = array[search_index], array[start] # Swap the current element with the index.
            # Sleep for specified delay.
            if delay: time.sleep(delay)
        
        # Swap the pivot with the index.
        array[start+1], array[end] = array[end], array[start+1]
        
        # Sleep for specified delay.
        if delay: time.sleep(delay)
        
        # Return the index of the pivot.
        return start + 1
    
    # Start the recursive sort function.
    _quickSort(sorting_array, 0, len(sorting_array) - 1)

