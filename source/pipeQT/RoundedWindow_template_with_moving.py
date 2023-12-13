
import os, sys
import PySide2.QtGui

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    from source.pipeQT import GradientMovingProgressbar
else:
    from . import GradientMovingProgressbar

from PySide2.QtWidgets import (
                                QMainWindow, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy,
                                QWidget, QApplication, QLabel, QPushButton, QDesktopWidget
                            )
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QMouseEvent




def move_2_center(main_view):
    qr = main_view.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    main_view.move(qr.topLeft())
    
    
class ClickableSpacer(QWidget):
    old_pos = QPoint()
    def __init__(self, _parent=None) -> None:
        super(ClickableSpacer, self).__init__(_parent)
        self.p = _parent
        self.setMouseTracking(True)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.old_pos = event.globalPos()
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event :QMouseEvent):
        if event.buttons() & Qt.LeftButton:
            self.new_pos = event.globalPos()
            delta = self.new_pos - self.old_pos
            
            _x = self.p.x() + delta.x()
            _y = self.p.y() + delta.y()
            self.p.move(_x, _y)
            
            self.old_pos = event.globalPos()
            
            # _x = event.screenPos().x()+
            # _y = event.screenPos().y()+event.localPos().y()
            
            
    
            
            
    
class RoundedWindow(QMainWindow):
    def __init__(self, _parent :QWidget=None) -> None:
        super(RoundedWindow, self).__init__(_parent)
        self.__IS_CANCELED__ = False
        
        horizontal_spacer = ClickableSpacer(self)
        
        self.minimize_btn = QPushButton("-")
        self.minimize_btn.setStyleSheet(f'''QPushButton{{background-color:rgba(49,54,59,0);padding-top:13px;border: none;font: 20pt;color : #f0f0f0;}}''')
        self.minimize_btn.clicked.connect(self.showMinimized)
        
        self.close_btn = QPushButton("X")
        self.close_btn.setStyleSheet(f'''QPushButton{{background-color:rgba(49,54,59,0);padding-top:13px;border: none;font: 20pt;color : #f0f0f0;}}''')
        self.close_btn.clicked.connect(self.close)
        
        
        
        self.msg_lb = QLabel("Message ... ")
        self.msg_lb.setAlignment(Qt.AlignCenter)
        self.msg_lb.setStyleSheet(f'''QLabel{{padding-top:20px;font: 15pt;color : #f0f0f0;}}''')
        
        
        
        self.sub_hl = QHBoxLayout()
        self.sub_hl.addWidget(horizontal_spacer)
        self.sub_hl.addWidget(self.minimize_btn)
        self.sub_hl.addWidget(self.close_btn)
        self.sub_hl.setStretch(0, 20)
        self.sub_hl.setStretch(1, 1)
        self.sub_hl.setStretch(2, 1)
        self.sub_hl.setContentsMargins(0, 0, 10, 5)
        
        
        
        self.main_vl = QVBoxLayout()
        self.main_vl.addLayout(self.sub_hl)
        self.main_vl.addWidget(self.msg_lb)
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
            background-color:rgba(49,54,59,180);'''.format("8"))
        
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