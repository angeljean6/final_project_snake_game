import tkinter as tk
import random
from abc import ABC, abstractmethod

game_width = 600
game_height = 400
speed = 100  
space_size = 20  
snake_color = "#00FF00"  
food_color = "#FF0000"   
background_color = "#000000"

class game_object(ABC):
    def __init__(self, canvas):
        self.canvas = canvas

    @abstractmethod
    def draw(self):
        pass


class snake_player(game_object):
    def __init__(self, canvas, initial_parts=3):
        super().__init__(canvas)
        self.__coordinates = [[0, 0] for _ in range(initial_parts)]
        self.__squares = []
        self.__direction = 'down'

    def get_coordinates(self):
        return self.__coordinates

    def get_head(self):
        return self.__coordinates[0]

    def get_direction(self):
        return self.__direction

    def set_direction(self, new_direction):
        opposites = {('left', 'right'), ('right', 'left'), ('up', 'down'), ('down', 'up')}
        if (new_direction, self.__direction) not in opposites:
            self.__direction = new_direction

    def move(self):
        x, y = self.__coordinates[0]

        if self.__direction == "up":
            y -= space_size
        elif self.__direction == "down":
            y += space_size
        elif self.__direction == "left":
            x -= space_size
        elif self.__direction == "right":
            x += space_size

        self.__coordinates.insert(0, [x, y])

    def trim_tail(self):
        del self.__coordinates[-1]
        self.canvas.delete(self.__squares[-1])
        del self.__squares[-1]

    def draw(self):
        for square in self.__squares:
            self.canvas.delete(square)
        self.__squares.clear()

        for x, y in self.__coordinates:
            square = self.canvas.create_rectangle(
                x, y, x + space_size, y + space_size, 
                fill=snake_color, tag="snake"
            )
            self.__squares.append(square)

class snake_food(game_object):
    def __init__(self, canvas, snake_coordinates):
        super().__init__(canvas)
        self.__coordinates = None
        self.spawn(snake_coordinates)

    def get_coordinates(self):
        return self.__coordinates

    def spawn(self, snake_coordinates):
        while True:
            x = random.randint(0, int((game_width / space_size)) - 1) * space_size
            y = random.randint(0, int((game_height / space_size)) - 1) * space_size
            
            if [x, y] not in snake_coordinates:
                self.__coordinates = [x, y]
                break

    def draw(self):
        self.canvas.delete("food")
        x, y = self.__coordinates
        self.canvas.create_oval(
            x, y, x + space_size, y + space_size, 
            fill=food_color, tag="food"
        )

class snake_game_engine:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("OOP Classic Snake")
        self.window.resizable(False, False)

        self.score = 0
        self.running = True

        self.label = tk.Label(self.window, text=f"Score: {self.score}", font=('consolas', 20))
        self.label.pack()

        self.canvas = tk.Canvas(self.window, bg=background_color, height=game_height, width=game_width)
        self.canvas.pack()

        self.window.update()
        self.center_window()

        self.window.bind('<Left>', lambda e: self.snake.set_direction('left'))
        self.window.bind('<Right>', lambda e: self.snake.set_direction('right'))
        self.window.bind('<Up>', lambda e: self.snake.set_direction('up'))
        self.window.bind('<Down>', lambda e: self.snake.set_direction('down'))

        self.snake = snake_player(self.canvas)
        self.food = snake_food(self.canvas, self.snake.get_coordinates())

        self.snake.draw()
        self.food.draw()

        self.next_turn()
        self.window.mainloop()

    def center_window(self):
        w, h = self.window.winfo_width(), self.window.winfo_height()
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = int((sw/2) - (w/2)), int((sh/2) - (h/2))
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    def next_turn(self):
        if not self.running:
            return

        self.snake.move()
        
        head_x, head_y = self.snake.get_head()
        food_x, food_y = self.food.get_coordinates()

        if head_x == food_x and head_y == food_y:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.food.spawn(self.snake.get_coordinates())
        else:
            self.snake.trim_tail()

        self.snake.draw()
        self.food.draw()

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(speed, self.next_turn)

    def check_collisions(self):
        x, y = self.snake.get_head()

        if x < 0 or x >= game_width or y < 0 or y >= game_height:
            return True

        for body_part in self.snake.get_coordinates()[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        self.running = False
        self.canvas.delete("all")
        self.canvas.create_text(
            game_width/2, game_height/2,
            font=('consolas', 40), text="GAME OVER", fill="red"
        )   