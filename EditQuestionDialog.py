from PyQt5.QtWidgets import (QDialog, QFormLayout, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QMessageBox, QTextEdit)
from PyQt5.QtSql import QSqlQuery

class EditQuestionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.resize(400, 100)
        self.setWindowTitle('Edit Question')

        self.subject_box = QComboBox()
        self.subject_box.currentIndexChanged.connect(self.selectedIndexSubject)
        self.subject_box.currentIndexChanged.connect(self.loadTests)
        self.test_box = QComboBox()
        self.test_box.currentIndexChanged.connect(self.selectedIndexTest)
        self.test_box.currentIndexChanged.connect(self.loadQuestions)
        self.question_box = QComboBox()
        self.question_box.currentIndexChanged.connect(self.selectedIndexQuestion)
        self.question_box.currentIndexChanged.connect(self.loadQuestion)
        self.question_box.currentIndexChanged.connect(self.loadAnswers)          
        
        form_layout = QFormLayout()
        form_layout.addRow("Subject", self.subject_box)
        form_layout.addRow("Test", self.test_box)
        form_layout.addRow("Question", self.question_box) 

        self.question_edit = QTextEdit()

        self.answers_layout = QVBoxLayout()        

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.question_edit)
        main_layout.addLayout(self.answers_layout)
        self.setLayout(main_layout)

        self.loadSubject()

    def selectedIndexSubject(self):
        subject_id = self.subject_box.currentData()
        return subject_id 

    def selectedIndexTest(self):
        test_id = self.test_box.currentData()
        return test_id

    def selectedIndexQuestion(self):
        question_id = self.question_box.currentData()
        return question_id      

    def loadSubject(self):
        self.subject_box.clear()
        query = QSqlQuery('SELECT id, subject_name FROM subjects')

        while query.next():
            subject_id = query.value(0)
            name = query.value(1)
            #print(subject_id, name)
            self.subject_box.addItem(name, subject_id)  

    def loadTests(self):
        self.test_box.clear()
        subject_id = self.selectedIndexSubject()

        query = QSqlQuery()
        query.prepare("SELECT id, title FROM tests WHERE subject_id = :subject_id")
        query.bindValue(":subject_id", subject_id)
        query.exec_()

        while query.next():
            self.test_box.addItem(query.value(1), query.value(0))  
    
    def loadQuestions(self):
        self.question_box.clear()
        test_id = self.selectedIndexTest()

        query = QSqlQuery()
        query.prepare("SELECT id, question FROM question WHERE test_id = :test_id") 
        query.bindValue(":test_id", test_id)
        query.exec_()
        while query.next():
            self.question_box.addItem(query.value(1), query.value(0))

    def loadQuestion(self):
        self.question_edit.clear()
        question_id = self.selectedIndexQuestion() 

        query = QSqlQuery()
        query.prepare("SELECT question FROM question WHERE id = :question_id")
        query.bindValue(":question_id", question_id) 
        query.exec_()         

        while query.next():
            self.question_edit.setText(query.value(0))        

    def loadAnswers(self):
        pass             