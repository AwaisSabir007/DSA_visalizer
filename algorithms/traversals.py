"""
Tree and graph traversal code snippets for educational display
"""


def get_traversal_code(traversal_type: str, structure: str = "tree") -> str:
    """
    Get code snippet for a specific traversal type
    
    Args:
        traversal_type: "inorder", "preorder", or "postorder"
        structure: "tree" or "graph"
    
    Returns:
        Python code snippet as string
    """
    if structure == "tree":
        if traversal_type == "inorder":
            return """def inorder(self):
    res = []
    self._in(self.root, res)
    return res

def _in(self, node, arr):
    if node:
        self._in(node.left, arr)
        arr.append(node.value)
        self._in(node.right, arr)"""
        
        elif traversal_type == "preorder":
            return """def preorder(self):
    res = []
    self._pre(self.root, res)
    return res

def _pre(self, node, arr):
    if node:
        arr.append(node.value)
        self._pre(node.left, arr)
        self._pre(node.right, arr)"""
        
        elif traversal_type == "postorder":
            return """def postorder(self):
    res = []
    self._post(self.root, res)
    return res

def _post(self, node, arr):
    if node:
        self._post(node.left, arr)
        self._post(node.right, arr)
        arr.append(node.value)"""
    
    elif structure == "graph":
        if traversal_type == "preorder":
            return """def graph_preorder(self, start):
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
        
        elif traversal_type == "postorder":
            return """def graph_postorder(self, start):
    visited = []
    def dfs(node):
        for nbr, _ in self.graph.get(node, []):
            if nbr not in visited:
                dfs(nbr)
        visited.append(node)
    dfs(start)
    visited.reverse()
    return visited"""
    
    return "# Code not available"
