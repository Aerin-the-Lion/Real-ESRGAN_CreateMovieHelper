'''

    @file Real-ESRGAN-NV-CreateMovieHelper
    @brief Real-ESRGANで楽に動画化するためのものです。
    @author Aerin the Lion(aka. Lost History)
    @date 12.29.2021
    
    [課題]
    multi-gpuなどの特定少数の人に向けてのものは搭載していません。
    また、ttaなどの機能もまだありません。※ttaは、若干の向上の引き換えに非常に長い処理を要するので、なしにしている。

'''
import subprocess
from subprocess import Popen, PIPE
import configparser
import os
import shutil
from ffmpy import FFmpeg, FFprobe
import json

#from cv2 import cv2

#  --- 変数定義 ---
input_f = 'input_frames'
output_f = 'output_frames'
config = 'config.ini'
config_path = './' + config
Model_name = ''
Scale_size = ''

# モデル用クラス生成
class Models:
    def __init__(self, name, scalesize, number):
        self.name = name
        self.scalesize = scalesize
        self.number = number

# オブジェクト生成
realesrgan_x4plus = Models('realesrgan-x4plus', '4', '1')
realesrnet_x4plus = Models('realesrnet-x4plus', '4', '2')
realesrgan_x4plus_anime = Models('realesrgan-x4plus-anime', '4', '3')
RealESRGANv2_animevideo_xsx2 = Models('RealESRGANv2-animevideo-xsx2', '2' ,'4')
RealESRGANv2_animevideo_xsx4 = Models('RealESRGANv2-animevideo-xsx4', '4', '5')

'''
# OpenCVを使用したfpsの読み取り。だが、簡単な使用にするには、exeが膨大になってしまうので、断念。
# どのくらい大きくなるかというと、約300MB。ちょっと配布としては無理。体制的には、どちらもffprobeを使用しているので、これにこだわらなくてもOK
def Capture_fps(file):
    global fps
    cap = cv2.VideoCapture(file)
    fps = str(cap.get(cv2.CAP_PROP_FPS))
    # print('動画のfpsは', cap.get(cv2.CAP_PROP_FPS))
'''
# 外部のffprobeを使用したfpsの読み取り。
def Capture_fps(file):
    if not os.path.isfile('ffprobe.exe'):
        print('＋＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＋')
        print('exeファイル直下にffprobe.exeが見当たりません。用意しないと、予期せぬアクシデントが起きます。')
        input('＋＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＋')
    global fps
    ff = FFprobe(
        global_options='-of json -show_streams -select_streams v',
        inputs={file: None},
    )
    res = ff.run(stdout=PIPE, stderr=PIPE)
    video_stream = res[0]
    video_detail = json.loads(video_stream).get('streams')[0]
    frame_rate = str(eval(video_detail.get('r_frame_rate')))
    fps = frame_rate
    print('動画のfpsは', fps)
    return fps

def Print_Three_Reader():
    print('.')
    print('.')
    print('.')

def DialogForModel():
    global UseModel,UseModelName,UseModelScalesize
    UseModel = ''
    UseModelName = ''
    UseModelScalesize = ''
    if DialogForUseModel == str(True):
        print('☆対話形式による処理を開始します。')
        print('+＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
        print(' 1.' +  realesrgan_x4plus.name)
        print(' 2.' +  realesrnet_x4plus.name)
        print(' 3.' +  realesrgan_x4plus_anime.name)
        print(' 4.' +  RealESRGANv2_animevideo_xsx2.name)
        print(' 5.' +  RealESRGANv2_animevideo_xsx4.name)
        print('+＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')

        getUseModel = input('どのモデルを使用しますか？上記より選択してください。')

        if getUseModel == realesrgan_x4plus.number:
            UseModelName = realesrgan_x4plus.name
            UseModel = realesrgan_x4plus
            UseModelScalesize = realesrgan_x4plus.scalesize
        elif getUseModel == realesrnet_x4plus.number:
            UseModelName = realesrnet_x4plus.name
            UseModel = realesrnet_x4plus
            UseModelScalesize = realesrnet_x4plus.scalesize
        elif getUseModel == realesrgan_x4plus_anime.number:
            UseModelName = realesrgan_x4plus_anime.name
            UseModel = realesrgan_x4plus_anime
            UseModelScalesize = realesrgan_x4plus_anime.scalesize
        elif getUseModel == RealESRGANv2_animevideo_xsx2.number:
            UseModelName = RealESRGANv2_animevideo_xsx2.name
            UseModel = RealESRGANv2_animevideo_xsx2.name
            UseModelScalesize = RealESRGANv2_animevideo_xsx2.scalesize
        elif getUseModel == RealESRGANv2_animevideo_xsx4.number:
            UseModelName = RealESRGANv2_animevideo_xsx4.name
            UseModel = RealESRGANv2_animevideo_xsx4
            UseModelScalesize = RealESRGANv2_animevideo_xsx4.scalesize
        else:
            print('fetal error! 不明な数値もしくは文字を検出しました。再度プログラムを起動してください。')
            input()
            exit()
        print('使用するモデルは' + str(UseModel) + 'です。')
        return UseModelName, UseModel, UseModelScalesize

    else:
        print('☆対話を省略し、configファイルから読み取ります。')

def Make_file(file):
    if not os.path.exists(file):
        print(str(file),'がないため、新規作成します。')
        os.mkdir(file)

def Import_config(file):
    global config,Bitrate,Codec,Extention,DialogForUseModel
    #  --- コンフィグ読み取り ---
    config = configparser.ConfigParser(comment_prefixes=';', allow_no_value=True)
    if not os.path.exists(file):
        print(str(file),'がないため、新規作成します。')
        config['DEFAULT'] = {
            'DialogForUseModel': 'True',
            '; Default = True ; if you use config setting then switch to False.':'',
            ';				  ; もしconfig.iniから読み取る場合は、Falseに切り替えてください。':'',
            'Codec': 'h264_nvenc',
            '; Default = h264_nvenc, hevc_nvenc, libx264 ...etc':'',
            'Bitrate': '100M',
            '; Default = 100M ; if you feels huge the value, decrease it.':'',
            ';				  ; もし数字が大きいと感じた場合は、下げてください。':'',
            'Extension': 'png',
            '; Default = png ; png,jpg,webp':'',
            '; --- !! These settings enables when DialogForUseModel is False !! ---':'',
            '; --- !! これらの設定はDialogForUseModelがFalseの場合に有効化されます !! ---':'',
            'UseModel': 'RealESRGANv2-animevideo-xsx2',
            '; Default = RealESRGANv2-animevideo-xsx2':'',
            'ScaleSize': 'Auto',
            '; Default = Auto ; 4 equals x4 and force mode, if you want use xsx2 then switch to 2 or Auto.':'',
            '				  ; 4は4倍加工(強制モード)、xsx2モデルを使用する場合は2もしくはAutoに切り替えてください。':'',
            '; Models list on below for UseModel':'',
            '; realesrgan-x4plus 				(default)':'',
            '; realesrnet-x4plus':'',
            '; realesrgan-x4plus-anime 			(optimized for anime images, small model size)':'',
            '; RealESRGANv2-animevideo-xsx2 		(anime video, X2)':'',
            '; RealESRGANv2-animevideo-xsx4 		(anime video, X4)':'',
        }
        with open(file, 'w') as file:
            config.write(file)

    # 同じファイルパス上にあることを認識させる
    # ↓exe化の場合は、こちらを使用
    #path = os.path.dirname(sys.executable)
    # ↓pyの場合は、こちらを使用
    #path = os.path.join(os.path.dirname(__file__), 'config.ini')
    #　こちらは相対パスにて設定、config.iniはexe/pyファイルの直下
    config.read(config_path, encoding='SJIS')
    Bitrate = config.get('DEFAULT', 'Bitrate')
    Codec = config.get('DEFAULT', 'Codec')
    Extention = config.get('DEFAULT', 'Extension')
    DialogForUseModel = config.get('DEFAULT', 'DialogForUseModel')

# フォルダーを作成
def Make_Files():
    Make_file(input_f)
    Make_file(output_f)

# フォルダ内が空かを確認する簡単な関数
def is_empty(dir_path: str) -> bool:
    return len(os.listdir(dir_path)) == 0
    
# 前に作成した画像がある場合は警告
def Alert_RemainingOldCreated():
    if is_empty(input_f + '/') == False:
        print('＋＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＋')
        print('・前回の連番作成した連番画像があります。バグが起きる可能性があるため、取り除いてください。')
        print('・それでも行う場合はなにかキーを押すと作業に入ります。')
        input('＋＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＋')

# exeファイルを起動したあとのcmd画面にD&Dをしたファイルを読み取り
def Filein():
    print('+＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    print('・ファイルを画面上にドラッグアンドドロップしてください。')
    print('+＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    global filename
    global basename
    global basename_without_ext
    filename = input()
    print('フルパスは' + filename)
    basename = os.path.basename(filename)
    print('basenameは', basename)
    basename_without_ext = os.path.splitext(os.path.basename(filename))[0]
    Print_Three_Reader()
    return filename, basename, basename_without_ext

# D&Dした動画を入力、png連番を「input_frames」内に作成。
def Make_Video_to_Consecutive_Pictures():
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    print('・動画の連番を作成しています…')
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    Print_Three_Reader()
    cmd_text = 'ffmpeg -i ' + basename + ' -qscale:v 1 -qmin 1 -qmax 1 -vsync 0 -vcodec png .\input_frames\%08d.png'
    print(cmd_text)
    subprocess.call(cmd_text, shell=True)
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    print('・動画の連番を終了しました。')
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    Print_Three_Reader()

# うまく作れていない場合は警告文
def Check_Consecutive_Pictures():
       if not is_empty(input_f + '/') == False:
            print('＋＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＋')
            print('・処理がうまくできていません。動画名にスペースや特殊文字を使用していませんか？アンダーバーなどで代用するようにしてください。')
            input('＋＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＝＝＝＝＝!Alert!＝＝＝＝＝＝＝＋')
            exit()

def SuperResolution_exe():
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    print('・超解像処理を実行します…')
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    Print_Three_Reader()
    if DialogForUseModel == str(True):
        Scale_size = UseModelScalesize
        Model_name = UseModelName
        cmd_text = 'realesrgan-ncnn-vulkan.exe -i input_frames/ -o output_frames/ -n ' + Model_name + ' -s ' + Scale_size + '-f ' + Extention
        subprocess.call(cmd_text, shell=True)
    else:
        # Scale_size強制モード
        # RealESRGANv2-animevideo-xsx2のみ、2倍でやらなければならないので、これで修正
        config = configparser.ConfigParser()
        config.read(config_path, encoding='SJIS')
        Model_name = config.get('DEFAULT', 'UseModel')
        Scale_size = config.get('DEFAULT', 'ScaleSize')
        if Scale_size == 'Auto':
            if Model_name == 'RealESRGANv2-animevideo-xsx2':
                Scale_size = '2'
            else:
                Scale_size = '4'
        cmd_text = 'realesrgan-ncnn-vulkan.exe -i input_frames/ -o output_frames/ -n ' + Model_name + ' -s ' + Scale_size + '-f ' + Extention
        subprocess.call(cmd_text, shell=True)
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    print('・超解像処理を終了しました。')
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    Print_Three_Reader()

def Combining_Picture():
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    print('・連番の結合を実行します…')
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    Print_Three_Reader()

    # 最初の処理。動画の音声を連番動画に入れ込む。
    cmd_text = 'ffmpeg -framerate ' + fps + ' -i .\output_frames\%08d.png -i "' + basename + '" -map 0:v:0 -map 1:a:0 -strict -2 -vcodec ' + Codec + ' -acodec copy -b:v ' + Bitrate + ' -pix_fmt yuv420p -r ' + fps + ' "'+ basename_without_ext +'_enhanced.mp4"'
    subprocess.call(cmd_text, shell=True)

    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    print('・連番の結合が正しく終えたかチェックします…')
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    Print_Three_Reader()

    enhanced_name = basename_without_ext + '_enhanced.mp4'
    if not os.path.isfile(enhanced_name):
        # ファイルが無い場合。音声が無い場合にこの処理となり、音声オフで出力する。
        print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
        print('・失敗を確認。再処理を実行…')
        print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
        Print_Three_Reader()

        cmd_text_NoMusic = 'ffmpeg -framerate ' + fps + ' -i .\output_frames\%08d.png -vcodec ' + Codec + ' -b:v ' + Bitrate + ' -pix_fmt yuv420p -r ' + fps + ' "'+ basename_without_ext +'_enhanced_nomusic.mp4"'
        subprocess.call(cmd_text_NoMusic, shell=True)

    elif os.path.getsize(enhanced_name) == 0:
            print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
            print('・失敗を確認。再処理を実行…')
            print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
            Print_Three_Reader()

            # 再処理。音声をmp3で出力をする。
            cmd_text_fix = 'ffmpeg -framerate ' + fps + ' -i .\output_frames\%08d.png -i "' + basename + '" -map 0:v:0 -map 1:a:0 -strict -2 -vcodec ' + Codec + ' -ab 320k -acodec libmp3lame -b:v ' + Bitrate + ' -pix_fmt yuv420p -r ' + fps + ' "'+ basename_without_ext +'_enhanced.mp4"'
            #cmd_text_fix = 'ffmpeg -framerate ' + fps + ' -i .\output_frames\%08d.png -i "' + basename_without_ext + '_music.wav" -map 0:v:0 -map 1:a:0 -strict -2 -vcodec ' + Codec + ' -ab 320k -acodec libmp3lame -b:v ' + Bitrate + ' -pix_fmt yuv420p -r ' + fps + ' "'+ basename_without_ext +'_enhanced.mp4"'
            #subprocess.call('ffmpeg -i "' + basename + '" "' + basename_without_ext + '_music.wav"', shell=True)
            subprocess.call(cmd_text_fix, shell=True)

    else:
        print('・正常に処理したことを確認しました。')

    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    print('・連番の結合を終了しました。')
    print('＋＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＋')
    Print_Three_Reader()

def Delete_Files():
    def yes_no_input():
        while True:
            choice = input('作成時に出たファイルを削除しますか？(yes/no)').lower()
            if choice in ['y', 'ye', 'yes']:
                return True
            elif choice in ['n','no']:
                return False

    ask_delete = yes_no_input()
    if bool(ask_delete) == True:
        shutil.rmtree(input_f)
        shutil.rmtree(output_f)
        if(os.path.isfile(basename_without_ext + '_music.wav')):
            os.remove(basename_without_ext + '_music.wav')
    elif bool(ask_delete) == False:
        print('ファイルの削除を行いません。')
    elif ask_delete == 0:
        print('不正な値です。ファイルの削除を行いません。')
    else:
        print('不正な値です。ファイルの削除を行いません。')

def Main():
    Import_config(config)
    Make_Files()
    Alert_RemainingOldCreated()
    DialogForModel()
    Filein()
    Capture_fps(basename)
    Make_Video_to_Consecutive_Pictures()
    Check_Consecutive_Pictures()
    SuperResolution_exe()
    Combining_Picture()
    Delete_Files()
    print('処理を終了しました。')

Main()





