
# на основе статьи Ильина
# https://cpd-program.ru/methods/tt.htm
from description import *

viaKSNS = True          # использовать для расчётов формулу КСНС                #
AVERAGE = True          # считать среднее с двух рук. Если False - только правую#
FALL = -26              # нижнее значение КСНС, после которого система слабая   #
MEDIUM = -13            # значение ниже которого система средне-слабая          #
HARD = 15               # верхнее значение КСНС, после которого система сильная #
DIFF = 10               # процент, на который изменяются показатели в квадрате  #
PEAKPOINT = 3           # до какого квадрата (включительно) ищем пик            #


def testKSNS(lst):
    """ Высчитываем коэффициент силы нервной системы по формуле Ильина
    Ориентируемся на значения FALL и HARD. Функция возвращает список 
    [int, double]. Первый элемент может принимать значения
    -1 - тест некорректен (в одном из квадратов пользователь ничего не нажимал)
    0 - средняя нервная система
    1 - сильная нервная система
    2 - слабая нервная система
    3 - средне-слабая система
    Второй элемент  - сам коэффициент"""

    ksns = 0
    if any(i == 0 for i in lst): return [-1, ksns]           # Тест некорректен (пропущен квадрат)

    ksns = ((lst[1] + lst[2] + lst[3] + lst[4] + lst[5] - 5*lst[0])/lst[0]) * 100

    if(ksns < FALL): return [2, ksns]
    if(ksns > HARD): return [1, ksns]
    if(FALL < ksns < MEDIUM): return [3, ksns]
    if(MEDIUM < ksns < HARD): return [0, ksns]

    else: return [0, ksns]

def testTypes(lst):
    """ Методика предусматривающая 5 типов, а не 3. Функция возвращает int. 
    -1 - тест некорректен (в одном из квадратов пользователь ничего не нажимал)
    0 - ровный тип
    1 - выпуклый тип
    2 - вогнутый тип
    3 - нисходящий тип
    4 - промежуточный тип
"""
    if any(i == 0 for i in lst): return -1       # Если тест некорректен
    peak = max(lst);              # определяем пик
    difference = (peak/100) * DIFF      # определяем что считать разницей

    difList = [(i - peak) for i in lst]                 # разница всех квадратов по сравнению с максимальным
    if all(abs(i) <= difference for i in difList):         # если изменения всех квадратов в пределах difference
        return 0

    peakIndex = lst.index(peak);                                 # определяем индекс пика
    difList = [(i - peak) for i in lst[peakIndex+1:-1]]    # список разниц от пика до -1 индекса
    if peakIndex < PEAKPOINT:
        if(all(abs(i) < difference for i in difList)):           # если все изменения в пределах difference
            return 1

    if any((i >= peak) for i in lst[peakIndex+1:]):
        return 2

    if (peakIndex == 0):
        if(any((abs(i) > difference) for i in difList)):
            return 3

    if (peakIndex >= 1):
        if all(i < peak for i in lst[peakIndex+1:]) and any(i + difference < peak for i in lst[peakIndex+1:]):
            return 4
    return 4                   # если ничего не подошло, ставим промежуточный тип


def getImage(info):
    """ Возвращает имя файла """
    if(viaKSNS):
        # Если выбрана опция работать через КСНС
        if AVERAGE:
            average = [round((info[3][i] + info[4][i])/2, 1) for i in range(6)]
        else:
            average = info[3]

        result = testKSNS(average)
        nerve = result[0]
    else:
        # Если используется наш алгоритм
        if AVERAGE:
            average = [round((info[3][i] + info[4][i])/2, 1) for i in range(6)]
        else:
            average = info[3]
        result = testTypes(average)
        nerve = result
        # Переводим тип графика в тип нервной системы
        if result == 2: nerve = 3
        elif result == 3: nerve = 2
        elif result == 4: nerve = 3


    match info[0]:
        case "10-12":
            if info[1] == "Мужской":
                match nerve:
                    case -1: return "10-12_Мужской_некорректен.png"
                    case 0: return "10-12_Мужской_средняя.png"
                    case 1: return "10-12_Мужской_сильная.png"
                    case 2: return "10-12_Мужской_слабая.png"
                    case 3: return "10-12_Мужской_средне-слабая.png"

            elif info[1] == "Женский":
                match nerve:
                    case -1:return "10-12_Женский_некорректен.png"
                    case 0: return "10-12_Женский_средняя.png"
                    case 1: return "10-12_Женский_сильная.png"
                    case 2: return "10-12_Женский_слабая.png"
                    case 3: return "10-12_Женский_средне-слабая.png"

        case "13-14":
            if info[1] == "Мужской":
                match nerve:
                    case -1:return "13-14_Мужской_некорректен.png"
                    case 0: return "13-14_Мужской_средняя.png"
                    case 1: return "13-14_Мужской_сильная.png"
                    case 2: return "13-14_Мужской_слабая.png"
                    case 3: return "13-14_Мужской_средне-слабая.png"

            elif info[1] == "Женский":
                match nerve:
                    case -1:return "13-14_Женский_некорректен.png"
                    case 0: return "13-14_Женский_средняя.png"
                    case 1: return "13-14_Женский_сильная.png"
                    case 2: return "13-14_Женский_слабая.png"
                    case 3: return "13-14_Женский_средне-слабая.png"

        case "15-17":
            if info[1] == "Мужской":
                match nerve:
                    case -1:return "15-17_Мужской_некорректен.png"
                    case 0: return "15-17_Мужской_средняя.png"
                    case 1: return "15-17_Мужской_сильная.png"
                    case 2: return "15-17_Мужской_слабая.png"
                    case 3: return "15-17_Мужской_средне-слабая.png"

            elif info[1] == "Женский":
                match nerve:
                    case -1:return "15-17_Женский_некорректен.png"
                    case 0: return "15-17_Женский_средняя.png"
                    case 1: return "15-17_Женский_сильная.png"
                    case 2: return "15-17_Женский_слабая.png"
                    case 3: return "15-17_Женский_средне-слабая.png"

        case "18-24":
            if info[1] == "Мужской":
                match nerve:
                    case -1:return "18-24_Мужской_некорректен.png"
                    case 0: return "18-24_Мужской_средняя.png"
                    case 1: return "18-24_Мужской_сильная.png"
                    case 2: return "18-24_Мужской_слабая.png"
                    case 3: return "18-24_Мужской_средне-слабая.png"

            elif info[1] == "Женский":
                if info[2] == "Нет детей":
                    match nerve:
                        case -1:return "18-24_Женский_нетДетей_некорректен.png"
                        case 0: return "18-24_Женский_нетДетей_средняя.png"
                        case 1: return "18-24_Женский_нетДетей_сильная.png"
                        case 2: return "18-24_Женский_нетДетей_слабая.png"
                        case 3: return "18-24_Женский_нетДетей_средне-слабая.png"
                elif info[2] == "Есть дети":
                    match nerve:
                        case -1:return "18-24_Женский_естьДети_некорректен.png"
                        case 0: return "18-24_Женский_естьДети_средняя.png"
                        case 1: return "18-24_Женский_естьДети_сильная.png"
                        case 2: return "18-24_Женский_естьДети_слабая.png"
                        case 3: return "18-24_Женский_естьДети_средне-слабая.png"

        case "25-34":
            if info[1] == "Мужской":
                match nerve:
                    case -1:return "25-34_Мужской_некорректен.png"
                    case 0: return "25-34_Мужской_средняя.png"
                    case 1: return "25-34_Мужской_сильная.png"
                    case 2: return "25-34_Мужской_слабая.png"
                    case 3: return "25-34_Мужской_средне-слабая.png"

            elif info[1] == "Женский":
                if info[2] == "Нет детей":
                    match nerve:
                        case -1:return "25-34_Женский_нетДетей_некорректен.png"
                        case 0: return "25-34_Женский_нетДетей_средняя.png"
                        case 1: return "25-34_Женский_нетДетей_сильная.png"
                        case 2: return "25-34_Женский_нетДетей_слабая.png"
                        case 3: return "25-34_Женский_нетДетей_средне-слабая.png"
                elif info[2] == "Есть дети":
                    match nerve:
                        case -1:return "25-34_Женский_естьДети_некорректен.png"
                        case 0: return "25-34_Женский_естьДети_средняя.png"
                        case 1: return "25-34_Женский_естьДети_сильная.png"
                        case 2: return "25-34_Женский_естьДети_слабая.png"
                        case 3: return "25-34_Женский_естьДети_средне-слабая.png"

        case "35-44":
            if info[1] == "Мужской":
                match nerve:
                    case -1:return "35-44_Мужской_некорректен.png"
                    case 0: return "35-44_Мужской_средняя.png"
                    case 1: return "35-44_Мужской_сильная.png"
                    case 2: return "35-44_Мужской_слабая.png"
                    case 3: return "35-44_Мужской_средне-слабая.png"

            elif info[1] == "Женский":
                if info[2] == "Нет детей":
                    match nerve:
                        case -1:return "35-44_Женский_нетДетей_некорректен.png"
                        case 0: return "35-44_Женский_нетДетей_средняя.png"
                        case 1: return "35-44_Женский_нетДетей_сильная.png"
                        case 2: return "35-44_Женский_нетДетей_слабая.png"
                        case 3: return "35-44_Женский_нетДетей_средне-слабая.png"
                elif info[2] == "Есть дети":
                    match nerve:
                        case -1:return "35-44_Женский_естьДети_некорректен.png"
                        case 0: return "35-44_Женский_естьДети_средняя.png"
                        case 1: return "35-44_Женский_естьДети_сильная.png"
                        case 2: return "35-44_Женский_естьДети_слабая.png"
                        case 3: return "35-44_Женский_естьДети_средне-слабая.png"

        case "45-54":
            if info[1] == "Мужской":
                match nerve:
                    case -1:return "45-54_Мужской_некорректен.png"
                    case 0: return "45-54_Мужской_средняя.png"
                    case 1: return "45-54_Мужской_сильная.png"
                    case 2: return "45-54_Мужской_слабая.png"
                    case 3: return "45-54_Мужской_средне-слабая.png"

            elif info[1] == "Женский":
                if info[2] == "Нет детей":
                    match nerve:
                        case -1:return "45-54_Женский_нетДетей_некорректен.png"
                        case 0: return "45-54_Женский_нетДетей_средняя.png"
                        case 1: return "45-54_Женский_нетДетей_сильная.png"
                        case 2: return "45-54_Женский_нетДетей_слабая.png"
                        case 3: return "45-54_Женский_нетДетей_средне-слабая.png"
                elif info[2] == "Есть дети":
                    match nerve:
                        case -1:return "45-54_Женский_естьДети_некорректен.png"
                        case 0: return "45-54_Женский_естьДети_средняя.png"
                        case 1: return "45-54_Женский_естьДети_сильная.png"
                        case 2: return "45-54_Женский_естьДети_слабая.png"
                        case 3: return "45-54_Женский_естьДети_средне-слабая.png"

        case "55+":
            if info[1] == "Мужской":
                match nerve:
                    case -1:return "55_Мужской_некорректен.png"
                    case 0: return "55_Мужской_средняя.png"
                    case 1: return "55_Мужской_сильная.png"
                    case 2: return "55_Мужской_слабая.png"
                    case 3: return "55_Мужской_средне-слабая.png"

            elif info[1] == "Женский":
                if info[2] == "Нет детей":
                    match nerve:
                        case -1:return "55_Женский_нетДетей_некорректен.png"
                        case 0: return "55_Женский_нетДетей_средняя.png"
                        case 1: return "55_Женский_нетДетей_сильная.png"
                        case 2: return "55_Женский_нетДетей_слабая.png"
                        case 3: return "55_Женский_нетДетей_средне-слабая.png"
                elif info[2] == "Есть дети":
                    match nerve:
                        case -1:return "55_Женский_естьДети_некорректен.png"
                        case 0: return "55_Женский_естьДети_средняя.png"
                        case 1: return "55_Женский_естьДети_сильная.png"
                        case 2: return "55_Женский_естьДети_слабая.png"
                        case 3: return "55_Женский_естьДети_средне-слабая.png"
def getKSNS(info):
    if AVERAGE:
        average = [round((info[3][i] + info[4][i])/2, 1) for i in range(6)]
    else:
        average = info[3]
    result = testKSNS(average)
    return result[1]
