
import os, sys

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    from source.pipeQT import GradientMovingProgressbar
else:
    from . import GradientMovingProgressbar

from PySide2.QtWidgets import (
                                QMainWindow, QVBoxLayout, QHBoxLayout,
                                QWidget, QApplication, QLabel, QPushButton, QDesktopWidget
                            )
from PySide2.QtCore import Qt




def move_2_center(main_view):
    qr = main_view.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    main_view.move(qr.topLeft())
    
class RoundedWindow(QMainWindow):
    def __init__(self, _parent :QWidget=None) -> None:
        super(RoundedWindow, self).__init__(_parent)
        self.__IS_CANCELED__ = False
        
        self.msg_lb = QLabel("Message ... ")
        self.msg_lb.setAlignment(Qt.AlignCenter)
        self.msg_lb.setStyleSheet(f'''QLabel{{padding-top:20px;font: 15pt;color : #f0f0f0;}}''')
        
        self.close_btn = QPushButton("X")
        self.close_btn.setStyleSheet(f'''QPushButton{{padding-top:13px;border: none;font: 20pt;color : #f0f0f0;}}''')
        self.close_btn.clicked.connect(self.close)
        
        self.sub_hl = QHBoxLayout()
        self.sub_hl.addWidget(self.msg_lb)
        self.sub_hl.addWidget(self.close_btn)
        self.sub_hl.setStretch(0, 20)
        self.sub_hl.setStretch(1, 1)
        self.sub_hl.setContentsMargins(70, 0, 5, 5)
        
        
        
        self.main_vl = QVBoxLayout()
        self.main_vl.addLayout(self.sub_hl)
        self.main_vl.setContentsMargins(15, 5, 15, 40)
        
        self.main_wg = QWidget()
        self.main_wg.setLayout(self.main_vl)
        self.setCentralWidget(self.main_wg)
        
        self.setWindowTitle("Rounded Window Template")
        self.resize(450, 180)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_wg.setStyleSheet('''
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            background-color:rgba(49,54,59,255);'''.format("8"))
        
        # rgba(29, 34, 39, 255)
        
        
        move_2_center(self)
        
    def closeEvent(self, a0) -> None:
        self.__IS_CANCELED__ = True
        return super().closeEvent(a0)
               
    


if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    
    ui = RoundedWindow()
    ui.show()
    
    app.exec_()