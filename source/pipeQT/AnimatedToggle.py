import time
from PySide2.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF, QObject,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    Slot, Property)

from PySide2.QtWidgets import QCheckBox, QWidget, QVBoxLayout, QApplication
from PySide2.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter, QFont
class AnimatedToggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _font_pen = QPen(Qt.black)
    _light_grey_pen = QPen(Qt.lightGray)
    # bar_color=Qt.gray,
    def __init__(self, parent, sizeList, check_state,
                       _w_diff = 2,
                       _h_diff = 5,
                       dist = 25,
                       bar_color="#FF8B00",
                       checked_color="#00B0FF",
                       handle_color=Qt.white,
                       pulse_unchecked_color="#44999999",
                       pulse_checked_color="#4400B0EE"):
        super(AnimatedToggle, self).__init__(parent)

        turn_on_color = "#74b938"
        turn_off_color ="#c9c9c9"
        text_on_color = "#ffffff"
        text_off_color = "#353535"
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
            p.drawText(barRect.x()+self._w_diff+7, barRect.y()+barRect.height()-self._h_diff, "On")
        else:
            p.setPen(self._text_off_pen)
            p.drawText(barRect.x()+barRect.width()-self.dist-self._w_diff, barRect.y()+barRect.height()-self._h_diff, "Off")

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


class MainView(QWidget):
    def __init__(self, _parent=None) -> None:
        super(MainView, self).__init__(_parent)
    
        self.test_cb = AnimatedToggle(self, [150, 50], False)
    
        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.test_cb)
        
        
        self.setLayout(self.main_vl)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    ui = MainView()
    ui.show()
    
    app.exec_()