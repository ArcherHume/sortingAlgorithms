import os
import pygame
import random
import threading
import time
import sys


class Algorithm:
    def __init__(self, length, window, delay=0) -> None:
        self.name = "Algorithm"
        self.length = length
        self.window = window
        self.array = random.sample(list(range(1, length + 1)), length)
        self.running = False
        self.finished = False
        self.start_time = 0
        self.delay = delay
        self.algorithms = {"selection": self.selectionSort, "bubble": self.bubbleSort, "quick": self.quickSort}

    def reloadArray(self):
        self.array = random.sample(list(range(1, self.length + 1)), self.length)

    def start(self, alg):
        self.thread = threading.Thread(target=self.algorithms[alg])
        self.thread.start()
    
    def selectionSort(self):
        self.running = True
        self.start_time = time.time()
        self.name = "Selection Sort"
        for i in range(len(self.array)):
            min = i
            for j in range(i + 1, len(self.array)):
                if self.array[j] < self.array[min]:
                    min = j
            self.array[i], self.array[min] = self.array[min], self.array[i]
            window.updateArray(self.array, {i: 0, min+1: 1}, self.name, time.time() - self.start_time, self.running)
            time.sleep(self.delay)
        self.running = False
        self.finished = True

    def bubbleSort(self):
        self.running = True
        self.start_time = time.time()
        self.name = "Bubble Sort"
        for i in range(len(self.array)):
            for j in range(len(self.array) - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                window.updateArray(self.array, {j+1:0}, self.name, time.time() - self.start_time, self.running)
                time.sleep(self.delay)
        self.running = False
        self.finished = True

    def quickSort(self):
        self.running = True
        self.start_time = time.time()
        self.name = "Quick Sort"
        def _quicksort(begin, end):
            if begin >= end:
                return
            pivot = partition(begin, end)
            _quicksort(begin, pivot-1)
            _quicksort(pivot+1, end)
        def partition(begin, end):
            pivot = begin
            for i in range(begin+1, end+1):
                if self.array[i] <= self.array[begin]:
                    pivot += 1
                    self.array[i], self.array[pivot] = self.array[pivot], self.array[i]
                window.updateArray(self.array, {i:0, pivot+1:1}, self.name, time.time() - self.start_time, self.running)
            self.array[pivot], self.array[begin] = self.array[begin], self.array[pivot]
            return pivot
        _quicksort(0, len(self.array) - 1)
        self.running = False
        self.finished = True

class Window:
    def __init__(self, width, height, title, background=(22,22,22), foreground=(250,185,45), highlights=[(45,180,250), (45,250,110)]):
        self.width = width
        self.height = height
        self.title = title
        self.background = background
        self.foreground = foreground
        self.highlights = highlights
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.screen.fill(background)
        pygame.display.flip()

    def updateArray(self, arr, highlights, name, current_time, running):
        self.screen.fill(self.background)
        self.screen.blit(pygame.font.SysFont('Verdana', 15).render(f"Algorithm: {name} | Time: {round(current_time, 2)} | {'Running' if running else 'Finished'}", True, self.highlights[0]), (15, 8))
        maxHeight = self.height*0.8
        minHeight = self.height*0.1
        for i in range(len(arr)):
            pygame.draw.rect(self.screen, (self.highlights[highlights[i]] if i in highlights else self.foreground), (i*self.width/len(arr), self.height-(((arr[i]/max(arr))*maxHeight)+minHeight), self.width/len(arr), ((arr[i]/max(arr))*maxHeight)+minHeight))
        pygame.display.flip()


if __name__ == "__main__":
    window = Window(1000, 500, "Sorting Algorithms")
    alg = Algorithm(500, window, 0)
    print("+" + "-"*65 + "+" + "\n| Sorting Algorithm Visualizer by Archer Hume                     |\n" + "+" + "-"*65 + "+\n")
    if "-d" in sys.argv and sys.argv[sys.argv.index("-d") + 1].isdigit():
        alg.delay = int(sys.argv[sys.argv.index("-d") + 1])
        print(f"Delay set to {alg.delay}")
    if "-l" in sys.argv and sys.argv[sys.argv.index("-l") + 1].isdigit():
        alg.length = int(sys.argv[sys.argv.index("-l") + 1])
        print(f"Length set to {alg.length}")
        alg.reloadArray()
    if len(sys.argv) > 1 and "-t" in sys.argv and sys.argv[sys.argv.index("-t") + 1] in alg.algorithms:
        alg.start(sys.argv[sys.argv.index("-t") + 1])
    else:
        print("A sorting algorithm must be specified with the -t flag.\nAvailable algorithms:", *[i for i in alg.algorithms])
        pygame.quit()
        quit()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
