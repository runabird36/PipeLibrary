import sys, os
from PySide2.QtWidgets import QWidget, QVBoxLayout, QApplication, QSpacerItem, QSizePolicy
from PySide2.QtCore import Slot
from .Ui_library.app_custom_ui import ListWidget, ListItemWidget, Splitter, CollapsIcon
from qt_material import apply_stylesheet


class MainView(QWidget):
    def __init__(self, _parent :QWidget=None) -> None:
        super(MainView, self).__init__(_parent)
        
        self.setupUi()
        
    def setupUi(self) -> None:
        
        item01 = ListItemWidget("Maya", "Maya2023", "2023", "/home/taiyeong.song/Desktop/pipeTemp/PipeLibrary/resource/app_icons/Houdini_logo.png", "/opt/hfs19.5/bin/houdini")
        item01.signal.connect(self.app_thumbnail_clicked)
        self.icon_view_lw = ListWidget(square_icon=True)
        self.icon_view_lw.addListItem(item01)
        
        
        
        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.icon_view_lw)
        
        self.setLayout(self.main_vl)
        
        apply_stylesheet(self, "dark_blue.xml")
        
    @Slot(dict)
    def app_thumbnail_clicked(self, app_data):
        try:
            print(app_data['app_name'], app_data['app_exe_path'])
            os.system(app_data['app_exe_path'])
            # before_app_launch.BeforeAppLaunch().execute(app_data['app_name'], app_data['app_version_name'], app_data['app_version'], app_data['app_exe_path'])
            # app_launch.AppLaunch().execute(app_data['app_name'], app_data['app_exe_path'])

        except Exception:
            pass
            # log_file_path  = APP_LOG_PATH+'/'+'{0}.log'.format(self.app_initialize_data.get_user_name.replace('.', '_'))
            # log_error_text = traceback.format_exc()            
            # utils_toolkit.write_app_logs(log_file_path, log_error_text)
            
            # app_msg_dialog.MessageDialog(u'앱실행중 에러가 발생하였습니다.', parent=QtWidgets.QApplication.activeWindow()).exec_()

        
        
if __name__ == "__main__":
    _app = QApplication(sys.argv)
    
    _ui = MainView()
    _ui.show()
    
    _app.exec_()