import maya.cmds as cmds
from pxr import Usd
import mayaUsd
import os
import sys
import subprocess


def open_usdview():
    result = cmds.promptDialog(
                    title='USD view',
                    message='usd 파일 전체 경로를 입력해주십시오 :',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)



        mayaVer = 2023
        os.environ['MAYA_LOCATION'] = "/usr/autodesk/maya2023"
        os.environ['USD_LOCATION'] = "/usr/autodesk/mayausd/maya2023/0.20.0_202211021008-b68700b/mayausd/USD"
        target = text
        mayapyBinPath = os.path.join(os.environ['MAYA_LOCATION'], 'bin')
        if mayaVer == 2022:
            mayapyPath = os.path.join(mayapyBinPath, 'mayapy{ver}'.format(ver='' if sys.version_info.major == 3 else '2'))
        else:
            mayapyPath = os.path.join(mayapyBinPath, 'mayapy')  
        usdRootPath = os.environ['USD_LOCATION']
        
        # sanitise the path separators - slightly inefficient
        mayapyPath = mayapyPath.replace('\\', os.path.sep).replace('/', os.path.sep)
        usdRootPath = usdRootPath.replace('\\', os.path.sep).replace('/', os.path.sep)
        
        # finally build out the nice pathing
        usdToolsPath = os.path.join(usdRootPath, "bin")
        usdLibPath = os.path.join(usdRootPath, "lib")
        usdViewPath = os.path.join(usdToolsPath, 'usdview')
        
        # Install OpenGL module, if needed
        try:
            import OpenGL
        except:
            subprocess.check_call([mayapyPath, '-m', 'pip', 'install', 'PyOpenGL==3.1.0'])
        if sys.platform in ('win32'): 
            creationflags = 0x08000000 # CREATE_NO_WINDOW only for win32, not MacOS or Linux
        else:
            creationflags = 0
        
        print([mayapyPath, usdViewPath, target])
        print(f"{mayapyPath} {usdViewPath} {target}")
        subprocess.Popen([mayapyPath, usdViewPath, target], creationflags=creationflags)









def get_stage_from_path(_path :str) -> None:
    
    if os.path.exists(_path) == True:
        _stage = Usd.Stage.Open(_path)
        return _stage
    else:
        return None
    

def get_stage_from_selection() -> Usd.Stage:
    sel_res = cmds.ls(type="mayaUsdProxyShape", l=True)
    if sel_res:
        tar_stage = mayaUsd.ufe.getStage(sel_res[0])
        return tar_stage
    else:
        return None
    
    



def create_node(usd_path :str, name :str) -> str:
    usd_node = cmds.createNode("mayaUsdProxyShape", n=f"{name}Shape")
    transform_node = cmds.listRelatives(usd_node, p=True)[0]
    renamed_res = cmds.rename(transform_node, name)
    
    cmds.setAttr(f"{usd_node}.filePath", usd_path, type="string")
    
    return renamed_res



def get_path_from_stage(usd_proxy_node :str="") -> str:
    if usd_proxy_node == "":
        sel_res = cmds.ls(sl=True, ufe=True)
        if sel_res == []:
            return ""
        usd_proxy_node = sel_res[0]

    return cmds.getAttr(f"{usd_proxy_node}.filePath")




def is_with_namespace(_tar):
    if ':' in _tar:
        return True
    else:
        return False



def is_top_node(tar_node):
    element_list = tar_node.split('|')
    if len(element_list) == 2:
        return True
    else:
        return False




def get_targets(all_info_dict):
    all_tars = cmds.ls(sl=True, l=True)

    for _tar in all_tars:
        _each_asset_dict = {}
        _with_ns = False
        _is_top = False
        _parent_address = ''


        if is_with_namespace(_tar) == True:
            _with_ns = True
        else:
            _with_ns = False


        if is_top_node(_tar) == True:
            _is_top = True
        else:
            _is_top = False
            _temp = _tar.split('|')
            _temp.pop()
            _parent_address = '|'.join(_temp)

        all_info_dict[_tar] = {'IS_TOP':_is_top, 'PARENT_ADDRESS':_parent_address, 'NAMESPACE':_with_ns}

    return all_info_dict
















def get_all_shape_in_hierarchy(grp=None):
    if grp is None:
        grp = cmds.ls(sl=True)[0]

    return cmds.listRelatives(grp, ad=True, f=True, typ = 'shape')



def get_shading_engines(shape):
    # return cmds.listConnections (shape, source=False, destination=True)
    connected_list = cmds.listConnections (shape, source=False, destination=True)

    result_shading_engine_list = []
    if connected_list == None:
        return None
    else:
        for node in connected_list:
            node_type = cmds.nodeType(node)
            if node_type == 'shadingEngine':
                result_shading_engine_list.append(node)
        return result_shading_engine_list



def get_shading_groups_in_hierarchy(grp):
    shading_engine_list = []

    for shape in get_all_shape_in_hierarchy(grp):
        shading_engines = get_shading_engines(shape)
        if not shading_engines == None:
            check_engines_list = shading_engines
            while 'initialShadingGroup' in check_engines_list:
                shading_engines.remove('initialShadingGroup')
            if not shading_engines:
                continue
            else:
                for _shadinggroup in shading_engines:
                    if not _shadinggroup in shading_engine_list:
                        shading_engine_list.append(_shadinggroup)

            # print '{0} -----------------------> '.format(shape)
            # print shading_engines

    return shading_engine_list








def make_magic_path(f_path):
    _temp = f_path.split(':')[-1]
    if ':' in f_path:
        return '*:*{0}*'.format(_temp)
    else:
        return '*{0}*'.format(_temp)



def get_geom(sg):
    members = cmds.sets(sg, q=True)
    paths = []
    for member in members:
        _IS_ATTRIBUTE = False

        if '.f' in member:
            _IS_ATTRIBUTE = True
        else:
            _IS_ATTRIBUTE = False


        if _IS_ATTRIBUTE == False:
            # full_path = cmds.listRelatives(member, fullPath=True, allParents=True).pop()
            full_path = cmds.listRelatives(member, allParents=True, f=True).pop()
        else:
            full_path = cmds.ls(member, l=True).pop()
            # full_path = cmds.ls(member).pop()

        # print(full_path)
        # magic_path = make_magic_path(full_path)
        full_path = full_path.replace('|', '/')
        paths.append(full_path)

    return list(set(paths))






def get_mat(_sg):
    all_linked_node = cmds.listConnections(_sg, d=False, s=True)
    linked_mat = cmds.ls(all_linked_node, mat=True)

    if linked_mat is None or linked_mat == []:
        return ''
    return linked_mat[0]







def get_assigned_info():
    all_info_dict = {}
    all_info_dict = get_targets(all_info_dict)

    export_tar_sg_list = []
    for _tar, _tar_info_dict in all_info_dict.items():
        sg_list = get_shading_groups_in_hierarchy(_tar)
        export_tar_sg_list.extend(sg_list)

        link_info_dict = {}
        for _sg in sg_list:
            assigned_shapes = get_geom(_sg)
            assigned_mat = get_mat(_sg)
            # link_info_dict[assigned_mat] = assigned_shapes
            link_info_dict[_sg] = assigned_shapes
 
        _tar_info_dict['LINK'] = link_info_dict

    return (list(all_info_dict.values()).pop()).get('LINK')
