import sys
from PySide2.QtWidgets import (
                                QWidget, QLineEdit, QHBoxLayout, QVBoxLayout,
                                QListWidget, QListWidgetItem
                            )
from PySide2.QtGui import QCursor
from PySide2.QtCore import QObject, QEvent, Qt
import maya.cmds as cmds
from qt_material import apply_stylesheet

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass



class SelList(QListWidget):
    def __init__(self, _parent=None) -> None:
        super(SelList, self).__init__(_parent)
        self._idx = -1
    @property
    def IDX(self) -> int:
        return self._idx
    
    @IDX.setter
    def IDX(self, _idx :int) -> None:
        self._idx = _idx

    def add_item(self, l_name :str) -> None:
        sn_name = l_name.split("|")[-1]

        res_item = QListWidgetItem()
        res_item.setText(sn_name)
        res_item.setData(Qt.UserRole, l_name)
        self.addItem(res_item)
        
    def set_nextitem_selected(self) -> None:
        if (self.IDX + 1) >= self.count():
            self.IDX = -1
            self.clearSelection()
            return
        else:
            self.IDX += 1
        self.setItemSelected(self.item(self.IDX), True)

    def set_previousitem_selected(self) -> None:
        if (self.IDX) <= 0:
            # self.IDX = self.count() - 1
            self.IDX = -1
            self.clearSelection()
            return
        else:
            self.IDX -= 1
        self.setItemSelected(self.item(self.IDX), True)
    
    def get_selected_longname(self) -> str:
        selected_items = self.selectedItems()
        if selected_items:
            l_name = selected_items[0].data(Qt.UserRole)
            return l_name

    def is_item_selected(self) -> bool:
        if self.selectedItems() == []:
            return False
        else:
            return True
    
    def refresh_all(self) -> None:
        self.IDX = -1
        self.clear()
        


class SNview(QWidget):
    def __init__(self, _parent=None) -> None:
        super(SNview, self).__init__(_parent)

        self.WIN_WIDTH          = 260
        self.WIN_HEIGHT         = 25
        self.EDIT_MODE_HEIGHT   = 500
        

        self.setupUi()
        self.set_link()

    def setupUi(self) -> None:
        

        self.input_le = QLineEdit()
        self.input_le.setFixedHeight(self.WIN_HEIGHT)
        self.input_le.setPlaceholderText("Search node")

        self.input_hl = QHBoxLayout()
        self.input_hl.setContentsMargins(0,0,0,0)
        self.input_hl.addWidget(self.input_le)

        self.search_res_lw = SelList()
        self.search_res_lw.setVisible(False)

        self.main_vl = QVBoxLayout()
        self.main_vl.addLayout(self.input_hl)
        self.main_vl.addWidget(self.search_res_lw)
        self.main_vl.setContentsMargins(0,0,0,0)

        


        self.setLayout(self.main_vl)
        self.setFixedSize(self.WIN_WIDTH, self.WIN_HEIGHT)
        self.installEventFilter(self)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.input_le.setFocus()


        # qtRectangle = self.frameGeometry()
        # centerPoint = QDesktopWidget().availableGeometry().center()
        # qtRectangle.moveCenter(centerPoint)
        # self.move(qtRectangle.topLeft())
        
        self.move(QCursor.pos())
        apply_stylesheet(self, "dark_blue.xml")

        
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            pass
        elif event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()
            elif event.key() == Qt.Key_Down:
                self.search_res_lw.set_nextitem_selected()
            elif event.key() == Qt.Key_Up:
                self.search_res_lw.set_previousitem_selected()
            elif event.key() == Qt.Key_Return:
                self.set_targets()

        
        return super().eventFilter(watched, event)


    def set_link(self) -> None:
        self.input_le.textEdited.connect(self.search_res)

    def search_res(self, input_txt :str) -> None:
        if input_txt == "":
            self.switch_view("NONE")
        else:
            self.switch_view("EDIT")
        
        
        search_res = self.find_by_input(input_txt)

        if search_res == [] or search_res == None:
            return

        self.add_searchres(search_res)

    def find_by_input(self, input_txt :str) -> list:
        if "-t" in input_txt:
            tar_name = "*" + input_txt.split("-t ")[0] + "*"
            tar_type = input_txt.split("-t ")[1]
            search_res = cmds.ls(tar_name, l=True, typ=tar_type)
        else:
            tar_name = f"*{input_txt}*"
            search_res = cmds.ls(tar_name, l=True)
        return search_res
        
    def switch_view(self, flag :str) -> None:
        if flag == "EDIT":
            self.setFixedHeight(self.EDIT_MODE_HEIGHT)
            self.search_res_lw.setVisible(True)
            self.search_res_lw.setFixedHeight(self.EDIT_MODE_HEIGHT - self.WIN_HEIGHT)
        elif flag == "NONE":
            self.setFixedHeight(self.WIN_HEIGHT)
            self.search_res_lw.setVisible(False)
            self.search_res_lw.setFixedHeight(0)

    def add_searchres(self, search_res :list) -> None:
        self.search_res_lw.refresh_all()

        for tar in search_res:
            self.search_res_lw.add_item(tar)

    def set_targets(self) -> None:

        if self.search_res_lw.is_item_selected() == True:
            selected_item = self.search_res_lw.get_selected_longname()
            cmds.select(selected_item)
        else:
            input_text = self.input_le.text()
            search_res_all = self.find_by_input(input_text)
            cmds.select(search_res_all)

        self.close()


        