# modern_algo_dashboard.py
"""
Modern Dashboard Theme - Algorithm Visualizer Suite
Features:
 - Modern UI using CustomTkinter (sidebar + main area)
 - BST Visualizer (insert/delete/search/traversals)
 - Graph Visualizer (directed weighted graph from dict)
 - Sorting visualizer: Insertion, Bubble, Selection, Merge, Quick (step-by-step)
 - Queue & Stack simulators + postfix/prefix converters
Author: ChatGPT (GPT-5 Thinking mini)
"""
import pygame
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import math
import random
import heapq
from typing import Dict, List, Tuple, Optional
import time
import pygame
import numpy as np

# ----------- Utilities & Data Structures -----------

class NodeBST:
    def __init__(self, value: int):
        self.value = value
        self.left: Optional["NodeBST"] = None
        self.right: Optional["NodeBST"] = None
        # drawing coords
        self.x = 0
        self.y = 0
        self.canvas_x = 0
        self.canvas_y = 0

class BST:
    def __init__(self):
        self.root: Optional[NodeBST] = None

    def insert(self, value: int) -> bool:
        if self.root is None:
            self.root = NodeBST(value)
            return True
        return self._insert(self.root, value)

    def _insert(self, node: NodeBST, value: int) -> bool:
        if value == node.value:
            return False
        if value < node.value:
            if node.left:
                return self._insert(node.left, value)
            else:
                node.left = NodeBST(value)
                return True
        else:
            if node.right:
                return self._insert(node.right, value)
            else:
                node.right = NodeBST(value)
                return True

    def search(self, value: int) -> Optional[NodeBST]:
        return self._search(self.root, value)

    def _search(self, node: Optional[NodeBST], value: int) -> Optional[NodeBST]:
        if not node:
            return None
        if node.value == value:
            return node
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def delete(self, value: int) -> bool:
        self.root, deleted = self._delete(self.root, value)
        return deleted

    def _delete(self, node: Optional[NodeBST], value: int):
        if node is None:
            return None, False
        if value < node.value:
            node.left, deleted = self._delete(node.left, value)
            return node, deleted
        elif value > node.value:
            node.right, deleted = self._delete(node.right, value)
            return node, deleted
        else:
            # found
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            # two children
            succ = node.right
            while succ.left:
                succ = succ.left
            node.value = succ.value
            node.right, _ = self._delete(node.right, succ.value)
            return node, True

    # traversal lists
    def inorder(self):
        res = []
        self._in(self.root, res)
        return res

    def _in(self, node, arr):
        if node:
            self._in(node.left, arr)
            arr.append(node.value)
            self._in(node.right, arr)

    def preorder(self):
        res = []
        self._pre(self.root, res)
        return res

    def _pre(self, node, arr):
        if node:
            arr.append(node.value)
            self._pre(node.left, arr)
            self._pre(node.right, arr)

    def postorder(self):
        res = []
        self._post(self.root, res)
        return res

    def _post(self, node, arr):
        if node:
            self._post(node.left, arr)
            self._post(node.right, arr)
            arr.append(node.value)


# ---------- Graph utilities ----------
# Graph represented as dict[str] -> List[ (neighbor, weight) ]
GraphType = Dict[str, List[Tuple[str, float]]]

# Simple heuristic dict type alias
HeuristicsType = Dict[str, float]

# Search algorithm implementations (yield steps for visualization)
def bfs_steps(graph: GraphType, start: str, goal: str):
    from collections import deque
    q = deque([start])
    visited = set([start])
    parent = {start: None}
    while q:
        node = q.popleft()
        yield ("visit", node, list(q), visited)
        if node == goal:
            # reconstruct path
            path = []
            cur = node
            while cur:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            yield ("found", path)
            return
        for (nbr, _) in graph.get(node, []):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = node
                q.append(nbr)
                yield ("enqueue", nbr, list(q), visited)
    yield ("notfound", None)

def dfs_steps(graph: GraphType, start: str, goal: str):
    stack = [start]
    visited = set()
    parent = {start: None}
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        yield ("visit", node, list(stack), visited)
        if node == goal:
            path = []
            cur = node
            while cur:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            yield ("found", path)
            return
        # push neighbors in reverse order to preserve natural ordering
        neighbors = [n for (n,_) in graph.get(node,[])]
        for nbr in reversed(neighbors):
            if nbr not in visited:
                parent[nbr] = node
                stack.append(nbr)
                yield ("push", nbr, list(stack), visited)
    yield ("notfound", None)


# ----------- Sorting steps (insertion, bubble, selection, merge, quick) ----------
def insertion_steps(arr: List[int]):
    a = list(arr)
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        yield ("key", i, list(a))
        while j >= 0 and a[j] > key:
            yield ("compare", j, j + 1, list(a))
            a[j + 1] = a[j]
            yield ("shift", j + 1, list(a))
            j -= 1
        a[j + 1] = key
        yield ("insert", j + 1, list(a))
    yield ("done", list(a))

def bubble_steps(arr: List[int]):
    a = list(arr)
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            yield ("compare", j, j+1, list(a))
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                yield ("swap", j, j+1, list(a))
    yield ("done", list(a))

def selection_steps(arr: List[int]):
    a = list(arr)
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield ("compare", min_idx, j, list(a))
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            yield ("swap", i, min_idx, list(a))
    yield ("done", list(a))

def merge_steps(arr: List[int]):
    a = list(arr)
    n = len(a)
    curr_size = 1
    while curr_size < n:
        left_start = 0
        while left_start < n - 1:
            mid = min(left_start + curr_size - 1, n - 1)
            right_end = min(left_start + 2 * curr_size - 1, n - 1)
            yield ("merge", left_start, mid, right_end, list(a))
            temp = [0] * (right_end - left_start + 1)
            i = left_start
            j = mid + 1
            k = 0
            while i <= mid and j <= right_end:
                yield ("compare", i, j, list(a))
                if a[i] <= a[j]:
                    temp[k] = a[i]
                    i += 1
                else:
                    temp[k] = a[j]
                    j += 1
                k += 1
            while i <= mid:
                temp[k] = a[i]
                i += 1
                k += 1
            while j <= right_end:
                temp[k] = a[j]
                j += 1
                k += 1
            for m in range(len(temp)):
                a[left_start + m] = temp[m]
            yield ("merged", left_start, right_end, list(a))
            left_start += 2 * curr_size
        curr_size *= 2
    yield ("done", list(a))

def quick_steps(arr: List[int]):
    a = list(arr)
    def qs(a, l, r):
        if l >= r:
            return
        pivot = a[r]
        i = l
        for j in range(l, r):
            yield ("compare", j, r, list(a))
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                yield ("swap", i, j, list(a))
                i += 1
        a[i], a[r] = a[r], a[i]
        yield ("swap", i, r, list(a))
        yield from qs(a, l, i-1)
        yield from qs(a, i+1, r)
    yield from qs(a, 0, len(a)-1)
    yield ("done", a)

# ----------- Expression conversions (infix <-> postfix/prefix) ----------
def infix_to_postfix_steps(expr: str) -> Tuple[str, List[str]]:
    prec = {'+':1, '-':1, '*':2, '/':2, '^':3}
    output = []
    stack = []
    steps = []
    tokens = tokenize_expr(expr)
    for t in tokens:
        if t.isalnum():
            output.append(t)
        elif t == '(':
            stack.append(t)
        elif t == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
        else:
            while stack and stack[-1] != '(' and ((prec.get(stack[-1],0) > prec.get(t,0)) or (prec.get(stack[-1],0) == prec.get(t,0) and t != '^')):
                output.append(stack.pop())
            stack.append(t)
        steps.append(f"Token: {t}\nOutput: {' '.join(output)}\nStack: {' '.join(stack)}")
    while stack:
        output.append(stack.pop())
        steps.append(f"Drain stack\nOutput: {' '.join(output)}\nStack: {' '.join(stack)}")
    return " ".join(output), steps

def infix_to_prefix_steps(expr: str) -> Tuple[str, List[str]]:
    tokens = tokenize_expr(expr)
    tokens_rev = []
    for t in reversed(tokens):
        if t == '(':
            tokens_rev.append(')')
        elif t == ')':
            tokens_rev.append('(')
        else:
            tokens_rev.append(t)
    postfix, steps = infix_to_postfix_steps(" ".join(tokens_rev))
    pre_tokens = list(reversed(postfix.split()))
    # adjust steps for prefix (simplified, not exact)
    steps = [s.replace("postfix", "prefix") for s in steps]  # placeholder
    return " ".join(pre_tokens), steps

def tokenize_expr(expr: str) -> List[str]:
    toks = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i+=1; continue
        if c.isalnum():
            j=i
            while j < len(expr) and expr[j].isalnum():
                j+=1
            toks.append(expr[i:j]); i=j; continue
        if c in "+-*/^()":
            toks.append(c); i+=1; continue
        i+=1
    return toks

def eval_postfix_steps(postfix: str) -> Tuple[Optional[float], List[str]]:
    stack = []
    steps = []
    for token in postfix.split():
        steps.append(f"Token: {token}\nStack: {' '.join(map(str,stack))}")
        if token.isdigit():
            stack.append(int(token))
        elif token.isalnum() and not token.isdigit():
            return None, steps
        else:
            if len(stack) < 2:
                return None, steps
            b = stack.pop(); a = stack.pop()
            if token == '+': stack.append(a+b)
            elif token == '-': stack.append(a-b)
            elif token == '*': stack.append(a*b)
            elif token == '/': stack.append(a/b if b!=0 else None)
            elif token == '^': stack.append(a**b)
    return stack[-1] if stack else None, steps

# ----------- UI: Modern Dashboard Application -----------

class ModernDashboardApp:
    def __init__(self, root: ctk.CTk):
        pygame.init()
        self.pop_sound = self._create_pop_sound()
        self.root = root
        self.root.title("Modern Algorithm Dashboard")
        self.root.geometry("1200x720")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        # data models
        self.bst = BST()
        self.graph: GraphType = {}
        self.heuristics: HeuristicsType = {}
        # active canvas reference (for export)
        self.active_canvas: Optional[tk.Canvas] = None

        # build UI
        self._build_layout()

    def _create_pop_sound(self):
        freq = 600
        duration = 0.1
        sample_rate = 44100
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.02)
        wave = (wave * 32767).astype(np.int16)
        return pygame.mixer.Sound(buffer=wave.tobytes())

    def _build_layout(self):
        # main frames
        self.sidebar = ctk.CTkFrame(self.root, width=220)
        self.sidebar.pack(side="left", fill="y", padx=12, pady=12)
        self.sidebar.pack_propagate(False)

        self.content = ctk.CTkFrame(self.root)
        self.content.pack(side="right", fill="both", expand=True, padx=12, pady=12)

        # Sidebar content (navigation)
        tk.Label(self.sidebar, text="", bg=self.sidebar._apply_appearance_mode(self.sidebar._fg_color), height=1).pack()

        ctk.CTkLabel(self.sidebar, text="Algorithm Suite", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(8,10))
        nav_items = [
            ("Home", self.show_home),
            ("BST Visualizer", self.show_bst),
            ("Graph Visualizer", self.show_graph),
            ("Sorting Visualizer", self.show_sorting),
            ("Queue & Stack", self.show_queue_stack),
            ("Expressions", self.show_expressions),
        ]
        for (label, cmd) in nav_items:
            b = ctk.CTkButton(self.sidebar, text=label, command=cmd)
            b.pack(fill="x", padx=12, pady=6)

        # help
        ctk.CTkButton(self.sidebar, text="Help", command=self.show_help).pack(side="bottom", fill="x", padx=12, pady=6)

        # content placeholder frames (we switch views by hiding/showing)
        self.frames = {}
        for name in ["home","bst","graph","sorting","qstack","expr"]:
            f = ctk.CTkFrame(self.content)
            f.pack(fill="both", expand=True)
            self.frames[name] = f
            f.pack_forget()

        # create panels
        self._create_home(self.frames["home"])
        self._create_bst_panel(self.frames["bst"])
        self._create_graph_panel(self.frames["graph"])
        self._create_sorting_panel(self.frames["sorting"])
        self._create_queue_stack_panel(self.frames["qstack"])
        self._create_expression_panel(self.frames["expr"])

        # show home by default
        self.show_home()

    # ---------------- Home ----------------
    def _create_home(self, parent):
        frame = parent
        frame.pack(fill="both", expand=True)
        ctk.CTkButton(frame, text="Random DSA Fact", command=self.random_dsa_fact).pack(pady=10)
        self.home_canvas = tk.Canvas(frame, bg="#F8F8F8")
        self.home_canvas.pack(fill="both", expand=True)
        self.home_canvas.bind("<Configure>", lambda e: self.draw_home_tree())

    def draw_home_tree(self):
        c = self.home_canvas
        c.delete("all")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 10 or h < 10:
            return
        c.create_text(w/2, 60, text="Welcome to DSA Visualizer", font=("Helvetica", 24, "bold"), fill="#059669")
        # draw simple BST
        c.create_oval(w/2 - 20, 120, w/2 + 20, 160, fill="#34D399", outline="#059669")
        c.create_text(w/2, 140, text="50", fill="white", font=("Helvetica", 12, "bold"))
        c.create_line(w/2, 160, w/2 - 100, 220, width=2)
        c.create_oval(w/2 - 120, 200, w/2 - 80, 240, fill="#34D399", outline="#059669")
        c.create_text(w/2 - 100, 220, text="30", fill="white", font=("Helvetica", 12, "bold"))
        c.create_line(w/2, 160, w/2 + 100, 220, width=2)
        c.create_oval(w/2 + 80, 200, w/2 + 120, 240, fill="#34D399", outline="#059669")
        c.create_text(w/2 + 100, 220, text="70", fill="white", font=("Helvetica", 12, "bold"))
        c.create_text(w/2, h-100, text="Explore algorithms with interactive visualizations!", font=("Helvetica", 16), fill="#047857")

    def random_dsa_fact(self):
        facts = [
            "Binary Search Trees enable efficient searching in O(log n) time on average.",
            "Graphs are used to model relationships like social networks or maps.",
            "Sorting algorithms like Quick Sort have average time complexity of O(n log n).",
            "Stacks follow Last In First Out (LIFO) principle.",
            "Queues follow First In First Out (FIFO) principle.",
            "Postfix expressions eliminate the need for parentheses in evaluation."
        ]
        messagebox.showinfo("DSA Fact", random.choice(facts))

    # ---------------- BST Panel ----------------
    def _create_bst_panel(self, parent):
        frame = parent
        frame.columnconfigure(0, weight=1); frame.rowconfigure(0, weight=1)
        # top controls
        ctrl = ctk.CTkFrame(frame)
        ctrl.pack(fill="x", pady=8, padx=8)
        self.bst_entry = ctk.CTkEntry(ctrl, placeholder_text="Integer")
        self.bst_entry.pack(side="left", padx=(6,6))
        ctk.CTkButton(ctrl, text="Insert", command=self.bst_insert).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Delete", command=self.bst_delete).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Search", command=self.bst_search).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Inorder", command=lambda: messagebox.showinfo("Inorder", ", ".join(map(str,self.bst.inorder())))).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Preorder", command=lambda: messagebox.showinfo("Preorder", ", ".join(map(str,self.bst.preorder())))).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Postorder", command=lambda: messagebox.showinfo("Postorder", ", ".join(map(str,self.bst.postorder())))).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="In Code", command=lambda: self.show_traversal_code("inorder")).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Pre Code", command=lambda: self.show_traversal_code("preorder")).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Post Code", command=lambda: self.show_traversal_code("postorder")).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Clear", command=self.bst_clear).pack(side="left", padx=6)
        # canvas
        canvas_frame = ctk.CTkFrame(frame)
        canvas_frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.bst_canvas = tk.Canvas(canvas_frame, bg="#F8F8F8")
        self.bst_canvas.pack(fill="both", expand=True)
        self.active_canvas = self.bst_canvas
        # simple pan by dragging
        self._bst_pan = {"drag": False, "x":0, "y":0}
        self.bst_canvas.bind("<ButtonPress-1>", self._bst_on_press)
        self.bst_canvas.bind("<B1-Motion>", self._bst_on_drag)
        self.bst_canvas.bind("<ButtonRelease-1>", self._bst_on_release)
        # draw initial
        self._bst_layout_and_draw()

    def bst_insert(self):
        s = self.bst_entry.get().strip()
        try:
            v = int(s)
        except:
            messagebox.showwarning("Invalid", "Enter integer")
            return
        ok = self.bst.insert(v)
        if not ok:
            messagebox.showinfo("Info", f"{v} already exists")
        self.bst_entry.delete(0, "end")
        self._bst_layout_and_draw()

    def bst_delete(self):
        s = self.bst_entry.get().strip()
        try:
            v = int(s)
        except:
            messagebox.showwarning("Invalid", "Enter integer")
            return
        ok = self.bst.delete(v)
        if not ok:
            messagebox.showinfo("Info", f"{v} not found")
        self.bst_entry.delete(0, "end")
        self._bst_layout_and_draw()

    def bst_search(self):
        s = self.bst_entry.get().strip()
        try:
            v = int(s)
        except:
            messagebox.showwarning("Invalid", "Enter integer")
            return
        algo = simpledialog.askstring("Search Algorithm", "Choose: BFS or DFS")
        if algo not in ("BFS", "DFS"):
            messagebox.showwarning("Invalid", "Choose BFS or DFS")
            return
        found, path, visited_order = self._bst_search_algo(v, algo)
        if found:
            messagebox.showinfo("Found", f"{v} found via {algo}\nPath: {' -> '.join(map(str, [n.value for n in path]))}")
        else:
            messagebox.showinfo("Not Found", f"{v} not found")
        self.bst_entry.delete(0, "end")
        self._animate_bst_search(visited_order, [n.value for n in path] if path else [])

    def _bst_search_algo(self, value, algo):
        parent = {self.root: None} if self.root else {}
        visited = []
        path = []
        if algo == "BFS":
            from collections import deque
            if not self.root:
                return False, [], []
            q = deque([self.root])
            while q:
                node = q.popleft()
                visited.append(node)
                if node.value == value:
                    cur = node
                    while cur:
                        path.append(cur)
                        cur = parent[cur]
                    path.reverse()
                    return True, path, visited
                if node.left:
                    parent[node.left] = node
                    q.append(node.left)
                if node.right:
                    parent[node.right] = node
                    q.append(node.right)
            return False, [], visited
        elif algo == "DFS":
            if not self.root:
                return False, [], []
            stack = [self.root]
            seen = set()
            while stack:
                node = stack.pop()
                if node in seen:
                    continue
                seen.add(node)
                visited.append(node)
                if node.value == value:
                    cur = node
                    while cur:
                        path.append(cur)
                        cur = parent[cur]
                    path.reverse()
                    return True, path, visited
                if node.right:
                    parent[node.right] = node
                    stack.append(node.right)
                if node.left:
                    parent[node.left] = node
                    stack.append(node.left)
            return False, [], visited

    def _animate_bst_search(self, visited_order, path_values):
        def animate(index=0):
            if index >= len(visited_order):
                self._bst_layout_and_draw(highlight_path=path_values)
                return
            value = visited_order[index].value
            self._bst_layout_and_draw(highlight_value=value)
            self.root.after(800, lambda: animate(index + 1))
        animate()

    def show_traversal_code(self, typ):
        code = ""
        if typ == "inorder":
            code = """def inorder(self):
    res = []
    self._in(self.root, res)
    return res

def _in(self, node, arr):
    if node:
        self._in(node.left, arr)
        arr.append(node.value)
        self._in(node.right, arr)"""
        elif typ == "preorder":
            code = """def preorder(self):
    res = []
    self._pre(self.root, res)
    return res

def _pre(self, node, arr):
    if node:
        arr.append(node.value)
        self._pre(node.left, arr)
        self._pre(node.right, arr)"""
        elif typ == "postorder":
            code = """def postorder(self):
    res = []
    self._post(self.root, res)
    return res

def _post(self, node, arr):
    if node:
        self._post(node.left, arr)
        self._post(node.right, arr)
        arr.append(node.value)"""
        messagebox.showinfo(f"{typ.capitalize()} Traversal Code", code)

    def bst_clear(self):
        self.bst = BST()
        self._bst_layout_and_draw()

    # BST drawing helpers
    def _bst_layout_and_draw(self, highlight_value: Optional[int]=None, highlight_path: List[int]=[]):
        self.bst_canvas.delete("all")
        # assign inorder x positions and levels
        counter = {"x":0}
        def assign(n, depth=0):
            if not n:
                return
            assign(n.left, depth+1)
            counter["x"] += 1
            n.x = counter["x"]
            n.y = depth
            assign(n.right, depth+1)
        assign(self.bst.root)
        if counter["x"] == 0:
            return
        w = max(self.bst_canvas.winfo_width(), 600)
        spacing = max((w-40)/(counter["x"]+1), 40)
        # compute coords
        def setcoords(n):
            if not n: return
            n.canvas_x = int(20 + n.x*spacing)
            n.canvas_y = int(60 + n.y*80)
            setcoords(n.left); setcoords(n.right)
        setcoords(self.bst.root)
        # draw edges then nodes
        def draw_edges(n):
            if not n: return
            if n.left:
                self.bst_canvas.create_line(n.canvas_x, n.canvas_y, n.left.canvas_x, n.left.canvas_y, width=2)
            if n.right:
                self.bst_canvas.create_line(n.canvas_x, n.canvas_y, n.right.canvas_x, n.right.canvas_y, width=2)
            draw_edges(n.left); draw_edges(n.right)
        draw_edges(self.bst.root)
        # nodes
        def draw_nodes(n):
            if not n: return
            r = 22
            fill = "#34D399"
            if n.value in highlight_path:
                fill = "#10B981"
            elif n.value == highlight_value:
                fill = "#FBBF24"
            self.bst_canvas.create_oval(n.canvas_x-r, n.canvas_y-r, n.canvas_x+r, n.canvas_y+r, fill=fill, outline="#1F2937", width=2)
            self.bst_canvas.create_text(n.canvas_x, n.canvas_y, text=str(n.value), font=("Helvetica", 11, "bold"), fill="white")
            draw_nodes(n.left); draw_nodes(n.right)
        draw_nodes(self.bst.root)

    def _bst_on_press(self, evt):
        self._bst_pan["drag"] = True
        self._bst_pan["x"] = evt.x
        self._bst_pan["y"] = evt.y

    def _bst_on_drag(self, evt):
        if self._bst_pan["drag"]:
            dx = evt.x - self._bst_pan["x"]
            dy = evt.y - self._bst_pan["y"]
            self.bst_canvas.scan_dragto(int(self.bst_canvas.canvasx(-dx)), int(self.bst_canvas.canvasy(-dy)), gain=1)
            self._bst_pan["x"] = evt.x; self._bst_pan["y"] = evt.y

    def _bst_on_release(self, evt):
        self._bst_pan["drag"] = False

    # ---------------- Graph Panel ----------------
    def _create_graph_panel(self, parent):
        frame = parent
        # controls
        top = ctk.CTkFrame(frame)
        top.pack(fill="x", padx=8, pady=8)
        self.graph_text = ctk.CTkTextbox(top, width=420, height=160)
        example = ("graph={\n"
                   "  'A':[('B',3),('C',1),('D',5)],\n"
                   "  'B':[('E',7)],\n"
                   "  'C':[('F',4),('E',7)],\n"
                   "  'D':[('F',9)],\n"
                   "  'E':[('H',6)],\n"
                   "  'F':[('G',2)],\n"
                   "  'G':[],\n"
                   "  'H':[('G',7)]\n}\n\nHeuristic example:\nHeuristic_Values = {'A':40,'B':32,'C':25,'D':35,'E':19,'F':17,'G':0,'H':10}")
        self.graph_text.insert("0.0", example)
        self.graph_text.pack(side="left", padx=6, pady=6)
        right_controls = ctk.CTkFrame(top)
        right_controls.pack(side="left", fill="y", padx=8, pady=6)
        ctk.CTkButton(right_controls, text="Load From Text", command=self.load_graph_from_text).pack(pady=6)
        ctk.CTkButton(right_controls, text="Clear Graph", command=self.clear_graph).pack(pady=6)
        ctk.CTkButton(right_controls, text="Auto Layout & Draw", command=self.draw_graph).pack(pady=6)
        ctk.CTkButton(right_controls, text="Add Node", command=self.add_graph_node).pack(pady=6)
        ctk.CTkButton(right_controls, text="Add Edge", command=self.add_graph_edge).pack(pady=6)
        ctk.CTkButton(right_controls, text="Delete Node", command=self.delete_graph_node).pack(pady=6)
        ctk.CTkLabel(right_controls, text="Heuristics (optional)").pack(pady=(10,0))
        self.heur_text = ctk.CTkEntry(right_controls, placeholder_text="e.g. A:40,B:32")
        self.heur_text.pack(pady=6)
        # search and traversal controls
        ctrl = ctk.CTkFrame(frame)
        ctrl.pack(fill="x", pady=8, padx=8)
        self.graph_start = ctk.CTkEntry(ctrl, placeholder_text="Start node")
        self.graph_start.pack(side="left", padx=6)
        self.graph_goal = ctk.CTkEntry(ctrl, placeholder_text="Goal node")
        self.graph_goal.pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Search", command=self.graph_search).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Preorder DFS", command=self.graph_preorder_show).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Postorder DFS", command=self.graph_postorder_show).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Pre Code", command=lambda: self.show_graph_traversal_code("preorder")).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Post Code", command=lambda: self.show_graph_traversal_code("postorder")).pack(side="left", padx=6)
        # main canvas
        canvas_frame = ctk.CTkFrame(frame)
        canvas_frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.graph_canvas = tk.Canvas(canvas_frame, bg="#F8F8F8")
        self.graph_canvas.pack(fill="both", expand=True)
        self.active_canvas = self.graph_canvas
        # node positions stored in self._graph_positions
        self._graph_positions: Dict[str, Tuple[float,float]] = {}

    def load_graph_from_text(self):
        s = self.graph_text.get("0.0", "end").strip()
        if not s:
            messagebox.showwarning("No text", "Paste graph dictionary text into the box first")
            return
        try:
            loc = {}
            exec(s, {}, loc)
            if "graph" in loc and isinstance(loc["graph"], dict):
                self.graph = loc["graph"]
                messagebox.showinfo("Loaded", "Graph dictionary loaded successfully")
                if "Heuristic_Values" in loc and isinstance(loc["Heuristic_Values"], dict):
                    self.heuristics = loc["Heuristic_Values"]
                else:
                    self.heuristics = {}
                self._graph_auto_layout()
                self.draw_graph()
            else:
                messagebox.showerror("Error", "Text must define variable named 'graph' as a dict")
        except Exception as e:
            messagebox.showerror("Parse error", str(e))

    def clear_graph(self):
        self.graph = {}
        self.heuristics = {}
        self._graph_positions = {}
        self.graph_canvas.delete("all")

    def add_graph_node(self):
        node = simpledialog.askstring("Add Node", "Enter node name")
        if node and node not in self.graph:
            self.graph[node] = []
            self._graph_auto_layout()
            self.draw_graph()

    def add_graph_edge(self):
        from_node = simpledialog.askstring("From", "From node")
        to_node = simpledialog.askstring("To", "To node")
        weight = simpledialog.askfloat("Weight", "Edge weight")
        if from_node in self.graph and to_node in self.graph and weight is not None:
            self.graph[from_node].append((to_node, weight))
            self.draw_graph()

    def delete_graph_node(self):
        node = simpledialog.askstring("Delete Node", "Node name")
        if node in self.graph:
            del self.graph[node]
            for u in list(self.graph):
                self.graph[u] = [(v, w) for v, w in self.graph[u] if v != node]
            self._graph_auto_layout()
            self.draw_graph()

    def graph_preorder_show(self):
        start = self.graph_start.get().strip() or (list(self.graph.keys())[0] if self.graph else "")
        if not start:
            messagebox.showwarning("No graph", "No nodes")
            return
        order = self._graph_preorder(start)
        messagebox.showinfo("Preorder DFS", " -> ".join(order))

    def graph_postorder_show(self):
        start = self.graph_start.get().strip() or (list(self.graph.keys())[0] if self.graph else "")
        if not start:
            messagebox.showwarning("No graph", "No nodes")
            return
        order = self._graph_postorder(start)
        messagebox.showinfo("Postorder DFS", " -> ".join(order))

    def _graph_preorder(self, start):
        visited = []
        stack = [start]
        seen = set()
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

    def _graph_postorder(self, start):
        visited = []
        def dfs(node):
            for nbr, _ in self.graph.get(node, []):
                if nbr not in visited:
                    dfs(nbr)
            visited.append(node)
        dfs(start)
        visited.reverse()
        return visited

    def show_graph_traversal_code(self, typ):
        code = ""
        if typ == "preorder":
            code = """def _graph_preorder(self, start):
    visited = []
    stack = [start]
    seen = set()
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
    return visited"""
        elif typ == "postorder":
            code = """def _graph_postorder(self, start):
    visited = []
    def dfs(node):
        for nbr, _ in self.graph.get(node, []):
            if nbr not in visited:
                dfs(nbr)
        visited.append(node)
    dfs(start)
    visited.reverse()
    return visited"""
        messagebox.showinfo(f"{typ.capitalize()} DFS Code", code)

    def graph_search(self):
        goal = self.graph_goal.get().strip()
        if not goal:
            messagebox.showwarning("Input", "Enter goal node")
            return
        start = self.graph_start.get().strip() or (list(self.graph.keys())[0] if self.graph else "")
        if not start:
            messagebox.showwarning("No graph", "No nodes")
            return
        algo = simpledialog.askstring("Search Algorithm", "Choose: BFS or DFS")
        if algo not in ("BFS", "DFS"):
            return
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
            messagebox.showinfo("Found", f"Path: {' -> '.join(path)}")
        else:
            messagebox.showinfo("Not Found", "Not found")
        self._animate_graph_search(visited_order, path or [])

    def _animate_graph_search(self, visited_order, path):
        def animate(index=0):
            if index >= len(visited_order):
                if path:
                    self._highlight_path(path)
                return
            node = visited_order[index]
            self._highlight_graph_node(node)
            self.root.after(800, lambda: animate(index + 1))
        self.draw_graph()
        animate()

    def _graph_auto_layout(self):
        nodes = sorted(self.graph.keys())
        n = len(nodes)
        if n == 0:
            return
        w = max(self.graph_canvas.winfo_width(), 600)
        h = max(self.graph_canvas.winfo_height(), 420)
        cx, cy = w/2, h/2
        r = min(w,h)/2 - 80
        self._graph_positions = {}
        for i, node in enumerate(nodes):
            ang = 2*math.pi*i/n
            x = cx + r*math.cos(ang)
            y = cy + r*math.sin(ang)
            self._graph_positions[node] = (x,y)

    def draw_graph(self):
        self.graph_canvas.delete("all")
        if not self.graph:
            return
        if not self._graph_positions:
            self._graph_auto_layout()
        # draw edges with weights
        for u, edges in self.graph.items():
            ux, uy = self._graph_positions.get(u, (50,50))
            for (v,w) in edges:
                vx, vy = self._graph_positions.get(v, (50,50))
                self._draw_arrow(self.graph_canvas, ux, uy, vx, vy, text=str(w))
        # draw nodes
        for node, (x,y) in self._graph_positions.items():
            r = 26
            self.graph_canvas.create_oval(x-r, y-r, x+r, y+r, fill="#34D399", outline="#0F172A", width=2)
            self.graph_canvas.create_text(x, y, text=str(node), font=("Helvetica",12,"bold"), fill="#001219")
            if node in self.heuristics:
                self.graph_canvas.create_text(x, y+20, text=f"h={self.heuristics[node]}", font=("Helvetica",9), fill="#334155")

    def _draw_arrow(self, canvas, x1,y1,x2,y2, text=""):
        dx = x2-x1; dy = y2-y1
        d = math.hypot(dx,dy)
        if d==0:
            return
        ux, uy = dx/d, dy/d
        pad = 28
        sx = x1 + ux*pad; sy = y1 + uy*pad
        ex = x2 - ux*pad; ey = y2 - uy*pad
        canvas.create_line(sx, sy, ex, ey, width=2, arrow=tk.LAST, smooth=True)
        mx = (sx+ex)/2; my=(sy+ey)/2
        if text:
            canvas.create_text(mx, my-10, text=text, font=("Helvetica",9,"bold"), fill="#0F172A")

    def _highlight_graph_node(self, node):
        self.draw_graph()
        pos = self._graph_positions.get(node)
        if pos:
            x, y = pos
            r = 30
            self.graph_canvas.create_oval(x - r, y - r, x + r, y + r, outline="#FBBF24", width=4)
            self.graph_canvas.create_text(x, y - 30, text=f"Visiting {node}", font=("Helvetica",10,"bold"))

    def _highlight_path(self, path: List[str]):
        if not path:
            return
        for i in range(len(path)-1):
            u = path[i]; v = path[i+1]
            p1 = self._graph_positions.get(u); p2 = self._graph_positions.get(v)
            if p1 and p2:
                self.graph_canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=4, fill="#10B981", arrow=tk.LAST)

    # ---------------- Sorting Panel ----------------
    def _create_sorting_panel(self, parent):
        frame = parent
        top = ctk.CTkFrame(frame)
        top.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(top, text="Sorting Visualizer", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left", padx=6)
        ctrl = ctk.CTkFrame(frame)
        ctrl.pack(fill="x", padx=8, pady=6)
        self.sort_entry = ctk.CTkEntry(ctrl, placeholder_text="Comma-separated ints e.g. 5,3,8,1")
        self.sort_entry.pack(side="left", padx=6, fill="x", expand=True)
        self.sort_algo = ctk.CTkComboBox(ctrl, values=["Insertion", "Bubble", "Selection", "Merge", "Quick"])
        self.sort_algo.set("Bubble")
        self.sort_algo.pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Start Step", command=self.sort_step).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Run Full", command=self.sort_full).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Show Code", command=self.show_sort_code).pack(side="left", padx=6)
        # canvas for bars
        canvas_frame = ctk.CTkFrame(frame)
        canvas_frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.sort_canvas = tk.Canvas(canvas_frame, bg="#F8F8F8")
        self.sort_canvas.pack(fill="both", expand=True)
        self.active_canvas = self.sort_canvas
        # state
        self._sort_gen = None
        self._sort_arr = []

    def sort_step(self):
        s = self.sort_entry.get().strip()
        if not s:
            messagebox.showwarning("Input", "Enter numbers")
            return
        arr = [int(x.strip()) for x in s.split(",") if x.strip()]
        if self._sort_gen is None:
            algo = self.sort_algo.get()
            if algo == "Insertion":
                self._sort_gen = insertion_steps(arr)
            elif algo == "Bubble":
                self._sort_gen = bubble_steps(arr)
            elif algo == "Selection":
                self._sort_gen = selection_steps(arr)
            elif algo == "Merge":
                self._sort_gen = merge_steps(arr)
            else:
                self._sort_gen = quick_steps(arr)
            self._sort_arr = list(arr)
            self._draw_sort_array(self._sort_arr, [])
        try:
            step = next(self._sort_gen)
            self._handle_sort_step(step)
        except StopIteration:
            self._sort_gen = None

    def sort_full(self):
        s = self.sort_entry.get().strip()
        if not s:
            messagebox.showwarning("Input", "Enter numbers")
            return
        arr = [int(x.strip()) for x in s.split(",") if x.strip()]
        algo = self.sort_algo.get()
        if algo == "Insertion":
            gen = insertion_steps(arr)
        elif algo == "Bubble":
            gen = bubble_steps(arr)
        elif algo == "Selection":
            gen = selection_steps(arr)
        elif algo == "Merge":
            gen = merge_steps(arr)
        else:
            gen = quick_steps(arr)
        # run to completion with animation
        def run_next(g):
            try:
                step = next(g)
                self._handle_sort_step(step)
                self.root.after(220, lambda: run_next(g))
            except StopIteration:
                pass
        run_next(gen)

    def _handle_sort_step(self, step):
        typ = step[0]
        arr = step[-1]
        highlights = []
        if typ == "compare":
            highlights = [step[1], step[2]]
        elif typ == "swap":
            highlights = [step[1], step[2]]
        elif typ == "shift":
            highlights = [step[1]]
        elif typ == "key":
            highlights = [step[1]]
        elif typ == "insert":
            highlights = [step[1]]
        elif typ == "merge":
            highlights = list(range(step[1], step[3] + 1))
        elif typ == "merged":
            highlights = list(range(step[1], step[2] + 1))
        # for done, []
        self._draw_sort_array(arr, highlights)

    def _draw_sort_array(self, arr: List[int], highlights: List[int]=[]):
        self.sort_canvas.delete("all")
        if not arr:
            return
        w = max(self.sort_canvas.winfo_width(), 400)
        h = max(self.sort_canvas.winfo_height(), 200)
        n = len(arr)
        bar_w = max(8, w / (n * 1.6))
        maxv = max(arr) if arr else 1
        for i, val in enumerate(arr):
            x = 10 + i * (bar_w + 6)
            bar_h = (val / maxv) * (h - 50) if maxv > 0 else 10
            y = h - bar_h - 20
            color = "#FB7185" if i in highlights else "#34D399"
            self.sort_canvas.create_rectangle(x, y, x + bar_w, h - 20, fill=color, outline="#0F172A")
            self.sort_canvas.create_text(x + bar_w / 2, y - 10, text=str(val), font=("Helvetica", 9))

    def show_sort_code(self):
        algo = self.sort_algo.get()
        code = ""
        if algo == "Insertion":
            code = """def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key"""
        elif algo == "Bubble":
            code = """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]"""
        elif algo == "Selection":
            code = """def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]"""
        elif algo == "Merge":
            code = """def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr"""
        elif algo == "Quick":
            code = """def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)"""
        messagebox.showinfo(f"{algo} Sort Code", code)

    # ---------------- Queue & Stack Panel ----------------
    def _create_queue_stack_panel(self, parent):
        frame = parent
        top = ctk.CTkFrame(frame)
        top.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(top, text="Queue & Stack Simulator", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=8)

        # Size input
        size_frame = ctk.CTkFrame(frame)
        size_frame.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(size_frame, text="Structure Size:").pack(side="left", padx=6)
        self.qs_size_entry = ctk.CTkEntry(size_frame, width=80, placeholder_text="e.g. 8")
        self.qs_size_entry.pack(side="left", padx=6)
        ctk.CTkButton(size_frame, text="Create Structures", command=self.create_qs_structures).pack(side="left", padx=6)

        # Controls
        ctrl = ctk.CTkFrame(frame)
        ctrl.pack(fill="x", padx=8, pady=6)
        self.qs_entry = ctk.CTkEntry(ctrl, placeholder_text="Value")
        self.qs_entry.pack(side="left", padx=6, fill="x", expand=True)
        ctk.CTkButton(ctrl, text="Push (Stack)", fg_color="#10B981", command=self.s_push).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Pop (Stack)", fg_color="#F59E0B", command=self.s_pop).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Enqueue (Queue)", fg_color="#10B981", command=self.q_enqueue).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Dequeue (Queue)", fg_color="#F59E0B", command=self.q_dequeue).pack(side="left", padx=6)

        # Display area
        display_frame = ctk.CTkFrame(frame)
        display_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Stack (vertical)
        stack_frame = ctk.CTkFrame(display_frame)
        stack_frame.pack(side="left", fill="both", expand=True, padx=20)
        ctk.CTkLabel(stack_frame, text="Stack (Top → Bottom)", font=ctk.CTkFont(size=16)).pack(pady=10)
        self.stack_canvas = tk.Canvas(stack_frame, bg="#F8F8F8")
        self.stack_canvas.pack(fill="both", expand=True, padx=20, pady=10)

        # Queue (vertical)
        queue_frame = ctk.CTkFrame(display_frame)
        queue_frame.pack(side="right", fill="both", expand=True, padx=20)
        ctk.CTkLabel(queue_frame, text="Queue (Rear → Front)", font=ctk.CTkFont(size=16)).pack(pady=10)
        self.queue_canvas = tk.Canvas(queue_frame, bg="#F8F8F8")
        self.queue_canvas.pack(fill="both", expand=True, padx=20, pady=10)

        # Initial state
        self._queue = []
        self._stack = []
        self.max_size = 0
        self.stack_boxes = []
        self.queue_boxes = []

    def create_qs_structures(self):
        try:
            self.max_size = int(self.qs_size_entry.get().strip())
            if self.max_size <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Invalid", "Enter positive integer size")
            return
        self._queue = []
        self._stack = []
        self._draw_qs_boxes()

    def _draw_qs_boxes(self):
        # Clear canvases
        self.stack_canvas.delete("all")
        self.queue_canvas.delete("all")
        self.stack_boxes = []
        self.queue_boxes = []

        if self.max_size == 0:
            return

        w_stack = self.stack_canvas.winfo_width()
        w_queue = self.queue_canvas.winfo_width()
        h = max(self.stack_canvas.winfo_height(), 400)

        box_h = (h - 80) // self.max_size
        box_h = max(box_h, 40)

        # Stack boxes (top to bottom)
        for i in range(self.max_size):
            y = 40 + i * box_h
            box = self.stack_canvas.create_rectangle(
                w_stack//2 - 80, y, w_stack//2 + 80, y + box_h - 10,
                fill="#E0E0E0", outline="#065F46", width=2
            )
            text = self.stack_canvas.create_text(w_stack//2, y + box_h//2 - 5, text="", font=("Helvetica", 14, "bold"))
            self.stack_boxes.append((box, text))

        # Queue boxes (rear at top, front at bottom)
        for i in range(self.max_size):
            y = 40 + i * box_h
            box = self.queue_canvas.create_rectangle(
                w_queue//2 - 80, y, w_queue//2 + 80, y + box_h - 10,
                fill="#E0E0E0", outline="#065F46", width=2
            )
            text = self.queue_canvas.create_text(w_queue//2, y + box_h//2 - 5, text="", font=("Helvetica", 14, "bold"))
            self.queue_boxes.append((box, text))

        self._update_qs_display()

    def _update_qs_display(self):
        # Update stack (top is last element)
        for i in range(self.max_size):
            if i < len(self._stack):
                val = self._stack[-(i+1)]  # top at index 0 in display
                self.stack_canvas.itemconfigure(self.stack_boxes[i][1], text=str(val))
                self.stack_canvas.itemconfigure(self.stack_boxes[i][0], fill="#34D399")
            else:
                self.stack_canvas.itemconfigure(self.stack_boxes[i][1], text="")
                self.stack_canvas.itemconfigure(self.stack_boxes[i][0], fill="#E0E0E0")

        # Update queue (rear at top, front at bottom)
        for i in range(self.max_size):
            if i < len(self._queue):
                val = self._queue[i]  # rear at 0, front at len-1
                self.queue_canvas.itemconfigure(self.queue_boxes[i][1], text=str(val))
                self.queue_canvas.itemconfigure(self.queue_boxes[i][0], fill="#34D399")
            else:
                self.queue_canvas.itemconfigure(self.queue_boxes[i][1], text="")
                self.queue_canvas.itemconfigure(self.queue_boxes[i][0], fill="#E0E0E0")

    def s_push(self):
        if self.max_size == 0:
            messagebox.showwarning("Size", "Create structure size first")
            return
        v = self.qs_entry.get().strip()
        if not v:
            return
        if len(self._stack) >= self.max_size:
            messagebox.showinfo("Full", "Stack is full")
            return
        self._stack.append(v)
        self.qs_entry.delete(0, "end")
        self._animate_push_pop("stack", add=True)
        self._update_qs_display()

    def s_pop(self):
        if self.max_size == 0:
            messagebox.showwarning("Size", "Create structure size first")
            return
        if not self._stack:
            messagebox.showinfo("Empty", "Stack is empty")
            return
        self._stack.pop()
        self.pop_sound.play()
        self._animate_push_pop("stack", add=False)
        self._update_qs_display()

    def q_enqueue(self):
        if self.max_size == 0:
            messagebox.showwarning("Size", "Create structure size first")
            return
        v = self.qs_entry.get().strip()
        if not v:
            return
        if len(self._queue) >= self.max_size:
            messagebox.showinfo("Full", "Queue is full")
            return
        self._queue.append(v)
        self.qs_entry.delete(0, "end")
        self._animate_push_pop("queue", add=True)
        self._update_qs_display()

    def q_dequeue(self):
        if self.max_size == 0:
            messagebox.showwarning("Size", "Create structure size first")
            return
        if not self._queue:
            messagebox.showinfo("Empty", "Queue is empty")
            return
        self._queue.pop(0)
        self.pop_sound.play()
        self._animate_push_pop("queue", add=False)
        self._update_qs_display()

    def _animate_push_pop(self, structure: str, add: bool):
        canvas = self.stack_canvas if structure == "stack" else self.queue_canvas
        boxes = self.stack_boxes if structure == "stack" else self.queue_boxes
        data = self._stack if structure == "stack" else self._queue

        def flash(index=0):
            if index > 5:
                return
            color = "#10B981" if add else "#FBBF24"
            target_i = len(data) - 1 if (structure == "stack" and add) or (structure == "queue" and not add) else 0 if add and structure == "queue" else len(data)
            if 0 <= target_i < len(boxes):
                canvas.itemconfigure(boxes[target_i][0], fill=color if index % 2 == 0 else "#34D399")
            self.root.after(150, lambda: flash(index + 1))
        flash()

    # ---------------- Expression Panel ----------------
    def _create_expression_panel(self, parent):
        frame = parent
        top = ctk.CTkFrame(frame)
        top.pack(fill="x", padx=8, pady=8)
        ctk.CTkLabel(top, text="Expression Converter & Evaluator", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=8)

        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=8, pady=8)
        self.expr_entry = ctk.CTkEntry(input_frame, placeholder_text="Infix: e.g. (A+B)*(C-D)")
        self.expr_entry.pack(side="left", fill="x", expand=True, padx=6)
        ctk.CTkButton(input_frame, text="To Postfix", fg_color="#10B981", command=self.conv_to_postfix).pack(side="left", padx=6)
        ctk.CTkButton(input_frame, text="To Prefix", fg_color="#10B981", command=self.conv_to_prefix).pack(side="left", padx=6)
        ctk.CTkButton(input_frame, text="Evaluate Postfix", fg_color="#059669", command=self.eval_postfix_clicked).pack(side="left", padx=6)

        # Output
        self.expr_output = ctk.CTkTextbox(frame, height=300)
        self.expr_output.pack(fill="both", expand=True, padx=8, pady=8)

        # Steps display
        self.expr_steps = ctk.CTkTextbox(frame, height=200)
        self.expr_steps.pack(fill="both", expand=True, padx=8, pady=8)
        ctk.CTkLabel(frame, text="Conversion Steps:").pack(anchor="w", padx=12)

    def conv_to_postfix(self):
        expr = self.expr_entry.get().strip()
        if not expr:
            return
        try:
            postfix, steps = infix_to_postfix_steps(expr)
            self.expr_output.delete("0.0", "end")
            self.expr_output.insert("end", f"Postfix: {postfix}\n")
            self.expr_steps.delete("0.0", "end")
            for s in steps:
                self.expr_steps.insert("end", s + "\n\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def conv_to_prefix(self):
        expr = self.expr_entry.get().strip()
        if not expr:
            return
        try:
            prefix, steps = infix_to_prefix_steps(expr)
            self.expr_output.delete("0.0", "end")
            self.expr_output.insert("end", f"Prefix: {prefix}\n")
            self.expr_steps.delete("0.0", "end")
            for s in steps:
                self.expr_steps.insert("end", s + "\n\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eval_postfix_clicked(self):
        expr = self.expr_entry.get().strip()
        if not expr:
            return
        try:
            # First convert to postfix
            postfix, _ = infix_to_postfix_steps(expr)
            val, steps = eval_postfix_steps(postfix)
            self.expr_output.delete("0.0", "end")
            self.expr_output.insert("end", f"Postfix: {postfix}\n")
            if val is not None:
                self.expr_output.insert("end", f"Result: {val}\n")
            else:
                self.expr_output.insert("end", "Cannot evaluate (variables or error)\n")
            self.expr_steps.delete("0.0", "end")
            self.expr_steps.insert("end", "Evaluation Steps:\n\n")
            for s in steps:
                self.expr_steps.insert("end", s + "\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------- Navigation helpers ----------------
    def _hide_all_frames(self):
        for f in self.frames.values():
            f.pack_forget()

    def show_home(self):
        self._hide_all_frames()
        self.frames["home"].pack(fill="both", expand=True)

    def show_bst(self):
        self._hide_all_frames()
        self.frames["bst"].pack(fill="both", expand=True)
        self.active_canvas = self.bst_canvas
        self._bst_layout_and_draw()

    def show_graph(self):
        self._hide_all_frames()
        self.frames["graph"].pack(fill="both", expand=True)
        self.active_canvas = self.graph_canvas
        self.draw_graph()

    def show_sorting(self):
        self._hide_all_frames()
        self.frames["sorting"].pack(fill="both", expand=True)
        self.active_canvas = self.sort_canvas

    def show_queue_stack(self):
        self._hide_all_frames()
        self.frames["qstack"].pack(fill="both", expand=True)

    def show_expressions(self):
        self._hide_all_frames()
        self.frames["expr"].pack(fill="both", expand=True)

    # -------------- Help ---------------
    def show_help(self):
        help_text = """
Modern Algorithm Visualizer - Help

Home:
- Eye-catching welcome page with a sample BST illustration.

BST Visualizer:
- Insert, delete, search (with BFS/DFS traversal animation).
- View Inorder, Preorder, Postorder results.
- Buttons to view code for each traversal.
- Search shows animated node-by-node traversal and highlights path.

Graph Visualizer:
- Load graph from Python dict text (nodes with weights).
- Search using BFS/DFS with animation.
- Preorder/Postorder DFS traversal display.
- Code buttons for traversals.

Sorting Visualizer:
- Supports Insertion, Bubble, Selection, Merge, Quick sort.
- Step-by-step or full animation with highlights.
- "Show Code" button displays Python code for selected algorithm.

Queue & Stack:
- Set size first → creates fixed vertical boxes.
- Push/Enqueue adds with animation.
- Pop/Dequeue removes with sound and animation.

Expressions:
- Convert infix → postfix or prefix with detailed steps.
- Evaluate numeric postfix expressions.

Theme: Off-white background with green accents.
All in a single clean script using CustomTkinter.
        """
        messagebox.showinfo("Help", help_text)

# --------------- Run app -----------------
if __name__ == "__main__":
    app = ctk.CTk()
    ModernDashboardApp(app)
    app.mainloop()