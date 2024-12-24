# run.py
import sys
from PyQt5.QtWidgets import QApplication
from database import init_db
from models import MenuItem, User
from login import LoginWindow
from main_window import MainWindow

def main():
    init_db()
    MenuItem.create_initial_menu_items()
    User.create_superuser_if_not_exists()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    login_window = LoginWindow()
    if login_window.exec_() == LoginWindow.Accepted:
        user_data = login_window.user_data
        main_window = MainWindow(user_data)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
