#!/usr/bin/env python
""" 
This module contains the sorting algorithms and the logic for the backend of the project.

This is a library file and cannot be run directly.

Please Note: These files are greatly overdocumented, this is because this is to be used as an educational tool, it should be understandable with zero python knowledge.
"""

import cProfile
import random
import sys
import threading
import time


__author__ = "Archer Hume"
__copyright__ = "Copyright (C) 2022 Archer Hume"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Archer Hume"
__email__ = "archer@hume.email"
__status__ = "Development"


sys.setcheckinterval(1) # Set the interpreter check interval to 1 (Higher thread switching frequency increases delay accuracy).


class AlgorithmExistanceError(Exception):
    """Algorithm does not exist.

    Custom exception to be called when an algorithm does not exist."""
    pass


class Algorithm:
    """Algorithm class that handles all backend processing and sorting for the script."""
    
    def __init__(self, length, algorithm, repeats=3, delay=0, debug=False) -> None:
        """Initialize the algorithm class.

        Args:
            length (int): The length of the array to be sorted.
            algorithm (str): The algorithm to be run.
            repeats (int, optional): Amount of times algorithm will repeat. Defaults to 3.
            delay (int, optional): The delay between algorithm steps. Defaults to 0.

        Raises:
            AlgorithmExistanceError: When the algorithm does not exist.
        """
        self._display_name = "Algorithm" # The display name of the algorithm to be shown on the screen
        self._array_length = length # The length of the array to be sorted, stored so that on repeats the array can be recreated.
        self._finished_times, self.sorting_array = [], [] # The run times to be stored when an algorithm has finished running and the placeholder array to be sorted.
        self._running = True # Whether or not the algorithm is currently running.
        self._start_time = time.time() # Placeholder start time, will be used to measure algorithms run times.
        self._algorithm_delay = delay # The delay between each algorithm step.
        self._debug = debug # Whether or not the algorithm should be run in debug mode.
        self._algorithm_types = {
            "selection": self.selectionSort, 
            "selection-r": self.recursiveSelectionSort, 
            "bubble": self.bubbleSort, 
            "quick": self.quickSort
            } # Dictionary of all the algorithms that can be run.
        
        # If the algorithm is in the dictionary, run it.
        if algorithm in self._algorithm_types: 
            self.start(algorithm, repeats)
        else: # If the algorithm is not in the dictionary, raise an error.
            raise AlgorithmExistanceError("Algorithm does not exist")

    def getCurrentTime(self):
        """Get the current time of the algorithm.

        Returns:
            float: The current time in seconds.
        """
        return time.time() - self._start_time

    def start(self, algorithm, repeats):
        """Start the algorithm.

        Args:
            algorithm (function): The algorithm to be run.
            repeats (int): Amount of times algorithm will repeat.
        """
        
        def _loop():
            """Nested function used to enclose the algorithm start instructions."""
            for _ in range(repeats): # Repeat the algorithm the amount of times specified.
                self.sorting_array = random.sample(list(range(1, self._array_length + 1)), self._array_length) # Create a new array to be sorted.
                
                if self._debug: # If the algorithm is in debug mode...
                    p = cProfile.Profile() # Create a new profile object to be used to measure the debug data of the algorithm.
                    p.runcall(self._algorithm_types[algorithm]) # Run the algorithm with the profile object.
                    p.print_stats() # Print the debug data of the algorithm.
                else:
                    self._algorithm_types[algorithm]()
        
        # Create a new thread to run the algorithm start instructions.
        # This is done to prevent the main thread that runs the UI from freezing while the algorithm 
        # is running and prevents general interference between UI and algorithms.
        self.thread = threading.Thread(target=_loop)
        self.thread.start() # Start the thread.
    
    def selectionSort(self):
        """ Selection sort algorithm. """
        self._running = True # Sets the algorithm to running.
        self._start_time = time.time() # Sets the start time of the algorithm.
        self._display_name = "Selection Sort" # Sets the display name of the algorithm.
        STORED_LENGTH = len(self.sorting_array) # Length is stored to reduce the amount of times the length is calculated (Slows down algorithm to call len() often).
        
        for array_index in range(STORED_LENGTH): # For each element in the array...
            minimum_index = array_index # Set the minimum index to the current index.
            for search_index in range(array_index + 1, STORED_LENGTH): # For each element after the current array index...
                if self.sorting_array[search_index] < self.sorting_array[minimum_index]: # If the current element is less than the current minimum...
                    minimum_index = search_index # Set the minimum index to the current index.
            # Swap the minimum index with the current index.
            self.sorting_array[array_index], self.sorting_array[minimum_index] = self.sorting_array[minimum_index], self.sorting_array[array_index]
            # Sleep for specified delay.
            if self._algorithm_delay: time.sleep(self._algorithm_delay)
        
        self._finished_times.append(time.time() - self._start_time) # Add the time taken to the finished times list.
        self._running = False # Set the algorithm to not running.
    
    def recursiveSelectionSort(self):
        """ Recursive selection sort algorithm. 
        
        DISCLAIMER: Due to the nature of the algorithm (recursion), it becomes unstable with large arrays.        
        """
        self._running = True # Sets the algorithm to running.
        self._start_time = time.time() # Sets the start time of the algorithm.
        self._display_name = "Recursive Selection Sort" # Sets the display name of the algorithm.
        STORED_LENGTH = len(self.sorting_array) # Length is stored to reduce the amount of times the length is calculated (Slows down algorithm to call len() often).
        
        def _sort(item_index):
            """Nested function used to sort the array, recursive.

            Args:
                item_index (int): First index of unsorted section.
            """
            # If the item index is greater than the length of the array (Out of bounds), kill function.
            if item_index >= STORED_LENGTH: return
            
            minimum_index = item_index # Set the minimum index to the current index.
            for search_index in range(item_index + 1, STORED_LENGTH): # For each element after the current array index...
                if self.sorting_array[search_index] < self.sorting_array[minimum_index]: # If the current element is less than the current minimum...
                    minimum_index = search_index # Set the minimum index to the current index.
            
            # Swap the minimum index with the current index.
            self.sorting_array[item_index], self.sorting_array[minimum_index] = self.sorting_array[minimum_index], self.sorting_array[item_index]
            # Sleep for specified delay.
            if self._algorithm_delay: time.sleep(self._algorithm_delay)
            
            # Recursively call the sort function with the next index.
            _sort(item_index+1)
        
        # Start the recursive sort function.
        _sort(0)
        
        self._finished_times.append(round(time.time() - self._start_time, 2)) # Add the time taken to the finished times list.
        self._running = False # Set the algorithm to not running.

    def bubbleSort(self):
        """ Bubble sort algorithm. """
        self._running = True # Sets the algorithm to running.
        self._start_time = time.time() # Sets the start time of the algorithm.
        self._display_name = "Bubble Sort" # Sets the display name of the algorithm.
        STORED_LENGTH = len(self.sorting_array) # Length is stored to reduce the amount of times the length is calculated (Slows down algorithm to call len() often).
        
        for _ in self.sorting_array: # For each element in the array (Index not used so it is assigned to underscore)...
            for search_index in range(STORED_LENGTH - 1): # For each element after the current item index...
                if self.sorting_array[search_index] > self.sorting_array[search_index + 1]: # If the current element is greater than the next element...
                    # Swap the current element with the next element.
                    self.sorting_array[search_index], self.sorting_array[search_index + 1] = self.sorting_array[search_index + 1], self.sorting_array[search_index]
            # Sleep for specified delay.
            if self._algorithm_delay: time.sleep(self._algorithm_delay)
        
        self._finished_times.append(round(time.time() - self._start_time, 2)) # Add the time taken to the finished times list.
        self._running = False # Set the algorithm to not running.

    def quickSort(self):
        """ Quick sort algorithm. """
        
        self._running = True # Sets the algorithm to running.
        self._start_time = time.time() # Sets the start time of the algorithm.
        self._display_name = "Quick Sort" # Sets the display name of the algorithm.
        
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
                if self._algorithm_delay: time.sleep(self._algorithm_delay)
            
            # Swap the pivot with the index.
            array[start+1], array[end] = array[end], array[start+1]
            
            # Sleep for specified delay.
            if self._algorithm_delay: time.sleep(self._algorithm_delay)
            
            # Return the index of the pivot.
            return start + 1
        
        # Start the recursive sort function.
        _quickSort(self.sorting_array, 0, len(self.sorting_array) - 1)
        
        self._finished_times.append(round(time.time() - self._start_time, 2)) # Add the time taken to the finished times list.
        self._running = False # Set the algorithm to not running.
