# from source.pipeQT import ...

_path = "/home/taiyeong.song/Desktop/pipeTemp"

import sys
sys.path.append(_path)


from PipeLibrary.source.pipeQT import GradientProgressbarDialog
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)

ui = GradientProgressbarDialog.ProgressDialog()
ui.show()
ui.update_progress(75)

app.exec_()