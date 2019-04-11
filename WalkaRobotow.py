#       Game
#   Robocop
#   By Kamil Gierlach
#   start date: 20 - 02 - 2019
#   last update: 07 - 04 - 2019
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
rd = 0 #round


def savescore(score):
    file = open("stats", "a")
    file.write(score)
    return


def game():
    window.destroy()
    window2 = tk.Tk()
    window2.title('Robocop')
    window2.configure(bg='Light blue')
    window2.geometry('600x450+200+200')

    text1 = Label(window2, text = 'Player', bg = 'Light Blue')
    text1.grid(column = 0, row = 0)

    text2 = Label(window2, text = '  Computer', bg = 'Light Blue')
    text2.grid(column = 6, row = 0)

    canvas = tk.Canvas(window2, width='400', height='400')
    canvas.configure(bg='light blue')
    canvas.grid(column = 1, columnspan = 4 , row = 1, rowspan = 10)



    # create area
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

    # create robot
    class robot():
        def __init__(self, hp, x, y, color, visible_player):
            self.width = int(width)
            self.height = int(height)
            self.vector_move = [1, 0]  # initial vector
            self.body = [x, y]  # initial cords of body
            self.size = size
            self.hp = hp
            self.Robot = False #visible robot on map
            self.visible_Player = bool(visible_player) #robot players or computer
            self.color = color
            self.damage = 0
            self.killed_enemies = 0

        def Statistic(self):
            self.hp_text = Label(window2, text='HP: ', bg='light blue')
            self.damage_text = Label(window2, text=('Damage:', str(self.damage)), bg='Light blue')
            if self.visible_Player == True:
                self.hp_text.configure(text = ('HP:', str(self.hp)))
                self.hp_text.grid(column=0, row=1)
                self.damage_text.grid(column=0, row=2)
            elif self.visible_Player == False:
                self.hp_text.configure(text = ('HP:', str(self.hp)))
                self.hp_text.grid(column=6, row=1)
                self.damage_text.grid(column=6, row=2)

        #create stopwatch
        def update_time(self):
            self.DTime = Label(window2, text='00', bg='Light blue')
            self.DTime.grid(column=3, row=0)
            koniec = time.localtime()
            sec = koniec.tm_sec - self.start.tm_sec
            min = koniec.tm_min - self.start.tm_min
            if min < 10:
                if sec < 10:
                    Time = '0', min, ':', '0', sec
                else:
                    Time = '0', min, ':', sec
            else:
                Time = min, ':', sec
            self.DTime['text'] = Time
            window2.after(1000, self.update_time)

        #round of the game - it changes when 5 enemies die
        def rd(self):
            global rd
            text3 = Label(window2, text=('Round:', rd), bg='light blue')
            text3.grid(column=2, columnspan=1, row=0)
            if self.killed_enemies % 5 == 0 and self.killed_enemies > 0:
                rd += 1
                text3['text'] = 'Round:', rd
            elif self.killed_enemies >= 0 and self.killed_enemies % 5 != 0:
                print('else')
                window2.after(1000, self.rd)

        #score receive by player
        def Score(self):
            self.scr = Label(window2, text=('Score:', score), bg='Light Blue')
            self.scr.grid(column=0, row=3)
            self.scr['text'] = 'Score:', str(score)
            window2.after(1000, self.Score)

        def draw_Stat(self):
            self.start = time.localtime()
            self.update_time()
            self.Statistic()
            self.Score()
            self.rd()

        def Attack(self):
            self.hp -= 10
            if self.hp > 0:
                canvas.delete(self.Hp)
                self.Hp = canvas.create_text((self.body[0] + 10, self.body[1] + 10), text=self.hp)
            elif self.hp <= 0 and self.visible_Player == False:
                canvas.delete(self.robot, self.Hp)
                self.new_robot(100, (rn.randint(1, 19) * size), (rn.randint(1, 19) * size))
                self.killed_enemies += 1
            elif self.hp <= 0:
                canvas.delete(self.robot, self.Hp)
                canvas.delete('all')
                savescore(score)
                end = Label(window2, text = 'Game Over', bg = 'light blue')
                end.grid(column = 1, columnspan = 4, row = 1, rowspan = 10)
            print(self.killed_enemies)


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
            elif self.hp < 0 and self.visible_Player == False:
                canvas.delete(self.robot, self.Hp)
                self.body = [400, 400]
            elif self.hp < 0:
                canvas.delete(self.robot, self.Hp)

        def move(self):
            self.body[0] = self.body[0] + (self.vector_move[0] * size)
            self.body[1] = self.body[1] + (self.vector_move[1] * size)
            self.drawRobot()

        #create new robot when copmuter die
        def new_robot(self, hp, x, y):
            if self.hp <= 0:
                self.Robot = False
                self.hp = hp
                self.body = [x, y]
                self.drawRobot()
        # change initial vector
        def move_up(self):
            if self.body[1] > 0:
                self.vector_move = [0, -1]
            else:
                self.vector_move = [0, 0]

        def move_down(self):
            if self.body[1] < 380:
                self.vector_move = [0, 1]
            else:
                self.vector_move = [0, 0]

        def move_right(self):
            if self.body[0] < 380:
                self.vector_move = [1, 0]
            else:
                self.vector_move = [0, 0]

        def move_left(self):
            if self.body[0] > 0:
                self.vector_move = [-1, 0]
            else:
                self.vector_move = [0, 0]

    class enemy(robot):
        def changeX(self):
            move = rn.randint(-1, 1)
            if self.body[0]==379 or self.body[0] == 1:
                move = 0
            return move

        def changeY(self):
            move = rn.randint(-1, 1)
            if self.body[1]==379 or self.body[0] == 1:
                move = 0
            return move

        def move(self):
            self.body[0] = self.body[0] + (self.changeX() * size)
            self.body[1] = self.body[1] + (self.changeY() * size)
            self.drawRobot()
            window2.after(1000, self.move)




    def Game():
        area()
        # player RObocop - ROBPL
        # computer Robocop - ROBIT
        ROBPL = robot(100, 0, 0, 'Blue', True)
        ROBIT = enemy(100, (rn.randint(1, 19) * size), (rn.randint(1, 19) * size), 'Red', False)
        ROBPL.draw_Stat()
        ROBIT.draw_Stat()

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

        def moveLeft(event):
            if ROBPL.body[0] != ((ROBIT.body[0] + 20)) or ROBPL.body[1] != ROBIT.body[1]:
                ROBPL.move_left()
                ROBPL.move()
            else:
                ROBIT.Attack()
                global score
                score = score + 10

        def moveUp(event):
            if ROBPL.body[0] != ROBIT.body[0] or ROBPL.body[1] != (ROBIT.body[1] + 20):
                ROBPL.move_up()
                ROBPL.move()
            else:
                ROBIT.Attack()
                global score
                score = score + 10

        def moveDown(event):
            if ROBPL.body[0] != ROBIT.body[0] or ROBPL.body[1] != (ROBIT.body[1] - 20):
                ROBPL.move_down()
                ROBPL.move()
            else:
                ROBIT.Attack()
                global score
                score = score + 10


        # set keybord
        window2.after(speed, move)
        window2.bind_all("<KeyPress-Left>", moveLeft)
        window2.bind_all("<KeyPress-Right>", moveRight)
        window2.bind_all("<KeyPress-Up>", moveUp)
        window2.bind_all("<KeyPress-Down>", moveDown)


    if __name__ == '__main__':
        Game()
    window2.mainloop()

def restore():
    file = open("history.ini", "r+")
    file = file.read()
    global score
    score = int(file)
    game()


# make a Menu
def menu():
    text = Label(window, text='Robocop', fg='Black', bg='Light blue')
    text.config(font=('Courier', 80))
    text.grid(row=0, column=0, padx=140, pady=40)

    fight = Button(window, text='Fight', fg='Black', bg='Light blue', width=34, command=lambda: game())
    fight.grid(row=1, column=0)
    restoreButton = Button(window, text="Restore", fg="black",bg='Light blue', width=34, command = restore)
    restoreButton.grid(row=2, column=0)

menu()

#sztuczna inteligencja
#robot pojawia sie i porusza w kierunku gracza
#lvl zwieksza sie poziom computera
#rundy - konczy sie po zabiciu 5 przeciwnikow
#po 3 rundach jest boss 3Xstaty zwyklego IT


window.mainloop()