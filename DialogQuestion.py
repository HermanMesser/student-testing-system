from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QTextEdit, QWidget, QRadioButton, QMessageBox, 
                             QButtonGroup)
from PyQt5.QtSql import QSqlQuery

class DialogQuestion(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.resize(400, 100) 
        self.setWindowTitle('Add Question')
         
        self.test_box = QComboBox()
        self.test_box.currentIndexChanged.connect(self.selectedIndex)

        self.subject_box = QComboBox()
        self.subject_box.currentIndexChanged.connect(self.loadTests)

        self.question = QLineEdit()

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        
        self.answer = []
        self.answer_layout = QVBoxLayout()        
        self.addAnswerField()
        self.addAnswerField()

        

        flo = QFormLayout()
        flo.addRow('Subject', self.subject_box)        
        flo.addRow('Test', self.test_box)  
        flo.addRow('Question', self.question)      

        add_answer_btn = QPushButton('+')
        add_answer_btn.clicked.connect(self.addAnswerField)
        add_btn = QPushButton('Add Question')        
        add_btn.clicked.connect(self.accept)  

        hbox = QHBoxLayout()
        hbox.addWidget(add_answer_btn)
        hbox.addWidget(add_btn)        

        vbox = QVBoxLayout()
        vbox.addLayout(flo)         
        vbox.addLayout(self.answer_layout)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.loadSubjects()

        if self.test_box.count() > 0:
            self.selectedIndex()

    def loadTests(self):
        self.test_box.clear()
        subject_id = self.subject_box.currentData()

        query = QSqlQuery()
        query.prepare("SELECT id, title FROM tests WHERE subject_id = :subject_id")
        query.bindValue(":subject_id", subject_id)
        query.exec_()

        while query.next():
            self.test_box.addItem(query.value(1), query.value(0))

    def loadSubjects(self):
        self.subject_box.clear()
        query = QSqlQuery('SELECT id, subject_name FROM subjects')

        while query.next():
            self.subject_box.addItem(query.value(1), query.value(0))        
        
    def selectedIndex(self):
        test_id = self.test_box.currentData()
        print("Selected test:", test_id)  

    def accept(self):
        test_id = self.test_box.currentData()
        question = self.question.text() 

        if question == '':
            QMessageBox.warning(self, 'Qustion', 'Question dont must be empty ', QMessageBox.Ok)
            return          

        answers = []
        correct_index = None  

        for i, (edit, radio) in enumerate(self.answer):
            text = edit.toPlainText().strip()

            if not text:
                continue

            answers.append(text)

            if radio.isChecked():
                correct_index = i 

        if len(answers) < 2:
            QMessageBox.warning(self, 'Answer', 'Minimum 2 answers', QMessageBox.Ok)
            return 

        if correct_index is None:
            QMessageBox.warning(self, 'Choice', 'Choice a right answer', QMessageBox.Ok)
            return                   

        query = QSqlQuery()
        query.prepare("""
                        INSERT INTO question (test_id, question) 
                        VALUES (:test_id, :question)
                        RETURNING id
                        """)
        query.addBindValue(test_id)
        query.addBindValue(question)

        if query.exec_() and query.next():
            question_id = query.value(0)
        else:
            print("Ошибка:", query.lastError().text())
            return
        
        question_id = query.lastInsertId()

        for i, answer in enumerate(answers):
            is_correct = (i == correct_index)

            query = QSqlQuery()
            query.prepare("""
                        INSERT INTO answers (question_id, answer, is_correct) 
                        VALUES (:question_id, :answer, :is_correct)
                        """)
            query.addBindValue(question_id)
            query.addBindValue(answer)
            query.addBindValue(is_correct)
            

            if not query.exec_():
                print("Ошибка:", query.lastError().text())
            else:
                print("Тест добавлен")

        super().accept() 

    def addAnswerField(self):
        container = QWidget()
        layout = QHBoxLayout()

        radio = QRadioButton()
        answer_edit = QTextEdit()
        answer_edit.setFixedHeight(50)  

        self.button_group.addButton(radio)      

        layout.addWidget(radio)
        layout.addWidget(answer_edit)
        container.setLayout(layout)

        self.answer.append((answer_edit, radio))
        self.answer_layout.addWidget(container)
