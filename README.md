# DSA Algorithm Visualizer

A comprehensive, modern desktop application for visualizing data structures and algorithms built with PySide6.

## Features

### 🌳 Binary Search Tree Visualizer
- Insert, delete, and search operations
- Animated tree visualization
- Inorder, preorder, and postorder traversals
- Code display for educational purposes

### 🕸️ Graph Visualizer
- Directed weighted graph support
- BFS and DFS search algorithms with animation
- Preorder and postorder DFS traversals
- Auto-layout with circular positioning
- Load graphs from Python dictionary format

### 📊 Sorting Visualizer
- 5 sorting algorithms: Insertion, Bubble, Selection, Merge, Quick
- Step-by-step or full animation modes
- Visual bar chart representation
- Code display for each algorithm

### 📦 Queue & Stack Simulator
- Fixed-size queue and stack implementations
- Visual box representation
- Push/Pop and Enqueue/Dequeue operations
- Sound effects for operations

### 🔢 Expression Converter & Evaluator
- Convert infix expressions to postfix and prefix
- Evaluate numeric postfix expressions
- Step-by-step conversion display
- Support for variables and operators

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Requirements

- Python 3.8 or higher
- PySide6 6.6.0 or higher
- pygame 2.5.0 or higher
- numpy 1.24.0 or higher

## Project Structure

```
DSA/
├── main.py                      # Application entry point
├── requirements.txt             # Project dependencies
├── README.md                    # This file
│
├── core/                        # Core data structures
│   ├── bst.py                   # Binary Search Tree
│   ├── graph.py                 # Graph type definitions
│   └── queue_stack.py           # Queue and Stack
│
├── algorithms/                  # Algorithm implementations
│   ├── sorting.py               # Sorting algorithms
│   ├── searching.py             # BFS, DFS
│   ├── traversals.py            # Tree/graph traversals
│   └── expressions.py           # Expression converters
│
├── ui/                          # PySide6 UI components
│   ├── main_window.py           # Main application window
│   ├── styles.py                # Qt stylesheets
│   └── widgets/                 # Custom widgets
│       ├── bst_widget.py
│       ├── graph_widget.py
│       ├── sorting_widget.py
│       ├── queue_stack_widget.py
│       └── expression_widget.py
│
└── utils/                       # Utility modules
    ├── sound.py                 # Sound effects
    └── constants.py             # App constants
```

## Usage

### Binary Search Tree
1. Enter an integer value
2. Click "Insert" to add to tree
3. Click "Delete" to remove from tree
4. Click "Search" to find a value
5. Use traversal buttons to see different orderings

### Graph Visualizer
1. Enter graph definition in Python dictionary format:
   ```python
   graph={
     'A':[('B',3),('C',1)],
     'B':[('D',2)],
     'C':[('D',4)],
     'D':[]
   }
   ```
2. Click "Load Graph"
3. Enter start and goal nodes
4. Click "Search" and choose BFS or DFS

### Sorting Visualizer
1. Enter comma-separated integers (e.g., `5,3,8,1,9,2`)
2. Select sorting algorithm from dropdown
3. Click "Step" for step-by-step or "Run Full" for animation
4. Click "Show Code" to see the algorithm implementation

### Queue & Stack
1. Enter structure size (e.g., `8`)
2. Click "Create Structures"
3. Enter values and use Push/Pop or Enqueue/Dequeue buttons
4. Watch visual feedback with sound effects

### Expressions
1. Enter infix expression (e.g., `(A+B)*(C-D)` or `(3+5)*(2-1)`)
2. Click "To Postfix" or "To Prefix" for conversion
3. Click "Evaluate Postfix" for numeric expressions
4. View step-by-step conversion in the steps area

## Design

The application features a modern green theme with:
- Clean, intuitive interface
- Smooth animations
- Visual feedback for operations
- Educational code snippets
- Sound effects for enhanced UX

## License

This project is open source and available for educational purposes.

## Author

Created as a comprehensive DSA learning tool using modern Python and Qt technologies.
