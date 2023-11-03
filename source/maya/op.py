import maya.cmds as cmds
from maya_md import neon
import traceback



def del_all_tree(root):
    children = get_inputs(root)
    cmds.delete(root)
    if children is None:
        return
    else:
        for child in children:
            del_all_tree(child)


def convert_to_selection_string(_node_list):
    end_names = []
    for _node in _node_list:
        end_name = "*{0}*".format(_node)
        if '_GEOShapeDeform' in end_name:
            end_name = end_name.replace('_GEOShapeDeform','_GEOShape')
        end_names.append(end_name)
    return " or ".join(end_names)




#======================================================================
#List all the assignement path from a specific Shading Group : [ /group3/group1/pSphere1, /group3/group1/pSphere2, ...]
#======================================================================

def get_path_selection_string(assignment_paths):
    #Output List
    selection_path_string = ''

    #Add the wildcard and remove the rop node
    for r in range(len(assignment_paths)):
        assignment_paths[r] = '*' + ('/').join(assignment_paths[r].split('|')[2:]).replace('_GEOShapeDeform','_GEOShape') + '*'

    selection_path_string = (' or ').join(assignment_paths)

    return selection_path_string

#======================================================================
#Get next free input available
#======================================================================
def get_free_input(node_name):
    try:
        free_input = str(len(cmds.listConnections( node_name + '.inputs', d = True)))
    except:
        free_input = str(0)

    
    return free_input


def get_inputs(node_name):
    try:
        free_input = cmds.listConnections( node_name + '.inputs', d = True)
    except:
        free_input = None

    
    return free_input


def get_all_input_nodes(node_name):
    return cmds.listConnections( node_name + '.inputs', d = True)



def connect_operator(source, destination):
    freeInput = str(get_free_input(destination))
    sources = cmds.ls(source+'*')
    if len (sources) == 0:
        return
    source = sources[0]
    try:
        cmds.connectAttr( source + '.out', destination + '.inputs[' + freeInput + ']' )
    except:
        try:
            cmds.connectAttr( source + '.message', destination + '.inputs[' + freeInput + ']' )
        except Exception as e:
            traceback.print_exc()
            print(e)
            
            
def connect_operator_v02(from_fullname, to_fullname):
    '''
    - check multi instance attribute
    - and then connect
    '''
    if cmds.objExists(to_fullname + "[0]") == True:
        to_tar_name = to_fullname.split('.')[0]
        to_attrname = to_fullname.split('.')[1]
        to_next_idx = neon.get_next_available_attr(to_tar_name, to_attrname)
        neon.connect_attr(from_fullname, to_fullname, to_idx=to_next_idx)
    else:
        neon.connect_attr(from_fullname, to_fullname)
        




def get_shapes_by_attr(selection, attr):
    shapesByAttr = []
    for shape in neon.get_all_shape_in_hierarchy(selection):
        if cmds.getAttr( shape + '.' + attr, asString = True) == False:
            shapesByAttr.append( '*' + ('/').join( ( shape.split('|')[2:] ) [:-1] ) + '*' )

    
    return ' or '.join(shapesByAttr)

def create_collection(op_name, selection_string, op_collection):
    attrCollection = ""
    if cmds.objExists(op_name) and cmds.nodeType(op_name) == "aiCollection":
        attrCollection = op_name
    else:
        attrCollection = cmds.shadingNode('aiCollection', n = op_name + '_col', asRendering=True)
    cmds.setAttr(attrCollection + '.selection', selection_string, type='string')
    cmds.setAttr(attrCollection + '.collection', op_collection, type='string')


    return attrCollection



def create_setParameter(op_name, selection, assignments):
    
    if cmds.objExists(op_name) and cmds.nodeType(op_name) == "aiSetParameter":
        newSetParameter = op_name
    else:
        newSetParameter = cmds.shadingNode('aiSetParameter', n = op_name, asRendering=True)
    cmds.setAttr(newSetParameter + '.selection', selection, type='string')
    for r in range(len(assignments)):
        cmds.setAttr(newSetParameter + '.assignment[' + str(r) + ']', assignments[r], type='string')
    
    return newSetParameter



def create_includeGraph(op_name, ass_fullpath):
    cur_includeGrpah = ""
    if cmds.objExists(op_name) and cmds.nodeType(op_name) == "aiIncludeGraph":
        cur_includeGrpah = op_name
    else:
        cur_includeGrpah = cmds.shadingNode('aiIncludeGraph', n = op_name, asRendering=True)
    cmds.setAttr(cur_includeGrpah + '.filename', ass_fullpath, type='string')
    
    return cur_includeGrpah


def create_stringReplace(op_name, selection :str, os_type :int, from_str :str, to_str :str):
    cur_stringReplace = ""
    if cmds.objExists(op_name) and cmds.nodeType(op_name) == "aiStringReplace":
        cur_stringReplace = op_name
    else:
        cur_stringReplace = cmds.shadingNode('aiStringReplace', n = op_name, asRendering=True)
    cmds.setAttr(f"{op_name}.selection", selection, type='string')
    cmds.setAttr(f"{op_name}.os", os_type)
    cmds.setAttr(f"{op_name}.match", from_str, type="string")
    cmds.setAttr(f"{op_name}.replace", to_str, type="string")
    
    return cur_stringReplace


def create_merge(op_name):
    cur_merge = ""
    if cmds.objExists(op_name) and cmds.nodeType(op_name) == "aiMerge":
        cur_merge = op_name
    else:
        cur_merge = cmds.shadingNode('aiMerge', n = op_name, asRendering=True)
    
    return cur_merge








def get_reference_node_name(node_name, ref_name):
    '''
    Input 01 : node_name : str : node name which use reference aiCollection name in selection attribute like 'ryan_subdiv1'
    Input 02 : ref_name : str : reference name like '#ryanAll'
    return : aiCollection node name which has reference name in collection attribute like 'ryan_All_col1'

    This function find aiCollection node name which has reference name in collection attribute of aiCollection node
    '''
    if '#' in ref_name:
        ref_name = ref_name.replace('#', '')

    _assetname = node_name.split('_')[0]
    collection_node_list = cmds.ls(_assetname+'_*', typ='aiCollection')
    for _col in collection_node_list:
        ref_col_name = str(cmds.getAttr(_col+'.collection'))

        if ref_name == ref_col_name:
            return _col

    return ''



# def get_only_elements(selection_path_string):
#     element_list_res = []
#     if (' or ' in selection_path_string) or (' or' in selection_path_string) or ('or ' in selection_path_string):
#         element_list = selection_path_string.split('or')
#         for _element in element_list:
#             _element =_element.replace(' ', '')
#             if '*' in _element:
#                 _element = _element.replace('*', '')
#             element_list_res.append(_element)
#         return element_list_res
#     else:
#         return [selection_path_string]



def get_only_elements(selection_path_string):
    element_list_res = []

    element_list = selection_path_string.split('or')
    for _element in element_list:
        _element =_element.replace(' ', '')
        if '*' in _element:
            _element = _element.replace('*', '')
        element_list_res.append(_element)
    return element_list_res






def get_all_selections(node_name):
    selection_info = str(cmds.getAttr(node_name+'.selection'))

    all_selection_list = []
    for _sel_element in get_only_elements(selection_info):

        if '#' in _sel_element:
            ref_col_name = get_reference_node_name(node_name, _sel_element)
            if ref_col_name == '':
                continue
            sel_list_of_refsel = str(cmds.getAttr(ref_col_name+'.selection'))
            _selection_elements_list = get_only_elements(sel_list_of_refsel)

            all_selection_list.extend(_selection_elements_list)
        else:
            all_selection_list.append(_sel_element)

    return all_selection_list





def convert_stringparam_to_dict(string_param):
    splited_param = string_param.split('=')
    
    
    param_name = splited_param[0]
    param_value = splited_param[1]

    if ' ' in param_name:
        param_name = param_name.replace(' ' ,'')

    if ' ' in param_value:
        param_value = param_value.replace(' ' ,'')

    return { 'PARAM_NAME':param_name, 'PARAM_VALUE':param_value }


# def get_last_assignment_index(node_name):
#     assignmet_attr_list = cmds.getAttr(node_name + '.assignment', multiIndices=True)
#     if assignmet_attr_list is None:
#         return []
#
#     return int(len(assignmet_attr_list) - 1)



def get_last_assignment_index(node_name):
    assignmet_attr_list = cmds.getAttr(node_name + '.assignment', multiIndices=True)
    if assignmet_attr_list is None:
        return []

    return assignmet_attr_list


def get_all_assignments(node_name):
    if cmds.nodeType(node_name) != 'aiSetParameter':
        return []

    try:
        # assignmet_attr_list = cmds.getAttr(node_name + '.assignment', multiIndices=True)
        # if assignmet_attr_list == None:
        #     return []
        # last_index_num = int(assignmet_attr_list[-1])
        last_index_num = get_last_assignment_index(node_name)
        if last_index_num == []:
            return []
    except Exception as e:
        print(str(e))
        print('Error : Something wrong with get index of assignment')
        traceback.print_exc()
        return []


    attr_list = []
    for _idx in last_index_num:
        try:
            _value = cmds.getAttr(node_name+'.assignment[' + str(_idx) + ']' )

            _param_dict = convert_stringparam_to_dict(_value)
            attr_list.append(_param_dict)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return []

    return attr_list
