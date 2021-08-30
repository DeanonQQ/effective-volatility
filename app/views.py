from django.shortcuts import render
import math
import pandas as pd
from sklearn.linear_model import LinearRegression


def index(request):
    # моделирование динамики по годам
    return render(request, "index.html")


def dinyear(request):
    # моделирование динамики по годам
    if request.method == 'POST':
        summa = float(request.POST['q'])
        perc = int(request.POST['w'])
        year = int(request.POST['e'])

        q = 1 + perc/100
        result = []
        for i in range(year):
            summ = summa * math.pow(q, i+1)
            result.append(round(summ, 3))
        
        data = {"in": [summa, perc, year], "re": result}
        return render(request, "dinyear.html", context=data)
    return render(request, "dinyear.html")


def rasvklad(request):
    if request.method == 'POST':
        summa = float(request.POST['q'])
        perc = float(request.POST['w'])
        day = int(request.POST['e'])

        result = summa * (perc / 100) * (day / 365)
        
        data = {"in": [summa, perc, day], "re": round(result,3)}
        return render(request, "rasvklad.html", context=data)
    return render(request, "rasvklad.html")


def rasfirst(request):
    if request.method == 'POST':
        summa = int(request.POST['q'])
        perc = int(request.POST['w'])
        year = int(request.POST['e'])

        q = 1 + perc/100

        itog = summa / math.pow(q, year)

        result = []
        for i in range(year):
            summ = itog * math.pow(q, i+1)
            result.append(round(summ, 3))
        
        data = {"in": [summa, perc, year], "ge": itog, "re": result}
        return render(request, "rasfirst.html", context=data)
    return render(request, "rasfirst.html")


def srokst(request):
    if request.method == 'POST':
        v = int(request.POST['q'])
        perc = int(request.POST['w'])
        v0 = int(request.POST['e'])

        q = 1 + perc/100
        result = []

        year = math.fabs((math.log(v) - math.log(v0)) / math.log(q)) - 1

        for i in range(math.ceil(year)):
            summ = v0 * math.pow(q, i+1)
            result.append(round(summ, 3))
        
        data = {"in": [v, perc, v0], "ge": math.ceil(year), "re": result}
        return render(request, "srokst.html", context=data)
    return render(request, "srokst.html")


def usdcalc(request):
    predict_curs = get_predict("usd_curs.xlsx")
    exchange_rate = pd.read_excel("usd_curs.xlsx")
    apper = []
    for i in exchange_rate["data"]:
        apper.append([str(i).split(" ")[0]])
    for i in range(len(apper)):
        apper[i].append(exchange_rate["curs"][i])

    if request.method == 'POST':
        
        datestart = str(request.POST['f'])
        dateend = str(request.POST['d'])
        datestart = datestart.split("T")[0]
        dateend = dateend.split("T")[0]

        x = exchange_rate.curs[exchange_rate.data == datestart]
        y = exchange_rate.curs[exchange_rate.data == dateend]
        if float(x) and float(y):
            
            apd = []
            sind = exchange_rate[exchange_rate.data == datestart].index
            sfin = exchange_rate[exchange_rate.data == dateend].index

            for i in range(sind[0], sfin[0]+1):
                adq = str(exchange_rate[exchange_rate.index == exchange_rate.index[i]].data).split(" ")[3].split("\n")[0]
                adw = exchange_rate[exchange_rate.index == exchange_rate.index[i]].curs
                apd.append([adq, adw])

            curses = [] #курс за период
            for i in apd:
                curses.append([i[0], float(i[1])])

            # Волатильность
            summa = 0
            for i in range(len(curses)):
                if i == 0:
                    prev = i
                else:
                    summa += curses[prev][1] / curses[i][1] - 1
                    prev = i
            volat = summa / len(curses) * 100

        data = { "dat": [datestart, dateend], "diff": volat, "up": apper, "cur": curses, "pred": predict_curs}
        return render(request, "usd_calc.html", context=data)
    data = {"up": apper, "pred": predict_curs}
    return render(request, "usd_calc.html", context=data)


def eurcalc(request):
    predict_curs = get_predict("eur_curs.xlsx")
    exchange_rate = pd.read_excel("eur_curs.xlsx")
    apper = []
    for i in exchange_rate["data"]:
        apper.append([str(i).split(" ")[0]])
    for i in range(len(apper)):
        apper[i].append(exchange_rate["curs"][i])

    if request.method == 'POST':
        
        datestart = str(request.POST['f'])
        dateend = str(request.POST['d'])
        datestart = datestart.split("T")[0]
        dateend = dateend.split("T")[0]

        x = exchange_rate.curs[exchange_rate.data == datestart]
        y = exchange_rate.curs[exchange_rate.data == dateend]
        if float(x) and float(y):
            
            apd = []
            sind = exchange_rate[exchange_rate.data == datestart].index
            sfin = exchange_rate[exchange_rate.data == dateend].index

            for i in range(sind[0], sfin[0]+1):
                adq = str(exchange_rate[exchange_rate.index == exchange_rate.index[i]].data).split(" ")[3].split("\n")[0]
                adw = exchange_rate[exchange_rate.index == exchange_rate.index[i]].curs
                apd.append([adq, adw])

            curses = [] #курс за период
            for i in apd:
                curses.append([i[0], float(i[1])])

            # Волатильность
            summa = 0
            for i in range(len(curses)):
                if i == 0:
                    prev = i
                else:
                    summa += curses[prev][1] / curses[i][1] - 1
                    prev = i
            volat = summa / len(curses) * 100

        data = { "dat": [datestart, dateend], "diff": volat, "up": apper, "cur": curses, "pred": predict_curs}
        return render(request, "eur_calc.html", context=data)
    data = {"up": apper, "pred": predict_curs}
    return render(request, "eur_calc.html", context=data)


def simplepercent(request):
    summa = 10
    perc = 12
    day = 40
    result = summa * (perc / 100) * (day / 365)


def razmernakoplenniya(request):
    # размер накопленных средств к концу года
    summa = 10 
    perc = 12
    year = 40
    q = 1 + perc/100
    k = 1
    summ = 0
    result = []
    for i in range(year):
        summ += summa * (q * k)
        k = k + 1
        result.append(summ)

    return result 


def dinampogodam(request):
    # моделирование динамики по годам
    summa = 10 
    perc = 12
    year = 40
    q = 1 + perc/100
    result = []
    for i in range(year):
        summ = summa * math.pow(q, i)
        result.append(summ)
    
    data = {"re": result}
    return render(request, "index.html", context=data)


def get_predict(str):
    exchange_rate = pd.read_excel(str)
    past = 7 * 6
    future = 1 # 28 + 7 = 35
    money = exchange_rate["curs"]
    start = len(money) - past
    end = len(money)
    raw_df = []
    for i in range(start, end):
        past_and_future_values = money[(i - past): (i+future)]
        raw_df.append(list(past_and_future_values))
    past_columns = []
    for i in range(past):
        past_columns.append("past_{}".format(i))
    future_columns = []
    for i in range(future):
        future_columns.append("future_{}".format(i))
    df = pd.DataFrame(raw_df, columns=(past_columns + future_columns ))
    x = df[past_columns][:-10]
    y = df[future_columns][:-10]
    # Exam
    x_test = df[past_columns]
    LinReg = LinearRegression()
    LinReg.fit(x,y)
    prediction = LinReg.predict(x_test)
    return prediction[0][0]

