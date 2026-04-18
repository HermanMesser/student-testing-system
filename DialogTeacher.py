from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QPushButton, QVBoxLayout, 
                             QHBoxLayout)

class DialogTeacher(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.resize(400, 100)        
        self.pib = QLineEdit()
        self.e_mail = QLineEdit()
        
        flo = QFormLayout()        
        flo.addRow('PIB', self.pib)
        flo.addRow('Email', self.e_mail)
        

        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')  
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(flo) 
        vbox.addLayout(hbox)

        self.setLayout(vbox) 

        
