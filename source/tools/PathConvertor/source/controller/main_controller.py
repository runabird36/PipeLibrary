import sys
from ..toolkit.path_toolkit import is_windows, is_linux, copy_to_clipboard
from ..view.main_view import MainView
from os import path
class MainEngine():
    path_tool   = None
    cmd_tool    = None
    view        = None
    def __init__(self, view :MainView) -> None:
        self.view = view
        self.view.set_link(self)

        if is_windows() == True:
            from ..toolkit.path_toolkit import WinPathConvertor
            from ..toolkit.cmd_toolkit import WinCmdOperator
            self.path_tool = WinPathConvertor()
            self.cmd_tool  = WinCmdOperator()
        elif is_linux() == True:
            from ..toolkit.path_toolkit import LnxPathConvertor
            from ..toolkit.cmd_toolkit import LnxCmdOperator
            self.path_tool = LnxPathConvertor()
            self.cmd_tool  = LnxCmdOperator()
        else:
            return

    
    def convert_path(self) -> None:
        if self.path_tool == None:
            return
        
        from_path = self.view.get_from_path()
        to_path = self.path_tool.do_convert(from_path)
        self.view.set_to_path(to_path)
        

    def copy_to_clipboard(self) -> None:
        tar_path = self.view.get_to_path()
        copy_to_clipboard(tar_path)

    def open_dir(self) -> None:
        tar_path = self.view.get_to_path()
        if path.isdir(tar_path):
            tar_path = tar_path
        else:
            tar_path = path.dirname(tar_path)
        self.cmd_tool.open_folder(tar_path)
        
    def change_mode(self, status) -> None:
        cur_mode = self.view.get_cur_mode()
        if cur_mode.lower() == "win":
            from ..toolkit.path_toolkit import WinPathConvertor
            self.path_tool = WinPathConvertor()
        elif cur_mode.lower() == "linux":
            from ..toolkit.path_toolkit import LnxPathConvertor
            self.path_tool = LnxPathConvertor()

        self.view.switch_hint(cur_mode)

def main() -> None:
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    

    view    = MainView()
    engine  = MainEngine(view)
    view.show()


    app.exec_()


if __name__ == "__main__":
    main()

# /projects/2023_11_ces/assets/structure/wareHouse/modeling/mdl01/dev/scenes/maya/wareHouse_mdl01_v001_w04.mb
# X:\projects\2023_11_ces\assets\structure\wareHouse\modeling\mdl01\dev\scenes\maya\wareHouse_mdl01_v001_w04.mb
