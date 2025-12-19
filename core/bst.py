"""
Binary Search Tree implementation
"""
from typing import Optional, List


class NodeBST:
    """Node for Binary Search Tree"""
    def __init__(self, value: int):
        self.value = value
        self.left: Optional["NodeBST"] = None
        self.right: Optional["NodeBST"] = None
        # Drawing coordinates
        self.x = 0
        self.y = 0
        self.canvas_x = 0
        self.canvas_y = 0


class BST:
    """Binary Search Tree with insert, delete, search, and traversal operations"""
    
    def __init__(self):
        self.root: Optional[NodeBST] = None

    def insert(self, value: int) -> bool:
        """Insert a value into the BST. Returns True if successful, False if duplicate."""
        if self.root is None:
            self.root = NodeBST(value)
            return True
        return self._insert(self.root, value)

    def _insert(self, node: NodeBST, value: int) -> bool:
        if value == node.value:
            return False  # Duplicate
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
        """Search for a value in the BST. Returns the node if found, None otherwise."""
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
        """Delete a value from the BST. Returns True if successful, False if not found."""
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
            # Found the node to delete
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            # Node has two children - find successor
            succ = node.right
            while succ.left:
                succ = succ.left
            node.value = succ.value
            node.right, _ = self._delete(node.right, succ.value)
            return node, True

    def inorder(self) -> List[int]:
        """Return inorder traversal of the BST"""
        res = []
        self._in(self.root, res)
        return res

    def _in(self, node: Optional[NodeBST], arr: List[int]):
        if node:
            self._in(node.left, arr)
            arr.append(node.value)
            self._in(node.right, arr)

    def preorder(self) -> List[int]:
        """Return preorder traversal of the BST"""
        res = []
        self._pre(self.root, res)
        return res

    def _pre(self, node: Optional[NodeBST], arr: List[int]):
        if node:
            arr.append(node.value)
            self._pre(node.left, arr)
            self._pre(node.right, arr)

    def postorder(self) -> List[int]:
        """Return postorder traversal of the BST"""
        res = []
        self._post(self.root, res)
        return res

    def _post(self, node: Optional[NodeBST], arr: List[int]):
        if node:
            self._post(node.left, arr)
            self._post(node.right, arr)
            arr.append(node.value)
