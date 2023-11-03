
from PySide2.QtWidgets import QMessageBox, QWidget
from typing import Union

def show_message_box(title :str, message :str, msg_type :QMessageBox.Icon, btn_list :Union[QMessageBox.StandardButton, None], _parent :QWidget=None) -> QMessageBox.StandardButton:
    msg_w = QMessageBox(_parent)
    msg_w.setIcon(msg_type)
    msg_w.setText(message)
    msg_w.setWindowTitle(title)
    msg_w.setStandardButtons(btn_list)
    
    result = msg_w.exec_()
    return result


if __name__ == "__main__":
    import sys
    
    from PySide2.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    res = show_message_box("test", "test", QMessageBox.Information, QMessageBox.StandardButton.Yes)
    app.exec_()