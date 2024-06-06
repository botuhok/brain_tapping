from datetime import datetime, timedelta
from images import *                                              # модуль с изображениями
import os
from PIL import ImageTk
# import sys
import tkinter as tk
# from tkinter import ttk


res_dir = os.path.abspath('res')

RELAX1      = 5                                                        # время отдыха сразу после первого теста
RELAX2      = 3                                                        # сколько секунд висит поздравление
RELAX3      = 10                                                       # сколько секунд висят результаты
TESTSECONDS = 6                                                        # сколько секунд идёт сбор теппинга
SAFETIMER   = 60000
               
class windows(tk.Tk):
    # ОБЩИЕ НАСТРОЙКИ ОКНА
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Tapping Test")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.attributes('-fullscreen', True)                                   # на весь экран
        self.index = 0
        self.nextStep = False
        self.secondTestEnd = False                                             # для окончания теста второй руки, чтобы перейти к результатам 
        self.safeTimer = 0                                                     # Если SAFETIMER миллисекунд ничего не происходит - вернуться к старту

        # слой на котором будут отображаться изображения
        self.bg_canvas = tk.Canvas(self, width = WIDTH, height= HEIGHT, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)


    def eraseAll(self):
        pass
        



############################################################ ОБРАБОТКА НАЖАТИЙ ##################################################################
    def returnKey(self, event):
        # Если для перехода к следующему шагу нужно нажатие Enter
         # print("[*] Нажатие Enter!")
         self.nextStep = True

    def leftKey(self, event):
        """ НАЖАТИЕ КНОПКИ ВЛЕВО """
        if self.index > 0:
            self.index -= 1
        else:
            self.index = self.indexMax

    def rightKey(self, event):
        """ НАЖАТИЕ КНОПКИ ВПРАВО """
        if self.index < self.indexMax:
            self.index += 1
        else:
            self.index = 0

    def countPress(self, event):
        """ ЗАПОЛНЯЕТ 6 ЭЛЕМЕНТОВ self.counter ПО ВРЕМЕНИ """
        if(self.time//100 >= 5 * TESTSECONDS//6):
            self.counter[0] += 1
        elif(self.time//100 >= 4 * TESTSECONDS//6):
            self.counter[1] += 1
        elif(self.time//100 >= 3 * TESTSECONDS//6):
            self.counter[2] += 1
        elif(self.time//100 >= 2 * TESTSECONDS//6):
            self.counter[3] += 1
        elif(self.time//100 >= TESTSECONDS//6):
            self.counter[4] += 1
        elif(self.time//100 < TESTSECONDS//6):
            self.counter[5] += 1


################################################################ СТРАНИЦЫ ###############################################################
    def startpage(self):
        """ НАЧАЛЬНАЯ СТРАНИЦА С МИГАНИЕМ "НАЖМИТЕ КРАСНУЮ КНОПКУ" """
        self.info = ["ВОЗРАСТ", "ПОЛ", "", 0, 0]                                                         # Здесь копится вся информация из меню и количества нажатий
        self.bg = [ImageTk.PhotoImage(img1_1), ImageTk.PhotoImage(img1_2)]
        if(self.nextStep == False):
            if self.index == 0:
                self.index = 1
            elif self.index == 1:
                self.index = 0
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.bind('<KeyPress-Return>', self.returnKey)
            self.after(500, self.startpage)
        else:                                                                   # переход на страницу выбора возраста
            print("[*] -------> Выбор возраста")
            self.index = 4
            self.nextStep = False
            self.agepage()

    
    def agepage(self):
        """ ВЫБОР ВОЗРАСТА """
        self.bg = [ImageTk.PhotoImage(img2_1),
                   ImageTk.PhotoImage(img2_2),
                   ImageTk.PhotoImage(img2_3),
                   ImageTk.PhotoImage(img2_4),
                   ImageTk.PhotoImage(img2_5),
                   ImageTk.PhotoImage(img2_6),
                   ImageTk.PhotoImage(img2_7),
                   ImageTk.PhotoImage(img2_8),
                   ]
        # расшифровка пунктов меню
        description = ("10-12", "13-14", "15-17", "18-24", "25-34", "35-44", "45-54", "55+")

        self.indexMax = len(self.bg) - 1

        if(self.nextStep == False):    # Если Enter не нажат
            self.safeTimer += 1                                                   # увеличивает таймер, который вернёт к старту, если SAFETIMER миллисекунд ничего не нажат
            self.bind('<Left>', self.leftKey)                                            # биндим клавиши влево и вправо
            self.bind('<Right>', self.rightKey)
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')  # переключаем фон, если изменился индекс клавишами
            self.bind('<KeyPress-Return>', self.returnKey)                               # к следующему этапу, если нажат Enter (nextStep становится True)
            self.after(1, self.agepage)                                                  # в цикле на этом этапе пока не нажат Enter
        else:
            self.info[0] = description[self.index]                                       # записали выбранный возраст
            print("[*] -------> Выбор пола")                                             # Переход к выбору пола
            self.index = 0
            self.nextStep = False
            self.malepage()

    def malepage(self):
        """ ВЫБОР ПОЛА """
        self.bg = [ImageTk.PhotoImage(img3_1),
                   ImageTk.PhotoImage(img3_2)]

        # расшифровка пунктов меню
        description = ("Мужской", "Женский")
        self.indexMax = len(self.bg) - 1

        if(self.nextStep == False):
            self.bind('<Left>', self.leftKey)                                             # биндим кнопки влево-вправо
            self.bind('<Right>', self.rightKey)
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')   # меняем фон, если меняется index
            self.bind('<KeyPress-Return>', self.returnKey)                                # если нажимают Enter -> self.nextStep = True
            self.after(1, self.malepage)                                                  # в цикле пока self.nextStep == False
        else:
            self.info[1] = description[self.index]                                        # записали выбранный пол
            print("[*] -------> Есть ли дети?")                                           # переход к выбору детей
            self.nextStep = False
            self.index = 0
            if(self.info[1] == "Мужской" or self.info[0] in ("10-12", "13-14", "15-17")):    # для мужчин и женщин моложе 17 не переходим к вопросу о детях
                self.unbind('<Left>')                                                        # отключаем кнопки влево и вправо
                self.unbind('<Right>')
                self.tutorpage()
            else:
                self.childrenpage()


    def childrenpage(self):
        """ ЕСТЬ ЛИ ДЕТИ """
        self.bg = [ImageTk.PhotoImage(img4_1),
                   ImageTk.PhotoImage(img4_2)]
        self.indexMax = len(self.bg) - 1
        description = ("Есть дети", "Нет детей")

        if(self.nextStep == False):
            self.bind('<Left>', self.leftKey)                                             # биндим кнопки влево-вправо
            self.bind('<Right>', self.rightKey)
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.bind('<KeyPress-Return>', self.returnKey)
            self.after(1, self.childrenpage)
        else:
            self.info[2] = description[self.index]                                         # записали  есть ли дети
            print("[*] -------> Описание задачи")                                          # Переход к описанию задачи
            self.unbind('<Left>')                                                        # отключаем кнопки влево и вправо
            self.unbind('<Right>')
            self.nextStep = False
            self.index = 0
            self.tutorpage()


    def tutorpage(self):
        """ ОПИСАНИЕ ЗАДАЧИ 
        МИГАЕТ "НАЖМИТЕ КНОПКУ КОГДА БУДЕТЕ ГОТОВЫ """
        self.bg = [ImageTk.PhotoImage(img5_1),
                   ImageTk.PhotoImage(img5_2), ]
        if(self.nextStep == False):
            if self.index == 0: self.index = 1
            elif self.index == 1: self.index = 0
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.bind('<KeyPress-Return>', self.returnKey)
            self.after(500, self.tutorpage)
        else:                                                                                     # переход к подготовке таймера
            print("[*] -------> Подготовка к тесту")
            self.index = -1
            self.nextStep = False
            self.preTimer()


    def preTimer(self):
        """ ОБРАТНЫЙ ОТСЧЁТ ПЕРЕД ТЕСТОМ """
        self.bg = [ImageTk.PhotoImage(img6),
                   ImageTk.PhotoImage(img7),
                   ImageTk.PhotoImage(img8),
                   ImageTk.PhotoImage(img9),
                   ]
        self.indexMax = len(self.bg) - 1

        if (self.index <  self.indexMax):
            self.index += 1
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.after(900, self.preTimer)

        else:                                                                                     # переход к таймеру
            self.index = 0
            self.nextStep = False
             # предварительные настройки таймера
            self.timeNow = datetime.now()                                                         # время начала
            self.timeAfter = self.timeNow + timedelta(seconds=TESTSECONDS)                        # время окончания 
            self.time = TESTSECONDS * 100
            self.counter = [0, 0, 0, 0, 0, 0]                                                     # количество нажатий
            self.timerLabel = tk.Label(self.bg_canvas, font = ("Arial", 25))                      # настройки шрифта таймера
            self.timerLabel.pack(fill="both", expand=True)                                        # размещение таймера
            print("[*] -------> Начало теста (таймер)")
            self.timer()


    def timer(self):
        """ ТАЙМЕР """
        self.timerLabel.config(text = f"{self.time//100:02}:{self.time%100:02}")
        if self.timeNow != self.timeAfter:                                                       # пока время не истекло
            self.bind('<KeyPress-Return>', self.countPress)                                      # считаем нажатие Enter
            self.timeNow += timedelta(seconds=0.01)                                              # увеличиваем счётчик времени
            self.time -= 1                                                                       # уменьшаем счётчик таймера
            self.after(10,self.timer)
        else:
            self.timerLabel.destroy()
            self.index = 0
            self.nextStep = False
            if(not self.secondTestEnd):
                self.info[3] = self.counter
                self.counter = [0, 0, 0, 0, 0, 0]                                         # Обнуляем статистику нажатий при переходе к след.руке 
                self.relaxTime = RELAX1 
                print("[*] -------> Отдых")
                self.relax()
            else:
                self.info[4] = self.counter
                self.relaxTime = -1
                self.index = 0
                self.secondTestEnd = False
                print("[*] -------> Поздравляем!")
                self.congratulations()

    def relax(self):
        # ОТДЫХ ПОСЛЕ ПЕРВОГО ТЕСТА
        self.bg = [ImageTk.PhotoImage(img11),]                                               # пока тут одна статичная фотка!
        self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
        if(self.relaxTime > 0):
            self.relaxTime -= 1
            self.after(1000, self.relax)
        else:
            self.index = 0
            self.nextStep = False
            print("[*] -------> Переход к другой руке ")
            self.preSecondTest()

    def preSecondTest(self):
        self.bg = [ImageTk.PhotoImage(img12_1),
                   ImageTk.PhotoImage(img12_2), ]
        if(self.nextStep == False):
            if self.index == 0:
                self.index = 1
            elif self.index == 1:
                self.index = 0
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.bind('<KeyPress-Return>', self.returnKey)
            self.after(500, self.preSecondTest)
        else:                                                                   # переход на подготовку к таймеру
            print("[*] -------> Обратный отсчёт до следующего теста")
            self.index = -1
            self.nextStep = False
            self.secondTestEnd = True
            self.preTimer()

    def congratulations(self):
        self.bg = [ImageTk.PhotoImage(img17_1),
                   ImageTk.PhotoImage(img17_2), ]
        if(self.relaxTime < RELAX2 * 2):
            if self.index == 0: self.index = 1
            elif self.index == 1: self.index = 0
            self.relaxTime += 1
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.after(500, self.congratulations)
        else:
            print("[*] -------> Переход к результатам")
            self.relaxTime = 0
            self.result()

    def result(self):
        """ ВЫВОД РЕЗУЛЬТАТОВ НА ЭКРАН """
        self.resultLabel = tk.Label(self.bg_canvas, font = ("Arial", 25), bg="#16c8f5")                               # настройки шрифта результатов
        self.resultLabel.pack(fill="both", expand=True)                                                 # размещение результатов

        resultString = f"""Ваш возраст {self.info[0]}\nВаш пол {self.info[1]}\n{self.info[2]}\n
Результаты для первой руки {self.info[3]}\n
Результаты для второй руки {self.info[4]}\n
таймер настроен на {TESTSECONDS} секунд"""

        self.resultLabel.config(text = resultString)
        self.relaxTime = -1
        self.ending()

    def ending(self):
        """ ОПРЕДЕЛЯЕТ СКОЛЬКО ВИСЯТ НА ЭКРАНЕ РЕЗУЛЬТАТЫ """
        if(self.relaxTime < RELAX3):
            self.relaxTime += 1
            self.after(1000, self.ending)
        else:
            """ ВСЁ ОБНУЛЯЕМ И ПЕРЕХОДИМ В НАЧАЛО """
            self.index = 0
            self.relaxTime = 0
            self.counter = [0, 0, 0, 0, 0, 0]                                                     # количество нажатий
            self.resultLabel.destroy()
            self.start()

    def start(self):
        """ ОПРЕДЕЛЯЕТ С ЧЕГО ВСЁ НАЧИНАЕТСЯ """ 
        self.startpage()



if __name__ == "__main__":
    testObj = windows()
    testObj.start()
    testObj.mainloop()
