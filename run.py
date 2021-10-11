
from vision import Vision
from controller import Controller
from game import Game

vision = Vision()
controller = Controller()
game = Game(vision, controller)
game.run()
