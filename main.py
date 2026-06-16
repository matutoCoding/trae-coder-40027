import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QIcon
from ui.main_window import MainWindow
from ui.styles import AppStyles


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("危化品罐区储运业务管理系统")
    app.setStyle("Fusion")
    
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    
    app.setStyleSheet(AppStyles.get_global_style())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
