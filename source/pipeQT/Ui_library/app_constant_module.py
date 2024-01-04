import os, sys

APP_NAME                = 'Application Launcher'

APP_WINDOW_ICON         = 'window_icon.png'

APP_CACHE_PATH          = (os.path.dirname(os.path.abspath(__file__))).split("/source/")[0] + "/resource"
print(APP_CACHE_PATH)

APP_LOG_PATH            = APP_CACHE_PATH+'/'+'app_logs'

APP_CONFIG_PATH         = APP_CACHE_PATH+'/'+'app_configs'

APP_ICON_PATH           = APP_CACHE_PATH+'/'+'app_icons'

UI_ICON_PATH            = APP_CACHE_PATH+'/'+'ui_icons/'

UI_FONT_FAMILTY         = 'DejaVu Sans'

UI_HIGHLIGHT_COLOR      = 'rgb(80, 175, 250)'

OS_YAML_TEMPLATE        = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates').replace('\\', '/')+'/'+'os_path_template.yml'

APP_YAML_TEMPLATE       = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates').replace('\\', '/')+'/'+'app_path_template.yml'

UPLOAD_TOOLS            = ['Milki', "Nebula", 'AssetLibrary', 'ScanManager', 'SgMovUp']

OTHER_TOOLS             = ['Deadline', 'RV', 'FolderMaker', 'TXConverter', 'YetiFurBakery', 'SgMovDown', 'GiantWeaver', 'KeyRmv', 'RefRep', 'PathRebuild']

CREATIVE_TOOLS          = ['Blender', 'Nuke', 'NukeX', 'NukeS', 'Hiero', 'Maya', 'Houdini', 'Clarisse', 'Mari', '3DE', 'PTGui', 'Mocha', 'Tree']

DEFAULT_TOOLS           = {
                           'CMP'    : ['Milki', 'Nebula', 'RV', 'Deadline', 'AssetLibrary', 'Nuke', 'NukeX', 'NukeS', 'Hiero', 'Mocha', 'Blender', 'SgMovDown'],
                           'LGT'    : ['Milki', 'Nebula', 'RV', 'Deadline', 'AssetLibrary', 'YetiFurBakery', 'Nuke', 'Maya', 'Clarisse', 'Mari', 'PTGui', 'TXConverter', 'SgMovDown', 'GiantWeaver'],
                           'FX'     : ['Milki', 'Nebula', 'RV', 'Deadline', 'AssetLibrary', 'Nuke', 'Houdini', 'Clarisse', 'SgMovDown', 'GiantWeaver'],
                           'MDL'    : ['Milki', 'Nebula', 'RV', 'Deadline', 'AssetLibrary', 'Nuke', 'Maya', 'Clarisse', 'TXConverter', 'GiantWeaver', 'SgMovDown', 'Tree', 'PathRebuild'],
                           'LDV'    : ['Milki', 'Nebula', 'RV', 'Deadline', 'AssetLibrary', 'Nuke', 'Maya', 'Clarisse', 'Mari', 'GiantWeaver', 'TXConverter', 'SgMovDown', 'PathRebuild'],
                           'ANI'    : ['Milki', 'Nebula', 'RV', 'Deadline', 'AssetLibrary', 'YetiFurBakery', 'Maya', 'SgMovDown', 'GiantWeaver', 'KeyRmv', 'RefRep'],
                           'MMV'    : ['Milki', 'Nebula', 'RV', 'Deadline', 'AssetLibrary', 'Maya', '3DE', 'SgMovDown', 'GiantWeaver', 'KeyRmv'],
                           'PD'     : ['Milki', 'Nebula', 'RV', 'Deadline', 'AssetLibrary', 'Nuke', 'Hiero', 'FolderMaker', 'Blender', 'ScanManager', 'SgMovDown', 'SgMovUp', 'PathRebuild'],
                           }

if __name__ == '__main__' :
    print (DEFAULT_TOOLS)
