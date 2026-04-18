from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QMessageBox)
from PyQt5.QtSql import QSqlQuery

class DialogTest(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.resize(400, 100) 
        self.setWindowTitle('Add Test')
         
        self.subject_box = QComboBox()
        self.subject_box.currentIndexChanged.connect(self.selectedIndex) 

        self.test = QLineEdit()        
        
        flo = QFormLayout()        
        flo.addRow('Subject', self.subject_box)
        flo.addRow('Test', self.test)        

        add_btn = QPushButton('Add Test')        
        add_btn.clicked.connect(self.accept)        

        hbox = QHBoxLayout()
        hbox.addWidget(add_btn)        

        vbox = QVBoxLayout()
        vbox.addLayout(flo) 
        vbox.addLayout(hbox)
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

    def accept(self):
        #subject_id = self.subject_box.currentData()
        subject_id = self.selectedIndex()
        test_name = self.test.text()

        if not test_name:
            QMessageBox.warning(self, 'Test', 'Name of test dont must be empty ', QMessageBox.Ok)
            return 

        query = QSqlQuery()
        query.prepare("""
                      INSERT INTO tests (subject_id, title) 
                      VALUES (:subject_id, :title)
                      """)
        query.addBindValue(subject_id)
        query.addBindValue(test_name)

        if not query.exec_():
            print("Ошибка:", query.lastError().text())
        else:
            print("Тест добавлен")

        super().accept()    