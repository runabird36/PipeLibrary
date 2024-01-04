# :coding: utf-8
import os
from .app_path_module import *
from .app_constant_module import *

class FrameBox(QtWidgets.QGroupBox):
    '''
    How to use : 
        self.apps_tab = TabMainWidget()
        -> apps_group = app_custom_ui.FrameBox('rgb(50, 50, 50)')
        apps_layout = QtWidgets.QVBoxLayout()
        apps_layout.addWidget(self.apps_tab)
        apps_layout.setContentsMargins(0, 4, 0, 0)
        -> apps_group.setLayout(apps_layout)

        self.banners_widget = BannersWidget()
        banners_group = app_custom_ui.FrameBox('rgb(50, 50, 50)')
        banners_layout = QtWidgets.QHBoxLayout()
        banners_layout.addWidget(self.banners_widget)
        banners_layout.setContentsMargins(0, 0, 0, 0)
        banners_group.setLayout(banners_layout)

        layout = QtWidgets.QVBoxLayout(main_widget)
        -> layout.addWidget(apps_group, 25)
        layout.addWidget(banners_group, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
    '''
    def __init__(self, background_color, border_style=False, border_radius='0px', parent=None):
        QtWidgets.QGroupBox.__init__(self)

        if not border_style:
            border_style = 'none'
        self.setStyleSheet('QGroupBox { background-color:%s; border:1.5px %s rgb(85,85,85); border-radius:%s; color:white; font:11pt; font-weight:bold; font-family:%s; }'
                           %(background_color, border_style, border_radius, UI_FONT_FAMILTY))

class Splitter(QtWidgets.QSplitter):
    def __init__(self, parent=None):
        QtWidgets.QSplitter.__init__(self)

        self.setOrientation(Qt.Orientation.Vertical)
        self.setChildrenCollapsible(False)
        self.setHandleWidth(1)        
        self.setStyleSheet('QSplitter:handle { background-color:rgb(60,60,60); border-radius:8px; margin:5px; }'
                           'QSplitter:handle:pressed { background-color:rgb(80,80,80); margin:5px; }'
                          )

class Frame(QtWidgets.QFrame):
    def __init__(self, style, width, parent=None):
        QtWidgets.QFrame.__init__(self,parent)

        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setLineWidth(width)
        if style == 'Sunken':
            self.setFrameShadow(QtWidgets.QFrame.Sunken)
        else:
            self.setStyleSheet('QFrame{ color: %s }' % style)

class BannerIcon(QtWidgets.QPushButton):
    def __init__(self, icon_name, parent=None):
        QtWidgets.QPushButton.__init__(self)

        icon_name = '{0}{1}.png'.format(UI_ICON_PATH, icon_name)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet('QPushButton { background-color:transparent; border-style:none; text-align:left; padding-left:0px; qproperty-icon:url(%s); qproperty-iconSize: 110px 35px; }' %icon_name)

class CollapsIcon(QtWidgets.QPushButton):
    def __init__(self, label_text, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)

        self.setDefault(True)
        self.setCheckable(True)
        self.setText(label_text)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setIconSize(QtCore.QSize(int(50), int(12)))
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'arrow_open.png'))
        # self.setStyleSheet('QPushButton { background-color:transparent; border-style:outset; text-align:left; font-weight: semi-bold; color: white; font: 11pt; font-family: %s }'
        #                    %(UI_FONT_FAMILTY)
        #                    )
        self.setStyleSheet('QPushButton { background-color:transparent; border:none; padding-left:1px; padding-top:10px; text-align:left; font-weight: semi-bold; color: white; font: 11pt; font-family: %s }'
                           %(UI_FONT_FAMILTY)
                           )

        self.setFixedSize(self.sizeHint())
        self.toggled.connect(self.setStateChanged)
        # self.setContentsMargins(10, 10, 10, 10)

    @QtCore.Slot(bool)
    def setStateChanged(self, state):
        if self.isChecked():
            self.setChecked(True)
            self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'arrow_open.png'))
        else:
            self.setChecked(False)
            self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'arrow_close.png'))

        self.update()

class Label(QtWidgets.QLabel):
    def __init__(self, label_text, label_width, font_color, font_weight, font_size, font_alignment, parent=None, text_wrap=False):
        QtWidgets.QLabel.__init__(self,parent)

        self.setText(label_text)
        if not label_width == 0:
            self.setFixedWidth(label_width)

        if font_alignment == 'AlignTop':
            self.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)
        elif font_alignment == 'AlignCenter':
            self.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignLeft)
        else:
            self.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeft)

        if font_weight == 'bold':
            self.setStyleSheet('QLabel { color: %s; font: %spt; font-weight: bold; font-family: %s }' %(font_color, font_size, UI_FONT_FAMILTY))
        elif font_weight == 'semi-bold':
            self.setStyleSheet('QLabel { color: %s; font: %spt; font-weight: semi-bold; font-family: %s }' %(font_color, font_size, UI_FONT_FAMILTY))
        else:
            self.setStyleSheet('QLabel { color: %s; font: %spt; font-family: %s }' %(font_color, font_size, UI_FONT_FAMILTY))

class PushButton(QtWidgets.QPushButton):
    def __init__(self, icon_name, icon_text, icon_width, icon_height, parent=None):
        QtWidgets.QPushButton.__init__(self,parent)

        self.icon_name = icon_name
        self.setText(icon_text)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setIconSize(QtCore.QSize(int(icon_width),int(icon_height)))
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'{0}.png'.format(self.icon_name)))
        self.setStyleSheet('QPushButton {background-color : transparent; border-style : outset; font-weight: semi-bold; color: white; font: 10pt; font-family: %s }' % UI_FONT_FAMILTY)

    def enterEvent(self, event):
        if os.path.isfile(UI_ICON_PATH+'{0}_hover.png'.format(self.icon_name)):
            self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'/'+'{0}_hover.png'.format(self.icon_name)))

    def leaveEvent(self, event):
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'{0}.png'.format(self.icon_name)))

class ExecuteIcon(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)

        self.setFixedSize(80,30)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('QPushButton { background-color:rgb(80,80,80); color:rgb(200,200,200); border:1.5px solid rgb(60,60,60); border-radius: 4px; font : 9pt; font-family : %s }' % UI_FONT_FAMILTY)

class CheckBox(QtWidgets.QCheckBox):
    clicked = QtCore.Signal(bool)
    def __init__(self, text, parent=None):
        QtWidgets.QCheckBox.__init__(self, parent)

        self.setText(text)
        # self.setChecked(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('QCheckBox { spacing: 5px; color :rgb(220,220,220); font:11pt; font-weight: semi-bold; font-family : %s }'
                            'QCheckBox:Indicator { width: 16px; height: 16px }'
                            'QCheckBox:Indicator:checked { image: url(%s); }'
                            'QCheckBox:Indicator:unchecked { image: url(%s); }'
                            %(UI_FONT_FAMILTY, UI_ICON_PATH+'checked.png', UI_ICON_PATH+'unchecked.png')
                           )

    def mousePressEvent(self, event):
        if self.isChecked():
            self.clicked.emit(True)

        else:
            self.clicked.emit(False)

        super(CheckBox, self).mousePressEvent(event)

class Slider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        QtWidgets.QSlider.__init__(self)

        self.setRange(30, 100)
        self.setPageStep(1)
        self.setSingleStep(1)
        self.setTickInterval(1)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setStyleSheet('QSlider { border-radius:12px; }'
                           'QSlider:groove:horizontal { background:rgb(75,75,75); height:6px }'
                           'QSlider:handle:horizontal { background:%s; width:18px; margin-top:-4px; margin-bottom:-4px; border-radius:6px; }'
                           % UI_HIGHLIGHT_COLOR
                          )

class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)

        self.set_ui_properties()
        self.set_ui_layout()

    def set_ui_properties(self):
        self.setFixedHeight(26)
        self.setFixedSize(250, 26)
        self.setStyleSheet('QLineEdit { background-color:rgb(80,80,80); border:none; border-radius:8; color:rgb(180,180,180); font:11pt; padding:2px 25px 2px 25px; font-family:%s }' % UI_FONT_FAMILTY)
        self.setPlaceholderText('Search Application...')

    def set_ui_layout(self):
        self.search_icon = LineEditToolButton('search')
        self.clear_icon = LineEditToolButton('clear_search')
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.search_icon, 0, Qt.AlignLeft)
        layout.addWidget(self.clear_icon, 0, Qt.AlignRight)
        layout.setSpacing(0)
        layout.setMargin(5)

class LineEditToolButton(QtWidgets.QToolButton):
    clicked = QtCore.Signal(str)
    def __init__(self, icon_name, parent=None):
        QtWidgets.QToolButton.__init__(self)

        self.icon_name = icon_name
        self.set_ui_properties()

    def set_ui_properties(self):
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setIcon(QtGui.QIcon(UI_ICON_PATH+'{}.png'.format(self.icon_name)))
        self.setStyleSheet('background:transparent; border:none;')

    def enterEvent(self, event):
        if os.path.isfile(UI_ICON_PATH+'{0}_hover.png'.format(self.icon_name)):
            self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'/'+'{0}_hover.png'.format(self.icon_name)))

    def leaveEvent(self, event):
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'{0}.png'.format(self.icon_name)))

    def mousePressEvent(self, event):
        self.clicked.emit(self.icon_name)
        super(LineEditToolButton, self).mousePressEvent(event)

class SettingToolButton(QtWidgets.QToolButton):
    def __init__(self, parent=None):
        super(SettingToolButton, self).__init__(parent)

        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setIconSize(QtCore.QSize(int(25), int(25)))
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'option_menu.png'))

        self.setStyleSheet('QToolButton { background-color:transparent; border:none; }'
                            'QToolButton:menu-button { background-color:none; top: 2px; width: 0px; height: 0px; border:none; border-radius: 6px }'
                            'QToolButton:menu-arrow { arrow-color:none; width: 0px; height: 0px; left: 0px; top: 1px }'
                           )

    def enterEvent(self, event):
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'option_menu_hover.png'))

    def leaveEvent(self, event):
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'option_menu.png'))

class CloseToolButton(QtWidgets.QToolButton):
    def __init__(self, parent=None):
        super(CloseToolButton, self).__init__(parent)

        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setIconSize(QtCore.QSize(int(20), int(20)))
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'close_setting.png'))

        self.setStyleSheet('QToolButton { background-color:transparent; border:none; }'
                            'QToolButton:menu-button { background-color:none; top: 2px; width: 0px; height: 0px; border:none; border-radius: 6px }'
                            'QToolButton:menu-arrow { arrow-color:none; width: 0px; height: 0px; left: 0px; top: 12px }'
                           )

    def enterEvent(self, event):
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'close_setting_hover.png'))

    def leaveEvent(self, event):
        self.setIcon(QtGui.QPixmap(UI_ICON_PATH+'close_setting.png'))

class ProfileThumbnailLabel(QtWidgets.QLabel):
    def __init__(self):
        super(ProfileThumbnailLabel, self).__init__()

        self.setFixedSize(28, 28)
        self.setFocusPolicy(Qt.NoFocus)
        self.setPixmap(UI_ICON_PATH+'unknown_user.png')

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        scaled_pix = self.pixmap().scaled(self.size().width(), self.size().height(), Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
        point = QtCore.QPoint(0, 0)
        point.setX((self.size().width()-scaled_pix.width())/2)
        point.setY((self.size().height()-scaled_pix.height())/2)
        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0,self.width(),self.height(), 24, 24)
        painter.setClipPath(path)
        painter.drawPixmap(point, scaled_pix)

class AppThumbnailIcon(QtWidgets.QPushButton):
    def __init__(self, icon_path, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)

        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setIconSize(QtCore.QSize(int(40), int(40)))
        self.setIcon(QtGui.QPixmap(icon_path))
        # self.setStyleSheet('QPushButton { background-color:transparent; border-style:outset; text-align:left; font-weight: semi-bold; color: white; font: 8pt; font-family: %s }'
        #                    %(UI_FONT_FAMILTY)
        #                    )
        self.setStyleSheet('QPushButton { background-color:transparent; border:none; font-weight: semi-bold; color: white; font: 8pt; font-family: %s }'
                           %(UI_FONT_FAMILTY)
                           )
        self.setFixedSize(self.sizeHint())

class ListItemWidget(QtWidgets.QWidget):
    signal = QtCore.Signal(dict)
    def __init__(self, app_name, app_version_name, app_version, app_icon_path, app_exe_path, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.app_name, self.app_version_name, self.app_version, self.icon_path, self.app_exe_path = app_name, app_version_name, app_version, app_icon_path, app_exe_path
        self.set_ui_layout()
        self.set_ui_properties()
        self.set_signal_slot()

    def set_ui_properties(self):
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

    def set_ui_layout(self):
        self.app_icon = AppThumbnailIcon(self.icon_path)
        self.app_name_label = Label(self.app_name, int(0), 'rgb(200,200,200)', 'semi-bold', int(9), 'AlignCenter')
        self.app_version_label = Label(self.app_version, int(0), 'rgb(200,200,200)', 'semi-bold', int(10), 'AlignCenter')

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.app_icon, alignment=Qt.AlignCenter)
        layout.addSpacerItem(QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        layout.addWidget(self.app_name_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.app_version_label, alignment=Qt.AlignCenter)
        layout.setContentsMargins(15, 8, 15, 8)
        layout.setSpacing(1)

        if not self.app_version:
            self.app_version_label.setVisible(False)

    def set_signal_slot(self):
        self.app_icon.mousePressEvent = self.mousePressEvent
        self.app_name_label.mousePressEvent = self.mousePressEvent
        self.app_version_label.mousePressEvent = self.mousePressEvent

    def mousePressEvent(self, event):
        self.signal.emit({'app_name':self.app_name, 'app_version_name':self.app_version_name, 'app_version':self.app_version, 'app_exe_path':self.app_exe_path})


class ListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None, square_icon=False):
        QtWidgets.QListWidget.__init__(self)

        self.setStyleSheet('QListWidget { background-color:transparent; border:none}'
                           'QScrollBar:vertical { border:none; width:10px; background: rgb(35, 35, 35); border-radius:5px;}'
                           'QScrollBar:handle:vertical {background: rgb(73, 73, 73); max-height: 8px; border-radius:5px }'
                           'QScrollBar:add-line:vertical {border:none; background: rgb(35, 35, 35); subcontrol-position: bottom;subcontrol-origin: margin;}'
                           'QScrollBar:sub-line:vertical {border:none; background: rgb(35, 35, 35); subcontrol-position: top;subcontrol-origin: margin;}'
                           'QScrollBar:up-arrow:vertical, QScrollBar:down-arrow:vertical {border:none; background: rgb(35, 35, 35); color: none}'
                           'QScrollBar:add-page:vertical, QScrollBar:sub-page:vertical {background: rgb(35, 35, 35);}'
                          )

        self.setMouseTracking(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setViewMode(QtWidgets.QListWidget.IconMode)
        self.setMovement(QtWidgets.QListWidget.Static)
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setDragEnabled(False)

        if square_icon:
            self.setGridSize(QtCore.QSize(90, 95))

        else:
            self.setGridSize(QtCore.QSize(115, 80))

        # self.setLayoutMode(QtWidgets.QListWidget.Batched)
        # self.setBatchSize(100)
        # self.setUniformItemSizes(True)
        # self.setIconSize(QtCore.QSize(80, 80))

    def addListItem(self, item_widget :ListItemWidget):
        if item_widget:
            self.list_item = QtWidgets.QListWidgetItem()
            self.list_item.setSizeHint(item_widget.sizeHint())
            self.addItem(self.list_item)
            self.setItemDelegate(ListItemDelegate(self))
            self.setItemWidget(self.list_item, item_widget)


class EmptyThumbnailLabel(QtWidgets.QLabel):
    def __init__(self):
        super(EmptyThumbnailLabel, self).__init__()

        self.pixmap = QtGui.QPixmap(UI_ICON_PATH+'no_items_found_text.png')
        self.setPixmap(self.pixmap)
        self.setFixedSize(self.size().width()/4, self.size().height()/4)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        scaled_pix = self.pixmap.scaled(self.size().width(), self.size().height() ,Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        point = QtCore.QPoint(0, 0)
        point.setX((self.size().width()-scaled_pix.width())/2)
        point.setY((self.size().height()-scaled_pix.height())/2)
        painter.drawPixmap(point, scaled_pix)

class ListItemDelegate(QtWidgets.QItemDelegate):
     def __init__(self, parent=None):
         QtWidgets.QItemDelegate.__init__(self, parent)

     def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtGui.QPen(Qt.NoPen))
        if option.state & QtWidgets.QStyle.State_MouseOver:
            painter.setBrush(QtGui.QBrush(QtGui.QColor(70, 170, 250, 150)))
            painter.drawRoundedRect(option.rect.x(), option.rect.y(),option.rect.width(), option.rect.height() - 3, 8, 8)

        painter.restore()

class WaitingSpinner(QtWidgets.QWidget):
    def __init__(self, parent=None, centerOnParent=True, disableParentWhenSpinning=False, modality=Qt.NonModal):
        super(WaitingSpinner, self ).__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        # WAS IN initialize()
        self._color = QtGui.QColor( QtGui.QColor( 250 , 150 , 10 ) )
        self._roundness = 20.0
        self._minimumTrailOpacity = 3.14159265358979323846
        self._trailFadePercentage = 80.0
        self._revolutionsPerSecond = 1.57079632679489661923
        self._numberOfLines = 10
        self._lineLength = 20
        self._lineWidth = 5
        self._innerRadius = 10
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QtCore.QTimer( self )
        self._timer.timeout.connect( self.rotate )
        self.updateSize()
        self.updateTimer()
        self.hide()
        # END initialize()

        self.setWindowModality( modality )
        self.setAttribute( Qt.WA_TranslucentBackground )

    def paintEvent( self, QPaintEvent ):
        self.updatePosition()
        painter = QtGui.QPainter( self )
        painter.fillRect( self.rect(), Qt.transparent )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen( Qt.NoPen )
        for i in range( 0, self._numberOfLines ):
            painter.save()
            painter.translate( self._innerRadius + self._lineLength, self._innerRadius + self._lineLength )
            rotateAngle = float( 360 * i ) / float( self._numberOfLines )
            painter.rotate( rotateAngle )
            painter.translate( self._innerRadius, 0 )
            distance = self.lineCountDistanceFromPrimary( i, self._currentCounter, self._numberOfLines )
            color = self.currentLineColor(distance, self._numberOfLines, self._trailFadePercentage, self._minimumTrailOpacity, self._color )
            painter.setBrush( color )
            painter.drawRoundedRect( QtCore.QRect( 0, -self._lineWidth / 2, self._lineLength, self._lineWidth ), self._roundness, self._roundness, Qt.RelativeSize )
            painter.restore()

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()
        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled( False )
        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop( self ):
        self._isSpinning = False
        self.hide()
        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled( True )
        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines( self, lines ):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength( self, length ):
        self._lineLength = length
        self.updateSize()

    def setLineWidth( self, width ):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius( self, radius ):
        self._innerRadius = radius
        self.updateSize()

    def color( self ):
        return self._color

    def roundness( self ):
        return self._roundness

    def minimumTrailOpacity( self ):
        return self._minimumTrailOpacity

    def trailFadePercentage( self ):
        return self._trailFadePercentage

    def revolutionsPersSecond( self ):
        return self._revolutionsPerSecond

    def numberOfLines( self ):
        return self._numberOfLines

    def lineLength( self ):
        return self._lineLength

    def lineWidth( self ):
        return self._lineWidth

    def innerRadius( self ):
        return self._innerRadius

    def isSpinning( self ):
        return self._isSpinning

    def setRoundness( self, roundness ):
        self._roundness = max( 0.0, min( 100.0, roundness ) )

    def setColor( self, color=Qt.black ):
        self._color = QtGui.QColor( color )

    def setRevolutionsPerSecond( self, revolutionsPerSecond ):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage( self, trail ):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity( self, minimumTrailOpacity ):
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate( self ):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize( self ):
        size = ( self._innerRadius + self._lineLength ) * 2
        self.setFixedSize( size, size )

    def updateTimer( self ):
        self._timer.setInterval( 1000 / ( self._numberOfLines * self._revolutionsPerSecond ) )

    def updatePosition( self ):
        if self.parentWidget() and self._centerOnParent:
            self.move( self.parentWidget().width() / 2 - self.width() / 2, self.parentWidget().height() / 2 - self.height() / 2 )

    def lineCountDistanceFromPrimary( self, current, primary, totalNrOfLines ):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor( self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, colorinput ):
        color = QtGui.QColor( colorinput )
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int( math.ceil( ( totalNrOfLines - 1 ) * trailFadePerc / 100.0 ) )
        if countDistance > distanceThreshold:
            color.setAlphaF( minAlphaF )
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float( distanceThreshold + 1 )
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min( 1.0, max( 0.0, resultAlpha ) )
            color.setAlphaF( resultAlpha )
        return color

if __name__ == '__main__' :
    pass