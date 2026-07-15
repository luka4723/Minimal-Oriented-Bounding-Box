# Minimum Oriented Bounding Box Solver

An interactive Python application designed to compute and visualize the minimum-area Oriented Bounding Box (OBB) for custom simple polygons. The project implements classical computational geometry algorithms, achieving an optimal $O(n \log n)$ time complexity.

## Features

* **Interactive Drawing:** Click on the canvas to draw a custom simple polygon.
* **Self-Intersection Prevention:** The sweep-line utility prevents the drawing of non-simple (self-intersecting) polygons.
* **Step-by-Step Visualization:** Iterate through the convex hull edges to see how the bounding box area changes at each step.
* **Save/Load Configurations:** Persist complex polygon configurations to text files for later analysis using the built-in Tkinter dialogs.

## Requirements

The project requires Python 3 and the `pygame` library for the graphical interface. 
