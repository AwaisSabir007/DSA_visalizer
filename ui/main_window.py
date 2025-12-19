"""
Main Window for DSA Visualizer
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QListWidget, QStackedWidget, QLabel, QMessageBox, 
                                QPushButton, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPainter, QColor
from ui.widgets import (BSTWidget, GraphWidget, SortingWidget,
                        QueueStackWidget, ExpressionWidget)
from utils.constants import COLORS, WINDOW_TITLE
import random


class HomeWidget(QWidget):
    """Beautiful Landing Page / Welcome Widget"""
    
    # Signal to notify when Get Started is clicked
    get_started_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize the beautiful landing page UI"""
        # Main layout for the widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Create a container for the gradient background
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e0f7f7,
                    stop:0.3 #d4f1f4,
                    stop:1 #ffffff
                );
                border: none;
            }}
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(60, 30, 60, 30)  # Reduced top/bottom
        container_layout.setSpacing(0)
        
        # Top section with title and buttons
        top_section = QWidget()
        top_section.setStyleSheet("background: transparent; border: none;")
        top_section_layout = QVBoxLayout(top_section)
        top_section_layout.setSpacing(15)  # Reduced from 20
        top_section_layout.setAlignment(Qt.AlignCenter)
        
        # Small badge/tag
        badge = QLabel("🚀 DSA Algorithm Visualizer")
        badge.setFont(QFont("Arial", 12, QFont.Bold))
        badge.setStyleSheet(f"""
            color: {COLORS['primary']};
            background-color: rgba(14, 116, 144, 0.1);
            padding: 6px 18px;
            border-radius: 18px;
            border: none;
        """)
        badge.setAlignment(Qt.AlignCenter)
        badge_container = QHBoxLayout()
        badge_container.addStretch()
        badge_container.addWidget(badge)
        badge_container.addStretch()
        top_section_layout.addLayout(badge_container)
        
        top_section_layout.addSpacing(8)
        
        # Main title - split into two lines for better design
        title_line1 = QLabel("Master Data Structures &")
        title_line1.setFont(QFont("Arial", 40, QFont.Bold))
        title_line1.setStyleSheet("color: #001219; padding: 0px; background: transparent; border: none;")
        title_line1.setAlignment(Qt.AlignCenter)
        top_section_layout.addWidget(title_line1)
        
        title_line2 = QLabel("Algorithms Visually")
        title_line2.setFont(QFont("Arial", 40, QFont.Bold))
        title_line2.setStyleSheet(f"color: {COLORS['primary']}; padding: 0px; margin-top: -10px; background: transparent; border: none;")
        title_line2.setAlignment(Qt.AlignCenter)
        top_section_layout.addWidget(title_line2)
        
        top_section_layout.addSpacing(10)
        
        # Subtitle/Description - BOLDER and LARGER
        subtitle = QLabel("Stop struggling with abstract concepts. Experience interactive\nvisualizations that make learning algorithms intuitive, engaging, and effective.")
        subtitle.setFont(QFont("Arial", 15, QFont.DemiBold))  # Changed to DemiBold
        subtitle.setStyleSheet("color: #2d3e50; line-height: 1.6; background: transparent; border: none;")  # Darker color
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        top_section_layout.addWidget(subtitle)
        
        top_section_layout.addSpacing(20)
        
        # Buttons - IMPROVED
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Get Started Button - Better text and hover effect
        get_started_btn = QPushButton("Start Visualizing →")  # Changed text
        get_started_btn.setFont(QFont("Arial", 15, QFont.Bold))
        get_started_btn.setMinimumHeight(52)
        get_started_btn.setMinimumWidth(180)
        get_started_btn.setCursor(Qt.PointingHandCursor)
        get_started_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 26px;
                padding: 14px 38px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_dark']};
                padding: 16px 40px;
            }}
            QPushButton:pressed {{
                background-color: #094d5e;
            }}
            QPushButton:focus {{
                outline: 2px solid {COLORS['primary']};
                outline-offset: 2px;
            }}
        """)
        get_started_btn.clicked.connect(self.start_exploring)
        
        # Learn More Button
        learn_more_btn = QPushButton("Learn More")
        learn_more_btn.setFont(QFont("Arial", 15))
        learn_more_btn.setMinimumHeight(52)
        learn_more_btn.setMinimumWidth(160)
        learn_more_btn.setCursor(Qt.PointingHandCursor)
        learn_more_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['primary']};
                border: 2px solid {COLORS['primary']};
                border-radius: 26px;
                padding: 14px 35px;
            }}
            QPushButton:hover {{
                background-color: rgba(14, 116, 144, 0.08);
                padding: 16px 37px;
            }}
            QPushButton:pressed {{
                background-color: rgba(14, 116, 144, 0.15);
            }}
        """)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(get_started_btn)
        buttons_layout.addWidget(learn_more_btn)
        buttons_layout.addStretch()
        top_section_layout.addLayout(buttons_layout)
        
        container_layout.addWidget(top_section)
        container_layout.addSpacing(40)  # Reduced from 50
        
        # Features section
        features_section = QWidget()
        features_section.setStyleSheet("background: transparent; border: none;")
        features_layout = QVBoxLayout(features_section)
        features_layout.setSpacing(20)
        
        # Section header
        explore_label = QLabel("EXPLORE CATEGORIES")
        explore_label.setFont(QFont("Arial", 11, QFont.Bold))
        explore_label.setStyleSheet(f"color: {COLORS['primary']}; letter-spacing: 2px; background: transparent; border: none;")
        explore_label.setAlignment(Qt.AlignCenter)
        features_layout.addWidget(explore_label)
        
        features_title = QLabel("What You'll Explore")
        features_title.setFont(QFont("Arial", 28, QFont.Bold))
        features_title.setStyleSheet("color: #001219; background: transparent; border: none;")
        features_title.setAlignment(Qt.AlignCenter)
        features_layout.addWidget(features_title)
        
        features_desc = QLabel("Dive deep into the core components of computer science with our\nspecialized interactive modules.")
        features_desc.setFont(QFont("Arial", 13))
        features_desc.setStyleSheet("color: #5a6c7d; background: transparent; border: none;")
        features_desc.setAlignment(Qt.AlignCenter)
        features_layout.addWidget(features_desc)
        
        features_layout.addSpacing(18)
        
        # Feature cards grid
        cards_grid = QHBoxLayout()
        cards_grid.setSpacing(18)
        
        features_data = [
            ("🌳", "Binary Search Tree", "Visualize Insert, Delete,\nand Search with BFS/DFS\ntraversals.", "Beginner"),
            ("🔗", "Graph Algorithms", "Explore directed weighted\ngraphs with BFS, DFS, and\nsearching.", "Intermediate"),
            ("📊", "Sorting Algorithms", "5 key sorting algorithms\nwith step-by-step visual\nfeedback.", "Beginner"),
            ("📚", "Queue & Stack", "Interactive simulators for\nLIFO and FIFO data\nstructures.", "Beginner"),
            ("🔢", "Expressions", "Convert and evaluate\ninfix, Postfix, and Prefix\nexpressions.", "Intermediate")
        ]
        
        for icon, title_text, desc, difficulty in features_data:
            card = self.create_feature_card(icon, title_text, desc, difficulty)
            cards_grid.addWidget(card)
        
        features_layout.addLayout(cards_grid)
        
        container_layout.addWidget(features_section)
        container_layout.addSpacing(25)
        
        # Footer
        footer = QLabel("© 2025 DSA Algorithm Visualizer. All rights reserved.")
        footer.setFont(QFont("Arial", 10))
        footer.setStyleSheet("color: #8b9ba8; padding: 15px; background: transparent; border: none;")
        footer.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(footer)
        
        # Set the container as the scroll area's widget
        scroll.setWidget(container)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll)
    
    def create_feature_card(self, icon, title, description, difficulty):
        """Create a clickable feature card widget with difficulty badge"""
        card = QPushButton()  # Changed to QPushButton to make it clickable
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8eef2;
                text-align: left;
                padding: 0px;
            }
            QPushButton:hover {
                border: 1px solid #0e7490;
                background-color: #f8fcfd;
                margin-top: -3px;
                margin-bottom: 3px;
            }
            QPushButton:pressed {
                background-color: #f0f9fa;
            }
        """)
        card.setMinimumHeight(220)
        card.setMaximumWidth(210)
        
        # Create layout for card content
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        card_layout.setContentsMargins(20, 25, 20, 25)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 38))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("background: transparent; border: none;")
        card_layout.addWidget(icon_label)
        
        card_layout.addSpacing(3)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #001219; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        card_layout.addWidget(title_label)
        
        # Difficulty badge
        difficulty_badge = QLabel(difficulty)
        difficulty_badge.setFont(QFont("Arial", 9, QFont.Bold))
        
        # Color based on difficulty
        if difficulty == "Beginner":
            badge_color = "#10b981"  # Green
        elif difficulty == "Intermediate":
            badge_color = "#f59e0b"  # Orange
        else:
            badge_color = "#ef4444"  # Red
            
        difficulty_badge.setStyleSheet(f"""
            color: {badge_color};
            background-color: rgba(16, 185, 129, 0.1);
            padding: 3px 10px;
            border-radius: 10px;
            border: none;
        """)
        difficulty_badge.setAlignment(Qt.AlignCenter)
        
        badge_container = QHBoxLayout()
        badge_container.addStretch()
        badge_container.addWidget(difficulty_badge)
        badge_container.addStretch()
        card_layout.addLayout(badge_container)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 11))
        desc_label.setStyleSheet("color: #5a6c7d; line-height: 1.5; background: transparent; border: none;")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        card_layout.addStretch()
        
        return card
    
    
    def start_exploring(self):
        """Emit signal to switch to dashboard"""
        self.get_started_clicked.emit()




class MainWindow(QMainWindow):
    """Main application window"""
    
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, 1200, 720)
        self.showing_landing = True  # Track if we're showing landing page
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        # Central widget with stacked layout for landing/dashboard switch
        self.central = QWidget()
        self.setCentralWidget(self.central)
        
        # Main stacked widget to switch between landing and dashboard
        self.main_stack = QStackedWidget(self.central)
        main_layout = QVBoxLayout(self.central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_stack)
        
        # Create landing page
        self.landing_widget = HomeWidget()
        self.landing_widget.get_started_clicked.connect(self.show_dashboard)
        
        # Create dashboard container
        self.dashboard_widget = QWidget()
        self.setup_dashboard()
        
        # Add both to main stack
        self.main_stack.addWidget(self.landing_widget)
        self.main_stack.addWidget(self.dashboard_widget)
        
        # Show landing page first
        self.main_stack.setCurrentIndex(0)
        
        # Menu bar
        self.create_menu()
    
    def setup_dashboard(self):
        """Setup the main dashboard with sidebar and features"""
        dashboard_layout = QHBoxLayout(self.dashboard_widget)
        dashboard_layout.setSpacing(12)
        dashboard_layout.setContentsMargins(12, 12, 12, 12)
        
        # Sidebar (without Home button)
        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(220)
        self.sidebar.setMinimumWidth(220)
        self.sidebar.addItems([
            "BST Visualizer",
            "Graph Visualizer",
            "Sorting Visualizer",
            "Queue & Stack",
            "Expressions"
        ])
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.change_page)
        dashboard_layout.addWidget(self.sidebar)
        
        # Stacked widget for content
        self.content_stack = QStackedWidget()
        
        # Add feature widgets (no home widget)
        self.bst_widget = BSTWidget()
        self.graph_widget = GraphWidget()
        self.sorting_widget = SortingWidget()
        self.queue_stack_widget = QueueStackWidget()
        self.expression_widget = ExpressionWidget()
        
        self.content_stack.addWidget(self.bst_widget)
        self.content_stack.addWidget(self.graph_widget)
        self.content_stack.addWidget(self.sorting_widget)
        self.content_stack.addWidget(self.queue_stack_widget)
        self.content_stack.addWidget(self.expression_widget)
        
        dashboard_layout.addWidget(self.content_stack)
    
    def show_dashboard(self):
        """Switch from landing page to dashboard"""
        self.showing_landing = False
        self.main_stack.setCurrentIndex(1)  # Show dashboard
        self.sidebar.setCurrentRow(0)  # Select first item (BST)
        self.content_stack.setCurrentIndex(0)  # Show BST widget
    
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
        """Change the displayed page in dashboard"""
        self.content_stack.setCurrentIndex(index)
    
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
