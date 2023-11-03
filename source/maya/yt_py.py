

import maya.mel as mel
import maya.cmds as cmds
import os

_main_path = os.path.dirname(os.path.abspath(__file__))
_main_path = _main_path.replace("\\", "/")
_mel_path = _main_path + '/yt_mel.mel'

mel.eval('source "{0}"'.format(_mel_path))



# def listAttr(tar_yeti_node, tar_node):
#     return mel.eval('listAttr(\"{0}\", \"{1}\");'.format(tar_yeti_node, tar_node))



def update_set_name(y_node, from_set, to_set):

    mel.eval('updateSetName(\"{0}\", \"{1}\", \"{2}\")'.format(
                                                            y_node,
                                                            from_set,
                                                            to_set))


def create_yeti_node(node_name):
    return mel.eval('create_yeti_without_addmesh_v02(\"{0}\")'.format(node_name))



def add_basemesh_to_yeti(tar_yeti_node, tar_basemesh):
    mel.eval('pgYetiAddGeometry( \"{0}\", \"{1}\" );'.format(tar_basemesh,
                                                            tar_yeti_node))



def add_set_to_yeti(tar_yeti_node, tar_setname):
    mel.eval("pgYetiAddGuideSet(\"{0}\", \"{1}\")".format(tar_setname, tar_yeti_node))




def import_groom_from_yeti(tar_grm, tar_basemesh, tar_yeti):
    return mel.eval("import_groomFile_from_yNode_v03(\"{0}\", \"{1}\", \"{2}\")".format(tar_grm,
                                                                                        tar_basemesh,
                                                                                        tar_yeti))
def get_info_from_yeti( yeti_node :str, info_type :str="all") -> list:
    '''
    - info_type : str
        mesh / pgYetiGroom / objectSet
    '''
    if info_type == "all":
        return cmds.listConnections(yeti_node, d=False, s=True, sh=True)
    else:
        return cmds.listConnections(yeti_node, d=False, s=True, sh=True, type=info_type)



def to_long_name(func):
    def is_longname(cur_name):
        if "|" in cur_name:
            return True
        else:
            return False
    def decorated(*args, **kwargs):
        y_node_name = kwargs["yeti_name"]
        if is_longname(y_node_name) == False:
            res = cmds.ls(y_node_name, l=True)
            y_node_name = res[0]
        kwargs["yeti_name"] = y_node_name
        print("Target Node : ", y_node_name)
        res = func(**kwargs)
        return res
    return decorated

@to_long_name
def get_yeti_imageSearchPath(yeti_name :str) -> str:
    attr_name = yeti_name + "." + "imageSearchPath"
    return cmds.getAttr(attr_name)
    

@to_long_name
def set_yeti_imageSearchPath(yeti_name :str, isp_path :str) -> str:
    if isp_path == None:
        return
    attr_name = yeti_name + "." + "imageSearchPath"
    cmds.setAttr(attr_name, isp_path, type="string")
    

@to_long_name
def get_yeti_cachepath(yeti_name :str) -> str:
    attr_name = yeti_name + "." + "cacheFileName"
    return cmds.getAttr(attr_name)
    

@to_long_name
def set_yeti_cachepath(yeti_name :str, cache_path :str) -> str:
    attr_name = yeti_name + "." + "cacheFileName"
    cmds.setAttr(attr_name, cache_path, type="string")
    
