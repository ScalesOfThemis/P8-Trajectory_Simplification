from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QListWidget,
)
import sys

# Use the commands before it can run:
# python -m venv .venv
# .venv\Scripts\Activate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trajectory Display")
        self.setGeometry(100,100, 400, 300)

        listwidget = QListWidget()
        listwidget.addItems(["Trajectory 1", "Trajectory 2", "Trajectory 3"])

        # listwidget.currentItemChanged

        layout = QVBoxLayout()
        layout.addWidget(listwidget)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
