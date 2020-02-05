from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import ffmpy
import sys
import os
import webbrowser
import pfycat
from pystreamable import StreamableApi
import subprocess

class GEditor_main(QWidget):
    def __init__(self):
        global vCodec
        global aCodec
        global preset
        global out_extension
        global importedFile
        global importedFiles
        global savePath
        global importedLut
        global completeText
        importedFile = ''
        savePath = ''
        importedFiles = ''
        importedLut = ''
        completeText = '''

\n   _____ ____  __  __ _____  _      ______ _______ ______ _____  
  / ____/ __ \|  \/  |  __ \| |    |  ____|__   __|  ____|  __ \ 
 | |   | |  | | \  / | |__) | |    | |__     | |  | |__  | |  | |
 | |   | |  | | |\/| |  ___/| |    |  __|    | |  |  __| | |  | |
 | |___| |__| | |  | | |    | |____| |____   | |  | |____| |__| |
  \_____\____/|_|  |_|_|    |______|______|  |_|  |______|_____/ 
'''
        super(GEditor_main, self).__init__()
        loadUi('GUI.ui',self)
        self.setWindowTitle('GEditor')
        self.editMenu.setStyle(QApplication.setStyle('windows'))
        self.button_menu_next.clicked.connect(self.get_ffmpeg_path)
        self.button_menu_next.clicked.connect(self.next_page)
        self.speedApply.clicked.connect(self.codec_choices)
        self.stabilizeVideo.clicked.connect(self.on_click_stab)
        self.convertMp3.clicked.connect(self.on_click_mp3)
        self.saveAsGif.clicked.connect(self.on_click_gif)
        self.uploadGfycat.clicked.connect(self.on_click_gfycat)
        self.uploadStreamable.clicked.connect(self.on_click_streamable)
        self.inputBrowse.clicked.connect(self.on_click_import)
        self.outputBrowse.clicked.connect(self.on_click_save)
        self.lutBrowse.clicked.connect(self.on_click_import_lut)
        self.speedApply.clicked.connect(self.on_click_speed)
        self.cropApply.clicked.connect(self.on_click_crop)
        self.lutApply.clicked.connect(self.on_click_lut)
        self.extractApply.clicked.connect(self.on_click_extract)
        self.inputLastFile.clicked.connect(self.on_click_last_file)
        self.x264Preset.setCurrentIndex(5)
        self.extractApply.clicked.connect(self.codec_choices)
        self.inputBrowse.clicked.connect(self.codec_choices)
        self.vCodecDrop.activated.connect(self.codec_choices)
        self.aCodecDrop.activated.connect(self.codec_choices)
        self.x264Preset.activated.connect(self.codec_choices)
        self.NVENCPresets.activated.connect(self.codec_choices)
        self.VP8Var.valueChanged.connect(self.codec_choices)
        self.XvidVar.valueChanged.connect(self.codec_choices)
        self.NVENCVar.valueChanged.connect(self.codec_choices)
        self.x264Var_2.valueChanged.connect(self.codec_choices)
        self.AACBitrateVar.valueChanged.connect(self.codec_choices)
        self.vorbisVar.valueChanged.connect(self.codec_choices)
        self.MP3Var.valueChanged.connect(self.codec_choices)
        self.lutPreview.clicked.connect(self.on_click_lut_preview)
        self.speedPreview.clicked.connect(self.on_click_speed_preview)
        self.extractPreview.clicked.connect(self.on_click_extract_preview)
        self.cropPreview.clicked.connect(self.on_click_crop_preview)
        self.changeFormat.clicked.connect(self.on_click_codec)
        self.customApply.clicked.connect(self.on_click_custom)


    ############ ACTUAL FUNCTIONS


    @pyqtSlot()
    def stabilize_vid(self, input_name, output_name):
        ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={'-': '-vf vidstabdetect -f null'}
        ).run()
        makeStab = ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={output_name: '{0} -vf vidstabtransform=smoothing=30,unsharp=5:5:0.8:3:3:0.4 {1}'.format(vCodec, aCodec)}
        )
        return makeStab

    def convertToMP3(self, input_name, output_name):
        convert = ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={output_name[:-3]+'mp3': '-b:a 192K -vn'}
        )
        return convert

    def saveToGif(self,input_name, output_name):
        ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={'palette.png': '-filter_complex "fps=10,scale=-1:640,crop=ih:ih,setsar=1,palettegen"'}
        ).run()
        makeGif = ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto', 'palette.png': '-y -hwaccel auto'},
            outputs={output_name[:-3]+'gif': '-filter_complex "[0]fps=10,scale=-1:640,crop=ih:ih,setsar=1[x];[x][1:v]paletteuse"'}
        )
        return makeGif

    def speedUp(self, input_name, output_name, percent):
        FFspeed = ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={output_name: '{0} -filter:v "setpts='.format(vCodec) + str(1/(int(percent) / 100)) + '*PTS" {0}'.format(aCodec)}
        )
        return FFspeed

    def cropVid(self, input_name, output_name, width, height):
        crop_command = ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={output_name: '{0} -filter:v "crop=in_w-'.format(vCodec) + str(width) + ':in_h-' + str(height) + '" {0}'.format(aCodec)}
        )
        return crop_command

    def applyLUT(self, input_name, output_name, LUT):
        LUTapply = ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={output_name: '{0} -vf lut3d="'.format(vCodec) + LUT + '" {0}'.format(aCodec)}
        )
        return LUTapply

    def extractSubclip(self, input_name, output_name, t_start, t_end):
        FFextract = ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={output_name: '{0} {1} -copyinkf -ss '.format(vCodec, aCodec) + str(t_start) + ' -to ' + str(t_end)}
        )
        return FFextract

    def changeCodec(self, input_name, output_name):
        FFCodec = ffmpy.FFmpeg(
            executable=exePath,
            inputs={input_name: '-y -loglevel debug -hwaccel auto'},
            outputs={output_name:'{0} {1}'.format(vCodec,aCodec)}
        )
        return FFCodec


    ################################ ON CLICK


    def get_ffmpeg_path(self):
        global exePath
        exePath = os.path.join(os.path.dirname(__file__), 'bin\\ffmpeg.exe').replace('/','\\')

    def on_click_import(self):
        global importedFile
        name = QFileDialog.getOpenFileName(self, "Import File",'', "All supported formats (*.mp4 *.webm *.avi *.mp3 *.ts *.mkv );;MP4 files (*mp4);; WebM files (*.webm);; AVI files (*.avi)")
        importedFile = name[0]
        self.inputPath.setText(importedFile)

    def on_click_save(self):
        global savePath
        name = QFileDialog.getSaveFileName(self, "Save File")
        try:
            if '.' in name[0][-4:]:
                savePath = name[0]
            else:
                savePath = name[0] + out_extension
        except:
            savePath = name[0]
        self.outputPath.setText(savePath)

    def on_click_import_lut(self):
        global importedLut
        name = QFileDialog.getOpenFileName(self, "Import LUT", '', 'LUT Files (*.cube)')
        importedLut = name[0]
        self.lutPath.setText(importedLut)

    def next_page(self):
        self.editMenu.setCurrentIndex(1)

    def upload_file_gfycat(self,input_name):
        r = pfycat.Client().upload(input_name)
        return "https://gfycat.com/" + r["gfyname"]

    def upload_file_streamable(self,input_name):
        r = StreamableApi("username", "KEY").upload_video(input_name, input_name)
        return "https://streamable.com/" + r["shortcode"]

    def on_click_gfycat(self):
        if importedFile == '':
            QMessageBox.warning(self, "Error", 'Import not specified.')
        else:
            link = self.upload_file_gfycat(importedFile)
            webbrowser.open(link)
            print(completeText)
            print(link)

    def on_click_streamable(self):
        if importedFile == '':
            QMessageBox.warning(self, "Error", 'Import not specified.')
        else:
            link = self.upload_file_streamable(importedFile)
            webbrowser.open(link)
            print(completeText)
            print(link)

    def on_click_gif(self):
        global vCodec
        global aCodec
        if importedFile == '' or savePath == '' or importedFile == savePath:
            QMessageBox.warning(self, "Error", 'Import/Output not specified or are equal.')
        else:
            if '-c:v copy' in vCodec:
                vCodec = vCodec.replace('-c:v copy', '')
            if '-c:a copy' in aCodec:
                aCodec = aCodec.replace('-c:a copy', '')
            self.saveToGif(importedFile, savePath).run()
            os.remove('palette.png')
            print(completeText)

    def on_click_mp3(self):
        if importedFile == '' or savePath == '' or importedFile == savePath:
            QMessageBox.warning(self, "Error", 'Import/Output not specified or are equal.')
        else:
            self.convertToMP3(importedFile, savePath).run()
            print(completeText)

    def on_click_stab(self):
        global vCodec
        global aCodec
        if importedFile == '' or savePath == '' or importedFile == savePath:
            QMessageBox.warning(self, "Error", 'Import/Output not specified or are equal.')
        else:
            if '-c:v copy' in vCodec:
                vCodec = vCodec.replace('-c:v copy', '')
            if '-c:a copy' in aCodec:
                aCodec = aCodec.replace('-c:a copy', '')
            self.stabilize_vid(importedFile,savePath).run()
            os.remove('transforms.trf')
            print(completeText)

    def on_click_speed(self):
        if importedFile == '' or savePath == '' or importedFile == savePath:
            QMessageBox.warning(self, "Error", 'Import/Output not specified or are equal.')
        else:
            global vCodec
            global aCodec
            percent = self.speedVar.value()
            if '-c:v copy' in vCodec:
                vCodec = vCodec.replace('-c:v copy', '')
            if '-c:a copy' in aCodec:
                aCodec = aCodec.replace('-c:a copy', '')
            self.speedUp(importedFile, savePath, percent).run()
            print(completeText)

    def on_click_crop(self):
        global vCodec
        global aCodec
        if importedFile == '' or savePath == '' or importedFile == savePath:
            QMessageBox.warning(self, "Error", 'Import/Output not specified or are equal.')
        else:
            if '-c:v copy' in vCodec:
                vCodec = vCodec.replace('-c:v copy', '')
            if '-c:a copy' in aCodec:
                aCodec = aCodec.replace('-c:a copy', '')
            heightPx = self.cropHeightVar.text()
            widthPx = self.cropWidthVar.text()
            if heightPx == '':
                heightPx = 0
            elif widthPx == '':
                widthPx = 0
            self.cropVid(importedFile, savePath, widthPx, heightPx).run()
            print(completeText)

    def on_click_lut(self):
        global vCodec
        global aCodec
        if importedFile == '' or savePath == '' or importedFile == savePath:
            QMessageBox.warning(self, "Error", 'Import/Output not specified or are equal.')
        else:
            if '-c:v copy' in vCodec:
                vCodec = vCodec.replace('-c:v copy', '')
            if '-c:a copy' in aCodec:
                aCodec = aCodec.replace('-c:a copy', '')
            LUTname = importedLut.replace('/', '\\\\\\\\\\\\\\\\')
            LUTname = LUTname[:1] + '\\\\\\\\' + LUTname[1:]
            self.applyLUT(importedFile, savePath, LUTname).run()
            print(completeText)

    def on_click_extract(self):
        if importedFile == '' or savePath == '' or importedFile == savePath:
            QMessageBox.warning(self, "Error", 'Import/Output not specified or are equal.')
        else:
            tStart = self.extractStartMinVar.value() * 60 + self.extractStartSecVar.value()
            tEnd = self.extractEndMinVar.value() * 60 + self.extractEndSecVar.value()
            self.extractSubclip(importedFile, savePath, tStart, tEnd).run()
            print(completeText)

    def on_click_codec(self):
        if importedFile == '' or savePath == '' or importedFile == savePath:
            QMessageBox.warning(self, "Error", 'Import/Output not specified or are equal.')
        else:
            if 'libvpx' in vCodec and ('aac' in aCodec or 'libmp3lame' in aCodec or 'copy' in aCodec):
                QMessageBox.warning(self, "Error", 'Incompatible formats. VP8 can only use Vorbis audio codec.')
            else:
                self.changeCodec(importedFile, savePath).run()
                print(completeText)

    def on_click_last_file(self):
        global importedFile
        self.inputPath.setText(savePath)
        importedFile = savePath
        print('Last file: {0}'.format(importedFile))

    def on_click_custom(self):
        path = os.path.join(os.path.dirname(__file__), 'bin\\ffmpeg.exe').replace('/', '\\')
        custom_command = self.customText.toPlainText()
        _command = '{0} {1}'.format(path, custom_command)
        self.process = subprocess.call(_command)
        print(completeText)


    ###########################  PREVIEWS


    def on_click_lut_preview(self):
        if importedFile == '':
            QMessageBox.warning(self, "Error", 'Import not specified.')
        else:
            path = os.path.join(os.path.dirname(__file__), 'bin\\ffplay.exe').replace('/','\\')
            LUTname = importedLut.replace('/','\\\\\\\\')
            LUTname = LUTname[:1] + '\\\\' + LUTname[1:]
            _command = '{0} -i -x 1280 -y 720 "{1}" -vf "lut3d={2}"'.format(path, importedFile,LUTname)
            self.process = subprocess.call(_command)
            print(completeText)

    def on_click_crop_preview(self):
        if importedFile == '':
            QMessageBox.warning(self, "Error", 'Import not specified.')
        else:
            path = os.path.join(os.path.dirname(__file__), 'bin\\ffplay.exe').replace('/','\\')
            heightPx = self.cropHeightVar.text()
            widthPx = self.cropWidthVar.text()
            if heightPx == '':
                heightPx = 0
            elif widthPx == '':
                widthPx = 0
            _command = '{0} -i -x 1280 -y 720 "{1}" -vf crop=in_w-'.format(path, importedFile)+ str(widthPx) + ':in_h-'+ str(heightPx)
            self.process = subprocess.call(_command)
            print(completeText)

    def on_click_extract_preview(self):
        if importedFile == '':
            QMessageBox.warning(self, "Error", 'Import not specified.')
        else:
            path = os.path.join(os.path.dirname(__file__), 'bin\\ffplay.exe').replace('/','\\')
            tStart = self.extractStartMinVar.value() * 60 + self.extractStartSecVar.value()
            tEnd = self.extractEndMinVar.value() * 60 + self.extractEndSecVar.value()
            _command = '{0} -i -x 1280 -y 720 "{1}" -ss {2} -t {3}'.format(path, importedFile, tStart, str(int(tEnd)-int(tStart)))
            self.process = subprocess.call(_command)
            print(completeText)

    def on_click_speed_preview(self):
        if importedFile == '':
            QMessageBox.warning(self, "Error", 'Import not specified.')
        else:
            percent = self.speedVar.value()
            frames = str(1 / (int(percent) / 100))
            path = os.path.join(os.path.dirname(__file__), 'bin\\ffplay.exe').replace('/','\\')
            _command = '{0} -i -x 1280 -y 720 "{1}" -vf setpts="{2}*PTS"'.format(path, importedFile, frames)
            self.process = subprocess.call(_command)
            print(completeText)

    def codec_choices(self):
        global vCodec
        global aCodec
        global preset
        global out_extension
        self.x264VarLabel.setText(str(self.x264Var_2.value()))
        self.XvidVarLabel.setText(str(self.XvidVar.value()))
        self.vorbisVarLabel.setText(str(self.vorbisVar.value()))
        self.MP3VarLabel.setText(str(self.MP3Var.value()))


        #Video Codecs


        preset = ''
        if self.vCodecDrop.currentText() == 'default':
            n = importedFile.rfind('.')
            out_extension = importedFile[n:]
            vCodec = '-c:v copy'
        if self.vCodecDrop.currentText() == 'x264 (mp4) (optimal)':
            out_extension = '.mp4'
            if self.x264Preset.currentText() == 'medium (Default)':
                preset = 'medium'
            else:
                preset = self.x264Preset.currentText()
            vCodec = '-c:v libx264 -preset {0} -crf {1} -pix_fmt yuv420p'.format(preset, self.x264Var_2.value())
        if self.vCodecDrop.currentText() == 'VP8 (webm)':
            out_extension = '.webm'
            vCodec = '-c:v libvpx -deadline realtime -b:v {0}k -pix_fmt yuv420p'.format(self.VP8Var.value())
        if self.vCodecDrop.currentText() == 'Xvid (avi)':
            out_extension = '.avi'
            vCodec = '-c:v libxvid -qscale:v {0}'.format(self.XvidVar.value())
        if self.vCodecDrop.currentText() == 'x265 (mp4)':
            out_extension = '.mp4'
            if self.x264Preset.currentText() == 'medium (Default)':
                preset = 'medium'
            else:
                preset = self.x264Preset.currentText()
            vCodec = '-c:v libx265 -preset {0} -crf {1} -pix_fmt yuv420p'.format(preset, self.x264Var_2.value())
        if self.vCodecDrop.currentText() == 'H.264 NVENC (mp4)':
            out_extension = '.mp4'
            n = self.NVENCPresets.currentText().find(' ')
            preset = self.NVENCPresets.currentText()[:n]
            vCodec = '-c:v h264_nvenc -preset {0} -b:v {1}k -pix_fmt yuv420p'.format(preset, self.NVENCVar.value())
        if self.vCodecDrop.currentText() == 'HEVC NVENC (mp4)':
            out_extension = '.mp4'
            n = self.NVENCPresets.currentText().find(' ')
            preset = self.NVENCPresets.currentText()[:n]
            vCodec = '-c:v hevc_nvenc -preset {0} -b:v {1}k -pix_fmt yuv420p'.format(preset, self.NVENCVar.value())

        #Audio codecs

        if self.aCodecDrop.currentText() == 'default':
            aCodec = '-c:a copy'
        elif self.aCodecDrop.currentText() == 'AAC':
            aCodec = '-c:a aac -ac 2 -b:a {0}k'.format(self.AACBitrateVar.value())
        elif self.aCodecDrop.currentText() == 'MP3':
            aCodec = '-c:a libmp3lame -qscale:a {}'.format(self.MP3Var.value())
        elif self.aCodecDrop.currentText() == 'Vorbis':
            aCodec = '-c:a libvorbis -qscale:a {0}'.format(self.vorbisVar.value())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = GEditor_main()
    widget.show()
    sys.exit(app.exec_())


