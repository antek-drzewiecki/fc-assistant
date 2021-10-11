import numpy as np
import time

class Game:

    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.state = 'inactive'

    def run(self):
        while True:
            self.vision.refresh_frame()
            if self.state == 'inactive':
                self.log('Round needs to be started, activating ship')
                self.activate_ship()
                #self.state = 'active'
            if self.state == 'active':
                self.log('Round needs to be started, launching pineapple')
                try:
                    self.find_enemy()
                    self.state = 'active'
                except Exception as ex:
                    self.log('Failed to find enemy character')
            
            else:
                self.log('Not doing anything')
            time.sleep(1)


    def activate_ship(self):
        matches = self.vision.find_template('enemy_freighter', None, 0.85)
        if np.shape(matches)[1] >= 1:
            x = matches[1][0] / 1.50 
            y = matches[0][0] / 1.50
            self.log(x)
            self.log(y)
            self.controller.move_mouse(x-60,y+20)
        else:
            self.log('not found');
        
        
    def round_starting(self, player):
        matches = self.vision.find_template('%s-health-bar' % player)
        return np.shape(matches)[1] >= 1

    def launch_player(self):
        # Try multiple sizes of goalpost due to perspective changes for
        # different opponents
        scales = [1.2, 1.1, 1.05, 1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.98, 0.97, 0.96, 0.95]
        matches = self.vision.scaled_find_template('left-goalpost', threshold=0.75, scales=scales)
        x = matches[1][0]
        y = matches[0][0]

        self.controller.left_mouse_drag(
            (x, y),
            (x-200, y+10)
        )

        time.sleep(0.5)

    def round_finished(self):
        matches = self.vision.find_template('tap-to-continue')
        return np.shape(matches)[1] >= 1

    def click_to_continue(self):
        matches = self.vision.find_template('tap-to-continue')

        x = matches[1][0]
        y = matches[0][0]

        self.controller.move_mouse(x+50, y+30)
        self.controller.left_mouse_click()

        time.sleep(0.5)

    def can_start_round(self):
        matches = self.vision.find_template('next-button')
        return np.shape(matches)[1] >= 1

    def start_round(self):
        matches = self.vision.find_template('next-button')

        x = matches[1][0]
        y = matches[0][0]

        self.controller.move_mouse(x+100, y+30)
        self.controller.left_mouse_click()

        time.sleep(0.5)

    def has_full_rocket(self):
        matches = self.vision.find_template('full-rocket', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def use_full_rocket(self):
        matches = self.vision.find_template('full-rocket')

        x = matches[1][0]
        y = matches[0][0]

        self.controller.move_mouse(x, y)
        self.controller.left_mouse_click()

        time.sleep(0.5)

    def found_pinata(self):
        matches = self.vision.find_template('filled-with-goodies', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def click_cancel(self):
        matches = self.vision.find_template('cancel-button')

        x = matches[1][0]
        y = matches[0][0]

        self.controller.move_mouse(x, y)
        self.controller.left_mouse_click()

        time.sleep(0.5)

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
