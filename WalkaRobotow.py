#       Game
#   Robocop
#   By Kamil Gierlach
#   20 - 02 - 2019
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
import random as rn
import time

# new window and set it
window = tk.Tk()
window.geometry('600x400+200+200')
window.title('Robocop')
window.configure(background='Light blue')

width = 400 / 20
height = 400 / 20
size = 20
speed = 100
score = 0

def game():
    window.destroy()
    window2 = tk.Tk()
    window2.title('Robocop')
    window2.configure(bg='Light blue')
    window2.geometry('600x450+200+200')

    text1 = Label(window2, text = 'Player', bg = 'Light Blue')
    text1.grid(column = 0, row = 0, padx = 25)

    text2 = Label(window2, text = '  Computer', bg = 'Light Blue')
    text2.grid(column = 3, row = 0)

    #score receive by player
    def Score():
        scr['text'] = 'Score:', str(score)
        window2.after(1000, Score)

    scr = Label(window2, text = '00', bg = 'Light Blue')
    scr.grid(column = 0, row = 1)
    Score()

    # def update_time():
    #     start = time.localtime()
    #     sec = start.tm_sec - koniec.tm_sec
    #     min = start.tm_min - koniec.tm_min
    #
    #     if min < 10:
    #         if sec < 10:
    #             lbl['text'] = ('0', min, ":", '0', sec)
    #         else:
    #             lbl['text'] = ('0', min, ":", sec)
    #     else:
    #         lbl['text'] = min, ':', sec
    #
    #     window2.after(1000, update_time)
    #
    # koniec = time.localtime()
    # lbl = Label(window2, text = '00:00', bg = 'Light Blue')
    # lbl.grid(column = 1, row = 0)
    # update_time()

    canvas = tk.Canvas(window2, width='400', height='400')
    canvas.configure(bg='light blue')
    canvas.grid(column = 1, row = 1)
    # canvas.pack()

    # make area
    class area():
        def __init__(self):
            self.width = int(width)
            self.height = int(height)
            self.Draw_area()

        def Draw_area(self):
            for i in range(self.width):
                for j in range(self.height):
                    canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, outline='black')

            # Robot's spawn point
            canvas.create_rectangle(0, 0, 20, 20, fill='Dark green')
            canvas.create_rectangle(380, 380, 400, 400, fill='Dark green')
            canvas.create_rectangle(380, 0, 400, 20, fill='light yellow')
            canvas.create_rectangle(0, 380, 20, 400, fill='light yellow')

    # make robot
    class robot():
        def __init__(self, hp, x, y, color, player):
            self.width = int(width)
            self.height = int(height)
            self.verctor_move = [1, 0]  # initial vector
            self.body = [x, y]  # initial cords of body
            self.size = size
            self.hp = hp
            self.Robot = False
            self.Player = bool(player)
            self.color = color


        def Attack(self):
            self.hp -= 10
            if self.hp > 0:
                canvas.delete(self.Hp)
                self.Hp = canvas.create_text((self.body[0] + 10, self.body[1] + 10), text=self.hp)
            elif self.hp <= 0 and self.Player == False:
                canvas.delete(self.robot, self.Hp)
                self.new_robot(100, (rn.randint(1, 19) * size), (rn.randint(1, 19) * size))
            elif self.hp <= 0:
                canvas.delete(self.robot, self.Hp)


        def drawRobot(self):
            if self.hp > 0:
                if self.Robot == False:  # visible a robot
                    self.robot = canvas.create_rectangle(self.body[0], self.body[1], self.body[0] + size,
                                                         self.body[1] + size, fill=self.color)
                    self.Hp = canvas.create_text((self.body[0] + 10, self.body[1] + 10), text=self.hp)
                    self.Robot = True
                elif self.Robot == True:
                    canvas.delete(self.robot, self.Hp)
                    self.robot = canvas.create_rectangle(self.body[0], self.body[1], self.body[0] + size,
                                                         self.body[1] + size, fill=self.color)
                    self.Hp = canvas.create_text((self.body[0] + 10, self.body[1] + 10), text=self.hp)
            elif self.hp < 0 and self.Player == False:
                canvas.delete(self.robot, self.Hp)
                self.body = [400, 400]
            elif self.hp < 0:
                canvas.delete(self.robot, self.Hp)


        def move(self):
            self.body[0] = self.body[0] + (self.verctor_move[0] * size)
            self.body[1] = self.body[1] + (self.verctor_move[1] * size)
            self.drawRobot()

        def new_robot(self, hp, x, y):
            if self.hp <= 0:
                self.Robot = False
                self.hp = hp
                self.body = [x, y]
                self.drawRobot()

        # change initial vector
        def move_up(self):
            if self.body[1] > 0:
                self.verctor_move = [0, -1]
            else:
                self.verctor_move = [0, 0]

        def move_down(self):
            if self.body[1] < 380:
                self.verctor_move = [0, 1]
            else:
                self.verctor_move = [0, 0]

        def move_right(self):
            if self.body[0] < 380:
                self.verctor_move = [1, 0]
            else:
                self.verctor_move = [0, 0]

        def move_left(self):
            if self.body[0] > 0:
                self.verctor_move = [-1, 0]
            else:
                self.verctor_move = [0, 0]

    def Game():
        area()
        # player RObocop - ROBPL
        # computer Robocop - ROBIT
        ROBPL = robot(100, 0, 0, 'Blue', True)
        ROBIT = robot(100, (rn.randint(1, 19) * size), (rn.randint(1, 19) * size), 'Red', False)


        def move():
            ROBPL.move()
            ROBIT.move()

        def moveRight(event):
            if ROBPL.body[0] != (ROBIT.body[0] - 20) or ROBPL.body[1] != ROBIT.body[1]:
                ROBPL.move_right()
                ROBPL.move()
            else:
                ROBIT.Attack()
                global score
                score += 10
                ROBPL.drawRobot()


        def moveLeft(event):
            if ROBPL.body[0] != ((ROBIT.body[0] + 20)) or ROBPL.body[1] != ROBIT.body[1]:
                ROBPL.move_left()
                ROBPL.move()
            else:
                ROBIT.Attack()
                global score
                score = score + 10
                ROBPL.drawRobot()

        def moveUp(event):
            if ROBPL.body[0] != ROBIT.body[0] or ROBPL.body[1] != (ROBIT.body[1] + 20):
                ROBPL.move_up()
                ROBPL.move()
            else:
                ROBIT.Attack()
                global score
                score = score + 10
                ROBPL.drawRobot()

        def moveDown(event):
            if ROBPL.body[0] != ROBIT.body[0] or ROBPL.body[1] != (ROBIT.body[1] - 20):
                ROBPL.move_down()
                ROBPL.move()
            else:
                ROBIT.Attack()
                global score
                score = score + 10
                ROBPL.drawRobot()

        # set keybord
        window2.after(speed, move)
        window2.bind_all("<KeyPress-Left>", moveLeft)
        window2.bind_all("<KeyPress-Right>", moveRight)
        window2.bind_all("<KeyPress-Up>", moveUp)
        window2.bind_all("<KeyPress-Down>", moveDown)

    if __name__ == '__main__':
        Game()
    window2.mainloop()


# make a Menu
def menu():
    text = Label(window, text='Robocop', fg='Black', bg='Light blue')
    text.config(font=('Courier', 80))
    text.grid(row=0, column=0, padx=140, pady=40)

    fight = Button(window, text='Fight', fg='Black', bg='Light blue', width=34, command=game)
    fight.grid(row=1, column=0)


menu()

#wypisywanie punktow na ekranie
#sztuczna inteligencja
#robot pojawia sie i porusza w kierunku gracza
#lvl zwieksza sie poziom computera
#czas
#rundy - konczy sie po zabiciu 5 przeciwnikow
#po 3 rundach jest boss 3Xstaty zwyklego IT


window.mainloop()