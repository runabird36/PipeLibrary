from PySide2.QtWidgets import QApplication, QProgressBar
from PySide2.QtCore import Property, QPropertyAnimation, QAbstractAnimation, QEasingCurve
from time import sleep

class BlinkingProgressbar(QProgressBar):
    def __init__(self, _parent=None) -> None:
        super(BlinkingProgressbar, self).__init__(_parent)
        self.tar_color      = (67, 139, 250)
        self.diff           = -40
        self.start_value    = 250
        self.end_value = self.start_value + self.diff
        self.DOT_MODE       = True
        
        self._chunk_color = self.start_value
        self.setup_ani()
        
        self.setRange(0, 100)
        self.setStyleSheet(f'''
                            QProgressBar{{
                                            border : 1px solid #4f5b62;
                                            border-radius : 7px;
                                        }}
                            QProgressBar::chunk{{
                                border : 1px solid #4f5b62;
                                border-radius : 7px;
                            }}
                           ''')
        
    @Property(int)
    def chunk_color(self):
        return self._chunk_color
    
    @chunk_color.setter
    def chunk_color(self, value):
        self._chunk_color = value
        
        cur_diff = self.start_value - value 
        
        _R = self.tar_color[0] - cur_diff
        _G = self.tar_color[1] - cur_diff
        _B = self.tar_color[2] - cur_diff
        
        self.update_stylesheet(_R, _G, _B)
        
    def setup_ani(self):
        self.opa_anim = QPropertyAnimation(self, b"chunk_color")
        self.opa_anim.setStartValue(self.start_value)
        self.opa_anim.setEndValue(self.end_value)
        self.opa_anim.setDuration(500)
        self.opa_anim.finished.connect(self.start_reverse)
        self.opa_anim.setEasingCurve(QEasingCurve.OutCubic)
         
    def update_stylesheet(self, _R, _G, _B) -> None:
        if self.DOT_MODE == True:
            self.setStyleSheet(f'''
                            QProgressBar{{
                                                border : 1px solid #4f5b62;
                                                border-radius : 7px;
                                            }}
                            QProgressBar::chunk {{
                                    border : 1px solid #4f5b62;
                                    border-radius : 7px;
                                    background-color: rgba({_R}, {_G}, {_B}, 1.0);
                                    width: 15px;
                                }}
                            ''')
        else:
            self.setStyleSheet(f'''
                            QProgressBar{{
                                                border : 1px solid #4f5b62;
                                                border-radius : 7px;
                                            }}
                            QProgressBar::chunk {{
                                    border : 1px solid #4f5b62;
                                    border-radius : 7px;
                                    background-color: rgba({_R}, {_G}, {_B}, 1.0);
                                }}
                            ''')
        
    def start_reverse(self) -> None:
        if self.opa_anim.direction() == QAbstractAnimation.Forward:
            self.opa_anim.setDirection(QAbstractAnimation.Backward)
        else:
            self.opa_anim.setDirection(QAbstractAnimation.Forward)
        self.opa_anim.start()
          
    def update_progress(self, to_value :int) -> None:
        self.opa_anim.start()
        from_value = self.value()

        for cur_value in range(from_value, to_value+1):
            self.setValue(cur_value)
            QApplication.processEvents()
            sleep(0.005)
            
            
    
'''
How to use :


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from qt_material import apply_stylesheet
class BlinkingProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Blinking Progress Dialog')

        layout = QVBoxLayout()

        self.progress_bar = BlinkingProgressbar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_blinking)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        apply_stylesheet(self, "dark_blue.xml")

        

    def start_blinking(self):
        
        self.progress_bar.update_progress(100)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = BlinkingProgressDialog()
    dialog.show()
    sys.exit(app.exec_())


'''
