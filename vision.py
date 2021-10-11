import cv2
from mss import mss
from PIL import Image
import numpy as np
import time

class Vision:
    def __init__(self):
        self.static_templates = {
            'ship_active': 'assets/ship.png',
            'ship_inactive': 'assets/ship_inactive.png',
            'enemy_freighter': 'assets/ship_enemy_freighter2.png'
        }

        self.templates = { k: cv2.cvtColor(cv2.imread(v, 1), cv2.COLOR_BGR2HSV) for (k, v) in self.static_templates.items() }

        #self.monitor   = {'top': 0, 'left': 0, 'width': 3840, 'height': 2160}
        self.screen = mss()
        #self.monitor = self.screen.monitors[0]
        #self.log(self.screen.monitors)
        self.frame = None

    def take_screenshot(self):
        sct_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def get_image(self, path):
        return cv2.imread(path, 0)

    def bgr_to_rgb(self, img):
        b,g,r = cv2.split(img)
        return cv2.merge([r,g,b])

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def match_template(self, img_hsf, template, threshold=0.95):
        """
        Matches template image in a target grayscaled image
        """

        res = cv2.matchTemplate(img_hsf, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

    def find_template(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
        )

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        initial_template = self.templates[name]
        for scale in scales:
            scaled_template = cv2.resize(initial_template, (0,0), fx=scale, fy=scale)
            matches = self.match_template(
                image,
                scaled_template,
                threshold
            )
            if np.shape(matches)[1] >= 1:
                return matches
        return matches

    def refresh_frame(self):
        self.frame = self.take_screenshot()

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
