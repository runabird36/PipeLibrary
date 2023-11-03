

import PySide2.QtGui
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide2.QtGui import QResizeEvent


class ResizedTable(QTableWidget):
    def __init__(self, _parent :QWidget=None) -> None:
        super(ResizedTable, self).__init__(_parent)
        self.IS_INITIALIZED = False

    def resizeEvent(self, event: QResizeEvent) -> None:
        '''
            need to customized this function according to the number of columns, 
            not to use it as it is
            
            - principle : use the difference between old size() and new size()
        '''
        if self.IS_INITIALIZED == False:
            self.IS_INITIALIZED = True
            return
        
        old_w = event.oldSize().width()
        new_w = event.size().width()
        diff_width = new_w - old_w
        if diff_width % 2 != 0 and diff_width > 0:
            diff_width += 1
        elif diff_width % 2 != 0 and diff_width < 0:
            diff_width -= 1
        
        old_col_00_width = self.columnWidth(0)
        old_col_01_width = self.columnWidth(1)
        
        new_col_00_width = int(old_col_00_width + diff_width/2)
        new_col_01_width = int(old_col_01_width + diff_width/2)
        
        self.setColumnWidth(0, new_col_00_width)
        self.setColumnWidth(1, new_col_01_width)
        return super().resizeEvent(event)
        
        






if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication
    class TestWin(QWidget):
        def __init__(self, _parent :QWidget=None) -> None:
            super(TestWin, self).__init__(_parent)
            
            
            self.test_tw = ResizedTable(self)
            self.test_tw.setRowCount(2)
            self.test_tw.setColumnCount(2)
            self.test_tw.setColumnWidth(0, 190)
            self.test_tw.setColumnWidth(1, 190)
            for i in range(0, 4):
                item = QTableWidgetItem(str(i))
                _row = i / 2
                _col = i % 2
                self.test_tw.setItem(_row, _col, item)
            
            self.main_vl = QVBoxLayout()
            self.main_vl.addWidget(self.test_tw)
            self.setLayout(self.main_vl)
            self.resize(400, 300)
    app = QApplication(sys.argv)
    
    ui = TestWin()
    ui.show()
    
    app.exec_()