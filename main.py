"""
DSA Algorithm Visualizer
Main entry point for the application
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles import get_stylesheet


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Apply stylesheet
    app.setStyleSheet(get_stylesheet())
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
