"""
人脸识别模块
本模块包括人脸识别的主要实现代码
"""
import numpy as np
import os
import cv2
from PIL import Image, ImageDraw, ImageFont



class FaceRecognitionGetter:
    """
    负责人脸识别的图片采集
    """

    def __init__(self):
        self.__user_name_path = "user_name"  # 保存使用者姓名文件的地址
        # 创建级联分类器
        self.__face_detector = cv2.CascadeClassifier('./cascade/haarcascades/haarcascade_frontalface_default.xml')
    def get_face_data(self, face_name):
        """
        得到人脸识别的图片数据，将图片写入到Facedata文件夹中
        :param face_name: 识别者信息
        """
        i = 0  # 控制频率
        FREQUENCY = 3  # 频率
        self.__count = 0  # 计数图片输入
        self.__sign = None  # 建立标志如果原有信息不存在的话才写入图片
        self.__write_name_data(face_name)  # 写入识别者信息
        if self.__sign:
            print("""
        =- 接下来会搜集1000张您的信息，请将耐心等待-=            
            """)
            self.__get_jpg_data(i, FREQUENCY)  # 获取人脸图片信息
        elif self.__sign is None:
            print("=-人物信息已存在-=")
        return self.__sign
    def __get_jpg_data(self, i, FREQUENCY):
        """
        获得人脸信息
        :param count:图片数量
        :param i: 控制频率用
        :param FREQUENCY: 频率
        """
        cap = cv2.VideoCapture(0)  # 打开摄像头
        while True:
            # 分帧读取图像
            sucess, img = cap.read()
            # 转为灰度图片
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 检测人脸
            faces = self.__face_detector.detectMultiScale(gray, 1.3, 5)
            self.__write_jpg(faces, gray, img, i, FREQUENCY)  # 将读取的每帧图片按频率保存
            # 保持画面的持续。
            k = cv2.waitKey(1)
            if k == 27:  # 通过esc键退出摄像
                break
            elif self.__count >= 1000:  # 得到1000个样本后退出摄像
                break
        # 关闭摄像头
        cap.release()
        cv2.destroyAllWindows()
    def __write_jpg(self, faces, gray, img, i, FREQUENCY):
        """
        写入人脸信息图片
        :param faces: 人脸识别器
        :param gray: 灰度图片
        :param img: 视频中按频率得到的图片
        :param i: 控制频率
        :param count: 图片数量
        :param FREQUENCY: 频率
        """
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0, 0))
            if i % FREQUENCY == 0:
                self.__count += 1
                # 保存图像
                cv2.imwrite("Facedata/User." + str(self.__face_id) + '.' + str(self.__count) + '.jpg',
                            gray[y: y + h, x: x + w])
            i += 1
            # 显示图片
            cv2.imshow('image', img)

    def __write_name_data(self, face_name):
        with open(self.__user_name_path, "r") as f:  # 以读形式打开user_name
            list_name = [item for item in f]  # 将user_name内的名字添加到列表中
        with open(self.__user_name_path, "a") as f:
            # 如果识别者信息之前不存在则添加
            if face_name + "\n" not in list_name and face_name is not "":
                f.write(face_name + "\n")
                self.__sign = True  # 修改标志
            self.___get_id(face_name, list_name)  # 得到识别者id

    def ___get_id(self, face_name, list_name):
        """
        获取识别者信息
        :param face_name:识别者姓名
        :param list_name: 姓名列表
        """
        self.__face_id = 0
        for item in list_name:
            if item == face_name:
                break
            else:
                self.__face_id += 1


class FaceRecognitionTrainer:
    """
    人脸识别的训练者
    """
    def __init__(self):
        # 创建级联分类器
        self.__detector = cv2.CascadeClassifier("./cascade/haarcascades/haarcascade_frontalface_default.xml")
    def trainer(self):
        self.__recognizer = cv2.face.LBPHFaceRecognizer_create()
        print("""
        =-训练需要一定时间，请耐心等待······-=""")
        faces, ids = self.__getImagesAndLabels()
        # 训练数据
        self.__recognizer.train(faces, np.array(ids))
        # 训练结果以yml形式文件保存
        self.__recognizer.write(r'face_trainer/trainer.yml')
        print("""
        =-有{0}位使用者信息已经被训练-=""".format(len(np.unique(ids))))

    def __getImagesAndLabels(self):
        """
        得到图片和标签
        :return: 含有图片信息和标签的列表
        """
        # 得到所有图片的路径
        imagePaths = [os.path.join('Facedata', f) for f in os.listdir('Facedata')]
        # 创建列表用于存储图片信息
        faceSamples = []
        # 用于存储图片id信息
        ids = []
        self.__add_img_id(faceSamples, ids, imagePaths)
        # 返回图片信息和图片id
        return faceSamples, ids

    def __add_img_id(self, faceSamples, ids, imagePaths):
        """
        :param faceSamples: 储存图片信息的列表
        :param ids: 标签
        :param imagePaths: 图片路径
        """
        for imagePath in imagePaths:
            # 得到灰度图像
            PIL_img = Image.open(imagePath).convert('L')
            # 将图片类型转化为 unin8
            img_numpy = np.array(PIL_img, 'uint8')
            # 得到id
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            # 得到图像矩阵
            faces = self.__detector.detectMultiScale(img_numpy)
            self.__add_message(faceSamples, faces, id, ids, img_numpy) # 将图片信息分别添加到列表中

    def __add_message(self, faceSamples, faces, id, ids, img_numpy):
        """
        添加信息
        :param faceSamples:储存图片信息的列表
        :param faces: 图像矩阵
        :param id: 标签
        :param ids: 标签列表
        :param img_numpy: 灰度图片
        """
        for (x, y, w, h) in faces:
            # 添加图片信息
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            # 添加id信息
            ids.append(id)


class FaceRecognitionRecognizer:
    """
    人脸识别的识别者
    """
    def __init__(self):
        self.__cascadePath = "./cascade/haarcascades/haarcascade_frontalface_default.xml"
        # 定义字体
        self.__font = ImageFont.truetype('simhei.ttf', 30, encoding='utf-8')
    def recognizer(self):
        # 创建人脸识别者
        self.__recognizer = cv2.face.LBPHFaceRecognizer_create()
        # 读取训练数据
        self.__recognizer.read('face_trainer/trainer.yml')
        # 创建级联分类器
        faceCascade = cv2.CascadeClassifier(self.__cascadePath)
        # 创建列表存储使用者姓名
        names = self.__read_user_name()
        # 打开摄像头
        cap = cv2.VideoCapture(0)
        minW = 0.1 * cap.get(3)
        minH = 0.1 * cap.get(4)
        while True:
            # 分帧数返回图片
            ret, img = cap.read()
            # 将图片转化为灰度图片
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 返回图像矩阵
            faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(int(minW), int(minH)))
            # 返回预测id和置信度
            img = self.__get_id_and_confidence(faces, gray, img, names)
            # 显示图像
            cv2.imshow('camera', img)
            k = cv2.waitKey(10)
            if k == 27: # 如果用户按下ese则退出
                break
        # 关闭摄像头
        cap.release()
        cv2.destroyAllWindows()

    def __get_id_and_confidence(self, faces, gray, img, names):
        """
        得到id和置信度
        :param faces: 图像矩阵
        :param gray: 灰度图片
        :param img: 图片
        :param names: 使用者姓名列表
        :return: 处理后的图片
        """
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 调用预测函数返回预测id和置信度
            idnum, confidence = self.__recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 100:
                idnum = names[idnum]
                confidence = "{0}%".format(round(100 - confidence))
            else:
                idnum = "unknown\n"
                confidence = "{0}%".format(round(100 - confidence))
            # 将opencv图像格式转换成PIL格式, 数据类型是PIL.Image.Image
            img = self.__switch_img(confidence, h, idnum, img, x, y)
        return img

    def __switch_img(self, confidence, h, idnum, img, x, y):
        # 将图片转化为PIL形式
        img_PIL = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_PIL)
        # 将需要的信息显示在图片上
        draw.text((x + 5, y - 5), str(idnum)[:-1], font=self.__font)
        draw.text((x + 5, y + h - 5), str(confidence), font=self.__font)
        # 将图片转化回cv2格式
        img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
        return img

    def __read_user_name(self):
        # 读取user_name文件，得到names列表
        with open("user_name", "r") as f:
            names = [item for item in f]
            return names
