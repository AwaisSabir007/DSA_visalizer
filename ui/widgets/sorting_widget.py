"""
Sorting Visualizer Widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                                QLineEdit, QLabel, QMessageBox, QComboBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from algorithms.sorting import (insertion_steps, bubble_steps, selection_steps,
                                 merge_steps, quick_steps)
from utils.constants import COLORS
from typing import List, Optional, Generator


class SortingCanvas(QWidget):
    """Canvas widget for drawing sorting bars"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.array: List[int] = []
        self.highlights: List[int] = []
        self.setMinimumSize(600, 300)
    
    def set_array(self, array: List[int], highlights: List[int] = None):
        """Set the array to visualize"""
        self.array = array
        self.highlights = highlights if highlights else []
        self.update()
    
    def paintEvent(self, event):
        """Draw the sorting bars"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.array:
            painter.setPen(QColor(COLORS['text_light']))
            painter.setFont(QFont("Arial", 14))
            painter.drawText(self.rect(), Qt.AlignCenter,
                           "Enter comma-separated numbers to visualize sorting")
            return
        
        w = self.width()
        h = self.height()
        n = len(self.array)
        bar_w = max(8, w / (n * 1.6))
        max_val = max(self.array) if self.array else 1
        
        for i, val in enumerate(self.array):
            x = 10 + i * (bar_w + 6)
            bar_h = (val / max_val) * (h - 50) if max_val > 0 else 10
            y = h - bar_h - 20
            
            # Color based on highlight
            color = COLORS['bar_compare'] if i in self.highlights else COLORS['bar_default']
            
            painter.setBrush(QBrush(QColor(color)))
            painter.setPen(QPen(QColor(COLORS['text']), 1))
            painter.drawRect(int(x), int(y), int(bar_w), int(bar_h))
            
            # Draw value
            painter.setPen(QColor(COLORS['text']))
            painter.setFont(QFont("Arial", 9))
            painter.drawText(int(x), int(y - 10), int(bar_w), 10,
                           Qt.AlignCenter, str(val))


class SortingWidget(QWidget):
    """Sorting Visualizer Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sort_gen: Optional[Generator] = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_step)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 20)
        layout.setSpacing(8)  # Reduced from 15 to 8
        
        # Title
        title = QLabel("Sorting Visualizer")
        title.setFont(QFont("Arial", 32, QFont.Bold))  # Increased from 28 to 32
        title.setStyleSheet(f"color: {COLORS['primary']}; padding: 0px; margin: 0px;")
        layout.addWidget(title)
        
        # Controls
        controls = QHBoxLayout()
        controls.setSpacing(8)
        controls.setContentsMargins(0, 0, 0, 0)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Comma-separated integers (e.g., 5,3,8,1,9)")
        self.input_field.setMinimumHeight(35)  # Make input field taller
        controls.addWidget(self.input_field)
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Insertion", "Bubble", "Selection", "Merge"])
        self.algo_combo.setMinimumHeight(35)  # Match input field height
        controls.addWidget(self.algo_combo)
        
        step_btn = QPushButton("Step")
        step_btn.clicked.connect(self.step_sort)
        step_btn.setMinimumHeight(35)
        controls.addWidget(step_btn)
        
        run_btn = QPushButton("Run Full")
        run_btn.clicked.connect(self.run_full)
        run_btn.setMinimumHeight(35)
        controls.addWidget(run_btn)
        
        code_btn = QPushButton("Show Code")
        code_btn.clicked.connect(self.show_code)
        code_btn.setMinimumHeight(35)
        controls.addWidget(code_btn)
        
        layout.addLayout(controls)
        
        # Canvas
        self.canvas = SortingCanvas()
        layout.addWidget(self.canvas, 1)  # Give canvas stretch factor
    
    def step_sort(self):
        """Perform one step of sorting"""
        if self.sort_gen is None:
            # Initialize generator
            arr = self._parse_input()
            if arr is None:
                return
            
            algo = self.algo_combo.currentText()
            if algo == "Insertion":
                self.sort_gen = insertion_steps(arr)
            elif algo == "Bubble":
                self.sort_gen = bubble_steps(arr)
            elif algo == "Selection":
                self.sort_gen = selection_steps(arr)
            elif algo == "Merge":
                self.sort_gen = merge_steps(arr)
            else:
                self.sort_gen = quick_steps(arr)
        
        try:
            step = next(self.sort_gen)
            self._handle_step(step)
        except StopIteration:
            self.sort_gen = None
    
    def run_full(self):
        """Run full sorting with animation"""
        arr = self._parse_input()
        if arr is None:
            return
        
        algo = self.algo_combo.currentText()
        if algo == "Insertion":
            self.sort_gen = insertion_steps(arr)
        elif algo == "Bubble":
            self.sort_gen = bubble_steps(arr)
        elif algo == "Selection":
            self.sort_gen = selection_steps(arr)
        elif algo == "Merge":
            self.sort_gen = merge_steps(arr)
        else:
            self.sort_gen = quick_steps(arr)
        
        self.timer.start(220)
    
    def next_step(self):
        """Timer callback for animation"""
        try:
            step = next(self.sort_gen)
            self._handle_step(step)
        except StopIteration:
            self.timer.stop()
            self.sort_gen = None
    
    def _parse_input(self) -> Optional[List[int]]:
        """Parse input field to get array"""
        text = self.input_field.text().strip()
        if not text:
            QMessageBox.warning(self, "No Input", "Please enter numbers")
            return None
        
        try:
            arr = [int(x.strip()) for x in text.split(",") if x.strip()]
            return arr
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter comma-separated integers")
            return None
    
    def _handle_step(self, step):
        """Handle a sorting step"""
        typ = step[0]
        arr = step[-1]
        highlights = []
        
        if typ == "compare":
            highlights = [step[1], step[2]]
        elif typ == "swap":
            highlights = [step[1], step[2]]
        elif typ in ("shift", "key", "insert"):
            highlights = [step[1]]
        elif typ == "merge":
            highlights = list(range(step[1], step[3] + 1))
        elif typ == "merged":
            highlights = list(range(step[1], step[2] + 1))
        
        self.canvas.set_array(arr, highlights)
    
    def show_code(self):
        """Show code for selected algorithm"""
        algo = self.algo_combo.currentText()
        
        codes = {
            "Insertion": """def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key""",
            
            "Bubble": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]""",
            
            "Selection": """def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]""",
            
            "Merge": """def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        # Merge left and right
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1""",
            
            "Quick": """def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)"""
        }
        
        QMessageBox.information(self, f"{algo} Sort Code", codes.get(algo, "Code not available"))
