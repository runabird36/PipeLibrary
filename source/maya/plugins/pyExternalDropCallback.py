"""
To use, make sure that externalDropCallback.py is in your MAYA_PLUG_IN_PATH
then do the following:

import maya
maya.cmds.loadPlugin("externalDropCallback.py")

Drag and drop events should appear in the script editor output.
"""

import sys, re
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

from maya_md import op

class CommandFactory:
    @staticmethod
    def get_toolname(inputs :str):
        toolname = inputs.split("_")[0]
        return toolname
    
    @staticmethod
    def execute_command(tool_name :str, inputs :list):
        if tool_name == "OTX":
            for _idx, input in enumerate(inputs):
                
                if _idx == 0:
                    assetname    = input.split('_')[1]
                    ass_pub_path = "/"+input.split('_/')[1]
                    # ass_pub_path = re.sub(r"^OTX\_", "", inputs[0])
                else:
                    assetname    = input.split('_')[0]
                    ass_pub_path = "/"+input.split('_/')[1]



                created_node = op.create_includeGraph(f"{assetname}_ldv", ass_pub_path)
                cmds.setAttr(f"{created_node}.target", f"{assetname}_look", type="string")

                root_node = op.create_merge(f"{assetname}_root")
                
                op.connect_operator_v02(f"{created_node}.out", f"{root_node}.inputs")

    



# callback
class PyExternalDropCallback(OpenMayaUI.MExternalDropCallback):
    instance = None

    def __init__(self):
        OpenMayaUI.MExternalDropCallback.__init__(self)
        
    def externalDropCallback( self, doDrop, controlName, data ):
        str = ("External Drop:  doDrop = %d,  controlName = %s" % (doDrop, controlName))
        
        # Mouse button
        if data.mouseButtons() & OpenMayaUI.MExternalDropData.kLeftButton:
            str += ", LMB"
        if data.mouseButtons() & OpenMayaUI.MExternalDropData.kMidButton:
            str += ", MMB"
        if data.mouseButtons() & OpenMayaUI.MExternalDropData.kRightButton:
            str += ", RMB"
            
        # Key modifiers
        if data.keyboardModifiers() & OpenMayaUI.MExternalDropData.kShiftModifier:
            str += ", SHIFT"
        if data.keyboardModifiers() & OpenMayaUI.MExternalDropData.kControlModifier:
            str += ", CONTROL"
        if data.keyboardModifiers() & OpenMayaUI.MExternalDropData.kAltModifier:
            str += ", ALT"
            
        # Data
        if data.hasText():
            dropped_txt = data.text()
            str += (", text = %s" % data.text())
            toolname = CommandFactory().get_toolname(dropped_txt)
            CommandFactory().execute_command(toolname, dropped_txt.split(";"))
            if cmds.pluginInfo("pyExternalDropCallback", query=True, loaded=True) == True:
                cmds.unloadPlugin("pyExternalDropCallback")
        
        if data.hasUrls():
            urls = data.urls()
            for (i,url) in enumerate(urls):
                str += (", url[%d] = %s" % (i, url))
            # end
        if data.hasHtml():
            str += (", html = %s" % data.html())
        if data.hasColor():
            color = data.color()
            str += (", color = (%d, %d, %d, %d)" % (color.r, color.g, color.b, color.a))
        if data.hasImage():
            str += (", image = true")
        str += "\n"
        sys.stdout.write( str )
        return OpenMayaUI.MExternalDropCallback.kMayaDefault
        
# end


# Initialize the plug-in
def initializePlugin(plugin):
    try:
        PyExternalDropCallback.instance = PyExternalDropCallback()
        OpenMayaUI.MExternalDropCallback.addCallback( PyExternalDropCallback.instance )
        sys.stdout.write("Successfully registered callback: PyExternalDropCallback\n")
    except:
        sys.stderr.write("Failed to register callback: PyExternalDropCallback\n")
        raise
# end
        

# Uninitialize the plug-in
def uninitializePlugin(plugin):
    try:
        OpenMayaUI.MExternalDropCallback.removeCallback( PyExternalDropCallback.instance )
        sys.stdout.write("Successfully deregistered callback: PyExternalDropCallback\n")
    except:
        sys.stderr.write("Failed to deregister callback: PyExternalDropCallback\n")
        raise
# end

#-
# ==========================================================================
# Copyright (C) 2011 Autodesk, Inc. and/or its licensors.  All 
# rights reserved.
#
# The coded instructions, statements, computer programs, and/or related 
# material (collectively the "Data") in these files contain unpublished 
# information proprietary to Autodesk, Inc. ("Autodesk") and/or its 
# licensors, which is protected by U.S. and Canadian federal copyright 
# law and by international treaties.
#
# The Data is provided for use exclusively by You. You have the right 
# to use, modify, and incorporate this Data into other products for 
# purposes authorized by the Autodesk software license agreement, 
# without fee.
#
# The copyright notices in the Software and this entire statement, 
# including the above license grant, this restriction and the 
# following disclaimer, must be included in all copies of the 
# Software, in whole or in part, and all derivative works of 
# the Software, unless such copies or derivative works are solely 
# in the form of machine-executable object code generated by a 
# source language processor.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. 
# AUTODESK DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED 
# WARRANTIES INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF 
# NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR 
# PURPOSE, OR ARISING FROM A COURSE OF DEALING, USAGE, OR 
# TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS LICENSORS 
# BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL, 
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK 
# AND/OR ITS LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY 
# OR PROBABILITY OF SUCH DAMAGES.
#
# ==========================================================================
#+