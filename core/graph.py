"""
Graph data structure and type definitions
"""
from typing import Dict, List, Tuple

# Graph represented as adjacency list: dict[node] -> List[(neighbor, weight)]
GraphType = Dict[str, List[Tuple[str, float]]]

# Heuristics for informed search algorithms
HeuristicsType = Dict[str, float]
