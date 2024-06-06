
FALL = -38              # нижнее значение КСНС, после которого система слабая   #
HARD = 10               # верхнее значение КСНС, после которого система сильная #
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
    Второй элемент  - сам коэффициент"""

    ksns = 0
    if any(i == 0 for i in lst): return [-1, ksns]           # Тест некорректен (пропущен квадрат)
    ksns = ((lst[1] + lst[2] + lst[3] + lst[4] + lst[5] - 5*lst[0])/lst[0]) * 100
    if(ksns < FALL): return [2, ksns]
    elif(ksns > HARD): return [1, ksns]
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
    if peakIndex < 3:
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


def gentype(lst1, lst2):
    nerve1 = testKSNS(lst1)
    nerve2 = testKSNS(lst2)
    graph1 = testTypes(lst1)
    graph2 = testTypes(lst2)
    nerveString = "\n==================== Ведущая рука ====================\n"

    match nerve1[0]:
        case -1:
            nerveString += "Тест некорректен (кажется в какой-то момент вы ничего не нажимали)\n"
        case 0:
            nerveString += f"Средняя нервная система\nКоэффициент силы нервной системы = {str(nerve1[1])}\n"
        case 1:
            nerveString += "Сильная нервная система\nКоэффициент силы нервной системы = {str(nerve1[1])}\n"
        case 2:
            nerveString += "Слабая нервная система\nКоэффициент силы нервной системы = {str(nerve1[1])}\n"

    nerveString += "Тип графика: "

    match graph1:
        case -1:
            nerveString += "Тест некорректен (кажется в какой-то момент вы ничего не нажимали)\n"
        case 0:
            nerveString += """Ровный тип. Максимальный темп удерживается примерно на одном уровне
в течение всего времени работы. Этот тип кривой  характеризует нервную
систему испытуемого как нервную  систему  средней силы"""
        case 1:
            nerveString += """Выпуклый тип. Темп нарастает  до  максимального  в  первые 10-15 сек.
работы; в последующем, к 25-30 сек., он может снизиться ниже исходного
уровня (т.е. наблюдавшегося в первые 5  сек.  работы). Этот тип кривой
свидетельствует о наличии испытуемого сильной нервной системы."""
        case 2:
            nerveString += """Вогнутый тип: первоначальное снижение максимального  темпа сменяется
затем кратковременным возрастанием темпа до исходного уровня. Вследствие
способности к кратковременной мобилизации такие испытуемые относятся также
к группе лиц со средне-слабой нервной системой."""
        case 3:
            nerveString += """Нисходящий тип: максимальный темп снижается уже со второго 5-сек. 
отрезка и остается на сниженном уровне в течение всей работы. Этот тип
свидетельствует о слабости нервной системы испытуемого."""
        case 4:
            nerveString += """Промежуточный тип:  темп  работы  снижается  после  первых 10-15 сек.
Этот тип расценивается как промежуточный между средней и слабой силой
нервной системы - средне-слабая нервная система."""

    nerveString += "\n==================== Другая рука ====================\n"

    match nerve2[0]:
        case -1:
            nerveString += "Тест некорректен (кажется в какой-то момент вы ничего не нажимали)\n"
        case 0:
            nerveString += f"Средняя нервная система\nКоэффициент силы нервной системы = {str(nerve1[1])}\n"
        case 1:
            nerveString += "Сильная нервная система\nКоэффициент силы нервной системы = {str(nerve1[1])}\n"
        case 2:
            nerveString += "Слабая нервная система\nКоэффициент силы нервной системы = {str(nerve1[1])}\n"

    nerveString += "Тип графика: "

    match graph2:
        case -1:
            nerveString += "Тест некорректен (кажется в какой-то момент вы ничего не нажимали)\n"
        case 0:
            nerveString += """Ровный тип. Максимальный темп удерживается примерно на одном уровне
в течение всего времени работы. Этот тип кривой  характеризует нервную
систему испытуемого как нервную  систему  средней силы"""
        case 1:
            nerveString += """Выпуклый тип. Темп нарастает  до  максимального  в  первые 10-15 сек.
работы; в последующем, к 25-30 сек., он может снизиться ниже исходного
уровня (т.е. наблюдавшегося в первые 5  сек.  работы). Этот тип кривой
свидетельствует о наличии испытуемого сильной нервной системы."""
        case 2:
            nerveString += """Вогнутый тип: первоначальное снижение максимального  темпа сменяется
затем кратковременным возрастанием темпа до исходного уровня. Вследствие
способности к кратковременной мобилизации такие испытуемые относятся также
к группе лиц со средне-слабой нервной системой."""
        case 3:
            nerveString += """Нисходящий тип: максимальный темп снижается уже со второго 5-сек. 
отрезка и остается на сниженном уровне в течение всей работы. Этот тип
свидетельствует о слабости нервной системы испытуемого."""
        case 4:
            nerveString += """Промежуточный тип:  темп  работы  снижается  после  первых 10-15 сек.
Этот тип расценивается как промежуточный между средней и слабой силой
нервной системы - средне-слабая нервная система."""

    return nerveString






