from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Finance Management System")
window.show()

# Start the event loop.
app.exec()