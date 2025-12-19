"""
Graph and tree searching algorithms with step-by-step visualization
"""
from typing import Generator, Tuple, Any, Set
from collections import deque
from core.graph import GraphType


def bfs_steps(graph: GraphType, start: str, goal: str) -> Generator[Tuple[str, ...], None, None]:
    """
    Breadth-First Search with step-by-step visualization
    Yields: (step_type, node, queue, visited)
    """
    q = deque([start])
    visited: Set[str] = set([start])
    parent = {start: None}
    
    while q:
        node = q.popleft()
        yield ("visit", node, list(q), visited)
        
        if node == goal:
            # Reconstruct path
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


def dfs_steps(graph: GraphType, start: str, goal: str) -> Generator[Tuple[str, ...], None, None]:
    """
    Depth-First Search with step-by-step visualization
    Yields: (step_type, node, stack, visited)
    """
    stack = [start]
    visited: Set[str] = set()
    parent = {start: None}
    
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        yield ("visit", node, list(stack), visited)
        
        if node == goal:
            # Reconstruct path
            path = []
            cur = node
            while cur:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            yield ("found", path)
            return
        
        # Push neighbors in reverse order to preserve natural ordering
        neighbors = [n for (n, _) in graph.get(node, [])]
        for nbr in reversed(neighbors):
            if nbr not in visited:
                parent[nbr] = node
                stack.append(nbr)
                yield ("push", nbr, list(stack), visited)
    
    yield ("notfound", None)
