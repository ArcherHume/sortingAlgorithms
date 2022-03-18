#!/usr/bin/env python
"""
This module contains the window engine used to visualize the sorting algorithms.

This is a library file and cannot be run directly.

Please Note: These files are greatly overdocumented, this is because this is to be used as an educational tool, it should be understandable with zero python knowledge.
"""

import math
import pygame


class Window:
    """Window class to handle all UI related methods"""
    
    def __init__(self, width, height, algorithm_engine, background=(22,22,22), foreground=(250,185,45)):
        """ Initialise the window object.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
            title (str): The title of the window.
            background (tuple, optional): The RGB values to set as background. Defaults to (22,22,22).
            foreground (tuple, optional): The RGB values to set as foreground. Defaults to (250,185,45).
        """
        
        self.algorithm_engine = algorithm_engine # Store the algorithm engine.
        
        self._SCREEN_WIDTH, self.height = width, height # Set the width and height of the window.
        self._SCREEN_BACKGROUND, self.foreground, self.text_colour = background, foreground, (45, 180, 250) # Set the background and foreground colours of the window.
        
        pygame.font.init() # Initialise the pygame font module.
        self._SYSTEM_FONT = pygame.font.SysFont("arial", 20) # Create a new font object.
        self._screen = pygame.display.set_mode((self._SCREEN_WIDTH, self.height)) # Create a new pygame screen.
        self._screen.fill(background) # Fill the screen with the background colour.
        pygame.display.set_caption("Sorting Algorithm Visualiser") # Set the title of the window.
        pygame.display.update() # Update the display.

    def update_window(self, current_array, display_name, current_time, is_running):
        """ Update the window with the current array and the current times.

        Args:
            current_array (array): The current array to be displayed.
            display_name (str): The name of the algorithm being run.
            current_time (float): The current time of the algorithm.
            is_running (bool): Whether the algorithm is running or not.
        """
        MAX_HEIGHT = self.height*0.8 # The maximum height of the array.
        MIN_HEIGHT = self.height*0.1 # The minimum height of the array.
        
        # Set current_array to only elements that can fit on the screen. (Extremely scalable, can render millions of items extremely quickly)
        # EXPLAINATION:
        # Python array slicing syntax is [start:end:step].
        # This means that if we divide the length of the array by the width, we can get every Nth element, stopping screen overflow (No rectangle should have a width less than 1px).
        current_array = current_array[::math.ceil(len(current_array)/self._SCREEN_WIDTH)]
        
        # Store current_array dependant constants.
        STORED_LEN, STORED_MAX = len(current_array), max(current_array) # Get the length and maximum value of the array.
        ITEM_WIDTH = round(self._SCREEN_WIDTH/STORED_LEN) # The width of each item.
        
        # Store strings to display on screen.
        data_strings = [
            (f"Algorithm: {display_name} | Time: {round(current_time, 2)} | {'Running' if is_running else 'Finished'}" if is_running else f"Algorithm: {display_name} | Mean: {round(sum(self.algorithm_engine._finished_times)/len(self.algorithm_engine._finished_times),2)}"), # Display the algorithm name, time taken and whether the algorithm is running or finished.
            *[round(time, 2) for time in self.algorithm_engine._finished_times] # Add the finished times rounded to 2 significant figures to the data strings.
        ] # Create a list of strings to display on screen.
        
        # Draw all relevent data to screen.
        self._screen.fill(self._SCREEN_BACKGROUND) # Fill the screen with the background colour to empty display.
        
        # For each string in the data strings list (Enumerate method turns list to list of tuples with index and value)...
        for string_index, display_string in enumerate(data_strings): 
            text = self._SYSTEM_FONT.render(str(display_string), True, self.text_colour) # Create a new text object.
            self._screen.blit(text, (15, 8 + string_index * 26)) # Display the text object on the screen, determining height from the index.
        
        # Iterate through all the elements in the current array...
        for item_index in range(STORED_LEN):
            # Draw rectangle to represent the item.
            pygame.draw.rect(
                self._screen, # The screen object to draw on.
                self.foreground, # The colour of the rectangle.
                (
                    item_index*ITEM_WIDTH, # The x position of the rectangle.
                    self.height-(((current_array[item_index]/STORED_MAX)*MAX_HEIGHT)+MIN_HEIGHT), # The y position of the rectangle.
                    ITEM_WIDTH, # The width of the rectangle.
                    ((current_array[item_index]/STORED_LEN)*MAX_HEIGHT)+MIN_HEIGHT # The height of the rectangle.
                ),
            )
        
        # Update the display.
        pygame.display.flip()