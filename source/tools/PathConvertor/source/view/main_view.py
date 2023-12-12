

from PySide2.QtWidgets import (
                                    QWidget, QMainWindow, QLineEdit, QGridLayout,
                                    QLabel, QPushButton, QDesktopWidget, QVBoxLayout, QHBoxLayout, 
                                    QApplication, QTabWidget, QCheckBox
                            )
from PySide2.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    Slot, Property)
from PySide2.QtGui import QColor, QBrush, QMouseEvent, QPen, QPainter, QFont
from qt_material import apply_stylesheet
from ..toolkit.path_toolkit import is_windows, is_linux


def move_2_center(main_view):
    qr = main_view.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    main_view.move(qr.topLeft())


class AnimatedToggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _font_pen = QPen(Qt.black)
    _light_grey_pen = QPen(Qt.lightGray)
    # bar_color=Qt.gray,
    def __init__(self, parent, sizeList, check_state, state_txt, bg_color,
                       _w_diff = 3,
                       _h_diff = 8,
                       dist = 28,
                       bar_color="#FF8B00",
                       checked_color="#00B0FF",
                       handle_color=Qt.white,
                       pulse_unchecked_color="#44999999",
                       pulse_checked_color="#4400B0EE"):
        super(AnimatedToggle, self).__init__(parent)

        self.status_txt = state_txt
        turn_on_color = "#1db882"
        turn_off_color ="#255a9d"
        turn_on_color = bg_color[0]
        turn_off_color =bg_color[1]
        text_on_color = "#ffffff"
        text_off_color = "#ffffff"
        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(QColor(bar_color).lighter())
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(QColor(bar_color))
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))


        self._turn_on_brush = QBrush(QColor(turn_on_color))
        self._turn_off_brush = QBrush(QColor(turn_off_color))
        self._text_on_brush = QBrush(QColor(text_on_color))
        self._text_on_pen = QPen(QColor(text_on_color))
        self._text_off_pen = QPen(QColor(text_off_color))


        # Setup the rest of the widget.

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self._pulse_radius = 0
        self._w_diff = _w_diff
        self._h_diff = _h_diff
        self.dist = dist
        

        _anim_speed = 500
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.OutBounce )
        self.animation.setDuration(_anim_speed)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(_anim_speed)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)
        self.setFixedWidth(sizeList[0])
        self.setFixedHeight(sizeList[1])
        self.setChecked(check_state)
        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    @Slot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e):

        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())


        p = QPainter(self)
        p.setRenderHint(QPainter.HighQualityAntialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._turn_on_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._text_on_brush)

        else:
            p.setBrush(self._turn_off_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            # p.setPen(self._light_grey_pen)
            p.setBrush(self._text_on_brush)
       
        font = QFont()
        font.setFamily('DejaVu Sans')
        font.setBold(True)
        font.setPointSize(9)
        p.setFont(font)

        
        if self.isChecked():
            p.setPen(self._text_on_pen)
            p.drawText(barRect.x()+self._w_diff+7, barRect.y()+barRect.height()-self._h_diff, self.status_txt[0])
        else:
            p.setPen(self._text_off_pen)
            p.drawText(barRect.x()+barRect.width()-self.dist-self._w_diff, barRect.y()+barRect.height()-self._h_diff, self.status_txt[1])

        p.setPen(self._transparent_pen)
        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)
        p.end()

    def get_handle_position(self): return self._handle_position
    def set_handle_position(self, _h_pos): self._handle_position = _h_pos; self.update()
    handle_position = Property(float, get_handle_position, set_handle_position)

    def get_pulse_radius(self): return self._pulse_radius
    def set_pulse_radius(self, _p_radius): self._pulse_radius = _p_radius; self.update()
    pulse_radius = Property(float, get_pulse_radius, set_pulse_radius)

    def get_cur_mode(self) -> str:
        if self.isChecked() == True:
            return self.status_txt[0]
        else:
            return self.status_txt[1]
    
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
            
    


class MainView(QMainWindow):
    def __init__(self, _parent=None) -> None:
        super(MainView, self).__init__(_parent)
        self.__IS_CANCELED__ = False
        
        
        if is_linux():
            self.mode_toggle_cb = AnimatedToggle(self, [105,65], False, ["Win", "Linux"], ["#255a9d", "#1db882"], dist=40)
        else:
            self.mode_toggle_cb = AnimatedToggle(self, [105,65], False, ["Linux", "Win"], ["#1db882", "#255a9d"])
        
        self.header_wg = ClickableSpacer(self)

        self.minimize_btn = QPushButton("-")
        self.minimize_btn.setStyleSheet(f'''QPushButton{{background-color:rgba(49,54,59,0);padding-top:13px;border: none;font: 20pt;color : #f0f0f0;}}''')
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.close_btn = QPushButton("X")
        self.close_btn.setStyleSheet(f'''QPushButton{{background-color:rgba(49,54,59,0);padding-top:13px;border: none;font: 20pt;color : #f0f0f0;}}''')
        self.close_btn.clicked.connect(self.close)


        self.header_hl = QHBoxLayout()
        self.header_hl.addWidget(self.mode_toggle_cb)
        self.header_hl.addWidget(self.header_wg)
        self.header_hl.addWidget(self.minimize_btn)
        self.header_hl.addWidget(self.close_btn)
        self.header_hl.setStretch(0, 2)
        self.header_hl.setStretch(1, 20)
        self.header_hl.setStretch(2, 1)
        self.header_hl.setStretch(3, 1)
        self.header_hl.setContentsMargins(0, 0, 10, 5)

        self.from_lb    = QLabel("From : ")
        self.to_lb      = QLabel("To : ")

        self.from_input_le  = QLineEdit()
        self.to_input_le    = QLineEdit()
        self.to_input_le.setReadOnly(True)

        self.convert_btn            = QPushButton("변환")
        self.copy_to_clipboard_btn  = QPushButton("ㅁ")
        self.open_folder_btn        = QPushButton("경로 열기")
        self.copy_to_clipboard_btn.setFixedSize(30, 30)
        self.open_folder_btn.setFixedSize(100, 50)

        self.input_gl = QGridLayout()
        self.input_gl.addWidget(self.from_lb,           0, 0)
        self.input_gl.addWidget(self.to_lb,             1, 0)
        self.input_gl.addWidget(self.from_input_le,     0, 1)
        self.input_gl.addWidget(self.to_input_le,       1, 1)

        self.body_btn_vl = QVBoxLayout()
        self.body_btn_vl.addWidget(self.convert_btn)
        self.body_btn_vl.addWidget(self.copy_to_clipboard_btn)

        self.body_hl = QHBoxLayout()
        self.body_hl.addLayout(self.input_gl)
        self.body_hl.addLayout(self.body_btn_vl)
        

        self.body_wg = QWidget()
        self.body_wg.setLayout(self.body_hl)

        self.body_tw = QTabWidget()
        self.body_tw.setTabPosition(QTabWidget.West)
        self.body_tw.addTab(self.body_wg, "경로 정보")

        self.main_vl = QVBoxLayout()
        self.main_vl.addLayout(self.header_hl)
        self.main_vl.addWidget(self.body_tw)
        self.main_vl.addWidget(self.open_folder_btn, alignment=Qt.AlignCenter)
        self.main_vl.setStretch(0, 1)
        self.main_vl.setStretch(1, 5)
        self.main_vl.setStretch(2, 1)

        self.main_wg = QWidget()
        self.main_wg.setLayout(self.main_vl)

        self.setCentralWidget(self.main_wg)


        self.setWindowTitle("Rounded Window Template")
        self.resize(700, 180)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_wg.setStyleSheet('''
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            background-color:rgba(49,54,59,150);'''.format("8"))
        
        # rgba(29, 34, 39, 255)
        
        
        apply_stylesheet(self, "dark_blue.xml")
        move_2_center(self)
        self.set_hint()
        
        

    def closeEvent(self, a0) -> None:
        self.__IS_CANCELED__ = True
        return super().closeEvent(a0)
    

    def set_link(self, controller) -> None:
        self.mode_toggle_cb.stateChanged.connect(controller.change_mode)
        self.convert_btn.clicked.connect(controller.convert_path)
        self.copy_to_clipboard_btn.clicked.connect(controller.copy_to_clipboard)
        self.open_folder_btn.clicked.connect(controller.open_dir)


    def get_from_path(self) -> str:
        return self.from_input_le.text()
    
    def get_to_path(self) -> str:
        return self.to_input_le.text()

    def set_to_path(self, to_path :str) -> None:
        self.to_input_le.setText(to_path)

    def set_hint(self):
        if is_windows():
            self.from_input_le.setPlaceholderText("리눅스 경로 입력")
        elif is_linux():
            self.from_input_le.setPlaceholderText("윈도우 경로 입력")

    def switch_hint(self, cur_os :str) -> None:
        if cur_os.lower() == "win":
            self.from_input_le.setPlaceholderText("리눅스 경로 입력")
        elif cur_os.lower() == "linux":
            self.from_input_le.setPlaceholderText("윈도우 경로 입력")
            
    def get_cur_mode(self) -> str:
        return self.mode_toggle_cb.get_cur_mode()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    ui = MainView()
    ui.show()

    app.exec_()