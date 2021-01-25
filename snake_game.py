from random import randint

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.core.window import Window


class Food(Widget):
    pass


class SnakePart(Widget):
    pass


class SnakeGame(Widget):

    #: The size of a step at snake motion
    step_size = NumericProperty(50)

    #: A list of SnakePart object representing the snake
    snake_body = ListProperty([])

    #: A Food object representing the food block
    food = ObjectProperty()

    #: Tuple of bool to indicate next movement, in the form (x, y)
    motion = ()

    def new_game(self):
        # Clears the window
        self.clear_widgets()

        # Makes a one-block snake and puts it in the window
        self.snake_body = []
        self.snake_body.append(SnakePart(pos=(150, 50)))
        self.snake_body.append(SnakePart(pos=(100, 50)))
        self.snake_body.append(SnakePart(pos=(50, 50)))
        for part in self.snake_body:
            self.add_widget(part)

        # Puts a food block randomly in the window
        self.food = Food()
        self.add_widget(self.food)
        self.spawn_food()

        # Initialises the motion
        self.motion = (self.step_size, 0)

    def spawn_food(self):
        """ Changes the position of the food block.
        """
        horiz_pos = self.step_size * randint(0, Window.width // self.step_size)
        vert_pos = self.step_size * randint(0, Window.height // self.step_size)
        self.food.pos = (horiz_pos, vert_pos)

    def on_touch_up(self, touch):
        """ Stores in :attr:`motion` the command to move the snake.
        """
        dx = touch.x - self.snake_body[0].x
        dy = touch.y - self.snake_body[0].y
        if abs(dx) > abs(dy):
            sign = dx/abs(dx)
            self.motion = (sign * self.step_size, 0)
        else:
            sign = dy/abs(dy)
            self.motion = (0, sign * self.step_size)

    def next_frame(self, dt):
        """ Moves to the next frame by updating the snake position,
        and performing necessary action depending if the snake hit
        a wall, itself or food.
        """
        head = self.snake_body[0]
        last_pos = self.snake_body[-1].pos

        # Moves body
        new_pos = [part.pos for part in reversed(self.snake_body[:-1])]
        for index, part in enumerate(reversed(self.snake_body[1:])):
            part.pos = new_pos[index]

        # Moves head
        head.x += self.motion[0]
        head.y += self.motion[1]

        # If snake gets food
        if self.check_widget_collides(head, self.food):
            new_part = SnakePart(pos=last_pos)
            self.snake_body.append(new_part)
            self.add_widget(new_part)
            self.spawn_food()

        # If snake bites itself, restart game
        for part in self.snake_body[1:]:
            if self.check_widget_collides(head, part):
                self.new_game()

        # If snake hits a wall, restart game
        if not self.check_widget_collides(self, head):
            self.new_game()

    def check_widget_collides(self, wid1, wid2):
        """ An alternative version of Widget.collide_widget(),
        where borders aren't counted as a collision.
        """
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True


class SnakeApp(App):

    time_step = NumericProperty(0.2)

    def build(self):
        game = SnakeGame()
        game.new_game()
        Clock.schedule_interval(game.next_frame, self.time_step)
        return game
