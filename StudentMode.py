from PyQt5.QtWidgets import (QTableView, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QHeaderView,
                             QMessageBox)
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import Qt
from DialogStudent import DialogStudent

class StudentMode(QWidget):
    def __init__(self):
        super().__init__()

        self.model = QSqlTableModel()
        self.model.setTable('student')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.doubleClicked.connect(self.updateRow)

        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.table.resizeColumnToContents(1)
        self.table.setAlternatingRowColors(True)
        self.table.hideColumn(0)

        self.add_row = QPushButton('Add Row') 
        self.add_row.clicked.connect(self.addRow)
        self.del_row = QPushButton('Delete Row')
        self.del_row.clicked.connect(self.delRow)
        self.update_row = QPushButton('Update Row')
        self.update_row.clicked.connect(self.updateRow)
        hbox = QHBoxLayout() 
        hbox.addStretch() 
        hbox.addWidget(self.add_row)
        hbox.addWidget(self.del_row)
        hbox.addWidget(self.update_row)

        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        

    def addRow(self):
        dialog = DialogStudent()
        if dialog.exec_():
            f_name = dialog.f_name.text().strip()
            l_name = dialog.l_name.text().strip()

            row = self.model.rowCount()
            self.model.insertRow(row)
                    
            self.model.setData(self.model.index(row,1), f_name)
            self.model.setData(self.model.index(row,2), l_name)
        
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
        
        f_name = self.model.data(self.model.index(row, 1))
        l_name = self.model.data(self.model.index(row, 2))        

        dialog = DialogStudent()        
        dialog.f_name.setText(f_name)
        dialog.l_name.setText(l_name)        

        if dialog.exec_():
            
            self.model.setData(self.model.index(row, 1), dialog.f_name.text())
            self.model.setData(self.model.index(row, 2), dialog.l_name.text())            

            self.model.submitAll()    

