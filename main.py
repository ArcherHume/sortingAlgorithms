#!/usr/bin/env python
"""The main, directly runnable, script for visualising sorting algorithms.

This file specifically only handles visualisation, not the algorithms themselves.

Please Note: These files are greatly overdocumented, this is because this is to be used as an educational tool, it should be understandable with zero python knowledge.
"""

import math
import pygame
import sys
import algorithms


__author__ = "Archer Hume"
__copyright__ = "Copyright (C) 2022 Archer Hume"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Archer Hume"
__email__ = "archer@hume.email"
__status__ = "Development"


__help__ = """
USAGE:
    python main.py -t [algorithm]

    Flags:
        -t [algorithm] (Required): The algorithm you would like to run.
            Choose from: selection, selection-r, bubble, quick
        -l [length] (Optional): The length of the array to be sorted. Defaults to 5000.
        -r [repeats] (Optional): The number of times to repeat the algorithm. Defaults to 3.
        -d [delay] (Optional): The delay between each step of the algorithm, used to watch each individual step. Defaults to 0.
        -w [width] (Optional): The width of the screen. Defaults to 800.
        -h [height] (Optional): The height of the screen. Defaults to 600.
        -debug (Optional): Enables debug mode.

    Example: python main.py -t selection -l 10000 -r 6
"""


class Window:
    """Window class to handle all UI related methods"""
    
    def __init__(self, width, height, title, background=(22,22,22), foreground=(250,185,45)):
        """ Initialise the window object.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
            title (str): The title of the window.
            background (tuple, optional): The RGB values to set as background. Defaults to (22,22,22).
            foreground (tuple, optional): The RGB values to set as foreground. Defaults to (250,185,45).
        """
        self._SCREEN_WIDTH, self.height = width, height # Set the width and height of the window.
        self._SCREEN_BACKGROUND, self.foreground, self.text_colour = background, foreground, (45, 180, 250) # Set the background and foreground colours of the window.
        
        pygame.font.init() # Initialise the pygame font module.
        self._SYSTEM_FONT = pygame.font.SysFont("arial", 20) # Create a new font object.
        self._screen = pygame.display.set_mode((self._SCREEN_WIDTH, self.height)) # Create a new pygame screen.
        self._screen.fill(background) # Fill the screen with the background colour.
        pygame.display.set_caption(title) # Set the title of the window.
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
            (f"Algorithm: {display_name} | Time: {round(current_time, 2)} | {'Running' if is_running else 'Finished'}" if is_running else f"Algorithm: {display_name} | Mean: {round(sum(current_algorithm._finished_times)/len(current_algorithm._finished_times),2)}"), # Display the algorithm name, time taken and whether the algorithm is running or finished.
            *[round(time, 2) for time in current_algorithm._finished_times] # Add the finished times rounded to 2 significant figures to the data strings.
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


if __name__ == "__main__": # If the file is being run directly (not imported as a library)...
    
    
    # Placeholder/default command line arguments.
    array_length = 5000 # The length of the array to be sorted.
    algorithm_repeats = 3 # The number of times to repeat the algorithm.
    algorithm_delay = 0 # The delay between each algorithm step.
    screen_width, screen_height = 1000, 500 # The width and height of the window.
    
    # Print the header to command line.
    print("+" + "-"*65 + "+" + "\n| Sorting Algorithm Visualizer by Archer Hume                     |\n" + "+" + "-"*65 + "+\n")
    
    # Check if the user has specified a length of the array to be sorted.
    if "-l" in sys.argv and sys.argv[sys.argv.index("-l") + 1].isdigit(): # Checks if flag exists and if value is a digit.
        array_length = int(sys.argv[sys.argv.index("-l") + 1]) # Set the length of the array to be sorted.
    
    # Check if the user has specified the number of times to repeat the algorithm.
    if "-r" in sys.argv and sys.argv[sys.argv.index("-r") + 1].isdigit(): # Checks if flag exists and if value is a digit.
        algorithm_repeats = int(sys.argv[sys.argv.index("-r") + 1]) # Set the number of times to repeat the algorithm.
    
    # Check if the user has specified a delay between each algorithm step.
    if "-d" in sys.argv and sys.argv[sys.argv.index("-d") + 1].isnumeric(): # Checks if flag exists and if value is a number.
        algorithm_delay = int(sys.argv[sys.argv.index("-d") + 1]) # Set the delay between each algorithm step.
    
    # Check if the user has specified a width of the window.
    if "-w" in sys.argv and sys.argv[sys.argv.index("-w") + 1].isdigit(): # Checks if flag exists and if value is a digit.
        screen_width = int(sys.argv[sys.argv.index("-w") + 1]) # Set the width of the window.
    
    # Check if the user has specified a height of the window.
    if "-h" in sys.argv and sys.argv[sys.argv.index("-h") + 1].isdigit(): # Checks if flag exists and if value is a digit.
        screen_height = int(sys.argv[sys.argv.index("-h") + 1]) # Set the height of the window.
    
    # Check if the user has specified an algorithm to run.
    if len(sys.argv) > 1 and "-t" in sys.argv: # Checks if flag exists.
        # Initialise the new window.
        display_window = Window(screen_width, screen_height, "Sorting Algorithms") 
        # Create a new algorithm object.
        current_algorithm = algorithms.Algorithm(array_length, sys.argv[sys.argv.index("-t") + 1], repeats=algorithm_repeats, debug=("-debug" in sys.argv))
    elif "-h" in sys.argv: # Checks if help flag exists.
        # If no algorithm is specified or the -h flag is used, print __help__ and exit.
        print("No algorithm specified.")
        print(__help__)
        sys.exit()
    
    # Print all the algorithm information to command line.
    print(f"Algorithm: {sys.argv[sys.argv.index('-t') + 1]}")
    print(f"Array Length: {array_length}")
    print(f"Repeats: {algorithm_repeats}")
    print(f"Delay: {algorithm_delay}")
    print("\n")
    
    # Wait until the random array has been generated.
    while current_algorithm.sorting_array == []:
        pass
    
    # Initiate pygame clock/tick system.
    clock = pygame.time.Clock()
    time_since_action = 0
    
    # While true (until the user closes the window)...
    while True:
        delta_time = clock.tick() # Get the time since the last tick.
        time_since_action += delta_time # Add the time since the last tick to the time since the last action.
        
        if time_since_action >= 15: # If the time since the last action is greater than 15 milliseconds...
            # Update the display.
            display_window.update_window(current_algorithm.sorting_array, current_algorithm._display_name, current_algorithm.getCurrentTime(), current_algorithm._running)
            time_since_action = 0 # Reset the time since the last action.
        
        # Check if the user has pressed the exit button.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()