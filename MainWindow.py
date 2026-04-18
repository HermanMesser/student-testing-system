import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtSql import QSqlDatabase
from MainMenu import MainMenu
import Setting as st
from TeacherMode import TeacherMode
from StudentMode import StudentMode
from TestMode import TestMode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.showMaximized()
        self.setWindowTitle('TEST')
        self.createConnection()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.displayWidgets()

    def displayWidgets(self):
        self.main_menu = MainMenu()
        self.setMenuBar(self.main_menu)
        self.main_menu.modeChanged.connect(self.onModeChanged)

        self.teacher_page = TeacherMode()
        self.student_page = StudentMode()
        self.test_page = TestMode()
    
    def createConnection(self): 
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName(st.db_params['host'])
        db.setDatabaseName(st.db_params['dbname'])
        db.setPort(st.db_params['port'])
        db.setUserName(st.db_params['user'])
        db.setPassword(st.db_params['password'])

        if not db.open():
            print('Database connect falure')
            return False
        else:
            print('Databse connect')
            return True

    def onModeChanged(self, mode):
        if mode == "teacher":
            print('Teacher mode')
            self.showTeacherUI()

        elif mode == "student":
            print('Student Mode')
            self.showStudentUI()

        elif mode == "test":
            print('Test mode')
            self.showTestUI() 

    def showTeacherUI(self):
        self.stack.addWidget(self.teacher_page)
        self.stack.setCurrentWidget(self.teacher_page)


    def showStudentUI(self):
        self.stack.addWidget(self.student_page)
        self.stack.setCurrentWidget(self.student_page)

    def showTestUI(self):
        self.stack.addWidget(self.test_page)
        self.stack.setCurrentWidget(self.test_page)   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = MainWindow()
    root.show()
    sys.exit(app.exec_())            