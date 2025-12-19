"""
Binary Search Tree Visualizer Widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                                QLineEdit, QLabel, QMessageBox)
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from core.bst import BST, NodeBST
from algorithms.traversals import get_traversal_code
from utils.constants import COLORS, DEFAULT_NODE_RADIUS, ANIMATION_SPEED
from typing import Optional, List


class BSTCanvas(QWidget):
    """Canvas widget for drawing BST"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bst: Optional[BST] = None
        self.highlight_value: Optional[int] = None
        self.highlight_path: List[int] = []
        self.setMinimumSize(600, 400)
    
    def set_bst(self, bst: BST):
        """Set the BST to visualize"""
        self.bst = bst
        self.update()
    
    def set_highlight(self, value: Optional[int] = None, path: List[int] = None):
        """Set highlighting for search visualization"""
        self.highlight_value = value
        self.highlight_path = path if path else []
        self.update()
    
    def paintEvent(self, event):
        """Draw the BST"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.bst or not self.bst.root:
            painter.setPen(QColor(COLORS['text_light']))
            painter.setFont(QFont("Arial", 14))
            painter.drawText(self.rect(), Qt.AlignCenter, "Empty BST - Insert nodes to visualize")
            return
        
        # Layout the tree
        self._layout_tree()
        
        # Draw edges first
        self._draw_edges(painter, self.bst.root)
        
        # Draw nodes
        self._draw_nodes(painter, self.bst.root)
    
    def _layout_tree(self):
        """Calculate positions for all nodes"""
        counter = {'x': 0}
        
        def assign_positions(node: Optional[NodeBST], depth: int = 0):
            if not node:
                return
            assign_positions(node.left, depth + 1)
            counter['x'] += 1
            node.x = counter['x']
            node.y = depth
            assign_positions(node.right, depth + 1)
        
        assign_positions(self.bst.root)
        
        # Convert to canvas coordinates
        if counter['x'] == 0:
            return
        
        w = self.width()
        spacing = max((w - 40) / (counter['x'] + 1), 40)
        
        def set_canvas_coords(node: Optional[NodeBST]):
            if not node:
                return
            node.canvas_x = int(20 + node.x * spacing)
            node.canvas_y = int(60 + node.y * 80)
            set_canvas_coords(node.left)
            set_canvas_coords(node.right)
        
        set_canvas_coords(self.bst.root)
    
    def _draw_edges(self, painter: QPainter, node: Optional[NodeBST]):
        """Draw edges between nodes"""
        if not node:
            return
        
        pen = QPen(QColor(COLORS['text']), 2)
        painter.setPen(pen)
        
        if node.left:
            painter.drawLine(node.canvas_x, node.canvas_y,
                           node.left.canvas_x, node.left.canvas_y)
        if node.right:
            painter.drawLine(node.canvas_x, node.canvas_y,
                           node.right.canvas_x, node.right.canvas_y)
        
        self._draw_edges(painter, node.left)
        self._draw_edges(painter, node.right)
    
    def _draw_nodes(self, painter: QPainter, node: Optional[NodeBST]):
        """Draw nodes"""
        if not node:
            return
        
        r = DEFAULT_NODE_RADIUS
        
        # Determine fill color
        fill_color = COLORS['node_default']
        if node.value in self.highlight_path:
            fill_color = COLORS['node_path']
        elif node.value == self.highlight_value:
            fill_color = COLORS['node_highlight']
        
        # Draw circle
        painter.setBrush(QBrush(QColor(fill_color)))
        painter.setPen(QPen(QColor(COLORS['node_border']), 2))
        painter.drawEllipse(QPointF(node.canvas_x, node.canvas_y), r, r)
        
        # Draw value
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(node.canvas_x - r, node.canvas_y - r,
                        r * 2, r * 2, Qt.AlignCenter, str(node.value))
        
        self._draw_nodes(painter, node.left)
        self._draw_nodes(painter, node.right)


class BSTWidget(QWidget):
    """BST Visualizer Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bst = BST()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Binary Search Tree Visualizer")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']};")
        layout.addWidget(title)
        
        # Controls
        controls = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter integer value")
        controls.addWidget(self.input_field)
        
        insert_btn = QPushButton("Insert")
        insert_btn.clicked.connect(self.insert_node)
        controls.addWidget(insert_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_node)
        controls.addWidget(delete_btn)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_node)
        controls.addWidget(search_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_tree)
        controls.addWidget(clear_btn)
        
        layout.addLayout(controls)
        
        # Traversal buttons
        traversal_layout = QHBoxLayout()
        
        inorder_btn = QPushButton("Inorder")
        inorder_btn.clicked.connect(lambda: self.show_traversal("inorder"))
        traversal_layout.addWidget(inorder_btn)
        
        preorder_btn = QPushButton("Preorder")
        preorder_btn.clicked.connect(lambda: self.show_traversal("preorder"))
        traversal_layout.addWidget(preorder_btn)
        
        postorder_btn = QPushButton("Postorder")
        postorder_btn.clicked.connect(lambda: self.show_traversal("postorder"))
        traversal_layout.addWidget(postorder_btn)
        
        inorder_code_btn = QPushButton("In Code")
        inorder_code_btn.clicked.connect(lambda: self.show_code("inorder"))
        traversal_layout.addWidget(inorder_code_btn)
        
        preorder_code_btn = QPushButton("Pre Code")
        preorder_code_btn.clicked.connect(lambda: self.show_code("preorder"))
        traversal_layout.addWidget(preorder_code_btn)
        
        postorder_code_btn = QPushButton("Post Code")
        postorder_code_btn.clicked.connect(lambda: self.show_code("postorder"))
        traversal_layout.addWidget(postorder_code_btn)
        
        layout.addLayout(traversal_layout)
        
        # Canvas
        self.canvas = BSTCanvas()
        self.canvas.set_bst(self.bst)
        layout.addWidget(self.canvas)
    
    def insert_node(self):
        """Insert a node into the BST"""
        try:
            value = int(self.input_field.text())
            if self.bst.insert(value):
                self.canvas.set_bst(self.bst)
                self.input_field.clear()
            else:
                QMessageBox.information(self, "Info", f"{value} already exists in the tree")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer")
    
    def delete_node(self):
        """Delete a node from the BST"""
        try:
            value = int(self.input_field.text())
            if self.bst.delete(value):
                self.canvas.set_bst(self.bst)
                self.input_field.clear()
            else:
                QMessageBox.information(self, "Info", f"{value} not found in the tree")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer")
    
    def search_node(self):
        """Search for a node in the BST"""
        try:
            value = int(self.input_field.text())
            node = self.bst.search(value)
            if node:
                QMessageBox.information(self, "Found", f"{value} found in the tree!")
                # Highlight the found node
                self.canvas.set_highlight(value=value)
            else:
                QMessageBox.information(self, "Not Found", f"{value} not found in the tree")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer")
    
    def clear_tree(self):
        """Clear the entire tree"""
        self.bst = BST()
        self.canvas.set_bst(self.bst)
        self.canvas.set_highlight()
    
    def show_traversal(self, traversal_type: str):
        """Show traversal result"""
        if traversal_type == "inorder":
            result = self.bst.inorder()
        elif traversal_type == "preorder":
            result = self.bst.preorder()
        else:
            result = self.bst.postorder()
        
        QMessageBox.information(self, f"{traversal_type.capitalize()} Traversal",
                               ", ".join(map(str, result)) if result else "Empty tree")
    
    def show_code(self, traversal_type: str):
        """Show code for traversal"""
        code = get_traversal_code(traversal_type, "tree")
        QMessageBox.information(self, f"{traversal_type.capitalize()} Code", code)
