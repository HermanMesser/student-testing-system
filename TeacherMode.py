from PyQt5.QtWidgets import (QTableView, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QHeaderView,
                             QMessageBox)
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import Qt
from DialogTeacher import DialogTeacher
from DialogTest import DialogTest
from DialogQuestion import DialogQuestion
from EditTestDialog import EditTestDialog
from EditQuestionDialog import EditQuestionDialog

class TeacherMode(QWidget):
    def __init__(self):
        super().__init__()

        self.model = QSqlTableModel()
        self.model.setTable('teacher')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.doubleClicked.connect(self.updateRow)

        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.table.resizeColumnToContents(1)
        self.table.setAlternatingRowColors(True)
        #self.table.hideColumn(0)

        self.add_row = QPushButton('Add Row') 
        self.add_row.clicked.connect(self.addRow)
        self.del_row = QPushButton('Delete Row')
        self.del_row.clicked.connect(self.delRow)
        self.update_row = QPushButton('Update Row')
        self.update_row.clicked.connect(self.updateRow)
        self.add_test = QPushButton('Add Test')
        self.add_test.clicked.connect(self.addTest)
        self.edit_test = QPushButton('Edit Test')
        self.edit_test.clicked.connect(self.editTest)
        self.add_question = QPushButton('Add Question')
        self.add_question.clicked.connect(self.addQuestion)
        self.edit_question = QPushButton('Edit Question')
        self.edit_question.clicked.connect(self.editQuestion)
        hbox = QHBoxLayout() 
        hbox.addStretch() 
        hbox.addWidget(self.add_row)
        hbox.addWidget(self.del_row)
        hbox.addWidget(self.update_row)
        hbox.addWidget(self.add_test)
        hbox.addWidget(self.edit_test)
        hbox.addWidget(self.add_question)
        hbox.addWidget(self.edit_question)

        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        

    def addRow(self):
        dialog = DialogTeacher()
        if dialog.exec_():
            pib = dialog.pib.text().strip()
            e_mail = dialog.e_mail.text().strip()

            row = self.model.rowCount()
            self.model.insertRow(row)
                    
            self.model.setData(self.model.index(row,1), pib)
            self.model.setData(self.model.index(row,2), e_mail)
        
            self.model.submitAll()

    def delRow(self):
        index = self.table.currentIndex()        

        if not index.isValid():
            QMessageBox.warning(self, 'Choice', 'Choice a row', QMessageBox.Ok)
            return
        replay = QMessageBox.question(self, 'Delete Row', 
                                          'Are you sure you wanna delete this row?',
                                          QMessageBox.Yes | QMessageBox.No)
        if replay == QMessageBox.Yes:
            self.model.removeRow(index.row())
            self.model.submitAll()
    
    def updateRow(self):
        index = self.table.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, 'Choice', 'Choice a row', QMessageBox.Ok)
            return
            
        row = index.row()
        
        pib = self.model.data(self.model.index(row, 1))
        e_mail = self.model.data(self.model.index(row, 2))        

        dialog = DialogTeacher()        
        dialog.pib.setText(pib)
        dialog.e_mail.setText(e_mail)        

        if dialog.exec_():            
            self.model.setData(self.model.index(row, 1), dialog.pib.text())
            self.model.setData(self.model.index(row, 2), dialog.e_mail.text())            

            self.model.submitAll()

    def addTest(self):
        dialog = DialogTest()
        if dialog.exec_():
            print("Диалог закрыт с OK")

    def addQuestion(self):
        dialog = DialogQuestion()
        if dialog.exec_():
            print("Диалог закрыт с OK") 

    def editTest(self):
        dialog = EditTestDialog()
        if dialog.exec_():
            print('Dialog is close with OK') 

    def editQuestion(self):
        dialog = EditQuestionDialog()
        if dialog.exec_():
            print('Dialog close with Ok')                      

