from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window
import math


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def bounce(self):
        if self.y < 0 or self.top > self.parent.height:
            self.velocity_y *= -1

        if self.collide_widget(self.parent.player_1):
            self.velocity_x *= -1
            difference = self.center_y - self.parent.player_1.center_y
            percentage = difference / (self.parent.player_1.height / 2)
            angle = percentage * -45
            self.velocity_x *= 1.1
            self.velocity_y *= 1.1
            self.velocity = Vector(*self.velocity).rotate(angle)
        if self.collide_widget(self.parent.player_2):
            self.velocity_x *= -1
            difference = self.center_y - self.parent.player_2.center_y
            percentage = difference / (self.parent.player_2.height / 2)
            angle = percentage * 45
            self.velocity_x *= 1.1
            self.velocity_y *= 1.1
            self.velocity = Vector(*self.velocity).rotate(angle)

    def dead(self):
        if self.right > self.parent.width:
            return "p_2"
        elif self.x < 0:
            return "p_1"
        return False


class Player(Widget):
    def move_up(self):
        self.y += 100

    def move_down(self):
        self.y -= 100


class PongGame(Widget):
    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.player_1.move_up()
        elif keycode[1] == 'down':
            self.player_1.move_down()
        elif keycode[1] == 'w':
            self.player_2.move_up()
        elif keycode[1] == 's':
            self.player_2.move_down()

    ball = ObjectProperty(None)
    player_1 = ObjectProperty(None)
    player_2 = ObjectProperty(None)
    score_label_1 = ObjectProperty(None)
    score_label_2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.center = self.center
        angle = randint(-60, 60)
        if angle >= 0:
            angle += 60
        else:
            angle -= 60
        angle += 90
        self.ball.velocity = Vector(8, 0).rotate(angle)

    def update(self, dt):
        self.ball.move()
        self.ball.bounce()
        winner = self.ball.dead()
        if winner:
            if winner == "p_1":
                self.score_label_1.score = str(int(self.score_label_1.score)+1)
            elif winner == "p_2":
                self.score_label_2.score = str(int(self.score_label_2.score)+1)
            self.serve_ball()


class PongApp(App):
    def build(self):
        game = PongGame()
        Clock.schedule_interval(game.update, 1/60)
        game.serve_ball()
        return game


if __name__ == '__main__':
    PongApp().run()
