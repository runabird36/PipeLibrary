
import general_md.shotgun_api3 as shotgun_api3
import os, sys, subprocess, math, socket
from functools import partial


'''
1. make dictionary out of wm_stamp class

2. make instance and then operate set_path() function in this case, have to make path variable befor this.

3. do set_info_text_cmd function
        -first parameter : info dictionary
        -second parameter : leading among left text

4. do set_transparent_box_cmd function
        -first parameter : box height
        -second parameter : font color
        -third parameter : opacity of box



    title_info_dic = {'prj_name': prjName, 'start_frame': startFrame, 'total_frame':total_frame, \
                                        'user_name':userName, 'current_file_name':currentFileName, 'fps':fps, \
                                        'cam_name':camName, 'focal_lenth':focalLength, 'crop_factor':cropFactor}
    add_wm_stamp = wm_stamp.stamp()
    try:
        add_wm_stamp.set_path(movPath, wmMovPath)
    except wm_stamp.raise_path_error as e:
        print e
    add_wm_stamp.set_info_text_cmd(title_info_dic, 15)
    add_wm_stamp.set_transparent_box_cmd(177, 'white', 0.8)
    add_wm_stamp.create()
'''




class raise_path_error(Exception):
    def __str__(self):
        return "ther is no input path or output path!"


class stamp():
    def __init__(self):
        title_info_dic = {'prj_name':'', 'start_frame':0, 'total_frame':0, 'user_name':'', 'current_file_name':'', 'fps':0, 'cam_name':'', 'focal_lenth':'', 'crop_factor':'', 'final_date':'', 'final_time':''}
        leading = None
        height = None
        color = 'white'
        opacity = 0.8
        mov_path= ''
        wm_mov_path = ''

    def set_path(self, src=None, dst=None):
        self.mov_path = src
        self.wm_mov_path =dst

    def set_info_text_cmd(self, title_info_dic, leading=None):
        '''input : title info dic
            key : prj_name, start_frame, total_frame, user_name, current_file_name, fps, cam_name, focal_lenth, crop_factor'''

        padding = "177"
        leading = 15/3
        playblast_w = title_info_dic['playblast_w']
        print('width : {0}'.format(playblast_w))
        ratio_formating = float(1920)/float(playblast_w)
        print('ratio : {0}'.format(ratio_formating))
        scaled_fontsize = int(float(24)/float(ratio_formating))+3
        print('fontsize : {0}'.format(scaled_fontsize))
        scaled_title_fontsize = int(float(50)/float(ratio_formating))


        self.prjNameCmd = "drawtext=enable='between(t,0,100)':fontfile=/Windows/Fonts/Calibri.ttf:text='%s': fontcolor=white@0.7:fontsize=%d:x=(w-text_w)/2:y=h-th-8:box=1: boxcolor=black@0.2:boxborderw=8" % (title_info_dic['prj_name'], scaled_title_fontsize)
        msg_info_1 = "{0}\n{1}\n\t\t\t /{2}".format(title_info_dic['final_date'], title_info_dic['final_time'], title_info_dic['total_frame'])
        self.date_time_Cmd = "drawtext=enable='between(t,0,100)':fontfile=/Windows/Fonts/Calibri.ttf:text='%s': fontcolor=white@0.7: fontsize=%d: x=w-tw-5:y=h-th:box=1: boxcolor=black@0.2:boxborderw=10"%(msg_info_1, scaled_fontsize)

        self.frameNumCmd = "drawtext=enable='between(t,0,100)':fontfile=/Windows/Fonts/Calibri.ttf:text='%{0}': start_number={1} : fontcolor=white@0.7:fontsize={2}:x=w-tw*2-30:y=h-th-2".format('{frame_num}', title_info_dic['start_frame'], str(scaled_fontsize))
        # totalFrameNumCmd = "drawtext=enable='between(t,0,100)':fontfile=/Windows/Fonts/Calibri.ttf:text='%s': fontcolor=white@0.7: fontsize=24: x=w-tw-20:y=h-th-14:box=1: boxcolor=black@0.2:boxborderw=50:line_spacing=300"%(total_frame)


        msg_info_2 = 'Artist\: {0}\n\nVersion\: {1}\n\nfps\: {2}\n\nCamera\: {3}\n\nCamera Lens\: {4} mm ({5})'.format(title_info_dic['user_name'],title_info_dic['current_file_name'],title_info_dic['fps'],title_info_dic['cam_name'],title_info_dic['focal_lenth'],title_info_dic['crop_factor'])
        self.info_group_Cmd = "drawtext=enable='between(t,0,100)':fontfile=/Windows/Fonts/Calibri.ttf:text='Artist\: %s':fontcolor=white@0.7:fontsize=%d:x=5:y=h-th:box=1: boxcolor=black@0.2:boxborderw=8" % (msg_info_2,scaled_fontsize)



    # def set_transparent_box_cmd(self, height=177, color = 'white', opacity = 0.8):
    #     print type(height)
    #     print height
    #     print type(opacity)
    #     print opacity


    def turn_off_head_up_display(self):
        mel.eval('setAnimationDetailsVisibility(0);')
        mel.eval('setCameraNamesVisibility(0);')
        mel.eval('setCapsLockVisibility(0);')
        mel.eval('setCurrentContainerVisibility(0);')
        mel.eval('setCurrentFrameVisibility(0);')
        # mel.eval('ToggleEvaluationManagerHUDVisibility;')
        mel.eval('setFocalLengthVisibility(0);')
        mel.eval('setFrameRateVisibility(0);')
        mel.eval('setHikDetailsVisibility(0);')
        mel.eval('ToggleMaterialLoadingDetailsHUDVisibility(0);')
        mel.eval('setObjectDetailsVisibility(0);')
        # mel.eval('toggleAxis -o (!`toggleAxis -q -o`);')
        # mel.eval('if (!`exists originAxesMenuUpdate`) {eval "source buildDisplayMenu";} originAxesMenuUpdate;')
        mel.eval('setParticleCountVisibility(0);')
        mel.eval('setPolyCountVisibility(0);')
        mel.eval('setSceneTimecodeVisibility(0);')
        mel.eval('setSelectDetailsVisibility(0);')
        mel.eval('setSymmetryVisibility(0);')
        mel.eval('setViewAxisVisibility(0);')
        mel.eval('setViewportRendererVisibility(0);')



    def create(self):
        ffmpeg = "Z:/backstage/maya/loader/utils/assetPublisher/ffmpeg.exe"         ### change ffmpeg file for linux      // install //  git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
        textOption = "[0:v][1:v]overlay=10:10, %s,%s, %s,%s" % (  self.prjNameCmd, self.date_time_Cmd, self.frameNumCmd, self.info_group_Cmd)
        
        gstepLogo = '/usersetup/linux/module/ui_icons_md/giantstep_logo_white.png'


        wmProcess = subprocess.Popen([ffmpeg, '-y', '-i', self.mov_path, '-i', gstepLogo, '-filter_complex', textOption, '-c:v', 'mjpeg', '-q:v', '0', '-huffman', 'optimal', '-an', self.wm_mov_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)

        stdout, stderr = wmProcess.communicate()
        print(stdout)
        print(stderr)
