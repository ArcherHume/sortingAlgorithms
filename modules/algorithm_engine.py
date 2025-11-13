#!/usr/bin/env python
""" 
This module contains the engine used to run the sorting algorithms.

This is a library file and cannot be run directly.

Please Note: These files are greatly overdocumented, this is because this is to be used as an educational tool, it should be understandable with zero python knowledge.
"""

import cProfile
import random
import sys
import threading
import time

from modules.sorting_algorithms import algorithm_wrapper


__author__ = "Archer Hume"
__copyright__ = "Copyright (C) 2022 Archer Hume"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Archer Hume"
__email__ = "archer@hume.email"
__status__ = "Development"


sys.setswitchinterval(1) # Set the interpreter check interval to 1 (Higher thread switching frequency increases delay accuracy).


class AlgorithmExistanceError(Exception):
    """Algorithm does not exist.

    Custom exception to be called when an algorithm does not exist."""
    pass


class Algorithm:
    """Algorithm class that handles all backend processing and sorting for the script."""
    
    def __init__(self, length=50, repeats=3, delay=100, debug=False) -> None:
        """Initialize the algorithm class.

        Args:
            length (int): The length of the array to be sorted.
            algorithm (str): The algorithm to be run.
            repeats (int, optional): Amount of times algorithm will repeat. 
            delay (int, optional): The delay in milliseconds between algorithm steps. 

        Raises:
            AlgorithmExistanceError: When the algorithm does not exist.
        """
        self._display_name = "Algorithm" # The display name of the algorithm to be shown on the screen
        self._array_length = length # The length of the array to be sorted, stored so that on repeats the array can be recreated.
        self._finished_times, self._sorting_array = [], [] # The run times to be stored when an algorithm has finished running and the placeholder array to be sorted.
        self._running = True # Whether or not the algorithm is currently running.
        self._start_time = time.time() # Placeholder start time, will be used to measure algorithms run times.
        self._algorithm_delay = delay # The delay between each algorithm step.
        self._debug = debug # Whether or not the algorithm should be run in debug mode.
        self._repeats = repeats # The amount of times the algorithm should be run.
        self._algorithm_types = {} # The algorithm types to be used.

    def getCurrentTime(self):
        """Get the current time of the algorithm.

        Returns:
            float: The current time in seconds.
        """
        return time.time() - self._start_time
    
    def algorithm_add(self, func):
        """Adds an algorithm to the algorithm list.
        
        Args:
            func (function): The algorithm to be added.
        """
        self._algorithm_types[func.__name__] = func
    
    def algorithm_wrapper(self, func):
        """ Wrapper function for the algorithm.

        Args:
            func (function): The algorithm to be run.
        """
        def _wrapper():
            self._running = True # Sets the algorithm to running.
            self._start_time = time.time() # Sets the start time of the algorithm.
            self._display_name = " ".join([word.capitalize() for word in func.__name__.split("_")]) # Sets the display name of the algorithm.
            func(self._sorting_array, self._algorithm_delay/1000) # Run the algorithm.
            self._finished_times.append(time.time() - self._start_time) # Add the time taken to the finished times list.
            self._running = False # Set the algorithm to not running.
        return _wrapper

    def start(self, algorithm):
        """Start the algorithm.

        Args:
            algorithm (function): The algorithm to be run.
            repeats (int): Amount of times algorithm will repeat.
        """
        
        def _loop():
            """Nested function used to enclose the algorithm start instructions."""
            for _ in range(self._repeats): # Repeat the algorithm the amount of times specified.
                self._sorting_array = random.sample(list(range(1, self._array_length + 1)), self._array_length) # Create a new array to be sorted.
                
                if self._debug: # If the algorithm is in debug mode...
                    p = cProfile.Profile() # Create a new profile object to be used to measure the debug data of the algorithm.
                    p.runcall(self.algorithm_wrapper(self._algorithm_types[algorithm])) # Run the algorithm with the profile object.
                    p.print_stats() # Print the debug data of the algorithm.
                else:
                    self.algorithm_wrapper(self._algorithm_types[algorithm])()
        
        # Create a new thread to run the algorithm start instructions.
        # This is done to prevent the main thread that runs the UI from freezing while the algorithm 
        # is running and prevents general interference between UI and algorithms.
        self.thread = threading.Thread(target=_loop)
        self.thread.start() # Start the thread.
