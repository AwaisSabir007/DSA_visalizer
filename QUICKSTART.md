# Quick Start Guide - DSA Visualizer

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python main.py
```

### Step 3: Explore!
The application will open with a sidebar navigation. Click on any feature to explore.

---

## 📚 Feature Quick Reference

### 🌳 Binary Search Tree
**What it does**: Visualize BST operations with animations

**Quick test**:
1. Click "BST Visualizer" in sidebar
2. Enter numbers: 50, 30, 70, 20, 40, 60, 80
3. Click "Insert" for each
4. Try "Search" with any number
5. Click "Inorder" to see sorted output

---

### 🕸️ Graph Visualizer
**What it does**: Visualize directed weighted graphs and search algorithms

**Quick test**:
1. Click "Graph Visualizer"
2. The example graph is already loaded in the text box
3. Click "Load Graph"
4. Enter Start: `A`, Goal: `G`
5. Click "Search" and choose "BFS"
6. Watch the path highlight!

**Example graph format**:
```python
graph={
  'A':[('B',3),('C',1)],
  'B':[('D',2)],
  'C':[('D',4)],
  'D':[]
}
```

---

### 📊 Sorting Visualizer
**What it does**: Animate sorting algorithms step-by-step

**Quick test**:
1. Click "Sorting Visualizer"
2. Enter: `64,34,25,12,22,11,90`
3. Select "Bubble" from dropdown
4. Click "Run Full" to watch animation
5. Try other algorithms!

**Available algorithms**:
- Insertion Sort
- Bubble Sort
- Selection Sort
- Merge Sort
- Quick Sort

---

### 📦 Queue & Stack
**What it does**: Simulate queue and stack operations with visual feedback

**Quick test**:
1. Click "Queue & Stack"
2. Enter size: `6`
3. Click "Create Structures"
4. Enter values and click Push/Enqueue
5. Click Pop/Dequeue to hear sound effects!

**Operations**:
- **Stack**: Push (add to top), Pop (remove from top) - LIFO
- **Queue**: Enqueue (add to rear), Dequeue (remove from front) - FIFO

---

### 🔢 Expressions
**What it does**: Convert and evaluate mathematical expressions

**Quick test**:
1. Click "Expressions"
2. Enter: `(3+5)*(2-1)`
3. Click "To Postfix" → Result: `3 5 + 2 1 - *`
4. Click "Evaluate Postfix" → Result: `8`

**Supported**:
- Infix to Postfix conversion
- Infix to Prefix conversion
- Postfix evaluation (numeric only)
- Step-by-step display

---

## 🎨 UI Tips

### Navigation
- Use the **sidebar** on the left to switch between features
- Each feature is independent and self-contained

### Buttons
- **Green buttons**: Primary actions (Insert, Search, etc.)
- **Orange buttons**: Destructive actions (Delete, Pop, etc.)
- **Code buttons**: Show Python implementation

### Help
- Click **Help → Help** in menu bar for detailed instructions
- Click **Help → About** for app information

---

## 🎯 Learning Tips

### For Students
1. **Start with BST**: Understand tree structure
2. **Try Graph**: Learn BFS vs DFS differences
3. **Watch Sorting**: See algorithm efficiency visually
4. **Use Code buttons**: Study implementations

### For Teachers
1. Use **step-by-step** mode for demonstrations
2. Show **code snippets** to explain algorithms
3. Compare **different algorithms** side-by-side
4. Use **traversals** to explain tree concepts

---

## 🐛 Troubleshooting

### Application won't start
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Sound not working
- Check system volume
- Pygame mixer may need initialization (automatic in app)

### Visualization not updating
- Click the action button again
- Check if you entered valid input

---

## 📖 More Information

- See **README.md** for full documentation
- See **REFACTORING_SUMMARY.md** for technical details
- Each module has docstrings for developers

---

## 🎉 Enjoy Learning DSA!

This tool is designed to make data structures and algorithms **visual**, **interactive**, and **fun**!

**Happy Coding!** 🚀
