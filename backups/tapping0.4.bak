# Теппинг тест v0.4
# 30.05.2024
# - откорректирован тайминг для safeTimer для каждой СТРАНИЦЫ
# - добавлен модуль gentype с функциями testKSNS, testTypes для анализа результатов тестирования и функцией gentype 
#   для генерации текста анализа
# - добавлено проигрывание аудиофайла во время самого теста
# TODO: добавить кнопку вверх для сброса в начало, сделать вывод результата в виде фото, т.е. gentype должна возвращать
#       название файла, а не текст!

# Теппинг тест v0.3
# 06.05.2024
#  -  Добавлена константа TIMEDELTA для ускорения или замедления длительности секунд. Чем выше TIMEDELTA,
#     тем быстрее идёт время в таймере непосредственно во время теста. 
#  -  Добавлена работа со светодиодами красной кнопки и кнопок ВЛЕВО и ВПРАВО
#
#  - Чтобы не раздувать код, кнопки GPIO через системные вызовы эмулируют работу обычной клавиатуры
#    Работа кнопок должна быть прописана в файле /boot/firmware/config.txt в следующем формате!
#     dtoverlay=gpio-key,gpio=25,active_low=1,gpio_pull=up,keycode=105       # LEFT KEY TO 25 GPIO
#     dtoverlay=gpio-key,gpio=23,active_low=1,gpio_pull=up,keycode=106       # RIGHT KEY TO 23 GPIO
#     dtoverlay=gpio-key,gpio=18,active_low=1,gpio_pull=up,keycode=28        # RED KEY TO 18 GPIO

# Теппинг тест v0.2
# 13.04.2024
#   -  Добавлено логгирование в tapping.log, destroy окна и новое создание в случае, если пользователь забил на тест начав его
#   -  Добавлено подсчитывание пользователей закончивших тест и бросивших его.

######################### ВСЕ ОСНОВНЫЕ НАСТРОЙКИ СКРИПТА ТУТ ####################
RELAX1      = 10        # время отдыха (sec) сразу после первого теста          #
RELAX2      = 5         # сколько висит поздравление (sec)                      #
RELAX3      = 30        # сколько висят результаты (sec)                        # 
TESTSECONDS = 30        # сколько идёт сбор теппинга (sec)                      #
SAFETIMER   = 2         # через сколько минут скидывать в начало                #
MP3FILE = "vulfpeck.mp3" # имя файла, который будет проигрываться при тесте     #
#################################################################################


from datetime import datetime, timedelta
from gentype import gentype
from gpiozero import LED
from images import *                                 # модуль с изображениями
import logging
from logging.handlers import RotatingFileHandler
from PIL import ImageTk
import tkinter as tk
import vlc

############################ НАСТРОЙКИ ДИОДОВ GPIO #############################
LED_RED = LED(17)      # pin 11 по порядку
LED_LEFT = LED(9)      # pin 21
LED_RIGHT = LED(22)    # pin 15

################################################################################


USERS       = 0         # собирает количество пользователей                   #
BADUSERS    = 0         # собирает количество пользователей, бросивших тест   # 
TIMEDELTA   = 15        # ms на один тик (для таймера)                        #
TIMERSIZE   = 200       # размер шрифта таймера                               #
SAFETIMER  *= 10500     # переводим минуты в ms
# ЛОГИ
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
        # self.bg_canvas = tk.Canvas(self, width = WIDTH, height= HEIGHT, highlightthickness=0)
        self.bg_canvas = tk.Canvas(self, width = 640, height= 480, highlightthickness=0)
        self.delta = 1000//TIMEDELTA                                      # заранее считаем тики для таймера
        self.player = vlc.MediaPlayer(MP3FILE)
        self.eraseAll()



    def eraseAll(self):
        # Сбрасывает всё к чертям собачьим
        logging.info(f"{datetime.now()} : eraseAll")
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
        LED_LEFT.off()                                                         # выключаем левый диод
        LED_RED.off()                                                          # выключаем красный диод
        LED_RIGHT.off()                                                        # выключаем правый диод

    def reset(self):
        # вызывается, если safeTimer превысил значение SAFETIMER (когда пользователь забил на тест)
        global BADUSERS
        global USERS
        logging.warning(f"{datetime.now()} : Пользователь #{USERS} начал тест и не закончил")
        if(USERS > 0): USERS -= 1
        BADUSERS += 1
        # self.relaxTime = 10
        # self.eraseAll()
        # self.result()
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
        self.reset()

    def countPress(self, event):
        """ ЗАПОЛНЯЕТ 6 ЭЛЕМЕНТОВ self.counter ПО ВРЕМЕНИ """
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
            logging.info(f"{datetime.now()} : ПОЛЬЗОВАТЕЛЬ #{USERS} НАЧАЛ РАБОТУ")
            self.index = 4
            self.nextStep = False
            LED_RED.off()                                                       # выключаем красный диод
            self.bind('<Left>', self.leftKey)                   # биндим клавиши влево и вправо
            self.bind('<Right>', self.rightKey)
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
        if(self.safeTimer % 150 == 0):
            # мигаем левой и правой кнопками
            LED_RIGHT.toggle()
            LED_LEFT.toggle()

        if(self.nextStep == False):    # Если Enter не нажат
            self.safeTimer += 50       # увеличивает таймер, который вернёт к старту, если SAFETIMER миллисекунд ничего не нажат
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')  # переключаем фон, если изменился индекс клавишами
            self.after(50, self.agepage)                                                  # в цикле на этом этапе пока не нажат Enter

        else:
            LED_LEFT.off()                                                                           # выключаем левый диод
            LED_RIGHT.off()                                                                          # выключаем правый диод
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

        if(self.safeTimer % 150 == 0):
            # мигаем левой и правой кнопками
            LED_RIGHT.toggle()
            LED_LEFT.toggle()

        if(self.nextStep == False):
            self.safeTimer += 25       # увеличивает таймер, который вернёт к старту, если SAFETIMER миллисекунд ничего не нажат
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')   # меняем фон, если меняется index
            self.after(50, self.malepage)                                                  # в цикле пока self.nextStep == False
        else:
            LED_LEFT.off()                                                                           # выключаем левый диод
            LED_RIGHT.off()                                                                          # выключаем правый диод
            self.info[1] = description[self.index]                                                   # записали выбранный пол
            self.safeTimer = 0
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

        if(self.safeTimer > SAFETIMER):
            self.reset()

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
            LED_RED.toggle()
            self.safeTimer += 100
            if self.index == 0: self.index = 1
            elif self.index == 1: self.index = 0
            self.bg_canvas.create_image(0, 0, image = self.bg[self.index], anchor='nw')
            self.after(500, self.tutorpage)
        else:                                                                                     # переход к подготовке таймера
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
            # self.timeNow = datetime.now()                                                         # время начала
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
                logging.info(f"{datetime.now()} : Тест первой руки окончен")
                self.info[3] = self.counter
                self.counter = [0, 0, 0, 0, 0, 0]                                         # Обнуляем статистику нажатий при переходе к след.руке 
                self.relaxTime = RELAX1 
                LED_RED.off()
                self.unbind('<KeyPress-Return>')                                                        # отключаем кнопки влево и вправо
                self.relax()
            else:
                logging.info(f"{datetime.now()} : Тест второй руки окончен")
                self.info[4] = self.counter
                self.relaxTime = -1
                self.index = 0
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
        self.resultLabel = tk.Label(self.bg_canvas, font = ("Arial", 25), bg="#16c8f5")  # настройки шрифта результатов
        self.resultLabel.pack(fill="both", expand=True)                                                 # размещение результатов
        logging.info(f"{datetime.now()} : Тест окончен успешно {self.info}")
        nerveString = ""                                                                                # формируем строку описания
        nerveString = gentype(self.info[3], self.info[4])
        logging.info(f"Результат : {nerveString}")

        resultString = f"""Ваш возраст {self.info[0]}\nВаш пол {self.info[1]}\n{self.info[2]}\n
Результаты для первой руки {self.info[3]}\n
Результаты для второй руки {self.info[4]}\n
{nerveString}\n
"""

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
            logging.info(f"[*] С начала запуска успешно завершено {USERS} тестов, брошено {BADUSERS} тестов")
            self.index = 0
            self.relaxTime = 0
            self.counter = [0, 0, 0, 0, 0, 0]                                                     # количество нажатий
            self.resultLabel.destroy()
            self.start()

    def start(self):
        """ ОПРЕДЕЛЯЕТ С ЧЕГО ВСЁ НАЧИНАЕТСЯ """ 
        self.startpage()

if __name__ == "__main__":
    logging.info(f"{datetime.now()} : ВКЛЮЧЕНИЕ ПРОГРАММЫ")
    while 1:
        testObj = windows()
        testObj.start()
        testObj.mainloop()
