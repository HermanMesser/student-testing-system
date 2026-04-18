from PyQt5.QtWidgets import (QComboBox, QTabWidget, QWidget, QVBoxLayout, QLabel, QButtonGroup, QRadioButton)
from PyQt5.QtSql import QSqlQuery

class TestMode(QWidget):
    def __init__(self):
        super().__init__()

        self.subject_box = QComboBox()
        self.tabs = QTabWidget() 

        self.subject_box.currentIndexChanged.connect(self.selectedIndex)

        vbox = QVBoxLayout()
        vbox.addWidget(self.subject_box)
        vbox.addWidget(self.tabs)
        vbox.addStretch()
        self.setLayout(vbox)

        self.loadSubjects()

        if self.subject_box.count() > 0:
            self.selectedIndex()        

    def loadSubjects(self):
        self.subject_box.clear()
        query = QSqlQuery('SELECT id, subject_name FROM subjects')

        while query.next():
            subject_id = query.value(0)
            name = query.value(1)
            #print(subject_id, name)
            self.subject_box.addItem(name, subject_id)

    def selectedIndex(self):
        subject_id = self.subject_box.currentData()
        #print("Selected subject:", subject_id)

        if subject_id is not None:
            self.loadTests(subject_id)  

    def loadTests(self, subject_id):
        self.tabs.clear()

        query = QSqlQuery()
        query.prepare("SELECT id, title FROM tests WHERE subject_id = ?")
        query.addBindValue(subject_id)
        query.exec_()

        while query.next():
            test_id = query.value(0)
            title = query.value(1)

            tab = self.createTestTab(test_id)
            self.tabs.addTab(tab, title) 

    def createTestTab(self, test_id):
        widget = QWidget()
        layout = QVBoxLayout()

        #label = QLabel(f"Test ID: {test_id}")
        #layout.addWidget(label)          

        query = QSqlQuery()
        query.prepare("SELECT id, question FROM question WHERE test_id = ?")
        query.addBindValue(test_id)
        query.exec_() 

        while query.next():
            question_id = query.value(0)
            question_text = query.value(1)

            label = QLabel(question_text)
            layout.addWidget(label)
            #print("QUESTION:", question_text)

            button_group = QButtonGroup(widget)

            ans_query = QSqlQuery()
            ans_query.prepare("SELECT id, answer_text FROM answers WHERE question_id = ?")
            ans_query.addBindValue(question_id)
            ans_query.exec_()

            while ans_query.next():
                answer_id = ans_query.value(0)
                answer_text = ans_query.value(1)

                radio = QRadioButton(answer_text)

                # сохраняем ID ответа
                button_group.addButton(radio, answer_id)

                layout.addWidget(radio)                
                #print("ANSWER:", answer_text)

        layout.addStretch()
        widget.setLayout(layout)

        return widget            