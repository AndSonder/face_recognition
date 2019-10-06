
import time
import win32gui
import win32api
import win32con
import os
from pykeyboard import PyKeyboard
from ctypes import *
from face_recognition import *

class AutomaticLogin:
    def __init__(self):
        # 调用方法获得名称和路径
        self.__get_name()
        self.__get_path()
        self.get_name_list()
        self.__recognier = FaceRecognitionRecognizer()

    def QQ(self,user_name):
        """
        控制自动登录qq
        """
        # 识别人脸
        password, qq = self.__recognize_face(user_name)
        # 打开qq
        self.__open_qq()
        loginid = self.__open_window()
        # 定义一个键盘对象
        k = PyKeyboard()
        # 控制鼠标到指定位置
        self.__control_mouse(loginid)
        self.__input_message(k, password, qq)
        # 按下回车
        win32api.keybd_event(13, 0, 0, 0)
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)

    def __recognize_face(self,user_name):
        # 人脸识别
        self.__recognier.recognizer(user_name)
        with open("./message/qq.txt", "r") as f:
            for item in f:
                if item.split("----")[0] == user_name:
                    qq = item.split("----")[1]
                    password = item.split("----")[2]
                    # 输入账号和密码
        return password, qq

    def __input_message(self, k, password, qq):
        """
        输入账号和密码
        :param k: 键盘对象
        :param password: 密码
        :param qq: 账号
        """
        # 输入用户名
        k.type_string(qq)
        time.sleep(0.2)
        # 按下tab换行
        k.tap_key(k.tab_key)
        # 输入密码
        k.type_string(password)

    def __control_mouse(self, loginid):
        """
        控制鼠标到指定位置
        :param loginid: 窗口对象
        """
        # 把鼠标放置到登陆框的输入处
        if self.__name == "TIM":
            windll.user32.SetCursorPos(loginid[4][0] + 250, loginid[4][1] + 271)
            time.sleep(2)
            # 按下鼠标再释放
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, loginid[4][0] + 250, loginid[4][1] + 271, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, loginid[4][0] + 250, loginid[4][1] + 271, 0, 0)
            time.sleep(0.5)
        elif self.__name == "QQ":
            # 把鼠标放置到登陆框的输入处
            windll.user32.SetCursorPos(loginid[4][0] + 300, loginid[4][1] + 248)
            time.sleep(2)
            # 按下鼠标再释放
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, loginid[4][0] + 300, loginid[4][1] + 248, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, loginid[4][0] + 300, loginid[4][1] + 248, 0, 0)
            time.sleep(0.5)

    def __open_window(self):
        """
        获取窗口信息
        """
        # 获取QQ的窗口句柄
        a = win32gui.FindWindow(None, self.__name)
        # 获取QQ登录窗口的位置
        loginid = win32gui.GetWindowPlacement(a)
        return loginid

    def __open_qq(self):
        """
        启动
        """
        os.system('"'+self.__path+'"')
        time.sleep(1)

    def __get_path(self):
        """
        得到设置好的qq的路径
        """
        with open("./message/path", "r") as f:
            for item in f:
                self.__path = item

    def __get_name(self):
        """
        得到名称
        """
        with open("./message/name","r") as f:
            for item in f:
                self.__name = item

    def write_qq_and_password(self):
        """
        输入姓名，账号和密码
       """
        # while True:
        #     self.__user_name = input("""
        #     =-请输入姓名-=""")
        #     if self.__user_name not in self.__names:
        #         print("""
        # =-没有您的信息，请先采集人脸信息""")
        #         break
        #     else:
        #         break
        # 得到已记录的用户姓名
        qq_names = self.__get_qq_names()
        while True:
            name = input("""
        =-请输入您的姓名-=""")
            if name in qq_names:
                print("""
        =-用户已存在-=""")
                break
            elif name not in self.__names:
                print("""
        =-用户不存在-=""")
            else:
                qq = input("""
                =-请输入账号-=""")
                password = input("""
                =-请输入密码-=""")
                with open("./message/qq.txt","a") as f:
                    f.write(name + "----"+qq +"----"+password+"----\n")
                break


    def __get_qq_names(self):
        with open("./message/qq.txt", "r") as f:
            # 得要已经记录数据的用户信息
            qq_names = [item.split("----")[0] for item in f]
        return qq_names

    def get_name_list(self):
        with open("./message/user_name","r") as f:
            self.__names = [item[:-1] for item in f]




class set_message:
    """
    设置信息
    """

    def write_path(self):
        """
        设置qq路径
        """
        path = input("""
        =-请输入你选择软件的路径-=:""")
        with open("./message/path", "w") as f:
            f.write(path )

    def write_name(self):
        """
        设置软件名称
        """
        # 规定可以输入的软件名称
        list_name = ["QQ","TIM"]
        while True:
            name = input("""
        =-请输入软件的名称 如果是QQ 就输入QQ ，如果是TIM 就输入TIM:""")
            if name not in list_name:
                print("""
        =-请输入正确的名称:""")
            else:
                with open("./message/name", "w") as f:
                    f.write(name)
                break

#
# re = set_message()
# re.write_path()

# a.write_qq_and_password()

