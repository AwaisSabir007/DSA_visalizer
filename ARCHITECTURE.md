# DSA Visualizer - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                  │
│                    (Application Entry)                           │
│  • Initialize QApplication                                       │
│  • Apply global stylesheet                                       │
│  • Create and show MainWindow                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ui/main_window.py                             │
│                    (Main Application Window)                     │
│  ┌──────────────┐  ┌────────────────────────────────────────┐  │
│  │   Sidebar    │  │        Stacked Widget                  │  │
│  │  Navigation  │  │  ┌──────────────────────────────────┐  │  │
│  │              │  │  │  Home / BST / Graph / Sorting    │  │  │
│  │  • Home      │──┼─▶│  Queue & Stack / Expressions     │  │  │
│  │  • BST       │  │  └──────────────────────────────────┘  │  │
│  │  • Graph     │  │                                         │  │
│  │  • Sorting   │  │                                         │  │
│  │  • Q&S       │  │                                         │  │
│  │  • Expr      │  │                                         │  │
│  └──────────────┘  └────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  ui/widgets/ │  │ algorithms/  │  │    core/     │
│              │  │              │  │              │
│ • bst_widget │  │ • sorting    │  │ • bst        │
│ • graph_     │  │ • searching  │  │ • graph      │
│   widget     │  │ • traversals │  │ • queue_     │
│ • sorting_   │  │ • expressions│  │   stack      │
│   widget     │  │              │  │              │
│ • queue_     │  └──────────────┘  └──────────────┘
│   stack_     │         │                  │
│   widget     │         │                  │
│ • expression_│         │                  │
│   widget     │         │                  │
└──────────────┘         │                  │
        │                │                  │
        └────────────────┼──────────────────┘
                         ▼
                  ┌──────────────┐
                  │    utils/    │
                  │              │
                  │ • sound      │
                  │ • constants  │
                  └──────────────┘
```

## Data Flow

### Example: BST Insert Operation

```
User Input (UI)
      │
      ▼
┌─────────────────────┐
│  BSTWidget          │
│  (ui/widgets/)      │
│  • Get value from   │
│    input field      │
│  • Validate input   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  BST Class          │
│  (core/bst.py)      │
│  • insert(value)    │
│  • Update tree      │
│    structure        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  BSTCanvas          │
│  (ui/widgets/)      │
│  • Layout tree      │
│  • Calculate coords │
│  • Draw with QPainter│
└─────────────────────┘
           │
           ▼
      Visual Update
```

### Example: Sorting Animation

```
User Input (Array + Algorithm)
      │
      ▼
┌─────────────────────┐
│  SortingWidget      │
│  (ui/widgets/)      │
│  • Parse input      │
│  • Select algorithm │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Sorting Algorithm  │
│  (algorithms/)      │
│  • bubble_steps()   │
│  • Yield each step  │
│    (compare, swap)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  QTimer Loop        │
│  (SortingWidget)    │
│  • Get next step    │
│  • Update highlights│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SortingCanvas      │
│  (ui/widgets/)      │
│  • Draw bars        │
│  • Highlight active │
│  • Update display   │
└─────────────────────┘
           │
           ▼
      Animated Visualization
```

## Module Responsibilities

### Core Module
**Purpose**: Pure data structure implementations
- No UI dependencies
- No visualization logic
- Reusable in other projects
- Focus on correctness and efficiency

**Files**:
- `bst.py`: Binary Search Tree operations
- `graph.py`: Graph type definitions
- `queue_stack.py`: Queue and Stack classes

### Algorithms Module
**Purpose**: Algorithm implementations with step generation
- Generator functions for visualization
- Independent of UI
- Yields steps for animation
- Educational code snippets

**Files**:
- `sorting.py`: 5 sorting algorithms
- `searching.py`: BFS, DFS for graphs
- `traversals.py`: Tree/graph traversals
- `expressions.py`: Expression conversions

### UI Module
**Purpose**: PySide6 widgets and visualization
- Custom painting with QPainter
- Event handling
- Animation management
- User interaction

**Structure**:
```
ui/
├── main_window.py      # Main app window
├── styles.py           # Qt stylesheets
└── widgets/
    ├── bst_widget.py
    ├── graph_widget.py
    ├── sorting_widget.py
    ├── queue_stack_widget.py
    └── expression_widget.py
```

### Utils Module
**Purpose**: Shared utilities and constants
- Sound effects generation
- Color scheme definitions
- Animation timing constants
- Reusable across widgets

**Files**:
- `sound.py`: Pygame sound generation
- `constants.py`: App-wide constants

## Design Principles

### 1. Separation of Concerns
- **Data** (core) is separate from **Logic** (algorithms)
- **Logic** is separate from **Presentation** (ui)
- Each module has a single responsibility

### 2. Dependency Direction
```
UI ──depends on──> Algorithms ──depends on──> Core
                        │
                        └──depends on──> Utils
```
- UI depends on everything
- Algorithms depend on core and utils
- Core has no dependencies (pure data structures)

### 3. Reusability
- Core data structures can be used in other projects
- Algorithms can be tested independently
- Widgets can be embedded in other Qt applications

### 4. Extensibility
**Adding a new visualizer**:
1. Create widget in `ui/widgets/new_widget.py`
2. Import in `ui/widgets/__init__.py`
3. Add to MainWindow's stacked widget
4. Add to sidebar navigation

**Adding a new algorithm**:
1. Create generator function in appropriate module
2. Yield steps for visualization
3. Use in existing widget or create new one

## Technology Stack

```
┌─────────────────────────────────────┐
│         PySide6 (Qt 6)              │
│  • QMainWindow, QWidget             │
│  • QPainter for custom drawing      │
│  • QTimer for animations            │
│  • Stylesheets for theming          │
└─────────────────────────────────────┘
              │
┌─────────────┴─────────────┐
│         Python 3.8+        │
│  • Type hints              │
│  • Generators              │
│  • Dataclasses (future)    │
└────────────────────────────┘
              │
┌─────────────┴─────────────┐
│    Supporting Libraries    │
│  • pygame (sound)          │
│  • numpy (waveform gen)    │
└────────────────────────────┘
```

## Performance Considerations

### Efficient Drawing
- Only redraw when data changes
- Use QPainter's antialiasing selectively
- Cache calculated positions

### Animation Smoothness
- QTimer with appropriate intervals (150-800ms)
- Generator pattern for step-by-step execution
- Avoid blocking operations in UI thread

### Memory Management
- Widgets created once, reused
- Data structures cleared when not needed
- No memory leaks in event handlers

## Future Enhancements

### Possible Additions
1. **More Algorithms**
   - Dijkstra's shortest path
   - A* search
   - AVL tree balancing
   - Heap operations

2. **Advanced Features**
   - Export visualizations as images
   - Record animations
   - Playback speed control
   - Step backward capability

3. **Educational Tools**
   - Complexity analysis display
   - Quiz mode
   - Interactive tutorials
   - Code comparison

4. **Data Management**
   - Save/load structures
   - Import from files
   - Session history
   - Undo/redo

---

**This architecture provides a solid foundation for a maintainable, extensible, and professional DSA visualization tool!**
