import sys, os
from PySide2.QtWidgets import QWidget, QVBoxLayout, QApplication, QSpacerItem, QSizePolicy, QHBoxLayout
from PySide2.QtCore import Slot
from .Ui_library.app_custom_ui import ListWidget, ListItemWidget, Splitter, CollapsIcon, BannerIcon, Label
from qt_material import apply_stylesheet
class BannersWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        banner_icon = BannerIcon('banner')
        self.profiles = Label('', int(0), 'rgb(250,250,250)', 'semi-bold', int(11), 'AlignCenter')

        layout = QHBoxLayout(self)
        layout.addWidget(banner_icon)
        layout.addStretch()
        layout.addWidget(self.profiles)
        layout.setContentsMargins(8, 5, 8, 5)

class SubView(QWidget):
    def __init__(self, _parent :QWidget=None) -> None:
        super(SubView, self).__init__(_parent)
        self.collaps_icon = CollapsIcon('OTHER TOOLS')
        
        item01 = ListItemWidget("Maya", "Maya2023", "2023", "/home/taiyeong.song/Desktop/pipeTemp/PipeLibrary/resource/app_icons/Houdini_logo.png", "/opt/hfs19.5/bin/houdini")
        item01.signal.connect(self.app_thumbnail_clicked)
        self.icon_view_lw = ListWidget(square_icon=True)
        self.icon_view_lw.addListItem(item01)
        
        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.collaps_icon, 1)
        self.main_vl.addStretch()
        self.main_vl.addSpacerItem(QSpacerItem(0, 2, QSizePolicy.Fixed, QSizePolicy.Fixed))        
        self.main_vl.addWidget(self.icon_view_lw, 10)
        self.main_vl.setContentsMargins(10, 0, 10, 0)
        self.setLayout(self.main_vl)
    
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

    def get_collpase_btn(self) -> CollapsIcon:
        return self.collaps_icon
        
class MainView(QWidget):
    def __init__(self, _parent :QWidget=None) -> None:
        super(MainView, self).__init__(_parent)
        
        self.setupUi()
        
    def setupUi(self) -> None:
        self.banners_widget = BannersWidget()
        self.tool_view = SubView()
        self.tool_view.get_collpase_btn().toggled.connect(self.collapse_status_changed)
        self.tool_view02 = SubView()
        self.tool_view02.get_collpase_btn().toggled.connect(self.collapse_status_changed)
        
        
        
        
        self.spliter01 = Splitter()
        self.spliter01.addWidget(self.tool_view)
        self.spliter01.addWidget(self.tool_view02)
        
        self.main_vl = QVBoxLayout()
        
        self.main_vl.addWidget(self.banners_widget)
        self.main_vl.addWidget(self.spliter01)
        
        self.setLayout(self.main_vl)
        
        apply_stylesheet(self, "dark_blue.xml")
        
    
    def collapse_status_changed(self, connect_signal):
        '''
        [ How to use ! ]
        - When toggle button, get all widgets and set widgets unvisible
        
        
            if connect_signal == 'upload_tools_icon_clicked':
                app_collaps_icon   = self.main_window.apps_tab.apps_widget.upload_tools_widget.collaps_icon
                app_list_widget    = self.main_window.apps_tab.apps_widget.upload_tools_widget.list_widget
                app_widget_items   = self.get_application_item_list['upload_tool_items']
                app_splitter_index = 1

            elif connect_signal == 'other_tools_icon_clicked':
                app_collaps_icon   = self.main_window.apps_tab.apps_widget.other_tools_widget.collaps_icon
                app_list_widget    = self.main_window.apps_tab.apps_widget.other_tools_widget.list_widget
                app_widget_items   = self.get_application_item_list['other_tool_items']
                app_splitter_index = 2            

            else:
                app_collaps_icon   = self.main_window.apps_tab.apps_widget.creative_tools_widget.collaps_icon
                app_list_widget    = self.main_window.apps_tab.apps_widget.creative_tools_widget.list_widget
                app_widget_items   = self.get_application_item_list['creative_tool_items']
                app_splitter_index = False

            if not app_widget_items:
                app_collaps_icon.setStateChanged(False)
                return

            if app_collaps_icon.isChecked():
                app_list_widget.setVisible(True)
                app_collaps_icon.setStateChanged(True)

                if app_splitter_index:
                    self.main_window.widget_splitter.handle(app_splitter_index).setEnabled(True)

            else:
                app_list_widget.setVisible(False)
                app_collaps_icon.setStateChanged(False)

                if app_splitter_index:
                    collaps_icon_posistion = app_collaps_icon.pos().y()
                    self.main_window.widget_splitter.moveSplitter(collaps_icon_posistion+10, app_splitter_index)
                    self.main_window.widget_splitter.handle(app_splitter_index).setEnabled(False)

            self.main_window.update()
        '''
        pass
    
if __name__ == "__main__":
    _app = QApplication(sys.argv)
    
    _ui = MainView()
    _ui.show()
    
    _app.exec_()