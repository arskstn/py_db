# forms/window_module.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

def CascadeWindowsAction():
    # Можно убрать, если не понадобится. Я не знаю, что тут можно каскадом открывать
    pass

def MinimizeAllAction():
    for w in QApplication.topLevelWidgets():
        if not w.isWindow() or not w.isVisible():
            continue
        if w.windowState() & Qt.WindowMinimized:
            continue
        w.showMinimized()

def RestoreAllAction():
    for w in QApplication.topLevelWidgets():
        if not w.isWindow() or not w.isVisible():
            continue
        if w.windowState() & Qt.WindowMinimized:
            w.showNormal()
