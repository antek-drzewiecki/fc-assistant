import cv2
import numpy as np

from mss import mss
from vision import Vision
from controller import Controller
from game import Game

print(mss().monitors)
vision = Vision()
controller = Controller()
#game = Game(vision, controller)

screenshot = cv2.imread('tests/screens/miners.png',cv2.IMREAD_COLOR)
x = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
output = cv2.imread('tests/screens/miners.png')
threshold = 0.85

img_H, img_S, img_V = cv2.split(x)
template_HSV = cv2.cvtColor(vision.templates['enemy_freighter'], cv2.COLOR_BGR2HSV)
template_H, template_S, template_V = cv2.split(template_HSV)
resH = cv2.matchTemplate(img_H,template_H,cv2.TM_CCOEFF_NORMED)

res = resH
matches = np.where(res >= threshold)


#w, h = vision.templates['enemy_freighter'].shape[::-1]
w = 52
h= 55

#match = vision.find_template('enemy_freighter', image=x, threshold=0.8)

for pt in zip(*matches[::-1]):
    cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (255,0,255), 2)


img = cv2.cvtColor(vision.templates['enemy_freighter'], cv2.COLOR_BGR2HSV)
name = "output"
cv2.namedWindow(name)
cv2.moveWindow(name, -3560,0)

cv2.imshow("baoo, ", img)
cv2.imshow(name,screenshot)



#game.run()
cv2.waitKey(0)
cv2.destroyAllWindows()