# -*- coding:utf-8 -*-

import maya.cmds as cmds

def turn_on(_attr, _value):
    if cmds.getAttr(_attr) == _value:
        return
    try:
        cmds.setAttr(_attr, _value)
    except:
        return

def default_render_setting():
    try:
        cmds.setAttr("defaultArnoldRenderOptions.force_texture_cache_flush_after_render" , True)
        if cmds.getAttr("defaultArnoldRenderOptions.autotx") == True:
            cmds.setAttr("defaultArnoldRenderOptions.autotx" , False)
            cmds.setAttr("defaultArnoldRenderOptions.use_existing_tiled_textures" , True)
        else:
            cmds.setAttr("defaultArnoldRenderOptions.use_existing_tiled_textures" , True)
        cmds.setAttr("defaultArnoldRenderOptions.autotile" , False)
        print('Flush cache!!!')
        cmds.arnoldFlushCache(flushall=True)
    except Exception as e:
        print(e)
    turn_on("defaultArnoldRenderOptions.expandProcedurals", True)
    turn_on("defaultArnoldRenderOptions.exportAllShadingGroups", True)
    turn_on("defaultArnoldRenderOptions.exportFullPaths", True)
