from PyQt5.QtWidgets import (QDialog, QLineEdit, QFormLayout, QPushButton, QVBoxLayout, 
                             QHBoxLayout)

class DialogStudent(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.resize(400, 100)        
        self.f_name = QLineEdit()
        self.l_name = QLineEdit()
        
        flo = QFormLayout()        
        flo.addRow('First Name', self.f_name)
        flo.addRow('Last Name', self.l_name)        

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

        
