import sys

from PIL import Image
from inference_sdk import InferenceHTTPClient
from ultralytics import YOLO
import os
import torch
from datetime import datetime

from apps.home.models import RegistroImagen


class FunctionRecognize:

    def __init__(self, image):
        self.image = image
        self.model_recognize_Varroa = YOLO("IA_Bees/best.pt")
        self.CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="9f09fApqriZFvLddbbLf"
        )

    def bee_detection(self):
        print("Iniciando detección de abejas")
        predict_bees_detection = self.CLIENT.infer(self.image, model_id="honey-bee-detection-model-zgjnb/2")
        print('deteccion abejas')
        cropped_images = []
        date_time_now = str(datetime.now()).split('.')[0]
        date_time_now = date_time_now.replace(':', '_')
        for prediction in predict_bees_detection['predictions']:
            # Obtener las coordenadas de la caja delimitadora
            width = float(prediction['width']) * 1.2
            height = prediction['height'] * 1.2
            left = prediction['x'] - width / 2
            top = prediction['y'] - height / 2
            right = prediction['x'] + width / 2
            bottom = prediction['y'] + height / 2

            cropped_images.append(self.image.crop((left, top, right, bottom)))

        for index, cropped_image in enumerate(cropped_images):
            result_predict = self.model_recognize_Varroa.predict(cropped_image, save_txt=True, save_conf=True, save=False,
                                                            device='cpu', show_labels=True, show_conf=True)
            path_save_image = r"Images/ImagesBeesDetect"
            os.makedirs(path_save_image, exist_ok=True)
            image_path = os.path.join(path_save_image, f"bee_Varoa{date_time_now}_{index}.jpg")
            for i in result_predict:

                for elemento in result_predict[0].boxes.cls.cpu().numpy():
                    print(elemento)
                    if elemento == 0:
                        print("Abeja")
                    else:
                        print("Varroa")
                        i.save(filename=image_path)
                        # Guardar la URL en la base de datos
                        url_imagen = os.path.join(image_path)  # Relative URL
                        registro = RegistroImagen.objects.create(
                            contiene_varroa=True,
                            url=url_imagen
                        )
                        print("Registro guardado en la base de datos")
                i.save(filename=image_path)
