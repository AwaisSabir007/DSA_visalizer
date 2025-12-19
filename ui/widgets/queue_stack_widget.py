"""
Queue and Stack Simulator Widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                                QLineEdit, QLabel, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from core.queue_stack import Queue, Stack
from utils.constants import COLORS
from utils.sound import create_pop_sound
import pygame


class QueueStackCanvas(QWidget):
    """Canvas for drawing queue and stack boxes"""
    
    def __init__(self, structure_type: str, parent=None):
        super().__init__(parent)
        self.structure_type = structure_type  # "queue" or "stack"
        self.items: list = []
        self.max_size: int = 0
        self.setMinimumSize(200, 400)
    
    def set_data(self, items: list, max_size: int):
        """Set the data to visualize"""
        self.items = items
        self.max_size = max_size
        self.update()
    
    def paintEvent(self, event):
        """Draw the boxes"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.max_size == 0:
            painter.setPen(QColor(COLORS['text_light']))
            painter.setFont(QFont("Arial", 12))
            painter.drawText(self.rect(), Qt.AlignCenter, "Set size first")
            return
        
        w = self.width()
        h = self.height()
        box_h = max((h - 80) // self.max_size, 40)
        
        # Draw boxes (top to bottom)
        for i in range(self.max_size):
            y = 40 + i * box_h
            
            # Determine if box is filled
            if self.structure_type == "stack":
                # Stack: Fill from bottom to top, show most recent at top
                # Calculate position from bottom
                stack_size = len(self.items)
                box_from_bottom = self.max_size - i - 1  # 0 is bottom, max_size-1 is top
                
                if box_from_bottom < stack_size:
                    # This box should be filled
                    filled = True
                    # Get the item: bottom item is items[0], top item is items[-1]
                    value = self.items[box_from_bottom]
                else:
                    filled = False
                    value = ""
            else:
                # Queue: rear at index 0 in display (top), front at bottom
                filled = i < len(self.items)
                value = self.items[i] if filled else ""
            
            # Draw box
            color = COLORS['box_filled'] if filled else COLORS['box_empty']
            painter.setBrush(QBrush(QColor(color)))
            painter.setPen(QPen(QColor(COLORS['border']), 2))
            painter.drawRect(w // 2 - 80, y, 160, box_h - 10)
            
            # Draw value
            if filled:
                painter.setPen(QColor(COLORS['text']))
                painter.setFont(QFont("Arial", 14, QFont.Bold))
                painter.drawText(w // 2 - 80, y, 160, box_h - 10,
                               Qt.AlignCenter, str(value))


class QueueStackWidget(QWidget):
    """Queue and Stack Simulator Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.queue: Queue = None
        self.stack: Stack = None
        self.max_size = 0
        pygame.init()
        self.pop_sound = create_pop_sound()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 20)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Queue & Stack Simulator")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']}; padding: 0px; margin: 0px;")
        layout.addWidget(title)
        
        # Size input
        size_layout = QHBoxLayout()
        size_layout.setSpacing(8)
        size_layout.addWidget(QLabel("Structure Size:"))
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("e.g., 8")
        self.size_input.setMaximumWidth(100)
        self.size_input.setMinimumHeight(35)
        size_layout.addWidget(self.size_input)
        create_btn = QPushButton("Create Structures")
        create_btn.clicked.connect(self.create_structures)
        create_btn.setMinimumHeight(35)
        size_layout.addWidget(create_btn)
        size_layout.addStretch()
        layout.addLayout(size_layout)
        
        # Controls
        controls = QHBoxLayout()
        controls.setSpacing(8)
        controls.setContentsMargins(0, 0, 0, 0)
        
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Value")
        self.value_input.setMinimumHeight(35)
        controls.addWidget(self.value_input)
        
        push_btn = QPushButton("Push (Stack)")
        push_btn.setStyleSheet(f"background-color: {COLORS['accent']};")
        push_btn.clicked.connect(self.stack_push)
        push_btn.setMinimumHeight(35)
        controls.addWidget(push_btn)
        
        pop_btn = QPushButton("Pop (Stack)")
        pop_btn.setStyleSheet(f"background-color: {COLORS['warning']};")
        pop_btn.clicked.connect(self.stack_pop)
        pop_btn.setMinimumHeight(35)
        controls.addWidget(pop_btn)
        
        enqueue_btn = QPushButton("Enqueue (Queue)")
        enqueue_btn.setStyleSheet(f"background-color: {COLORS['accent']};")
        enqueue_btn.clicked.connect(self.queue_enqueue)
        enqueue_btn.setMinimumHeight(35)
        controls.addWidget(enqueue_btn)
        
        dequeue_btn = QPushButton("Dequeue (Queue)")
        dequeue_btn.setStyleSheet(f"background-color: {COLORS['warning']};")
        dequeue_btn.clicked.connect(self.queue_dequeue)
        dequeue_btn.setMinimumHeight(35)
        controls.addWidget(dequeue_btn)
        
        layout.addLayout(controls)
        
        # Display area
        display_layout = QHBoxLayout()
        display_layout.setSpacing(8)
        
        # Stack
        stack_group = QGroupBox("Stack (Top → Bottom)")
        stack_layout = QVBoxLayout(stack_group)
        self.stack_canvas = QueueStackCanvas("stack")
        stack_layout.addWidget(self.stack_canvas)
        display_layout.addWidget(stack_group)
        
        # Queue
        queue_group = QGroupBox("Queue (Rear → Front)")
        queue_layout = QVBoxLayout(queue_group)
        self.queue_canvas = QueueStackCanvas("queue")
        queue_layout.addWidget(self.queue_canvas)
        display_layout.addWidget(queue_group)
        
        layout.addLayout(display_layout, 1)
    
    def create_structures(self):
        """Create queue and stack with specified size"""
        try:
            size = int(self.size_input.text())
            if size <= 0:
                raise ValueError
            self.max_size = size
            self.queue = Queue(size)
            self.stack = Stack(size)
            self.update_display()
            QMessageBox.information(self, "Success", f"Created structures with size {size}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a positive integer")
    
    def stack_push(self):
        """Push to stack"""
        if not self.stack:
            QMessageBox.warning(self, "Error", "Create structures first")
            return
        
        value = self.value_input.text().strip()
        if not value:
            return
        
        if self.stack.push(value):
            self.value_input.clear()
            self.update_display()
        else:
            QMessageBox.information(self, "Full", "Stack is full")
    
    def stack_pop(self):
        """Pop from stack"""
        if not self.stack:
            QMessageBox.warning(self, "Error", "Create structures first")
            return
        
        value = self.stack.pop()
        if value is not None:
            self.pop_sound.play()
            self.update_display()
        else:
            QMessageBox.information(self, "Empty", "Stack is empty")
    
    def queue_enqueue(self):
        """Enqueue to queue"""
        if not self.queue:
            QMessageBox.warning(self, "Error", "Create structures first")
            return
        
        value = self.value_input.text().strip()
        if not value:
            return
        
        if self.queue.enqueue(value):
            self.value_input.clear()
            self.update_display()
        else:
            QMessageBox.information(self, "Full", "Queue is full")
    
    def queue_dequeue(self):
        """Dequeue from queue"""
        if not self.queue:
            QMessageBox.warning(self, "Error", "Create structures first")
            return
        
        value = self.queue.dequeue()
        if value is not None:
            self.pop_sound.play()
            self.update_display()
        else:
            QMessageBox.information(self, "Empty", "Queue is empty")
    
    def update_display(self):
        """Update both canvases"""
        if self.stack:
            self.stack_canvas.set_data(self.stack.items, self.max_size)
        if self.queue:
            self.queue_canvas.set_data(self.queue.items, self.max_size)
