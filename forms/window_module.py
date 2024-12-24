from PyQt5.QtWidgets import QMessageBox, QWidget

def CascadeWindowsAction(main_window):
    QMessageBox.information(main_window, "Окно", "Окна будут расположены каскадом (MDI).")

def MinimizeAllAction(main_window):
    for w in QWidget.topLevelWidgets():
        if w is not main_window:
            w.showMinimized()
    QMessageBox.information(main_window, "Окно", "Все окна (кроме главного) свернуты.")

def RestoreAllAction(main_window):
    for w in QWidget.topLevelWidgets():
        if w.isMinimized():
            w.showNormal()
    QMessageBox.information(main_window, "Окно", "Все окна восстановлены.")
