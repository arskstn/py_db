# forms/window_actions.py
from PyQt5.QtWidgets import QMessageBox

def CascadeWindowsAction(main_window):
    QMessageBox.information(main_window, "Окно", "Здесь каскадное расположение окон.")

def MinimizeAllAction(main_window):
    QMessageBox.information(main_window, "Окно", "Здесь сворачивание всех окон.")

def RestoreAllAction(main_window):
    QMessageBox.information(main_window, "Окно", "Здесь разворачивание всех окон.")
