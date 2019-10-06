"""
人脸识别的界面控制
"""
from automatic_login import  *
from face_recognition import *

class FaceRecognitionView:
    def __init__(self):
        self.__getter = FaceRecognitionGetter()
        self.__train = FaceRecognitionTrainer()
        self.__recognier = FaceRecognitionRecognizer()
        self.__register = AutomaticLogin()
        self.__setter = set_message()
    def __display_menu(self):
        """
        打印出视图菜单
        """
        print("""
        ***********************************************************************
                                    人脸识别系统                                
        ***********************************************************************
        1. =-注册用户-= 
        2. =-人脸识别-=
        3. =-设置QQ/TIM信息-=
        4. =-扫脸登录QQ/TIM-=
        5. =-注册QQ/TIM信息-=
        0. =-退出系统-=
        =======================================================================
        说明：通过数字键选择菜单
             请先设置QQ/TIM信息(只用设置一遍),然后注册QQ/TIM信息，最后再登录            
        =======================================================================                     
        
        """)

    def __select_menu(self):
        """
        选择菜单 将用户的选择通过功能实现
        """
        # 输入选择
        select_number = int(input("""
        =-请输入您的选择-="""))
        if select_number == 1:
            self.__print_message(1)
            face_name = input("""
        =-请输入您的姓名-=""")
            # 调用函数获取信息
            if self.__getter.get_face_data(face_name):
                # 训练图片信息
                self.__train.trainer()
            # 更新使用者信息
            self.__register.get_name_list()
        elif select_number == 2:
            self.__print_message(2)
            # 进行人脸识别
            self.__recognier.recognizer()
        elif select_number == 3:
            self.__print_message(3)
            self.__setter.write_name()
            self.__setter.write_path()

        elif select_number == 4:
            self.__print_message(4)
            # 输入姓名
            user_name = input("""
        =-请输入您的姓名-=""")
            self.__register.QQ(user_name)
        elif select_number == 5:
            self.__print_message(5)
            self.__register.write_qq_and_password()




    def main(self):
        while True:
            self.__display_menu()
            self.__select_menu()




    def __print_message(self,number):
        """
        打印提示信息
        """
        if number == 1:
            print("""
        ***********************************************************************
                                进入注册用户界面······                               
        ***********************************************************************
            """)
        elif number == 2:
            print("""
        ***********************************************************************
                                进入人脸识别界面······                               
        ***********************************************************************
            """)
        elif number == 3:
            print("""
        ***********************************************************************
                                进入注册QQ/TIM信息界面······                               
        ***********************************************************************
            """)
        elif number == 4:
            print("""
        ***********************************************************************
                                进入扫脸登录QQ/TIM界面······                               
        ***********************************************************************""")
        elif number == 5:
            print("""
        ***********************************************************************
                                进入注册QQ/TIM信息界面······                               
        ***********************************************************************""")

