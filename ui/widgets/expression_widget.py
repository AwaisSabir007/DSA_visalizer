"""
Expression Converter and Evaluator Widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                                QLineEdit, QLabel, QTextEdit)
from PySide6.QtGui import QFont
from algorithms.expressions import (infix_to_postfix_steps, infix_to_prefix_steps,
                                     eval_postfix_steps)
from utils.constants import COLORS


class ExpressionWidget(QWidget):
    """Expression Converter and Evaluator Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Expression Converter & Evaluator")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']};")
        layout.addWidget(title)
        
        # Input
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Infix expression (e.g., (A+B)*(C-D) or (3+5)*(2-1))")
        input_layout.addWidget(self.input_field)
        
        postfix_btn = QPushButton("To Postfix")
        postfix_btn.setStyleSheet(f"background-color: {COLORS['accent']};")
        postfix_btn.clicked.connect(self.convert_to_postfix)
        input_layout.addWidget(postfix_btn)
        
        prefix_btn = QPushButton("To Prefix")
        prefix_btn.setStyleSheet(f"background-color: {COLORS['accent']};")
        prefix_btn.clicked.connect(self.convert_to_prefix)
        input_layout.addWidget(prefix_btn)
        
        eval_btn = QPushButton("Evaluate Postfix")
        eval_btn.setStyleSheet(f"background-color: {COLORS['primary_dark']};")
        eval_btn.clicked.connect(self.evaluate_postfix)
        input_layout.addWidget(eval_btn)
        
        layout.addLayout(input_layout)
        
        # Output
        layout.addWidget(QLabel("Result:"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(150)
        layout.addWidget(self.output_text)
        
        # Steps
        layout.addWidget(QLabel("Conversion/Evaluation Steps:"))
        self.steps_text = QTextEdit()
        self.steps_text.setReadOnly(True)
        layout.addWidget(self.steps_text)
    
    def convert_to_postfix(self):
        """Convert infix to postfix"""
        expr = self.input_field.text().strip()
        if not expr:
            return
        
        try:
            postfix, steps = infix_to_postfix_steps(expr)
            self.output_text.setPlainText(f"Postfix: {postfix}")
            self.steps_text.setPlainText("\n\n".join(steps))
        except Exception as e:
            self.output_text.setPlainText(f"Error: {str(e)}")
    
    def convert_to_prefix(self):
        """Convert infix to prefix"""
        expr = self.input_field.text().strip()
        if not expr:
            return
        
        try:
            prefix, steps = infix_to_prefix_steps(expr)
            self.output_text.setPlainText(f"Prefix: {prefix}")
            self.steps_text.setPlainText("\n\n".join(steps))
        except Exception as e:
            self.output_text.setPlainText(f"Error: {str(e)}")
    
    def evaluate_postfix(self):
        """Evaluate postfix expression"""
        expr = self.input_field.text().strip()
        if not expr:
            return
        
        try:
            # First convert to postfix
            postfix, _ = infix_to_postfix_steps(expr)
            val, steps = eval_postfix_steps(postfix)
            
            result_text = f"Postfix: {postfix}\n"
            if val is not None:
                result_text += f"Result: {val}"
            else:
                result_text += "Cannot evaluate (contains variables or error)"
            
            self.output_text.setPlainText(result_text)
            self.steps_text.setPlainText("Evaluation Steps:\n\n" + "\n\n".join(steps))
        except Exception as e:
            self.output_text.setPlainText(f"Error: {str(e)}")
