#!/usr/bin/env python
"""The main, directly runnable, script for visualising sorting algorithms.

Please Note: These files are greatly overdocumented, this is because this is to be used as an educational tool, it should be understandable with zero python knowledge.
"""

import math
import pygame
import sys
import modules.algorithm_engine as algorithm_engine
import modules.window_engine as window_engine
import modules.sorting_algorithms as sorting_algorithms

__author__ = "Archer Hume"
__copyright__ = "Copyright (C) 2022 Archer Hume"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Archer Hume"
__email__ = "archer@hume.email"
__status__ = "Development"



ALGORITHM_ENGINE_OBJECT = algorithm_engine.Algorithm() # Declares the algorithm engine.
# Assigns the algorithms to be used to the algorithm engine using the algorithm wrapper.
for undecorated_algorithm in sorting_algorithms.__algorithms__:
    ALGORITHM_ENGINE_OBJECT.algorithm_add(undecorated_algorithm)

# The help text to be displayed on the screen.
__help__ = f"""
USAGE:
    python main.py -t [algorithm]

    Flags:
        -t [algorithm] (Required): The algorithm you would like to run.
            Choose from: {', '.join(ALGORITHM_ENGINE_OBJECT._algorithm_types.keys())}
        -l [length] (Optional): The length of the array to be sorted. Defaults to 50.
        -r [repeats] (Optional): The number of times to repeat the algorithm. Defaults to 3.
        -d [delay] (Optional): The delay in milliseconds between each step of the algorithm, used to watch each individual step. Defaults to 100.
        -width [width] (Optional): The width of the screen. Defaults to 800.
        -height [height] (Optional): The height of the screen. Defaults to 600.
        -h (Optional): Prints this message.
        -debug (Optional): Enables debug mode.

    Example: python main.py -t selection -l 10000 -r 6
"""


if __name__ == "__main__": # If the file is being run directly (not imported as a library)...
    
    screen_width, screen_height = 1000, 500 # Set the width and height of the window.
    
    # Print the header to command line.
    print("+" + "-"*65 + "+" + "\n| Sorting Algorithm Visualizer by Archer Hume                     |\n" + "+" + "-"*65 + "+\n")
    
    # Check if the user has specified a length of the array to be sorted.
    if "-l" in sys.argv and sys.argv[sys.argv.index("-l") + 1].isdigit(): # Checks if flag exists and if value is a digit.
        ALGORITHM_ENGINE_OBJECT._array_length = int(sys.argv[sys.argv.index("-l") + 1]) # Set the length of the array to be sorted.
    
    # Check if the user has specified the number of times to repeat the algorithm.
    if "-r" in sys.argv and sys.argv[sys.argv.index("-r") + 1].isdigit(): # Checks if flag exists and if value is a digit.
        ALGORITHM_ENGINE_OBJECT._repeats = int(sys.argv[sys.argv.index("-r") + 1]) # Set the number of times to repeat the algorithm.
    
    # Check if the user has specified a delay between each algorithm step.
    if "-d" in sys.argv and sys.argv[sys.argv.index("-d") + 1].isnumeric(): # Checks if flag exists and if value is a number.
        ALGORITHM_ENGINE_OBJECT._algorithm_delay = int(sys.argv[sys.argv.index("-d") + 1]) # Set the delay between each algorithm step.
    
    # Check if the user has specified a width of the window.
    if "-width" in sys.argv and sys.argv[sys.argv.index("-w") + 1].isdigit(): # Checks if flag exists and if value is a digit.
        screen_width = int(sys.argv[sys.argv.index("-w") + 1]) # Set the width of the window.
    
    # Check if the user has specified a height of the window.
    if "-height" in sys.argv and sys.argv[sys.argv.index("-h") + 1].isdigit(): # Checks if flag exists and if value is a digit.
        screen_height = int(sys.argv[sys.argv.index("-h") + 1]) # Set the height of the window.
    
    # Check if the user has specified an algorithm to run.
    if len(sys.argv) > 1 and "-t" in sys.argv: # Checks if flag exists.
        # Check if algorithm in flag exists.
        if sys.argv[sys.argv.index("-t") + 1] in ALGORITHM_ENGINE_OBJECT._algorithm_types.keys():
            # Initialise the new window.
            display_window = window_engine.Window(screen_width, screen_height, ALGORITHM_ENGINE_OBJECT) 
            # run the algorithm.
            ALGORITHM_ENGINE_OBJECT.start(sys.argv[sys.argv.index("-t") + 1])
        else:
            print(f"ERROR: The algorithm '{sys.argv[sys.argv.index('-t') + 1]}' does not exist.")
            print(__help__)
            sys.exit()
    elif "-h" in sys.argv: # Checks if help flag exists.
        # If no algorithm is specified or the -h flag is used, print __help__ and exit.
        print("No algorithm specified.")
        print(__help__)
        sys.exit()
    else:
        # If no algorithm is specified or the -h flag is used, print __help__ and exit.
        print("No algorithm specified.")
        print(__help__)
        sys.exit()

    
    # Print all the algorithm information to command line.
    print(f"Algorithm: {sys.argv[sys.argv.index('-t') + 1]}")
    print(f"Array Length: {ALGORITHM_ENGINE_OBJECT._array_length}")
    print(f"Repeats: {ALGORITHM_ENGINE_OBJECT._repeats}")
    print(f"Delay: {ALGORITHM_ENGINE_OBJECT._algorithm_delay}")
    print("\n")
    
    # Wait until the random array has been generated.
    while ALGORITHM_ENGINE_OBJECT._sorting_array == []:
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
            display_window.update_window(ALGORITHM_ENGINE_OBJECT._sorting_array, ALGORITHM_ENGINE_OBJECT._display_name, ALGORITHM_ENGINE_OBJECT.getCurrentTime(), ALGORITHM_ENGINE_OBJECT._running)
            time_since_action = 0 # Reset the time since the last action.
        
        # Check if the user has pressed the exit button.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
