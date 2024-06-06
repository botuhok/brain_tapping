# v 0.6 (02/06/2024)
# Теппинг тест по Ильину для raspberry.
# на основе статьи https://cpd-program.ru/methods/tt.htm
# 
# Внутри модуля gentype настраивается алгоритм расчета (через
# коэффициент силы или ориентируясь на силу перепада в графике). Результат выводится в 
# виде png файла и графиков по двум рукам. Внутри gentype также есть настройка того как
# следует анализировать результат (по среднему с двух рук или только по правой).
#  - Чтобы не раздувать код, кнопки GPIO через системные вызовы эмулируют работу обычной клавиатуры
#    Работа кнопок должна быть прописана в файле /boot/firmware/config.txt в следующем формате!
#     dtoverlay=gpio-key,gpio=25,active_low=1,gpio_pull=up,keycode=105       # LEFT KEY TO 25 GPIO
#     dtoverlay=gpio-key,gpio=23,active_low=1,gpio_pull=up,keycode=106       # RIGHT KEY TO 23 GPIO
#     dtoverlay=gpio-key,gpio=18,active_low=1,gpio_pull=up,keycode=28        # RED KEY TO 18 GPIO

# Определяет на чём запускается скрипт. False - ПК, True - RaspberryPi
RPIRUN = False

#*********************************************************************************
######################### ВСЕ ОСНОВНЫЕ НАСТРОЙКИ СКРИПТА ТУТ #####################
RELAX1      = 10         # время отдыха (sec) сразу после первого теста          #
RELAX2      = 5          # сколько висит поздравление (sec)                      #
RELAX3      = 30         # сколько висят результаты (sec)                        # 
TESTSECONDS = 30         # сколько идёт сбор теппинга (sec)                      #
SAFETIMER   = 2          # через сколько минут скидывать в начало                #
MP3FILE = "vulfpeck.mp3" # имя файла, который будет проигрываться при тесте      #
##################################################################################
#*********************************************************************************


from datetime import datetime, timedelta
from gentype import getImage, getKSNS
from gpiozero import LED
from images import *                                 # модуль с изображениями
import logging
from logging.handlers import RotatingFileHandler
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
from PIL import ImageTk
import tkinter as tk
import vlc



############################ НАСТРОЙКИ ДИОДОВ GPIO #############################
if RPIRUN:
    LED_RED = LED(17)      # pin 11 по порядку
    LED_LEFT = LED(9)      # pin 21
    LED_RIGHT = LED(22)    # pin 15

############################ ЭТИ НАСТРОЙКИ ЛУЧШЕ НЕ ТРОГАТЬ ###################
DEBUG       = True      # выводит служебную инфу на экран                     #
USERS       = 0         # собирает количество пользователей                   #
BADUSERS    = 0         # собирает количество пользователей, бросивших тест   # 
TIMEDELTA   = 15        # ms на один тик (для таймера)                        #
TIMERSIZE   = 200       # размер шрифта таймера                               #
SAFETIMER  *= 10500     # переводим минуты в ms                               #

############################ ЛОГИ #############################################
rfh = RotatingFileHandler(
        filename = "tapping.log",
        mode = "a",
        maxBytes = 5*1024*1024)
logging.basicConfig(level=logging.INFO, handlers = [rfh])


               
class windows(tk.Tk):
    global USERS                 # считает количество пользователей
    global BADUSERS              # считает количество пользователей, бросивших тест
    def __init__(self, *args, **kwargs):
        # ОБЩИЕ НАСТРОЙКИ ОКНА
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Tapping Test")
        self.geometry(f"{WIDTH}x{HEIGHT}")                        # ширину и высоту берём из images.py
        self.attributes('-fullscreen', True)                                   # на весь экран
        self.bg_canvas = tk.Canvas(self, width = WIDTH, height= HEIGHT, highlightthickness=0)
        # self.bg_canvas = tk.Canvas(self, width = 640, height= 480, highlightthickness=0)
        self.delta = 1000//TIMEDELTA                                           # заранее считаем тики для таймера
        self.player = vlc.MediaPlayer(MP3FILE)
        self.eraseAll()



    def eraseAll(self):
        # Сбрасывает всё к чертям собачьим
        self.bg_canvas.destroy()
        self.bg_canvas = tk.Canvas(self, width = WIDTH, height= HEIGHT, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg = []
        self.bg.clear()
        self.bg_canvas.create_image(0, 0, image = ImageTk.PhotoImage(img10), anchor='nw')
        self.info = ["ВОЗРАСТ", "ПОЛ", "", 0, 0]                # Здесь копится вся информация из меню и количества нажатий
        self.nextStep = False                                                  # Определяет нужно ли перейти к следующему шагу
        self.secondTestEnd = False                                             # для окончания теста второй руки, чтобы перейти к результатам 
        self.index = 0                                                         # перемещается по списку изображений
        self.safeTimer = 0                                                     # Если SAFETIMER миллисекунд ничего не происходит - вернуться к старту
        self.counter = [0, 0, 0, 0, 0, 0]                           # собирает нажатия красной кнопки
        if RPIRUN:
            LED_LEFT.off()                                                         # выключаем левый диод
            LED_RED.off()                                                          # выключаем красный диод
            LED_RIGHT.off()                                                        # выключаем правый диод

    def reset(self):
        # вызывается, если safeTimer превысил значение SAFETIMER (когда пользователь забил на тест)
        global BADUSERS
        global USERS
        logging.warning(f"{datetime.now():%Y-%m-%d %H:%M:%S} : Пользователь #{USERS} начал тест и не закончил")
        if(USERS > 0): USERS -= 1
        BADUSERS += 1
        self.destroy()
        

############################################################ ОБРАБОТКА НАЖАТИЙ ##################################################################
    def returnKey(self, event):
        # Если для перехода к следующему шагу нужно нажатие Enter
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
            
    def upKey(self, event):
        """ НАЖАТИЕ КНОПКИ ВВЕРХ """
        logging.info(f"{datetime.now():%Y-%m-%d %H:%M:%S} : Пользователь #{USERS} нажал кнопку вверх и вернулся к началу")
        self.reset()

    def countPress(self, event):
        """ ЗАПОЛНЯЕТ 6 ЭЛЕМЕНТОВ self.counter ПО ВРЕМЕНИ """
        if RPIRUN:
            LED_RED.toggle()
        testTimeNow = self.time//self.delta
        if(testTimeNow >= 5 * TESTSECONDS//6):
            self.counter[0] += 1
        elif(testTimeNow >= 4 * TESTSECONDS//6):
            self.counter[1] += 1
        elif(testTimeNow >= 3 * TESTSECONDS//6):
            self.counter[2] += 1
        elif(testTimeNow >= 2 * TESTSECONDS//6):
            self.counter[3] += 1
        elif(testTimeNow >= TESTSECONDS//6):
            self.counter[4] += 1
        elif(testTimeNow < TESTSECONDS//6):
            self.counter[5] += 1


################################################################ СТРАНИЦЫ ###############################################################
    def startpage(self):
        """ НАЧАЛЬНАЯ СТРАНИЦА С МИГАНИЕМ "НАЖМИТЕ КРАСНУЮ КНОПКУ" """
        global USERS
        self.info = ["ВОЗРАСТ", "ПОЛ", "", 0, 0]                # Здесь копится вся информация из меню и количества нажатий
        self.bg = [ImageTk.PhotoImage(img1_1), ImageTk.PhotoImage(img1_2)]
        self.safeTimer = 0


        if(self.nextStep == False):
            if RPIRUN:
                LED_RED.toggle()                                                # мигаем красной кнопочкой
            if self.index == 0:
                self.index = 1
            elif self.index == 1:
                self.index = 0
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.bind('<KeyPress-Return>', self.returnKey)

            self.after(500, self.startpage)

        else:                                                                   # переход на страницу выбора возраста
            USERS += 1
            logging.info(f"{datetime.now():%Y-%m-%d %H:%M:%S} : ПОЛЬЗОВАТЕЛЬ #{USERS} НАЧАЛ РАБОТУ")
            self.index = 4
            self.nextStep = False
            if RPIRUN:
                LED_RED.off()                                                       # выключаем красный диод
            self.bind('<Left>', self.leftKey)                   # биндим клавиши влево и вправо
            self.bind('<Right>', self.rightKey)
            self.bind('<Up>', self.upKey)                   # биндим клавиши влево и вправо
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

        if(self.safeTimer > SAFETIMER):
            self.reset()
        if RPIRUN:
            if(self.safeTimer % 150 == 0):
                # мигаем левой и правой кнопками
                LED_RIGHT.toggle()
                LED_LEFT.toggle()

        if(self.nextStep == False):    # Если Enter не нажат
            self.safeTimer += 50       # увеличивает таймер, который вернёт к старту, если SAFETIMER миллисекунд ничего не нажат
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')  # переключаем фон, если изменился индекс клавишами
            self.after(50, self.agepage)                                                  # в цикле на этом этапе пока не нажат Enter

        else:
            if RPIRUN:
                LED_LEFT.off()                                                           # выключаем левый диод
                LED_RIGHT.off()                                                          # выключаем правый диод
            self.info[0] = description[self.index]                                       # записали выбранный возраст
            self.index = 0
            self.safeTimer = 0
            self.nextStep = False
            self.malepage()

    def malepage(self):
        """ ВЫБОР ПОЛА """
        self.bg = [ImageTk.PhotoImage(img3_1),
                   ImageTk.PhotoImage(img3_2)]

        # расшифровка пунктов меню
        description = ("Мужской", "Женский")
        self.indexMax = len(self.bg) - 1

        if(self.safeTimer > SAFETIMER):
            self.reset()
        if RPIRUN:
            if(self.safeTimer % 150 == 0):
                # мигаем левой и правой кнопками
                LED_RIGHT.toggle()
                LED_LEFT.toggle()

        if(self.nextStep == False):
            self.safeTimer += 25       # увеличивает таймер, который вернёт к старту, если SAFETIMER миллисекунд ничего не нажат
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')    # меняем фон, если меняется index
            self.after(50, self.malepage)                                                      # в цикле пока self.nextStep == False
        else:
            if RPIRUN:
                LED_LEFT.off()                                                                           # выключаем левый диод
                LED_RIGHT.off()                                                                          # выключаем правый диод
            self.info[1] = description[self.index]                                                       # записали выбранный пол
            self.safeTimer = 0
            self.nextStep = False
            self.index = 0
            if(self.info[1] == "Мужской" or self.info[0] in ("10-12", "13-14", "15-17")):    # для мужчин и женщин моложе 17 не переходим к вопросу о детях
                self.unbind('<Left>')                                                        # отключаем кнопки влево и вправо
                self.unbind('<Right>')
                self.unbind('<Up>')                                                          # отключаем кнопку вверх
                self.tutorpage()
            else:
                self.childrenpage()


    def childrenpage(self):
        """ ЕСТЬ ЛИ ДЕТИ """
        self.bg = [ImageTk.PhotoImage(img4_1),
                   ImageTk.PhotoImage(img4_2)]
        self.indexMax = len(self.bg) - 1
        description = ("Есть дети", "Нет детей")

        if(self.safeTimer > SAFETIMER):
            self.reset()
        if RPIRUN:
            if(self.safeTimer % 150 == 0):
                # мигаем левой и правой кнопками
                LED_RIGHT.toggle()
                LED_LEFT.toggle()


        if(self.nextStep == False):
            self.safeTimer += 25
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.after(50, self.childrenpage)
        else:
            self.info[2] = description[self.index]                                         # записали  есть ли дети
            self.unbind('<Left>')                                                        # отключаем кнопки влево и вправо
            self.unbind('<Right>')
            self.unbind('<Up>')                                                          # отключаем кнопку вверх
            if RPIRUN:
                LED_LEFT.off()                                                                           # выключаем левый диод
                LED_RIGHT.off()                                                                          # выключаем правый диод
            self.nextStep = False
            self.safeTimer = 0
            self.index = 0
            self.tutorpage()


    def tutorpage(self):
        """ ОПИСАНИЕ ЗАДАЧИ 
        МИГАЕТ "НАЖМИТЕ КНОПКУ КОГДА БУДЕТЕ ГОТОВЫ """
        self.bg = [ImageTk.PhotoImage(img5_1),
                   ImageTk.PhotoImage(img5_2), ]

        if(self.safeTimer > SAFETIMER):
            self.reset()

        if(self.nextStep == False):
            if RPIRUN:
                LED_RED.toggle()
            self.safeTimer += 100
            if self.index == 0: self.index = 1
            elif self.index == 1: self.index = 0
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.after(500, self.tutorpage)
        else:                                                                                     # переход к подготовке таймера
            if RPIRUN:
                LED_RED.on()
            self.index = -1
            self.safeTimer = 0
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
            # self.timeNow = datetime.now():%Y-%m-%d %H:%M:%S                                                         # время начала
            # self.timeAfter = self.timeNow + timedelta(seconds=TESTSECONDS)                        # время окончания 
            self.time = TESTSECONDS * self.delta
            self.counter = [0, 0, 0, 0, 0, 0]                                                    # количество нажатий
            self.timerLabel = tk.Label(self.bg_canvas, font = ("Arial", TIMERSIZE))          # настройки шрифта таймера
            self.timerLabel.pack(fill="both", expand=True)                                                  # размещение таймера

            ############################ ВИДЕОФАЙЛ ##########################################################
            # player = tkvideo("timer.mp4", self.timerLabel, loop = 1, size = (WIDTH,HEIGHT))
            # player.play()
            #################################################################################################

            ########################### АУДИОФАЙЛ ###########################################################
            self.player.play()

            self.bind('<KeyPress-Return>', self.countPress)                                      # считаем нажатие Enter
            self.timer()


    def timer(self):
        """ ТАЙМЕР """
        self.timerLabel.config(text = f"{self.time//self.delta:02}:{self.time%self.delta:02}")
        # if self.timeNow != self.timeAfter and self.time > 0:                                     # пока время не истекло
        #     self.timeNow += timedelta(seconds=TIMEDELTA/1000)                                    # увеличиваем счётчик времени
            # self.time -= 1                                                                       # уменьшаем счётчик таймера
            # self.after(TIMEDELTA,self.timer)
        if self.time > 0:                                                                          # пока время не истекло
            self.time -= 1                                                                       # уменьшаем счётчик таймера
            self.after(TIMEDELTA,self.timer)
        else:
            self.timerLabel.destroy()
            self.player.stop()
            self.index = 0
            self.nextStep = False
            if(not self.secondTestEnd):
                logging.info(f"{datetime.now():%Y-%m-%d %H:%M:%S} : Тест первой руки окончен")
                self.info[3] = self.counter
                self.counter = [0, 0, 0, 0, 0, 0]                                         # Обнуляем статистику нажатий при переходе к след.руке 
                self.relaxTime = RELAX1 
                if RPIRUN:
                    LED_RED.off()
                self.unbind('<KeyPress-Return>')                                                        # отключаем кнопки влево и вправо
                self.relax()
            else:
                logging.info(f"{datetime.now():%Y-%m-%d %H:%M:%S} : Тест второй руки окончен")
                self.info[4] = self.counter
                self.relaxTime = -1
                self.index = 0
                if RPIRUN:
                    LED_RED.off()
                self.unbind('<KeyPress-Return>')                                                        # отключаем кнопки влево и вправо
                self.secondTestEnd = False
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
            self.bind('<KeyPress-Return>', self.returnKey)
            self.safeTimer = 0
            self.preSecondTest()

    def preSecondTest(self):
        # Окно перед тестом второй руки
        self.bg = [ImageTk.PhotoImage(img12_1),
                   ImageTk.PhotoImage(img12_2), ]

        if(self.safeTimer > SAFETIMER):
            self.reset()

        if(self.nextStep == False):
            if RPIRUN:
                LED_RED.toggle()
            self.safeTimer += 100
            if self.index == 0:
                self.index = 1
            elif self.index == 1:
                self.index = 0
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.after(500, self.preSecondTest)
        else:                                                                   # переход на подготовку к таймеру
            self.safeTimer = 0
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
            self.result()

    def result(self):
        """ ВЫВОД РЕЗУЛЬТАТОВ НА ЭКРАН """
############################################# Загрузка изображения с результатами
        imageName = getImage(self.info)
        imagePath = os.path.join(res_dir, imageName) 
        self.image = Image.open(imagePath)
        self.imageResult = self.image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.imageResult)
        self.bg_canvas.create_image(0, 0, image=self.photo, anchor='nw')

############################################ Создание и размещение графиков matplotlib
        points1 = [((index+1) * 5, num) for index, num in enumerate(self.info[3])]
        points2 = [((index+1) * 5, num) for index, num in enumerate(self.info[4])]

        # подсчёт среднего по обоим рукам
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
        
        # подписи к точкам для ведущей руки
        for x_val, y_val in points1:
            self.ax1.annotate(f'{y_val}', (x_val, y_val), textcoords="offset points", xytext=(0,7), ha='center')

        # подписи к точкам для второй руки
        for x_val, y_val in points2:
            self.ax2.annotate(f'{y_val}', (x_val, y_val), textcoords="offset points", xytext=(0,7), ha='center')

        # подписи к точкам для среднего значения по рукам
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
        self.fig_canvas.get_tk_widget().place(x=WIDTH - WIDTH//3 - WIDTH//20, y=HEIGHT//20)
        ksns = round(getKSNS(self.info), 2)

        logging.info(f" [>] Возраст: {self.info[0]}, Пол: {self.info[1]}, Дети: {self.info[2]}")
        logging.info(f" [>] Ведущая: {self.info[3]}, Вторая: {self.info[4]}")
        logging.info(f" [>] КСНС: {ksns}, загружено изображение {imageName}")

        if DEBUG:                           # инфа о загруженном изображении и среднем КСНС
            self.debugLabel = tk.Label(self.bg_canvas, font = ("Arial", 12))          # настройки шрифта таймера
            self.debugLabel.place(x = WIDTH - WIDTH//5, y = HEIGHT - HEIGHT//10)
            self.debugLabel.config(text = f'{imageName}\nКСНС: {ksns}')

        self.relaxTime = -1
        self.ending()

    def ending(self):
        """ ОПРЕДЕЛЯЕТ СКОЛЬКО ВИСЯТ НА ЭКРАНЕ РЕЗУЛЬТАТЫ """
        if(self.relaxTime < RELAX3):
            self.relaxTime += 1
            self.after(1000, self.ending)
        else:
            """ ВСЁ ОБНУЛЯЕМ И ПЕРЕХОДИМ В НАЧАЛО """
            logging.info(f" [*] С начала запуска успешно завершено {USERS} тестов, брошено {BADUSERS} тестов")
            self.index = 0
            self.relaxTime = 0
            self.counter = [0, 0, 0, 0, 0, 0]                                                     # количество нажатий
            self.fig_canvas.get_tk_widget().destroy()
            if DEBUG:
                self.debugLabel.destroy()
            self.start()

    def start(self):
        """ ОПРЕДЕЛЯЕТ С ЧЕГО ВСЁ НАЧИНАЕТСЯ """ 
        self.startpage()

if __name__ == "__main__":
    logging.info(f"{datetime.now():%Y-%m-%d %H:%M:%S} : ВКЛЮЧЕНИЕ ПРОГРАММЫ")
    while 1:
        try:
            testObj = windows()
            testObj.start()
            testObj.mainloop()
        except (Exception) as err:
            logging.warning(f"{datetime.now} : [!] Ошибка {type(err)} : {err} ({err.args})")
