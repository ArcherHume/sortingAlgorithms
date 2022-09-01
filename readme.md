# sortingAlgorithms

A collection of sorting algorithms written in Python. An educational tool used for demonstrations of said algorithms.

![](https://i.imgur.com/mVybEng.png)

## Current Algorithms

- [Bubble Sort](https://en.wikipedia.org/wiki/Bubble_sort)
- [Selection Sort](https://en.wikipedia.org/wiki/Selection_sort)
- [Selection Sort (Recursion)](https://en.wikipedia.org/wiki/Selection_sort)
- [Quick Sort](https://en.wikipedia.org/wiki/Quicksort)
- [Insertion Sort](https://en.wikipedia.org/wiki/Insertion_sort)
- [Shell sort](https://en.wikipedia.org/wiki/Shellsort)
- [Comb Sort](https://en.wikipedia.org/wiki/Comb_sort)

## Quick Start

- Clone Repository:
  ```
  git clone https://github.com/0xFuji/sortingAlgorithms.git
  cd sortingAlgorithms
  ```
- Install Dependencies:
  ```
  pip install -r requirements.txt
  ```
- Run Script: [Usage](#usage)

## Usage

```
USAGE:
    python main.py -t [algorithm]

    Flags:
        -t [algorithm] (Required): The algorithm you would like to run.
            Choose from: selection, selection_recursive, bubble, quick_sort, insertion, shell, comb.
        -l [length] (Optional): The length of the array to be sorted. Defaults to 5000.
        -r [repeats] (Optional): The number of times to repeat the algorithm. Defaults to 3.
        -d [delay] (Optional): The delay between each step of the algorithm, used to watch each individual step. Defaults to 0.
        -width [width] (Optional): The width of the screen. Defaults to 800.
        -height [height] (Optional): The height of the screen. Defaults to 600.
        -h (Optional): Prints this message.
        -debug (Optional): Enables debug mode.

    Example: python main.py -t selection -l 10000 -r 6
```

## How to add a new algorithm

- Open the `modules/sorting_algorithms.py` file.
- Create a function with a lowercase, underscore-separated name. Add the positional arguments `array` then `delay`.
  - Example: `def selection_sort(sorting_array, delay)`
- Any modifications/sorting done on the array will be reflected on screen.
