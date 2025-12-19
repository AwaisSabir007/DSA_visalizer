"""
Queue and Stack data structures with fixed size
"""
from typing import List, Optional


class Queue:
    """Fixed-size Queue implementation (FIFO)"""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.items: List[str] = []
    
    def enqueue(self, item: str) -> bool:
        """Add item to rear of queue. Returns True if successful, False if full."""
        if self.is_full():
            return False
        self.items.append(item)
        return True
    
    def dequeue(self) -> Optional[str]:
        """Remove and return item from front of queue. Returns None if empty."""
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.items) == 0
    
    def is_full(self) -> bool:
        """Check if queue is full"""
        return len(self.items) >= self.max_size
    
    def clear(self):
        """Clear all items from queue"""
        self.items = []


class Stack:
    """Fixed-size Stack implementation (LIFO)"""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.items: List[str] = []
    
    def push(self, item: str) -> bool:
        """Push item onto stack. Returns True if successful, False if full."""
        if self.is_full():
            return False
        self.items.append(item)
        return True
    
    def pop(self) -> Optional[str]:
        """Pop and return item from top of stack. Returns None if empty."""
        if self.is_empty():
            return None
        return self.items.pop()
    
    def is_empty(self) -> bool:
        """Check if stack is empty"""
        return len(self.items) == 0
    
    def is_full(self) -> bool:
        """Check if stack is full"""
        return len(self.items) >= self.max_size
    
    def clear(self):
        """Clear all items from stack"""
        self.items = []
