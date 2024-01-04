# :coding: utf-8
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(__file__,'..'))).replace('\\', '/'))
from app_path_module import *
from app_constant_module import *
from view import app_custom_ui
from toolkit import utils_toolkit

class AppMainUI(QtWidgets.QMainWindow):
    def __init__(self, app_name, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.app_name = app_name
        self.set_ui_properties()
        self.set_ui_layout()
        self.set_ui_default()

    def set_ui_position(self):
        center = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        frame_gm = self.frameGeometry()
        frame_gm.moveCenter(center)
        self.move(frame_gm.topLeft())

    def set_ui_properties(self):
        self.setWindowOpacity(0.98)
        # self.setFixedSize(500, 750)
        self.setFixedWidth(500)
        self.setMinimumHeight(750)
        self.setWindowTitle(self.app_name)
        self.setWindowIcon(QtGui.QIcon(UI_ICON_PATH+APP_WINDOW_ICON))
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint|QtCore.Qt.WindowMinimizeButtonHint)
        self.set_ui_position()

    def set_ui_layout(self):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        self.apps_tab = TabMainWidget()
        apps_group = app_custom_ui.FrameBox('rgb(50, 50, 50)')
        apps_layout = QtWidgets.QVBoxLayout()
        apps_layout.addWidget(self.apps_tab)
        apps_layout.setContentsMargins(0, 4, 0, 0)
        apps_group.setLayout(apps_layout)

        self.banners_widget = BannersWidget()
        banners_group = app_custom_ui.FrameBox('rgb(50, 50, 50)')
        banners_layout = QtWidgets.QHBoxLayout()
        banners_layout.addWidget(self.banners_widget)
        banners_layout.setContentsMargins(0, 0, 0, 0)
        banners_group.setLayout(banners_layout)

        layout = QtWidgets.QVBoxLayout(main_widget)
        layout.addWidget(apps_group, 25)
        layout.addWidget(banners_group, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def set_ui_default(self):
        self.apps_tab.apps_widget.upload_tools_widget.collaps_icon.setStateChanged(False)
        self.apps_tab.apps_widget.upload_tools_widget.list_widget.setVisible(False)
        self.apps_tab.apps_widget.upload_tools_widget.list_widget.setMinimumHeight(1)

        self.apps_tab.apps_widget.other_tools_widget.collaps_icon.setStateChanged(False)
        self.apps_tab.apps_widget.other_tools_widget.list_widget.setVisible(False)
        self.apps_tab.apps_widget.other_tools_widget.list_widget.setMinimumHeight(1)

        self.apps_tab.apps_widget.creative_tools_widget.collaps_icon.setStateChanged(False)
        self.apps_tab.apps_widget.creative_tools_widget.list_widget.setVisible(False)
        self.apps_tab.apps_widget.creative_tools_widget.list_widget.setMinimumHeight(1)

        self.widget_splitter = self.apps_tab.apps_widget.widget_splitter
        self.widget_splitter.setSizes([10, 10, 1500])

        self.apps_tab.preferences_widget.default_app_checkbox.setChecked(True)
        self.apps_tab.preferences_widget.latest_app_checkbox.setChecked(True)
        self.apps_tab.preferences_widget.opacitiy_app_slider.setValue(100)

        self.waiting_spinner = app_custom_ui.WaitingSpinner(self, True, True, Qt.ApplicationModal)
        self.waiting_spinner.hide()        

    def closeEvent(self, event):
        app_configs_data = utils_toolkit.AppConfigsData()
        app_configs_data.set_app_configs('app_window_size', self.size())
        app_configs_data.set_app_configs('app_window_opacity', self.windowOpacity())
        app_configs_data.set_app_configs('app_splitter_sizes', self.apps_tab.apps_widget.widget_splitter.saveState())

class BannersWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        banner_icon = app_custom_ui.BannerIcon('banner')
        self.profiles = app_custom_ui.Label('', int(0), 'rgb(250,250,250)', 'semi-bold', int(11), 'AlignCenter')

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(banner_icon)
        layout.addStretch()
        layout.addWidget(self.profiles)
        layout.setContentsMargins(8, 5, 8, 5)

class TabMainWidget(QtWidgets.QTabWidget):
    def __init__(self,parent=None):
        QtWidgets.QTabWidget.__init__(self)

        self.set_ui_properties()
        self.set_ui_layout()

    def set_ui_properties(self):
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet('QTabWidget { background:transparent; font:13pt; color:white; font-weight:semi-bold; font-family:%s; }'
                           'QTabWidget:pane { background:rgb(35,35,35); border:none; padding: 0px 0px 0px 0px }'
                           'QTabWidget:tab-bar:top { top:3px; }'
                           'QTabWidget:tab-bar:bottom { bottom:3px }'
                           'QTabBar:tab { border:none }'
                           'QTabBar:tab:selected { color:white; border-bottom:2px solid %s; }'
                           'QTabBar:tab:!selected { color:white; border-bottom:2px solid transparent; }'
                           'QTabBar:tab:tab-bar { margin-left:10px; margin-top:12px; margin-bottom:2px; padding: 1px 1px 5px 1px; }'
                           'QTabWidget:right-corner { background-color:none; bottom: 6px;}'
                           %(UI_FONT_FAMILTY, UI_HIGHLIGHT_COLOR)
                          )

    def set_ui_layout(self):
        self.apps_widget        = AppsWidget()
        self.preferences_widget = PreferencesWidget()
        self.addTab(self.apps_widget, '  Apps  ')
        self.addTab(self.preferences_widget, '  Preferences  ')
        self.setTabVisible(1, False)

        self.app_setting_icon = app_custom_ui.SettingToolButton()
        self.setCornerWidget(self.app_setting_icon)

class AppsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.app_search_edit = app_custom_ui.LineEdit()
        app_search_layout = QtWidgets.QHBoxLayout()
        app_search_layout.addStretch()
        app_search_layout.addWidget(self.app_search_edit)
        app_search_layout.setContentsMargins(10, 10, 8, 0)

        app_devider_frame = app_custom_ui.Frame('rgb(60,60,60)', 1)
        app_devider_layout = QtWidgets.QHBoxLayout()
        app_devider_layout.addWidget(app_devider_frame)
        app_devider_layout.setContentsMargins(4, 2, 4, 0)

        self.upload_tools_widget = ToolsWidget('upload_tools')
        self.other_tools_widget = ToolsWidget('other_tools')
        self.creative_tools_widget = ToolsWidget('creative_tools')
        self.widget_splitter = app_custom_ui.Splitter()
        self.widget_splitter.addWidget(self.upload_tools_widget)
        self.widget_splitter.addWidget(self.other_tools_widget)
        self.widget_splitter.addWidget(self.creative_tools_widget)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(app_search_layout, 1)
        layout.addLayout(app_devider_layout, 1)
        layout.addSpacerItem(QtWidgets.QSpacerItem(0, 3, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        layout.addWidget(self.widget_splitter)
        layout.setContentsMargins(0, 0, 0, 6)
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

class PreferencesWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.default_app_checkbox = app_custom_ui.CheckBox('Display department apps only')
        self.latest_app_checkbox = app_custom_ui.CheckBox('Display latest app version only')
        checkbox_layout = QtWidgets.QVBoxLayout()
        checkbox_layout.addWidget(self.default_app_checkbox)
        checkbox_layout.addWidget(self.latest_app_checkbox)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)

        opacity_label = app_custom_ui.Label('Opacity', int(0), 'rgb(220,220,220)', 'semi-bold', int(11), 'AlignCenter')
        self.opacitiy_app_slider = app_custom_ui.Slider()
        opacity_layout = QtWidgets.QHBoxLayout()
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addSpacerItem(QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        opacity_layout.addWidget(self.opacitiy_app_slider)
        opacity_layout.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(checkbox_layout)
        layout.addLayout(opacity_layout)
        layout.addStretch()
        layout.setContentsMargins(8, 12, 8, 0)

class ToolsWidget(QtWidgets.QWidget):
    def __init__(self, widget_name, parent=None):
        QtWidgets.QWidget.__init__(self)

        if widget_name == 'upload_tools':
            self.collaps_icon = app_custom_ui.CollapsIcon('UPLOAD TOOLS')
            self.list_widget = app_custom_ui.ListWidget()
        
        elif widget_name == 'other_tools':
            self.collaps_icon = app_custom_ui.CollapsIcon('OTHER TOOLS')
            self.list_widget = app_custom_ui.ListWidget()

        else:
            self.collaps_icon = app_custom_ui.CollapsIcon('CREATIVE TOOLS')
            self.list_widget = app_custom_ui.ListWidget(square_icon=True)

        layout = QtWidgets.QVBoxLayout(self)
        if not widget_name == 'upload_tools':
            layout.addSpacerItem(QtWidgets.QSpacerItem(0, 6, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        layout.addWidget(self.collaps_icon, 1)
        layout.addStretch()
        layout.addSpacerItem(QtWidgets.QSpacerItem(0, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))        
        layout.addWidget(self.list_widget, 10)
        layout.setContentsMargins(10, 0, 10, 0)

if __name__ == '__main__' :
    from models import app_template_model

    app = QtWidgets.QApplication(sys.argv)
    main_window = AppMainUI(APP_NAME)
    main_window.show()
    main_window.raise_()

    # template_model = app_template_model.TemplateModel(APP_YAML_TEMPLATE)
    # for app_name in sorted(template_model.get_app_names):
    #     template_model.app_name_value = app_name
    #     app_path_list = template_model.get_installed_app_paths
    #     if app_path_list:
    #         for app_path in app_path_list:
    #             app_exe_path           = template_model.get_app_exe_path(app_path)
    #             if os.path.isfile(app_exe_path):
    #                 app_version        = template_model.get_app_versions(app_path)
    #                 app_icon_path      = template_model.get_app_icon_path(app_path)
    #                 app_version_name   = template_model.set_app_version_name(app_name, app_version)

    #                 item_widget = app_custom_ui.ListItemWidget(app_name, app_version_name, app_version, app_icon_path, app_exe_path)

    #                 if app_name in UPLOAD_TOOLS:
    #                     main_window.apps_tab.apps_widget.upload_tools_widget.list_widget.addListItem(item_widget)

    #                 elif app_name in OTHER_TOOLS:
    #                     main_window.apps_tab.apps_widget.other_tools_widget.list_widget.addListItem(item_widget)

    #                 else:
    #                     main_window.apps_tab.apps_widget.creative_tools_widget.list_widget.addListItem(item_widget)

    # splitter = main_window.apps_tab.apps_widget.widget_splitter
    # splitter.setSizes([10, 10, 1500])

    # main_window.apps_tab.apps_widget.upload_tools_widget.collaps_icon.setChecked(True)
    # main_window.apps_tab.apps_widget.upload_tools_widget.list_widget.setVisible(True)
    # main_window.apps_tab.apps_widget.other_tools_widget.collaps_icon.setChecked(True)
    # main_window.apps_tab.apps_widget.other_tools_widget.list_widget.setVisible(True)
    # main_window.apps_tab.apps_widget.creative_tools_widget.collaps_icon.setChecked(True)
    # main_window.apps_tab.apps_widget.creative_tools_widget.list_widget.setVisible(True)

    # upload_tool_items = [main_window.apps_tab.apps_widget.upload_tools_widget.list_widget.item(i) for i in range(main_window.apps_tab.apps_widget.upload_tools_widget.list_widget.count())]
    # # upload_tool_items = []    
    # main_window.apps_tab.apps_widget.upload_tools_widget.list_widget.setMinimumHeight(80)
    # if not upload_tool_items:
    #     splitter.handle(1).setEnabled(False)
    #     main_window.apps_tab.apps_widget.upload_tools_widget.list_widget.setMinimumHeight(1)    

    # other_tool_items = [main_window.apps_tab.apps_widget.other_tools_widget.list_widget.item(i) for i in range(main_window.apps_tab.apps_widget.other_tools_widget.list_widget.count())]
    # other_tool_items = []
    # main_window.apps_tab.apps_widget.other_tools_widget.list_widget.setMinimumHeight(1)    
    # if other_tool_items:
    #     main_window.apps_tab.apps_widget.other_tools_widget.list_widget.setMinimumHeight(80)

    # creative_tool_items = [main_window.apps_tab.apps_widget.creative_tools_widget.list_widget.item(i) for i in range(main_window.apps_tab.apps_widget.creative_tools_widget.list_widget.count())]
    # creative_tool_items = []
    # main_window.apps_tab.apps_widget.creative_tools_widget.list_widget.setMinimumHeight(1)    
    # if creative_tool_items:
    #     main_window.apps_tab.apps_widget.creative_tools_widget.list_widget.setMinimumHeight(95)



    sys.exit(app.exec_())


