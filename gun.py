from random import randrange, choice
import tkinter as tk
import math
import time


G = 2
RESISTANCE = 0.5
WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, x, y, vx, vy):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canvas.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        global G, WIDTH, HEIGHT, RESISTANCE, target

        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x + self.r + self.vx >= WIDTH or self.x - self.r + self.vx <= 0:
            self.vx = -self.vx
            self.vy -= RESISTANCE * self.vy / abs(self.vy)

        if self.y + self.r - self.vy >= HEIGHT or self.y - self.r - self.vy <= 0:
            self.vy = -self.vy + 2 * G * self.vy / abs(self.vy)
            self.vx -= RESISTANCE * self.vx / abs(self.vx)

        self.vy -= G

        self.x += self.vx
        self.y -= self.vy

        self.vx -= RESISTANCE * self.vx / abs(self.vx)
        self.vy -= RESISTANCE * self.vy / abs(self.vy)

        if (abs(self.vx) - 0.1 < 0 and abs(self.vy) - 0.1 < 0) or (self.x >= WIDTH) or (self.x <= 0) or \
                (self.y >= HEIGHT) or (self.y <= 0) or (self.vx == 0):
            canvas.delete(self.id)

        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
                Args:
                    obj: Обьект, с которым проверяется столкновение.
                Returns:
                    Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
                """
        # FIXME
        if math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2) <= obj.r + self.r:
            return True
        else:
            return False


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.x = 20
        self.y = 450
        self.id = canvas.create_line(self.x, self.y, self.x + 30, self.y - 30, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        self.angle = math.atan((event.y - self.y) / (event.x - self.x))
        x = 20 + max(self.f2_power, 20) * math.cos(self.angle)
        y = 450 + max(self.f2_power, 20) * math.sin(self.angle)
        vx = self.f2_power * math.cos(self.angle)
        vy = - self.f2_power * math.sin(self.angle)
        new_ball = Ball(x, y, vx, vy)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y - self.y) / (event.x - self.x))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, self.x, self.y,
                      self.x + max(self.f2_power, self.x) * math.cos(self.angle),
                      self.y + max(self.f2_power, self.x) * math.sin(self.angle)
                      )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.points = 0
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0)
        self.id_points = canvas.create_text(30, 30, text=self.points, font='28')

        x = self.x = randrange(600, 780)
        y = self.y = randrange(300, 550)
        r = self.r = randrange(2, 50)
        print(x, y, r)
        color = self.color = 'red'
        canvas.coords(self.id, x - r, y - r, x + r, y + r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canvas.itemconfig(self.id_points, text=self.points)


def new_game(event=''):
    global  balls, bullet, canvas

    bullet = 0
    balls = []
    canvas.bind('<Button-1>', gun.fire2_start)
    canvas.bind('<ButtonRelease-1>', gun.fire2_end)
    canvas.bind('<Motion>', gun.targeting)


def time_handler():
    global target, balls, gun
    target.live = 1
    print(target.x)
    while target.live or balls:
        for ball in balls:
            ball.move()

            if ball.hittest(target) and target.live:
                target.live = 0
                target.hit()
                canvas.bind('<Button-1>', '')
                canvas.bind('<ButtonRelease-1>', '')
                canvas.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        canvas.update()
        time.sleep(0.03)
        gun.targeting()
        gun.power_up()
    canvas.itemconfig(screen1, text='')
    canvas.delete(gun)
    root.after(50, time_handler())


def main():
    global root, canvas, target, gun, bullet, balls, screen1
    root = tk.Tk()
    root.geometry('800x600')
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=1)
    target = Target()
    print(target.x)
    screen1 = canvas.create_text(400, 300, text='', font='28')
    gun = Gun()
    bullet = 0
    balls = []


main()
new_game()
time_handler()
root.mainloop()