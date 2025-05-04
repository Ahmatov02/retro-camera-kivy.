import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import numpy as np
import time

class RetroCameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Превью камеры
        self.image = Image()
        self.layout.add_widget(self.image)

        # Кнопка "Снять фото"
        self.btn = Button(text="Снять ретро фото!", size_hint=(1, 0.2))
        self.btn.bind(on_press=self.take_photo)
        self.layout.add_widget(self.btn)

        # Настройка камеры
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS

        return self.layout

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Конвертация BGR -> RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Флип изображения
            frame = cv2.flip(frame, 0)
            buf = frame.tobytes()

            # Обновление текстуры
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.image.texture = texture

    def take_photo(self, instance):
        ret, frame = self.capture.read()
        if ret:
            # Ретро-фильтр
            retro = self.apply_retro_effect(frame)

            # Сохранение
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f"retro_photo_{timestamp}.jpg", retro)
            self.btn.text = "Сохранено!"
            Clock.schedule_once(lambda dt: setattr(self.btn, 'text', 'Снять ретро фото!'), 2.0)

    def apply_retro_effect(self, img):
        # Сепия
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(img, kernel)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)

        # Шум
        noise = np.random.randint(-20, 20, sepia.shape, dtype=np.int16)
        sepia = np.clip(sepia.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # Виньетка
        rows, cols = sepia.shape[:2]
        X_resultant_kernel = cv2.getGaussianKernel(cols, 200)
        Y_resultant_kernel = cv2.getGaussianKernel(rows, 200)
        resultant_kernel = Y_resultant_kernel * X_resultant_kernel.T
        mask = 255 * resultant_kernel / np.linalg.norm(resultant_kernel)
        for i in range(3):
            sepia[:, :, i] = sepia[:, :, i] * mask
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)

        return sepia

    def on_stop(self):
        if self.capture:
            self.capture.release()

if __name__ == '__main__':
    RetroCameraApp().run()
