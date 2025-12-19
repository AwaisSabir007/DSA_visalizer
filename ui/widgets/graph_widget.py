"""
Graph Visualizer Widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                                QLineEdit, QLabel, QMessageBox, QTextEdit, QInputDialog)
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPolygonF
from core.graph import GraphType, HeuristicsType
from algorithms.searching import bfs_steps, dfs_steps
from algorithms.traversals import get_traversal_code
from utils.constants import COLORS, DEFAULT_GRAPH_NODE_RADIUS
from typing import Dict, Tuple, List, Set
import math


class GraphCanvas(QWidget):
    """Canvas widget for drawing graphs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph: GraphType = {}
        self.heuristics: HeuristicsType = {}
        self.positions: Dict[str, Tuple[float, float]] = {}
        self.highlight_node: str = ""
        self.highlight_path: List[str] = []
        self.setMinimumSize(600, 400)
    
    def set_graph(self, graph: GraphType, heuristics: HeuristicsType = None):
        """Set the graph to visualize"""
        self.graph = graph
        self.heuristics = heuristics or {}
        self.auto_layout()
        self.update()
    
    def auto_layout(self):
        """Automatically layout nodes in a circle"""
        nodes = sorted(self.graph.keys())
        n = len(nodes)
        if n == 0:
            return
        
        w = max(self.width(), 600)
        h = max(self.height(), 400)
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2 - 80
        
        self.positions = {}
        for i, node in enumerate(nodes):
            ang = 2 * math.pi * i / n
            x = cx + r * math.cos(ang)
            y = cy + r * math.sin(ang)
            self.positions[node] = (x, y)
    
    def set_highlight(self, node: str = "", path: List[str] = None):
        """Set highlighting for search visualization"""
        self.highlight_node = node
        self.highlight_path = path if path else []
        self.update()
    
    def paintEvent(self, event):
        """Draw the graph"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.graph:
            painter.setPen(QColor(COLORS['text_light']))
            painter.setFont(QFont("Arial", 14))
            painter.drawText(self.rect(), Qt.AlignCenter, "No graph loaded - Load graph from text")
            return
        
        # Draw edges with weights
        for u, edges in self.graph.items():
            ux, uy = self.positions.get(u, (50, 50))
            for (v, w) in edges:
                vx, vy = self.positions.get(v, (50, 50))
                self._draw_arrow(painter, ux, uy, vx, vy, str(w))
        
        # Draw nodes
        for node, (x, y) in self.positions.items():
            r = DEFAULT_GRAPH_NODE_RADIUS
            
            # Determine fill color
            fill_color = COLORS['graph_node']
            if node in self.highlight_path:
                fill_color = COLORS['node_path']
            elif node == self.highlight_node:
                fill_color = COLORS['node_highlight']
            
            # Draw circle
            painter.setBrush(QBrush(QColor(fill_color)))
            painter.setPen(QPen(QColor(COLORS['graph_edge']), 2))
            painter.drawEllipse(QPointF(x, y), r, r)
            
            # Draw node label
            painter.setPen(QColor("#001219"))
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(int(x - r), int(y - r), int(r * 2), int(r * 2),
                           Qt.AlignCenter, str(node))
            
            # Draw heuristic if available
            if node in self.heuristics:
                painter.setPen(QColor(COLORS['text_light']))
                painter.setFont(QFont("Arial", 9))
                painter.drawText(int(x - r), int(y + r + 5), int(r * 2), 20,
                               Qt.AlignCenter, f"h={self.heuristics[node]}")
    
    def _draw_arrow(self, painter: QPainter, x1: float, y1: float,
                   x2: float, y2: float, text: str = ""):
        """Draw directed edge with arrow and weight"""
        dx = x2 - x1
        dy = y2 - y1
        d = math.hypot(dx, dy)
        if d == 0:
            return
        
        ux, uy = dx / d, dy / d
        pad = 28
        sx = x1 + ux * pad
        sy = y1 + uy * pad
        ex = x2 - ux * pad
        ey = y2 - uy * pad
        
        # Draw line
        painter.setPen(QPen(QColor(COLORS['graph_edge']), 2))
        painter.drawLine(int(sx), int(sy), int(ex), int(ey))
        
        # Draw arrowhead
        arrow_size = 10
        angle = math.atan2(dy, dx)
        p1 = QPointF(ex - arrow_size * math.cos(angle - math.pi / 6),
                     ey - arrow_size * math.sin(angle - math.pi / 6))
        p2 = QPointF(ex, ey)
        p3 = QPointF(ex - arrow_size * math.cos(angle + math.pi / 6),
                     ey - arrow_size * math.sin(angle + math.pi / 6))
        
        painter.setBrush(QBrush(QColor(COLORS['graph_edge'])))
        painter.drawPolygon(QPolygonF([p1, p2, p3]))
        
        # Draw weight
        if text:
            mx = (sx + ex) / 2
            my = (sy + ey) / 2
            painter.setPen(QColor(COLORS['text']))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(int(mx - 15), int(my - 20), 30, 20,
                           Qt.AlignCenter, text)


class GraphWidget(QWidget):
    """Graph Visualizer Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph: GraphType = {}
        self.heuristics: HeuristicsType = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 20)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Graph Visualizer")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']}; padding: 0px; margin: 0px;")
        layout.addWidget(title)
        
        # Top controls
        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)
        
        # Graph input
        self.graph_text = QTextEdit()
        self.graph_text.setMaximumHeight(160)
        example = ("graph={\n"
                   "  'A':[('B',3),('C',1),('D',5)],\n"
                   "  'B':[('E',7)],\n"
                   "  'C':[('F',4),('E',7)],\n"
                   "  'D':[('F',9)],\n"
                   "  'E':[('H',6)],\n"
                   "  'F':[('G',2)],\n"
                   "  'G':[],\n"
                   "  'H':[('G',7)]\n}")
        self.graph_text.setPlainText(example)
        top_layout.addWidget(self.graph_text)
        
        # Right controls
        right_controls = QVBoxLayout()
        right_controls.setSpacing(8)
        
        load_btn = QPushButton("Load Graph")
        load_btn.clicked.connect(self.load_graph)
        load_btn.setMinimumHeight(35)
        right_controls.addWidget(load_btn)
        
        clear_btn = QPushButton("Clear Graph")
        clear_btn.clicked.connect(self.clear_graph)
        clear_btn.setMinimumHeight(35)
        right_controls.addWidget(clear_btn)
        
        layout_btn = QPushButton("Auto Layout")
        layout_btn.clicked.connect(self.auto_layout)
        layout_btn.setMinimumHeight(35)
        right_controls.addWidget(layout_btn)
        
        top_layout.addLayout(right_controls)
        layout.addLayout(top_layout)
        
        # Search controls
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Start node")
        self.start_input.setMinimumHeight(35)
        search_layout.addWidget(self.start_input)
        
        self.goal_input = QLineEdit()
        self.goal_input.setPlaceholderText("Goal node")
        self.goal_input.setMinimumHeight(35)
        search_layout.addWidget(self.goal_input)
        
        search_btn = QPushButton("Search (BFS/DFS)")
        search_btn.clicked.connect(self.search_graph)
        search_btn.setMinimumHeight(35)
        search_layout.addWidget(search_btn)
        
        preorder_btn = QPushButton("Preorder DFS")
        preorder_btn.clicked.connect(self.show_preorder)
        preorder_btn.setMinimumHeight(35)
        search_layout.addWidget(preorder_btn)
        
        postorder_btn = QPushButton("Postorder DFS")
        postorder_btn.clicked.connect(self.show_postorder)
        postorder_btn.setMinimumHeight(35)
        search_layout.addWidget(postorder_btn)
        
        layout.addLayout(search_layout)
        
        # Canvas
        self.canvas = GraphCanvas()
        layout.addWidget(self.canvas, 1)
    
    def load_graph(self):
        """Load graph from text input"""
        text = self.graph_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "No Input", "Please enter graph definition")
            return
        
        try:
            local_vars = {}
            exec(text, {}, local_vars)
            if "graph" in local_vars and isinstance(local_vars["graph"], dict):
                self.graph = local_vars["graph"]
                self.heuristics = local_vars.get("Heuristic_Values", {})
                self.canvas.set_graph(self.graph, self.heuristics)
                QMessageBox.information(self, "Success", "Graph loaded successfully!")
            else:
                QMessageBox.warning(self, "Error", "Text must define 'graph' variable")
        except Exception as e:
            QMessageBox.critical(self, "Parse Error", str(e))
    
    def clear_graph(self):
        """Clear the graph"""
        self.graph = {}
        self.heuristics = {}
        self.canvas.set_graph(self.graph, self.heuristics)
    
    def auto_layout(self):
        """Re-layout the graph"""
        self.canvas.auto_layout()
        self.canvas.update()
    
    def search_graph(self):
        """Search the graph using BFS or DFS"""
        start = self.start_input.text().strip()
        goal = self.goal_input.text().strip()
        
        if not start or not goal:
            QMessageBox.warning(self, "Input Required", "Enter start and goal nodes")
            return
        
        if start not in self.graph:
            QMessageBox.warning(self, "Error", f"Start node '{start}' not in graph")
            return
        
        algo, ok = QInputDialog.getItem(self, "Algorithm", "Choose search algorithm:",
                                        ["BFS", "DFS"], 0, False)
        if not ok:
            return
        
        # Run search
        if algo == "BFS":
            gen = bfs_steps(self.graph, start, goal)
        else:
            gen = dfs_steps(self.graph, start, goal)
        
        visited_order = []
        path = None
        for step in gen:
            if step[0] == "visit":
                visited_order.append(step[1])
            elif step[0] == "found":
                path = step[1]
                break
        
        if path:
            QMessageBox.information(self, "Found", f"Path: {' -> '.join(path)}")
            self.canvas.set_highlight(path=path)
        else:
            QMessageBox.information(self, "Not Found", "Goal not reachable from start")
    
    def show_preorder(self):
        """Show preorder DFS traversal"""
        start = self.start_input.text().strip() or (list(self.graph.keys())[0] if self.graph else "")
        if not start:
            QMessageBox.warning(self, "No Graph", "Load a graph first")
            return
        
        order = self._graph_preorder(start)
        QMessageBox.information(self, "Preorder DFS", " -> ".join(order))
    
    def show_postorder(self):
        """Show postorder DFS traversal"""
        start = self.start_input.text().strip() or (list(self.graph.keys())[0] if self.graph else "")
        if not start:
            QMessageBox.warning(self, "No Graph", "Load a graph first")
            return
        
        order = self._graph_postorder(start)
        QMessageBox.information(self, "Postorder DFS", " -> ".join(order))
    
    def _graph_preorder(self, start: str) -> List[str]:
        """Preorder DFS traversal"""
        visited = []
        stack = [start]
        seen: Set[str] = set()
        while stack:
            node = stack[-1]
            if node not in seen:
                seen.add(node)
                visited.append(node)
            found = False
            for nbr, _ in reversed(self.graph.get(node, [])):
                if nbr not in seen:
                    stack.append(nbr)
                    found = True
                    break
            if not found:
                stack.pop()
        return visited
    
    def _graph_postorder(self, start: str) -> List[str]:
        """Postorder DFS traversal"""
        visited = []
        def dfs(node):
            for nbr, _ in self.graph.get(node, []):
                if nbr not in visited:
                    dfs(nbr)
            visited.append(node)
        dfs(start)
        visited.reverse()
        return visited
