from PyQt5.QtWidgets import (QDialog, QFormLayout, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QMessageBox, QTextEdit)
from PyQt5.QtSql import QSqlQuery

class EditTestDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.resize(400, 100)
        self.setWindowTitle('Edit Test')

        self.subject_box = QComboBox()
        self.subject_box.currentIndexChanged.connect(self.selectedIndexSubject)
        self.subject_box.currentIndexChanged.connect(self.loadTests)
        self.test_box = QComboBox()
        self.test_box.currentIndexChanged.connect(self.selectedIndexTest)
        self.test_box.currentIndexChanged.connect(self.loadTest)
        self.test_edit = QTextEdit()

        flo = QFormLayout()
        flo.addRow('Subject', self.subject_box)
        flo.addRow('Test', self.test_box)

        edit_btn = QPushButton('Edit Test')
        edit_btn.clicked.connect(self.editTest)

        del_btn = QPushButton('Delete Test')
        del_btn.clicked.connect(self.delTest)

        hbox = QHBoxLayout()
        hbox.addWidget(edit_btn)
        hbox.addWidget(del_btn)
        
        vbox = QVBoxLayout()
        vbox.addLayout(flo)
        vbox.addWidget(self.test_edit)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.loadSubject()

    def selectedIndexSubject(self):
        subject_id = self.subject_box.currentData()
        return subject_id 

    def selectedIndexTest(self):
        test_id = self.test_box.currentData()
        return test_id 

    def editTest(self):
        test_id = self.selectedIndexTest()
        new_title = self.test_edit.toPlainText().strip()

        if not new_title:
            QMessageBox.warning(self, "Ошибка", "Введите название теста")
            return

        query = QSqlQuery()
        query.prepare("""UPDATE tests SET title = :title  WHERE id = :test_id""")
        query.bindValue(":title", new_title)
        query.bindValue(":test_id", test_id)

        if not query.exec_():
            QMessageBox.critical(self, "Ошибка", query.lastError().text())
        else:
            QMessageBox.information(self, "Успех", "Тест обновлён")
            self.loadTests()  # обновить список
    
    def delTest(self):
        reply = QMessageBox.question(self, "Удаление", "Вы уверены, что хотите удалить тест?",
                                    QMessageBox.Yes | QMessageBox.No )

        if reply == QMessageBox.Yes:
            test_id = self.selectedIndexTest() 

            query = QSqlQuery()
            query.prepare("DELETE FROM tests WHERE id = :test_id")
            query.bindValue(":test_id", test_id) 
            query.exec_()

            if not query.exec_():
                print("Ошибка:", query.lastError().text())
            else:
                print("Тест удалён")

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

    def loadTest(self):
        self.test_edit.clear()
        test_id = self.selectedIndexTest() 

        query = QSqlQuery()
        query.prepare("SELECT title FROM tests WHERE id = :test_id")
        query.bindValue(":test_id", test_id) 
        query.exec_()         

        while query.next():
            self.test_edit.setText(query.value(0))                



        
            