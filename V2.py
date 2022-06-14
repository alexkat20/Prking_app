'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

import requests  # FIXME
from kivy.app import App
from kivy.lang import Builder
from PIL import Image
from kivy.uix.screenmanager import ScreenManager, Screen
import time


global picture
global address
global timestr
global predicted1
global predicted2
global predicted3
global carplate
global carplate_img

classes = ["Вход в здание",
           "Контейнерная площадка",
           "Газон",
           "Пешеходный переход",
           "Тротуар/пешеходная дорожка",
           "Детская/спортивная площадка"]


class FirstWindow(Screen):
    pass


class ThirdWindow(Screen):
    def selected(self, filename):
        global picture, predicted3, predicted2, predicted1, classes
        try:
            picture = filename[0]
            self.ids['my_image1'].source = filename[0]
            url = 'https://parking-classification-app.herokuapp.com/predict1'  # FIXME
            my_img = {'image': open(filename[0], 'rb')}  # FIXME
            r = requests.post(url, files=my_img)  # FIXME
            # convert server response into JSON format.  # FIXME
            print(r.json())  # FIXME
            #  self.predict(filename[0]) FIXME

            predicted1, predicted2, predicted3 = r.json()['predictions']

        except:
            pass


class SecondWindow(Screen):
    # Import Haar Cascade XML file for Russian car plate numbers

    def show_photo(self):
        global timestr, classes, predicted1, predicted2, predicted3, picture, carplate
        url = 'https://carplate-detection-app.herokuapp.com/predict2'  # FIXME
        my_img = {'image': open(picture, 'rb')}  # FIXME
        r = requests.post(url, files=my_img)  # FIXME
        # convert server response into JSON format.  # FIXME
        print(r.json())  # FIXME
        #  self.predict(filename[0]) FIXME
        carplate = r.json()['prediction']

    def detect_carplate(self):
        global carplate
        try:
            self.show_photo()
        except:
            carplate = ""

        #  /sdcard/DCIM/Camera/
        self.ids['my_image'].source = picture  # "IMG_{}.jpg".format(timestr)

    def write_prediction(self):
        global address
        predictions = [int(predicted1), int(predicted2), int(predicted3)]  # FIXME

        # print(classes[predictions[0]], classes[predictions[1]], classes[predictions[2]])

        if predictions[2] == predictions[0] or predictions[2] == predictions[1] or predictions[2] == predictions[0] == \
                predictions[1]:
            my_text = f"Нарушение: {classes[predictions[2]]}" \
                      f" \n Номера: {carplate}. \n Адрес: {address}"
        elif predictions[0] == predictions[1]:
            my_text = f"Нарушение: {classes[predictions[2]]} или {classes[predictions[1]]}" \
                      f" \n Номера: {carplate}. \n Адрес: {address}"
        else:
            my_text = f"Нарушение: {classes[predictions[2]]}" \
                      f" \n Номера: {carplate}. \n Адрес: {address}"

        self.ids['label1'].text = my_text


class CameraClick(Screen):

    def capture(self):
        global timestr, predicted1, predicted2, predicted3, picture
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")

        texture = camera.texture
        size = texture.size
        pixels = texture.pixels

        pil_image = Image.frombytes(mode='RGBA', size=size, data=pixels)


        camera.export_to_png("IMG_{}.jpg".format(timestr)) # /sdcard/DCIM/Camera/

        picture = "IMG_{}.jpg".format(timestr)  # /sdcard/DCIM/Camera/

        url = 'https://parking-classification-app.herokuapp.com/predict1'  # FIXME
        my_img = {'image': open(picture, 'rb')}  # FIXME
        r = requests.post(url, files=my_img)  # FIXME
        # convert server response into JSON format.  # FIXME
        print(r.json())  # FIXME
        #  self.predict(filename[0]) FIXME

        predicted1, predicted2, predicted3 = r.json()['predictions']


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("front.kv")


class TestCamera(App):
    def set_text(self, text):
        global address
        address = text

    def build(self):
        return kv  # CameraClick()


TestCamera().run()
