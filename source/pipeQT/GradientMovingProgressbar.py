
from PySide2.QtWidgets import QApplication, QProgressBar
from PySide2.QtCore import Property, QPropertyAnimation, QEasingCurve
from time import sleep


class GMProgressbar(QProgressBar):
    def __init__(self, _parent=None) -> None:
        super(GMProgressbar, self).__init__(_parent)
        
        self._x = 0.0
        self.start_value    = 0.0
        self.end_value      = 1.0
        self.color_01 = "rgba(20, 101, 196, 255)"
        self.color_02 = "rgba(113, 169, 235, 255)"
        
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
        
    @Property(float)
    def stop01_pose(self):
        return self._x
    
    @stop01_pose.setter
    def stop01_pose(self, value):
        self._x = value
        
        self.update_stylesheet(self._x)
            
    def setup_ani(self):
        self.opa_anim = QPropertyAnimation(self, b"stop01_pose")
        self.opa_anim.setStartValue(self.start_value)
        self.opa_anim.setEndValue(self.end_value)
        self.opa_anim.setDuration(1200)
        self.opa_anim.finished.connect(self.re_start)
        self.opa_anim.setEasingCurve(QEasingCurve.OutCubic)
           
    def update_stylesheet(self, x_pose) -> None:
        # x_pose = 0.0
        
        x_pose = round(x_pose, 2)
        if x_pose <= 0.5:
            self.setStyleSheet(f'''
                            QProgressBar{{
                                                border : 1px solid #4f5b62;
                                                border-radius : 7px;
                                            }}
                            QProgressBar::chunk {{
                                    border : 1px solid #4f5b62;
                                    border-radius : 7px;
                                    background-color: qlineargradient(spread:reflect, x1:1.0, y1:0.5, x2:{x_pose}, y2:0.5, stop:0.78 {self.color_01}, stop:1 {self.color_02});
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
                                    background-color: qlineargradient(spread:reflect, x1:0.0, y1:0.5, x2:{x_pose}, y2:0.5, stop:0.78 {self.color_01}, stop:1 {self.color_02});
                                }}
                            ''')
             
    def re_start(self) -> None:
        self.opa_anim.stop()
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
class GradientProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Blinking Progress Dialog')

        layout = QVBoxLayout()

        self.progress_bar = GMProgressbar(self)
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
    dialog = GradientProgressDialog()
    dialog.show()
    sys.exit(app.exec_())


'''
