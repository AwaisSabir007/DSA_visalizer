"""
Main Window for DSA Visualizer
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QListWidget, QStackedWidget, QLabel, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QColor
from ui.widgets import (BSTWidget, GraphWidget, SortingWidget,
                        QueueStackWidget, ExpressionWidget)
from utils.constants import COLORS, WINDOW_TITLE
import random


class HomeWidget(QWidget):
    """Home/Welcome widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Welcome message
        welcome = QLabel("Welcome to DSA Visualizer")
        welcome.setFont(QFont("Arial", 28, QFont.Bold))
        welcome.setStyleSheet(f"color: {COLORS['primary']};")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)
        
        # Description
        desc = QLabel("Explore algorithms with interactive visualizations!")
        desc.setFont(QFont("Arial", 16))
        desc.setStyleSheet(f"color: {COLORS['primary_dark']};")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        layout.addSpacing(40)
        
        # Features list
        features = QLabel(
            "Features:\n\n"
            "• Binary Search Tree - Insert, Delete, Search with BFS/DFS\n"
            "• Graph Visualizer - Directed weighted graphs with search algorithms\n"
            "• Sorting Algorithms - Insertion, Bubble, Selection, Merge, Quick\n"
            "• Queue & Stack - Interactive simulators with animations\n"
            "• Expression Converter - Infix ↔ Postfix/Prefix with evaluation"
        )
        features.setFont(QFont("Arial", 14))
        features.setStyleSheet(f"color: {COLORS['text']};")
        features.setAlignment(Qt.AlignLeft)
        layout.addWidget(features)
        
        layout.addSpacing(20)
        
        # Random fact label
        self.fact_label = QLabel()
        self.fact_label.setFont(QFont("Arial", 12))
        self.fact_label.setStyleSheet(f"color: {COLORS['text_light']}; padding: 20px;")
        self.fact_label.setWordWrap(True)
        self.fact_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.fact_label)
        
        self.show_random_fact()
    
    def show_random_fact(self):
        """Show a random DSA fact"""
        facts = [
            "Binary Search Trees enable efficient searching in O(log n) time on average.",
            "Graphs are used to model relationships like social networks or maps.",
            "Sorting algorithms like Quick Sort have average time complexity of O(n log n).",
            "Stacks follow Last In First Out (LIFO) principle.",
            "Queues follow First In First Out (FIFO) principle.",
            "Postfix expressions eliminate the need for parentheses in evaluation.",
            "DFS uses a stack while BFS uses a queue for traversal.",
            "Merge Sort is a stable sorting algorithm with O(n log n) complexity."
        ]
        self.fact_label.setText(f"💡 Did you know?\n{random.choice(facts)}")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, 1200, 720)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(12, 12, 12, 12)
        
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(220)
        self.sidebar.setMinimumWidth(220)
        self.sidebar.addItems([
            "Home",
            "BST Visualizer",
            "Graph Visualizer",
            "Sorting Visualizer",
            "Queue & Stack",
            "Expressions"
        ])
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.change_page)
        main_layout.addWidget(self.sidebar)
        
        # Stacked widget for content
        self.stack = QStackedWidget()
        
        # Add widgets
        self.home_widget = HomeWidget()
        self.bst_widget = BSTWidget()
        self.graph_widget = GraphWidget()
        self.sorting_widget = SortingWidget()
        self.queue_stack_widget = QueueStackWidget()
        self.expression_widget = ExpressionWidget()
        
        self.stack.addWidget(self.home_widget)
        self.stack.addWidget(self.bst_widget)
        self.stack.addWidget(self.graph_widget)
        self.stack.addWidget(self.sorting_widget)
        self.stack.addWidget(self.queue_stack_widget)
        self.stack.addWidget(self.expression_widget)
        
        main_layout.addWidget(self.stack)
        
        # Menu bar
        self.create_menu()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
        help_action = help_menu.addAction("Help")
        help_action.triggered.connect(self.show_help)
    
    def change_page(self, index):
        """Change the displayed page"""
        self.stack.setCurrentIndex(index)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About DSA Visualizer",
            "DSA Algorithm Visualizer\n\n"
            "A comprehensive tool for visualizing data structures and algorithms.\n\n"
            "Built with PySide6 and Python\n"
            "Version 1.0"
        )
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
DSA Algorithm Visualizer - Help

Home:
- Welcome page with DSA facts and feature overview

BST Visualizer:
- Insert, delete, search nodes
- View inorder, preorder, postorder traversals
- Display code for each traversal

Graph Visualizer:
- Load graph from Python dictionary
- Search using BFS/DFS with visualization
- Preorder/Postorder DFS traversals

Sorting Visualizer:
- Supports 5 sorting algorithms
- Step-by-step or full animation
- View code for each algorithm

Queue & Stack:
- Create fixed-size structures
- Push/Pop and Enqueue/Dequeue operations
- Visual feedback with sound effects

Expressions:
- Convert infix to postfix/prefix
- Evaluate numeric postfix expressions
- Step-by-step conversion display
        """
        QMessageBox.information(self, "Help", help_text)
