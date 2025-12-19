"""
Constants and configuration for DSA Visualizer
"""

# Color scheme - Modern green theme
COLORS = {
    # Primary colors
    'primary': '#059669',
    'primary_light': '#34D399',
    'primary_dark': '#047857',
    
    # Accent colors
    'accent': '#10B981',
    'warning': '#FBBF24',
    'danger': '#F59E0B',
    'error': '#FB7185',
    
    # Neutral colors
    'background': '#F8F8F8',
    'surface': '#FFFFFF',
    'border': '#065F46',
    'text': '#1F2937',
    'text_light': '#6B7280',
    
    # Node colors
    'node_default': '#34D399',
    'node_highlight': '#FBBF24',
    'node_path': '#10B981',
    'node_border': '#1F2937',
    
    # Graph colors
    'graph_node': '#34D399',
    'graph_edge': '#0F172A',
    'graph_highlight': '#FBBF24',
    
    # Sorting colors
    'bar_default': '#34D399',
    'bar_compare': '#FB7185',
    'bar_sorted': '#10B981',
    
    # Queue/Stack colors
    'box_empty': '#E0E0E0',
    'box_filled': '#34D399',
}

# Animation settings
ANIMATION_SPEED = {
    'fast': 150,
    'medium': 300,
    'slow': 800,
}

# Default sizes
DEFAULT_NODE_RADIUS = 22
DEFAULT_GRAPH_NODE_RADIUS = 26
DEFAULT_SPACING = 40

# Window settings
WINDOW_TITLE = "DSA Algorithm Visualizer"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720
