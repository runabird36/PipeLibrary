

from subprocess import Popen, PIPE

class CmdOperator():
    def run_cmd(self, *argv) -> None:
        proc = Popen(*argv, stdout = PIPE)
        out, err = proc.communicate()
        
    def open_folder(self, _path :str) -> None:
        raise NotImplementedError
    
class WinCmdOperator(CmdOperator):
    def open_folder(self, _path :str) -> None:
        self.run_cmd(["explorer.exe", _path])

class LnxCmdOperator(CmdOperator):
    def open_folder(self, _path :str) -> None:
        self.run_cmd(["nautilus", _path])

        


if __name__ == "__main__":
    cmd_op = WinCmdOperator()
    cmd_op.run_cmd([1,2])