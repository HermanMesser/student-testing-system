from PyQt5.QtWidgets import QMenuBar, QActionGroup
from PyQt5.QtCore import pyqtSignal

class MainMenu(QMenuBar):
    modeChanged = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        mode_menu = self.addMenu('Mode')
        mode_action_group = QActionGroup(self)
        mode_action_group.setExclusive(True)
        mode_action_group.triggered.connect(self.changeMode)

        self.mode_menu_action = mode_menu.menuAction()
        self.teacher_mode_action = mode_menu.addAction('Teacher')
        self.teacher_mode_action.setCheckable(True)
        mode_action_group.addAction(self.teacher_mode_action)

        self.student_mode_action = mode_menu.addAction('Student')
        self.student_mode_action.setCheckable(True)
        mode_action_group.addAction(self.student_mode_action)

        self.test_mode_action = mode_menu.addAction('Test')
        self.test_mode_action.setCheckable(True)
        mode_action_group.addAction(self.test_mode_action)

        self.teacher_mode_action.setData("teacher")
        self.student_mode_action.setData("student")
        self.test_mode_action.setData("test")
        
    def changeMode(self, action):
        mode = action.data()
        print(f"Mode changed: {mode}")
        self.modeChanged.emit(mode)    

                 
