import base64
from aip import AipFace
from dj import settings

""" 你的 APPID AK SK """
APP_ID = settings.APP_ID
API_KEY = settings.API_KEY
SECRET_KEY = settings.SECRET_KEY
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

imageType = "BASE64"
options = {}
options["face_field"] = "age,gender,beauty,emotion"

def get_imgage(image):
   # image ='D:\code~\PY\dj\static\img'+image
    with open(image, 'rb') as f:
        my_image = base64.b64encode(f.read()).decode('utf-8')
        return my_image

# with open('1.jpg', 'rb') as f:
#     image = base64.b64encode(f.read()).decode('utf-8')
#
# """ 如果有可选参数 """
def my_detect(image):

    ret = client.detect(get_imgage(image), imageType, options)
    age = '年龄:'+str(ret['result']['face_list'][0]['age'])
    beauty = '分值:'+str(ret['result']['face_list'][0]['beauty'])
    gender = '性别:'+ret['result']['face_list'][0]['gender']['type']
    emotion = '情绪:'+ret['result']['face_list'][0]['emotion']['type']
    return age, beauty, gender, emotion

# """ 带参数调用人脸检测 """
# print(client.detect(image, imageType))










