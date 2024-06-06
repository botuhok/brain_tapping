# В вывод на графике добавить КСНС
# сделать генерацию возраста, пола и детей
from gentype import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk
from random import randint
from random import choice
import tkinter as tk

WIDTH=1920
HEIGHT=1080


# TESTS
def getTest():
    """ Генерирует рандомные результаты теппинг теста для одной руки """
    return [randint(28, 40), randint(28, 40), randint(28, 40), randint(28, 40), randint(25, 40), randint(25, 40)]

def testText():
    print(getKSNS(['10-12', 'Мужской', '', [32, 33, 37, 36, 36, 35], [34, 36, 34, 35, 36, 34]]))
    print(getKSNS(['10-12', 'Женский', '', [29, 27, 26, 25, 27, 28], [23, 20, 19, 20, 19, 20]]))
    print(getKSNS(['13-14', 'Мужской', '', [10, 15, 15, 14, 15, 15], [12, 13, 15, 16, 15, 16]]))
    print(getKSNS(['13-14', 'Женский', '', [27, 22, 32, 20, 35, 23], [27, 28, 27, 28, 27, 28]]))
    print(getKSNS(['15-17', 'Мужской', '', getTest(), getTest()]))
    print(getKSNS(['15-17', 'Женский', '',getTest(), getTest()]))

    print(getKSNS(['18-24', 'Мужской', '',getTest(), getTest()]))
    print(getKSNS(['18-24', 'Женский', 'Есть дети',getTest(), getTest()]))
    print(getKSNS(['18-24', 'Женский', 'Нет детей',getTest(), getTest()]))

    print(getKSNS(['25-34', 'Мужской', '',getTest(), getTest()]))
    print(getKSNS(['25-34', 'Женский', 'Есть дети',getTest(), getTest()]))
    print(getKSNS(['25-34', 'Женский', 'Нет детей',getTest(), getTest()]))

    print(getKSNS(['35-44', 'Мужской', '',getTest(), getTest()]))
    print(getKSNS(['35-44', 'Женский', 'Есть дети',getTest(), getTest()]))
    print(getKSNS(['35-44', 'Женский', 'Нет детей',getTest(), getTest()]))

    print(getKSNS(['45-54', 'Мужской', '',getTest(), getTest()]) )
    print(getKSNS(['45-54', 'Женский', 'Есть дети',getTest(), getTest()]))
    print(getKSNS(['45-54', 'Женский', 'Нет детей',getTest(), getTest()]))

    print(getKSNS(['55+', 'Мужской', '',getTest(), getTest()]))
    print(getKSNS(['55+', 'Женский', 'Есть дети',getTest(), getTest()]))
    print(getKSNS(['55+', 'Женский', 'Нет детей',getTest(), getTest()]))



# average = [round((info[3][i] + info[4][i])/2, 1) for i in range(6)]

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Test for Tapping Test")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.attributes('-fullscreen', True)
        self.bg_canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.nextStep = False
        self.start()

    def returnKey(self, event):
         self.nextStep = True

    def start(self):
        res_dir = os.path.abspath('res')
        ######### ГЕНЕРИРУЕМ РАНДОМНОГО ПЕРСОНАЖА ##########################################################################
        ages = ['25-34', '55+', '10-12', '13-14', '15-17', '18-24', '35-44']
        males = ['Мужской', 'Женский']
        childrens = ["Есть дети", "Нет детей"]
        self.info =[]
        self.info.append(choice(ages))
        self.info.append(choice(males))
        print(self.info[1], self.info[0])
        if self.info[1] == 'Женский' and self.info[0] in ('18-24', '25-34', '45-54', '55+'):
            self.info.append(choice(childrens))
        else:
            self.info.append('')
        # В редких случаях choice не отрабатывает, тогда вручную
        if self.info[1] == 'Женский' and self.info[0] in ('18-24', '25-34', '45-54', '55+') and self.info[2] == '':
            self.info[2] = 'Есть дети'

        self.info.append(getTest())
        self.info.append(getTest())
        print(self.info)

        #######################################################################################################################

        # Загрузка изображения с результатами
        imageName = getImage(self.info)
        imagePath = os.path.join(res_dir, imageName) 
        self.image = Image.open(imagePath)
        self.imageResult = self.image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.imageResult)
        self.bg_canvas.create_image(0, 0, image=self.photo, anchor='nw')

# Создание и размещение графиков matplotlib
        points1 = [((index+1) * 5, num) for index, num in enumerate(self.info[3])]
        points2 = [((index+1) * 5, num) for index, num in enumerate(self.info[4])]
        average = [round((self.info[3][i] + self.info[4][i])/2, 1) for i in range(6)]
        points3 = [((index+1) * 5, num) for index, num in enumerate(average)]
        fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(4, 6), dpi = WIDTH//15, facecolor='none')
        x1, y1 = zip(*points1)
        x2, y2 = zip(*points2)
        x3, y3 = zip(*points3)
        self.ax1.plot(x1, y1, color='red')                                # цвет графика
        self.ax2.plot(x2, y2, color='blue')
        self.ax3.plot(x3, y3, color='green')
        self.ax1.set_yticklabels([])                                      # скрыть надписи на оси Y
        self.ax2.set_yticklabels([])
        self.ax3.set_yticklabels([])
        
        # подписи к точкам
        for x_val, y_val in points1:
            self.ax1.annotate(f'{y_val}', (x_val, y_val), textcoords="offset points", xytext=(0,7), ha='center')

        for x_val, y_val in points2:
            self.ax2.annotate(f'{y_val}', (x_val, y_val), textcoords="offset points", xytext=(0,7), ha='center')
        for x_val, y_val in points3:
            self.ax3.annotate(f'{y_val}', (x_val, y_val), textcoords="offset points", xytext=(0,7), ha='center')

        self.ax1.set_title('Ведущая рука')
        self.ax2.set_title('Другая рука')
        self.ax3.set_title('Среднее значение')
        self.ax1.set_ylim(0, 55)
        self.ax2.set_ylim(0, 55)
        self.ax3.set_ylim(0, 55)
        self.ax1.grid(True)
        self.ax2.grid(True)
        self.ax3.grid(True)
        self.ax3.set_xlabel("Время")
        self.ax3.set_ylabel("Нажатия")
        fig = plt.gcf()
        fig.tight_layout()
        self.fig_canvas = FigureCanvasTkAgg(fig, self.bg_canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(x=WIDTH - WIDTH//4 - WIDTH//20, y=HEIGHT//20)
        self.imagenameLabel = tk.Label(self.bg_canvas, font = ("Arial", 12))          # настройки шрифта таймера
        self.imagenameLabel.place(x = WIDTH - WIDTH//5, y = HEIGHT - HEIGHT//10)
        self.imagenameLabel.config(text = f'{imageName}')
        self.bg_canvas.pack()












# testText()
runTests = windows()
runTests.mainloop()
