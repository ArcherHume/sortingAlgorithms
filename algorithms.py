#!/usr/bin/env python
"""
Various sorting algorithms demonstrated for educational projects.

The algorithms include: bubble sort, selection sort, selection sort with recursion, and quick sort.
"""

import math
import os
import pygame
import random
import threading
import time
import sys
import cProfile

__author__ = "Archer Hume"
__copyright__ = "Copyright (C) 2022 Archer Hume"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Archer Hume"
__email__ = "archer@hume.email"
__status__ = "Development"


class AlgorithmExistanceError(Exception):
    """Algorithm does not exist.
    
    Custom exception to be called when an algorithm does not exist."""
    pass


class Algorithm:
    """Algorithm class that handles all backend processing and sorting for the script."""
    def __init__(self, length, algorithm, repeats=3) -> None:
        """Initialize the algorithm class.
        :param length: The length of the array to be sorted.
        :param algorithm: The algorithm to be used.
        :param repeats: The amount of times to repeat the algorithm.
        """
        self.display_name = "Algorithm" # The display name of the algorithm to be shown on the screen
        self.array_length = length # The length of the array to be sorted, stored so that on repeats the array can be recreated.
        self.finished_times, self.sorting_array = [], [] # The run times to be stored when an algorithm has finished running and the placeholder array to be sorted.
        self.running = True # Whether or not the algorithm is currently running.
        self.start_time = 0 # Placeholder start time, will be used to measure algorithms run times.
        self.algorithms = {
            "selection": self.selectionSort, 
            "selection-r": self.recursiveSelectionSort, 
            "bubble": self.bubbleSort, 
            "quick": self.quickSort
            } # Dictionary of all the algorithms that can be run.
        if algorithm in self.algorithms: # If the algorithm is in the dictionary, run it.
            self.start(algorithm, repeats)
        else: # If the algorithm is not in the dictionary, raise an error.
            raise AlgorithmExistanceError("Algorithm does not exist")

    def getCurrentTime(self):
        """Get the current time of the algorithm while it is running."""
        return time.time() - self.start_time

    def start(self, algorithm, repeats):
        """Start the chosen algorithm.
        
        :param algorithm: The algorithm to be run.
        :param repeats: The amount of times to repeat the algorithm.
        """
        def _loop():
            """Nested function used to enclose the algorithm start instructions."""
            for _ in range(repeats): # Repeat the algorithm the amount of times specified.
                self.sorting_array = random.sample(list(range(1, self.array_length + 1)), self.array_length) # Create a new array to be sorted.
                p = cProfile.Profile() # Create a new profile object to be used to measure the debug data of the algorithm.
                p.runcall(self.algorithms[algorithm]) # Run the algorithm with the profile object.
                p.print_stats() # Print the debug data of the algorithm.
        
        # Create a new thread to run the algorithm start instructions.
        #
        # This is done to prevent the main thread that runs the UI from freezing while the algorithm 
        # is running and prevents general interference between UI and algorithms.
        self.thread = threading.Thread(target=_loop)
        self.thread.start() # Start the thread.
    
    def selectionSort(self):
        """Selection sort algorithm."""
        self.running = True # Sets the algorithm to running.
        self.start_time = time.time() # Sets the start time of the algorithm.
        self.display_name = "Selection Sort" # Sets the display name of the algorithm.
        
        for array_index in range(len(self.sorting_array)): # For each element in the array...
            minimum_index = array_index # Set the minimum index to the current index.
            for search_index in range(array_index + 1, len(self.sorting_array)): # For each element after the current array index...
                if self.sorting_array[search_index] < self.sorting_array[minimum_index]: # If the current element is less than the current minimum...
                    minimum_index = search_index # Set the minimum index to the current index.
            # Swap the minimum index with the current index.
            self.sorting_array[array_index], self.sorting_array[minimum_index] = self.sorting_array[minimum_index], self.sorting_array[array_index]
        
        self.finished_times.append(time.time() - self.start_time) # Add the time taken to the finished times list.
        self.running = False # Set the algorithm to not running.
    
    def recursiveSelectionSort(self):
        self.running = True
        self.start_time = time.time()
        self.display_name = "Recursive Selection Sort"
        def _sort(i):
            if i >= len(self.sorting_array):
                return
            min = i
            for j in range(i + 1, len(self.sorting_array)):
                if self.sorting_array[j] < self.sorting_array[min]:
                    min = j
            self.sorting_array[i], self.sorting_array[min] = self.sorting_array[min], self.sorting_array[i]
            _sort(i+1)
        _sort(0)
        self.finished_times.append(round(time.time() - self.start_time, 2))
        self.running = False
        self.finished = True

    def bubbleSort(self):
        self.running = True
        self.start_time = time.time()
        self.display_name = "Bubble Sort"
        for i in range(len(self.sorting_array)):
            for j in range(len(self.sorting_array) - 1):
                if self.sorting_array[j] > self.sorting_array[j + 1]:
                    self.sorting_array[j], self.sorting_array[j + 1] = self.sorting_array[j + 1], self.sorting_array[j]
        self.finished_times.append(round(time.time() - self.start_time, 2))
        self.running = False
        self.finished = True

    def quickSort(self):
        self.running = True
        self.start_time = time.time()
        self.display_name = "Quick Sort"
        # Quick sort with random pivot
        def _quickSort(array, start, end):
            if start >= end:
                return
            pivot = start
            self.sorting_array[pivot], self.sorting_array[end] = self.sorting_array[end], self.sorting_array[pivot]
            pivot = partition(array, start, end)
            _quickSort(array, start, pivot - 1)
            _quickSort(array, pivot + 1, end)
        def partition(array, start, end):
            pivot = array[end]
            i = start - 1
            for j in range(start, end):
                if array[j] <= pivot:
                    i += 1
                    array[i], array[j] = array[j], array[i]
            array[i+1], array[end] = array[end], array[i+1]
            return i + 1
        _quickSort(self.sorting_array, 0, len(self.sorting_array) - 1)
        self.finished_times.append(round(time.time() - self.start_time, 2))
        self.running = False
        self.finished = True

class Window:
    """Window class to handle all UI related methods"""
    def __init__(self, width, height, title, background=(22,22,22), foreground=(250,185,45)):
        """Initialise the window.
        
        :param width: The width of the window.
        :param height: The height of the window.
        :param title: The title of the window.

        OPTIONAL PARAMETERS:

        :param background: The background colour of the window.
        :param foreground: The foreground colour of the window.
        """
        self.width, self.height = width, height # Set the width and height of the window.
        self.background, self.foreground, self.text_colour = background, foreground, (45, 180, 250) # Set the background and foreground colours of the window.
        
        pygame.font.init() # Initialise the pygame font module.
        self.screen = pygame.display.set_mode((self.width, self.height)) # Create a new pygame screen.
        self.screen.fill(background) # Fill the screen with the background colour.
        pygame.display.set_caption(title) # Set the title of the window.
        pygame.display.update() # Update the display.

    def updateArray(self, current_array, name, current_time, running):
        """Update the array on the screen.

        :param current_array: The current array to be displayed.
        :param name: The name of the algorithm.
        :param current_time: The current time taken to sort the array.
        :param running: Whether the algorithm is running or not.
        """
        MAX_HEIGHT = self.height*0.8 # The maximum height of the array.
        MIN_HEIGHT = self.height*0.1 # The minimum height of the array.
        current_array = [i for i in current_array if i % math.floor(len(current_array)/self.width) == 0] # Only display elements that can fit on the screen (If element is divisible by array length / width).
        self.screen.fill(self.background) # Fill the screen with the background colour to empty display.
        data_strings = [
            (f"Algorithm: {name} | Time: {round(current_time, 2)} | {'Running' if running else 'Finished'}" if running else f"Algorithm: {name} | Mean: {round(sum(alg.finished_times)/len(alg.finished_times),2)}"), # Display the algorithm name, time taken and whether the algorithm is running or finished.
            *[round(time, 2) for time in alg.finished_times] # Add the finished times rounded to 2 significant figures to the data strings.
        ] # Create a list of strings to display on screen.
        for string_index, display_string in enumerate(data_strings): # For each string in the data strings list...
            text = pygame.font.SysFont("arial", 20).render(str(display_string), True, self.text_colour) # Create a new text object.
            self.screen.blit(text, (15, 8 + string_index * 26)) # Display the text object on the screen, determining height from the index.
        for i in range(len(current_array)):
            pygame.draw.rect(self.screen, self.foreground, (i*self.width/len(current_array), self.height-(((current_array[i]/max(current_array))*MAX_HEIGHT)+MIN_HEIGHT), self.width/len(current_array), ((current_array[i]/max(current_array))*MAX_HEIGHT)+MIN_HEIGHT))
        pygame.display.update()


if __name__ == "__main__":
    window = Window(1000, 500, "Sorting Algorithms")
    arrLen = 5000
    repeats = 3
    print("+" + "-"*65 + "+" + "\n| Sorting Algorithm Visualizer by Archer Hume                     |\n" + "+" + "-"*65 + "+\n")
    if "-l" in sys.argv and sys.argv[sys.argv.index("-l") + 1].isdigit():
        arrLen = int(sys.argv[sys.argv.index("-l") + 1])
        print(f"Length set to {arrLen}")
    if "-r" in sys.argv and sys.argv[sys.argv.index("-r") + 1].isdigit():
        repeats = int(sys.argv[sys.argv.index("-r") + 1])
        print(f"Repeats set to {repeats}")
    if len(sys.argv) > 1 and "-t" in sys.argv:
        alg = Algorithm(arrLen, sys.argv[sys.argv.index("-t") + 1], repeats=repeats)
    else:
        print("A sorting algorithm must be specified with the -t flag.")
        pygame.quit()
        quit()
    time_elapsed_since_last_action = 0
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(250)
        time_elapsed_since_last_action += dt

        # window.updateArray
        window.updateArray(alg.sorting_array, alg.display_name, alg.getCurrentTime(), alg.running)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
