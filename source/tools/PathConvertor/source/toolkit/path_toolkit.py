
import sys
import clipboard
def is_windows(platform=None):
    """
    Determine if the current platform is Windows.

    :param platform: sys.platform style string, e.g 'linux2', 'win32' or
                     'darwin'.  If not provided, sys.platform will be used.

    :returns: True if the current platform is Windows, otherwise False.
    :rtype: bool
    """
    if platform:
        return platform == "win32"
    return sys.platform == "win32"

def is_linux(platform=None):
    """
    Determine if the current platform is Linux.

    :param platform: sys.platform style string, e.g 'linux2', 'win32' or
                     'darwin'.  If not provided, sys.platform will be used.

    :returns: True if the current platform is Linux, otherwise False.
    :rtype: bool
    """
    if platform:
        return platform.startswith("linux")
    return sys.platform.startswith("linux")

def is_macos(platform=None):
    """
    Determine if the current platform is MacOS.

    :param platform: sys.platform style string, e.g 'linux2', 'win32' or
                     'darwin'.  If not provided, sys.platform will be used.

    :returns: True if the current platform is MacOS, otherwise False.
    :rtype: bool
    """
    if platform:
        return platform == "darwin"
    return sys.platform == "darwin"

def copy_to_clipboard(tar_path :str) -> None:
    clipboard.copy(tar_path)


class PathConvertor():
    win_x           = "\\\\vfx.gtserver04.net\\gstepvfx\\projects"
    win_z           = "\\\\vfx.gtserver04.net\\usersetup"
    win_asset       = "\\\\vfx.gtserver04.net\\gstepasset"
    win_x_alphabet  = "X:\\projects"
    win_z_alphabet  = "Z:\\"
    lnx_x           = "/projects"
    lnx_z           = "/usersetup"
    lnx_asset       = "/gstepasset"
    def do_convert(self, from_path :str) -> str:
        raise NotImplementedError
    
class WinPathConvertor(PathConvertor):
    def do_convert(self, from_path: str) -> str:
        if from_path.startswith(self.lnx_x):
            win_path = from_path.replace(self.lnx_x, self.win_x)
            win_path = win_path.replace("/", "\\")
            return win_path
        elif from_path.startswith(self.lnx_z):
            win_path = from_path.replace(self.lnx_z, self.win_z)
            win_path = win_path.replace("/", "\\")
            return win_path
        elif from_path.startswith(self.lnx_asset):
            win_path = from_path.replace(self.lnx_asset, self.win_asset)
            win_path = win_path.replace("/", "\\")
            return win_path
        else:
            return from_path.replace("/", "\\")
        
class LnxPathConvertor(PathConvertor):
    def do_convert(self, from_path: str) -> str:
        if from_path.startswith(self.win_x):
            lnx_path = from_path.replace(self.win_x, self.lnx_x)
            lnx_path = lnx_path.replace("\\", "/")
            return lnx_path
        elif from_path.startswith(self.win_z):
            lnx_path = from_path.replace(self.win_z, self.lnx_z)
            lnx_path = lnx_path.replace("\\", "/")
            return lnx_path
        elif from_path.startswith(self.win_x_alphabet):
            lnx_path = from_path.replace(self.win_x_alphabet, self.lnx_x)
            lnx_path = lnx_path.replace("\\", "/")
            return lnx_path
        elif from_path.startswith(self.win_z_alphabet):
            lnx_path = from_path.replace(self.win_z_alphabet, self.lnx_z)
            lnx_path = lnx_path.replace("\\", "/")
            return lnx_path
        elif from_path.startswith(self.win_asset):
            lnx_path = from_path.replace(self.win_asset, self.lnx_asset)
            lnx_path = lnx_path.replace("\\", "/")
            return lnx_path
        else:
            return from_path.replace("\\", "/")
        

if __name__ == "__main__":
    win_f_path = "\\\\vfx.gtserver04.net\\gstepvfx\\projects\\2023_08_theLastTicket"
    win_f_path = "X:\\projects\\2023_08_theLastTicket"
    lnx_f_path = "/projects/2023_08_theLastTicket"
    convertor = LnxPathConvertor()
    res = convertor.do_convert(win_f_path)
    print(res)
    convertor = WinPathConvertor()
    res = convertor.do_convert(lnx_f_path)
    print(res)
