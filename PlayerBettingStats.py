import os.path
import urllib
from tkinter import *
from tkinter import ttk
import customtkinter
import numpy as np
import pandas as pd
import requests
from PIL import Image, ImageTk
from bs4 import BeautifulSoup, NavigableString
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

dfNHL = pd.read_excel('NHLPlayers.xlsx')
dfNBA = pd.read_excel('NBAPlayers.xlsx')
dfNFL = pd.read_excel('NFLPlayers.xlsx')

nhlPlayers = dfNHL['Name'].tolist()
nhlPlayerLinks = dfNHL['Link'].tolist()

nbaPlayers = dfNBA['Name'].tolist()
nbaPlayerLinks = dfNBA['Link'].tolist()

nflPlayers = dfNFL['Name'].tolist()
nflPlayerPositions = dfNFL['Position'].tolist()
nflPlayerLinks = dfNFL['Links'].tolist()

root = customtkinter.CTk()
customtkinter.set_appearance_mode("light")


root.title('Player Cards')
root.geometry("1000x750")

global overLabel
global underLabel
global pushLabel
global topLabel
global posLabel
global ageLabel
global teamLabel
global playerpicLabel
global canvas
global frame
global chartName
global seasonTotalName
global seasonAvgLabel
global nameLine


def graphLast10(last10shots, line, games, statType):
    global canvas
    global frame
    global fig1
    global ax1
    last10shotsnp = np.array(last10shots)
    fig1, ax1 = plt.subplots()
    chart = ax1.bar(games, last10shots)
    if last10shotsnp.max() >= 200:
        ax1.set_yticks(np.arange(0, last10shotsnp.max(), 50))
    elif last10shotsnp.max() >= 100:
        ax1.set_yticks(np.arange(0, last10shotsnp.max(), 10))
    elif last10shotsnp.max() >= 30:
        ax1.set_yticks(np.arange(0, last10shotsnp.max(), 5))
    elif last10shotsnp.max() >= 10:
        ax1.set_yticks(np.arange(0, last10shotsnp.max(), 2))
    elif 5 <= last10shotsnp.max() <= 9:
        ax1.set_yticks(np.arange(0, last10shotsnp.max(), 1))
    else:
        ax1.set_yticks(np.arange(0, last10shotsnp.max(), .5))
    plt.xticks([])
    plt.xlabel('Last ' + str(len(games)) + ' Games', fontsize=10)
    plt.ylabel(statType, fontsize=10)
    ax1.axhline(y=float(line), color='grey')
    for bar in chart:
        if bar.get_height() > float(line):
            bar.set_color("green")
        elif bar.get_height() == float(line):
            bar.set_color("grey")
        else:
            bar.set_color("red")
    frame = customtkinter.CTkFrame(root)
    frame.place(x=40, y=350)
    canvas = FigureCanvasTkAgg(fig1, frame)
    frame.configure(width=300, height=175)
    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().configure(width=475, height=300)
    chartName.configure(text="Last " + str(len(games)) + " Games", font=('Arial', 26, 'bold'))
    chartName.place(x=175, y=300)


def home():
    global overLabel
    global underLabel
    global pushLabel
    global topLabel
    global posLabel
    global ageLabel
    global teamLabel
    global playerpicLabel
    global canvas
    global frame
    global chartName
    global seasonTotalName
    global seasonAvgLabel
    overLabel = customtkinter.CTkLabel(root, text="", font=('Arial', 28))
    overLabel.place(x=600, y=375)
    underLabel = customtkinter.CTkLabel(root, text="", font=('Arial', 28))
    underLabel.place(x=600, y=425)
    pushLabel = customtkinter.CTkLabel(root, text="", font=('Arial', 28))
    pushLabel.place(x=600, y=475)
    topLabel = customtkinter.CTkLabel(root, text="", font=('Helvetica', 34, 'bold', 'italic'))
    topLabel.place(x=500, y=50)
    posLabel = customtkinter.CTkLabel(root, text="", font=('Arial', 22, 'bold'))
    posLabel.place(x=555, y=100)
    ageLabel = customtkinter.CTkLabel(root, text="", font=('Arial', 22, 'bold'))
    ageLabel.place(x=555, y=150)
    teamLabel = customtkinter.CTkLabel(root, text="", font=('Arial', 22, 'bold'))
    teamLabel.place(x=555, y=200)
    seasonTotalName = customtkinter.CTkLabel(root, text="", font=('Arial', 26, 'bold'))
    seasonTotalName.place(x=650, y=300)
    seasonAvgLabel = customtkinter.CTkLabel(root, text="", font=('Arial', 28))
    seasonAvgLabel.place(x=600, y=525)
    playerpicLabel = Label(root)
    canvas = FigureCanvasTkAgg()
    frame = customtkinter.CTkFrame(root)
    chartName = customtkinter.CTkLabel(root)

    def hockeyStats():
        def hockeyBack():
            labelHockey.destroy()
            nameLabel.destroy()
            nameEntry.destroy()
            statDropdown.destroy()
            statLabel.destroy()
            lineLabel.destroy()
            getline.destroy()
            submit.destroy()
            backButton.destroy()
            overLabel.destroy()
            pushLabel.destroy()
            underLabel.destroy()
            canvas.get_tk_widget().destroy()
            frame.destroy()
            topLabel.destroy()
            posLabel.destroy()
            ageLabel.destroy()
            teamLabel.destroy()
            playerpicLabel.destroy()
            chartName.destroy()
            seasonTotalName.destroy()
            seasonAvgLabel.destroy()
            home()

        label.destroy()
        selectLabel.destroy()
        selectHockey.destroy()
        selectBasketball.destroy()
        selectFootball.destroy()
        labelHockey = customtkinter.CTkLabel(root, text="Hockey Player Stats", font=('Arial', 26, 'bold'))
        labelHockey.place(x=30, y=60)
        nameLabel = customtkinter.CTkLabel(root, text="Player Name:", font=('Arial', 14))
        nameLabel.place(x=10, y=100)

        name = StringVar()
        nameEntry = ttk.Combobox(root, width=25, values=nhlPlayers,textvariable = name)
        nameEntry.place(x=100, y=100)

        stat = customtkinter.StringVar()
        stats = ["Points", "Goals", "Assists", "Shots"]
        stat.set(stats[0])
        statDropdown = customtkinter.CTkOptionMenu(root, variable=stat, values=stats)
        statDropdown.place(x=100, y=140)

        statLabel = customtkinter.CTkLabel(root, text="Stat Type:", font=('Arial', 16))
        statLabel.place(x=10, y=140)

        lineLabel = customtkinter.CTkLabel(root, text="Line:", font=('Arial', 16))
        lineLabel.place(x=10, y=180)

        line = customtkinter.StringVar()
        line.set('0.0')
        getline = customtkinter.CTkEntry(root, width=100, textvariable=line)
        getline.place(x=102, y=182)

        submit = customtkinter.CTkButton(root, text="Get Stats",
                                         command=lambda: getHockeyStats(name.get(), stat.get(), line.get()))
        submit.place(x=25, y=225)

        backButton = customtkinter.CTkButton(root, text="Go Back", command=hockeyBack, width=25)
        backButton.place(x=5, y=5)

        def searchBox(event):
            value = event.widget.get()
            if value == '':
                nameEntry['values'] = nhlPlayers
            else:
                data = []
                for item in nhlPlayers:
                    if value.lower() in item.lower():
                        data.append(item)
                nameEntry['values'] = data

        nameEntry.bind('<KeyRelease>', searchBox)

        def getHockeyStats(playerName, chosenStat, bettingLine):
            overLabel.configure(text="")
            underLabel.configure(text="")
            pushLabel.configure(text="")
            seasonAvgLabel.configure(text="")

            canvas.get_tk_widget().destroy()
            frame.destroy()
            plt.close('all')

            x = 0
            url = ""

            for player in nhlPlayers:
                if playerName == player:
                    website2 = requests.get("https://www.hockey-reference.com/" + nhlPlayerLinks[x])
                    if website2.status_code == 429:
                        print(int(website2.headers["Retry-After"]))
                    soup2 = BeautifulSoup(website2.content, "lxml")
                    if os.path.isfile(fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NHLPlayerPics\{player}.jpg'):
                        img = (
                            Image.open(fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NHLPlayerPics\{player}.jpg'))
                        resize = img.resize((130, 145))
                        imgtk = ImageTk.PhotoImage(resize)
                        playerpicLabel.configure(image=imgtk, bg = 'black')
                        playerpicLabel.place(x=400, y=100)
                        label.image = imgtk
                    else:
                        image = soup2.find("img", attrs={'alt': "Photo of "})
                        if image is not None:
                            urllib.request.urlretrieve(image["src"],
                                                       fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NHLPlayerPics\{player}.jpg')
                            img = (Image.open(
                                fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NHLPlayerPics\{player}.jpg'))
                            resize = img.resize((130, 145))
                            imgtk = ImageTk.PhotoImage(resize)
                            playerpicLabel.configure(image=imgtk, bg = 'black')
                            label.image = imgtk
                            playerpicLabel.place(x=400, y=100)
                        elif image is None and website2.status_code != 429:
                            img = (Image.open(
                                fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NHLPlayerPics\NoPlayerPhoto.jpg'))
                            resize = img.resize((130, 145))
                            imgtk = ImageTk.PhotoImage(resize)
                            playerpicLabel.configure(image=imgtk, bg = 'black')
                            label.image = imgtk
                            playerpicLabel.place(x=400, y=100)

                    content2 = soup2.find("div", id="bottom_nav_container")
                    uls = content2.find_all("ul")
                    i = 0
                    for curr in uls:
                        if i == 2:
                            y = curr.find_all("li")
                            for years in y:
                                if years.get_text() == "2024-25":
                                    url = ("https://www.hockey-reference.com/" + years.find('a').get("href"))
                                    break
                        i += 1
                    break
                else:
                    x += 1
            if url == "":
                overLabel.place(x=250, y=375)
                overLabel.configure(text="That Player Doesn't Exist in Our Database!")
                return
            r = requests.get(url)
            overLabel.place(x=600, y=375)

            soup = BeautifulSoup(r.content, "lxml")

            table = soup.find("table", id="gamelog")
            info = soup.find("div", id="meta")
            positionandshoot = info.find_all("p")
            position = ''
            for ps in positionandshoot:
                if ps.find("strong") is not None:
                    if ps.find("strong").nextSibling.string[1:4].strip() in {"C","RW","LW","D","G"}:
                        position = ps.find("strong").nextSibling.string[1:4].strip()
                        print(ps.find("strong").nextSibling.nextSibling.nextSibling)
                        break

            teamnameget = info.find('a')
            teamname = teamnameget.get_text()

            rows = table.find_all("tr")
            age = rows[-1].find('td', {'data-stat': 'age'}).get_text()[:2]
            topLabel.configure(text=playerName, )
            posLabel.configure(text="Position:" + position)
            ageLabel.configure(text="Age: " + age)
            teamLabel.configure(text="Team: " + teamname)
            seasonTotalName.configure(text="Season Totals")
            over = 0
            under = 0
            push = 0
            games = 0
            shotTotal = 0
            last10stats = []
            last10games = []
            if chosenStat == "Shots":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'shots'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        shotTotal += float(td.get_text())
                avg = round(float(shotTotal / games), 2)
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'shots'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, chosenStat)
                overs = ("O" + str(float(bettingLine)) + " shots in " + str(over) + " games")
                unders = ("U" + str(float(bettingLine)) + " shots in " + str(under) + " games")
                pushes = ("Pushed " + str(float(bettingLine)) + " shots in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " shots/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " shots/GP")

            elif chosenStat == "Points":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'points'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        shotTotal += float(td.get_text())
                avg = round(float(shotTotal / games), 2)
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'points'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, chosenStat)
                overs = ("O" + str(bettingLine) + " points in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " points in " + str(under) + " games")
                pushes = ("Pushed " + str(bettingLine) + " points in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " points/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " points/GP")

            elif chosenStat == "Goals":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'goals'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        shotTotal += float(td.get_text())
                avg = round(float(shotTotal / games), 2)
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'goals'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, chosenStat)
                overs = ("O" + str(bettingLine) + " goals in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " goals in " + str(under) + " games")
                pushes = ("Pushed " + str(bettingLine) + " goals in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " G/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " G/GP")

            elif chosenStat == "Assists":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'assists'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        shotTotal += float(td.get_text())
                avg = round(float(shotTotal / games), 2)
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'assists'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, chosenStat)
                overs = ("O" + str(bettingLine) + " assists in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " assists in " + str(under) + " games")
                pushes = ("Pushed " + str(bettingLine) + " assists in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " A/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " A/GP")

    def basketballStats():
        def basketballBack():
            labelBasketball.destroy()
            nameLabel.destroy()
            nameEntry.destroy()
            statDropdown.destroy()
            statLabel.destroy()
            lineLabel.destroy()
            getline.destroy()
            submit.destroy()
            backButton.destroy()
            overLabel.destroy()
            pushLabel.destroy()
            underLabel.destroy()
            canvas.get_tk_widget().destroy()
            frame.destroy()
            topLabel.destroy()
            posLabel.destroy()
            ageLabel.destroy()
            teamLabel.destroy()
            playerpicLabel.destroy()
            chartName.destroy()
            seasonTotalName.destroy()
            seasonAvgLabel.destroy()
            home()

        label.destroy()
        selectLabel.destroy()
        selectHockey.destroy()
        selectBasketball.destroy()
        selectFootball.destroy()

        labelBasketball = customtkinter.CTkLabel(root, text="Basketball Player Stats", font=('Arial', 26, 'bold'))
        labelBasketball.pack(padx=10, pady=10)
        nameLabel = customtkinter.CTkLabel(root, text="Player Name:", font=('Arial', 14))
        nameLabel.place(x=10, y=100)

        name = StringVar()
        nameEntry = ttk.Combobox(root, width=25, values=nbaPlayers, textvariable=name)
        nameEntry.place(x=100, y=100)

        stat = customtkinter.StringVar()
        stats = ["Points", "Rebounds", "Assists", "Threes Made", "Steals", "Blocks", "Turnovers", "Record a Double Double",
                 "Record a Triple Double"]
        stat.set(stats[0])
        statDropdown = customtkinter.CTkOptionMenu(root, values=stats, variable=stat)
        statDropdown.place(x=100, y=140)

        statLabel = customtkinter.CTkLabel(root, text="Stat Type:", font=('Arial', 16))
        statLabel.place(x=10, y=140)

        lineLabel = customtkinter.CTkLabel(root, text="Line:", font=('Arial', 16))
        lineLabel.place(x=10, y=180)

        line = customtkinter.StringVar()
        possibleLines = ['0.0', '1.5', '2.5', '3.5', '4.5', '5.5', '6.5', '7.5']
        line.set(possibleLines[0])
        getline = customtkinter.CTkComboBox(root, width=100, variable=line, values=possibleLines)
        getline.place(x=102, y=182)

        submit = customtkinter.CTkButton(root, text="Get Stats",
                                         command=lambda: getBasketballStats(name.get(), stat.get(), line.get()))
        submit.place(x=25, y=225)

        backButton = customtkinter.CTkButton(root, text="Go Back", command=basketballBack, width=25)
        backButton.place(x=5, y=5)

        def searchBox(event):
            value = event.widget.get()
            if value == '':
                nameEntry['values'] = nbaPlayers

            else:
                data = []

                for item in nbaPlayers:
                    if value.lower() in item.lower():
                        data.append(item)
                nameEntry['values'] = data

        nameEntry.bind('<KeyRelease>', searchBox)

        def getBasketballStats(playerName, statPicked, bettingLine):
            overLabel.configure(text=" ")
            underLabel.configure(text=" ")
            pushLabel.configure(text=" ")
            seasonAvgLabel.configure(text="")
            canvas.get_tk_widget().destroy()
            frame.destroy()
            x = 0
            url = ""
            for player in nbaPlayers:
                if playerName == player:
                    website2 = requests.get("https://www.basketball-reference.com/" + nbaPlayerLinks[x])
                    soup2 = BeautifulSoup(website2.content, "lxml")
                    yeartable = soup2.find('table', id ='per_game')
                    year = yeartable.find('tr', id= 'per_game.2024')
                    getage = year.find('td', {'data-stat': 'age'})
                    ageLabel.configure(text='Age: ' + getage.get_text())
                    getpos = year.find('td', {'data-stat': 'pos'})
                    posLabel.configure(text='Position: ' + getpos.get_text())
                    getteam = year.find('td', {'data-stat': 'team_id'})
                    teamLabel.configure(text='Team: ' + getteam.get_text())
                    topLabel.configure(text=playerName)

                    if os.path.isfile(fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NBAPlayerPics\{player}.jpg'):
                        img = (
                            Image.open(fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NBAPlayerPics\{player}.jpg'))
                        resize = img.resize((130, 145))
                        imgtk = ImageTk.PhotoImage(resize)
                        playerpicLabel.configure(image=imgtk)
                        playerpicLabel.place(x=400, y=100)
                        label.image = imgtk
                    else:
                        image = soup2.find("img", attrs={'alt': "Photo of " + playerName})
                        if image is not None:
                            urllib.request.urlretrieve(image["src"],
                                                       fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NBAPlayerPics\{player}.jpg')
                            img = (Image.open(
                                fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NBAPlayerPics\{player}.jpg'))
                            resize = img.resize((130, 145))
                            imgtk = ImageTk.PhotoImage(resize)
                            playerpicLabel.configure(image=imgtk)
                            label.image = imgtk
                            playerpicLabel.place(x=400, y=100)
                        elif image is None and website2.status_code != 429:
                            playerpicLabel.configure(image=None)
                    content2 = soup2.find("div", id="bottom_nav_container")
                    uls = content2.find_all("ul")
                    i = 0
                    for curr in uls:
                        if i == 0:
                            y = curr.find_all("li")
                            for years in y:
                                if years.get_text() == "2023-24":
                                    url = ("https://www.basketball-reference.com/" + years.find('a').get("href"))
                                    break
                        i += 1
                    break
                else:
                    x += 1
            if url == "":
                overLabel.place(x=250, y=375)
                overLabel.configure(text="That Player Doesn't Exist in Our Database!")
                return
            r = requests.get(url)
            overLabel.place(x=600, y=375)
            seasonTotalName.configure(text="Season Totals")

            soup = BeautifulSoup(r.content, "lxml")
            table = soup.find("table", id="pgl_basic")
            rows = table.find_all("tr")

            over = 0
            under = 0
            push = 0
            games = 0
            statTotal = 0
            last10stats = []
            last10games = []
            if statPicked == "Points":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'pts'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        statTotal += float(td.get_text())
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'pts'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("O" + str(bettingLine) + " points in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " points in " + str(under) + " games ")
                pushes = ("Pushed " + str(bettingLine) + " points in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " PTS/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " PTS/GP")

            elif statPicked == "Rebounds":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'trb'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        statTotal += float(td.get_text())
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'trb'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("O" + str(bettingLine) + " rebounds in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " rebounds in " + str(under) + " games ")
                pushes = ("Pushed " + str(bettingLine) + " rebounds in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " REB/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " REB/GP")

            elif statPicked == "Assists":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'ast'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        statTotal += float(td.get_text())
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'ast'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("O" + str(bettingLine) + " assists in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " assists in " + str(under) + " games ")
                pushes = ("Pushed " + str(bettingLine) + " assists in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " AST/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " AST/GP")

            elif statPicked == "Threes Made":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'fg3'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        statTotal += float(td.get_text())
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'fg3'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("O" + str(bettingLine) + " threes in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " threes in " + str(under) + " games ")
                pushes = ("Pushed " + str(bettingLine) + " threes in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " 3PM/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " 3PM/GP")

            elif statPicked == "Steals":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'stl'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        statTotal += float(td.get_text())
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'stl'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("O" + str(bettingLine) + " steals in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " steals in " + str(under) + " games ")
                pushes = ("Pushed " + str(bettingLine) + " steals in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " STL/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " STL/GP")

            elif statPicked == "Blocks":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'blk'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        statTotal += float(td.get_text())
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'blk'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("O" + str(bettingLine) + " blocks in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " blocks in " + str(under) + " games ")
                pushes = ("Pushed " + str(bettingLine) + " blocks in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " BLK/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " BLK/GP")

            elif statPicked == "Record a Double Double":
                for trb in rows:
                    doubleDigit = 0
                    for td in trb.find_all('td', {'data-stat': 'pts'}):
                        if float(td.get_text()) >= 10.0:
                            doubleDigit += 1
                        if float(trb.find('td', {'data-stat':'trb'}).get_text()) >= 10:
                            doubleDigit += 1
                        if float(trb.find('td', {'data-stat':'ast'}).get_text()) >= 10:
                            doubleDigit += 1
                        if doubleDigit > 1:
                            over += 1
                            statTotal += 1
                        else:
                            under += 1
                        games += 1
                x = 0
                for trb in rows:
                    doubleDigit = 0
                    for td in trb.find_all('td', {'data-stat': 'pts'}):
                        if x >= games - 10:
                            if float(td.get_text()) >= 10.0:
                                doubleDigit += 1
                            if float(trb.find('td', {'data-stat': 'trb'}).get_text()) >= 10:
                                doubleDigit += 1
                            if float(trb.find('td', {'data-stat': 'ast'}).get_text()) >= 10:
                                doubleDigit += 1
                            if doubleDigit > 1:
                                last10stats.append(1)
                            else:
                                last10stats.append(0)
                            last10games.append("Game " + str(x))
                        x += 1
                graphLast10(last10stats, float(0.5), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("Has a DD in " + str(over) + " games")
                unders = ("Does not have a DD in " + str(under) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                seasonAvgLabel.place(x=600, y=475)
                seasonAvgLabel.configure(text="Average of " + str(avg) + " DD/GP")

            elif statPicked == "Record a Triple Double":
                for trb in rows:
                    doubleDigit = 0
                    for td in trb.find_all('td', {'data-stat': 'pts'}):
                        if float(td.get_text()) >= 10.0:
                            doubleDigit += 1
                        if float(trb.find('td', {'data-stat':'trb'}).get_text()) >= 10:
                            doubleDigit += 1
                        if float(trb.find('td', {'data-stat':'ast'}).get_text()) >= 10:
                            doubleDigit += 1
                        if doubleDigit > 2:
                            over += 1
                            statTotal += 1
                        else:
                            under += 1
                        games += 1
                x = 0
                for trb in rows:
                    doubleDigit = 0
                    for td in trb.find_all('td', {'data-stat': 'pts'}):
                        if x >= games - 10:
                            if float(td.get_text()) >= 10.0:
                                doubleDigit += 1
                            if float(trb.find('td', {'data-stat': 'trb'}).get_text()) >= 10:
                                doubleDigit += 1
                            if float(trb.find('td', {'data-stat': 'ast'}).get_text()) >= 10:
                                doubleDigit += 1
                            if doubleDigit > 2:
                                last10stats.append(1)
                            else:
                                last10stats.append(0)
                            last10games.append("Game " + str(x))
                        x += 1
                graphLast10(last10stats, float(0.5), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("Has a TD in " + str(over) + " games")
                unders = ("Does not have a TD in " + str(under) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                seasonAvgLabel.place(x=600, y=475)
                seasonAvgLabel.configure(text="Average of " + str(avg) + " TD/GP")

            elif statPicked == "Turnovers":
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'tov'}):
                        if float(td.get_text()) > float(bettingLine):
                            over += 1
                        elif float(td.get_text()) == float(bettingLine):
                            push += 1
                        else:
                            under += 1
                        games += 1
                        statTotal += float(td.get_text())
                x = 0
                for trb in rows:
                    for td in trb.find_all('td', {'data-stat': 'tov'}):
                        if x >= games - 10:
                            last10stats.append(int(td.get_text()))
                            last10games.append("Game " + str(x + 1))
                        x += 1
                graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                avg = round(float(statTotal / games), 2)
                overs = ("O" + str(bettingLine) + " turnovers in " + str(over) + " games")
                unders = ("U" + str(bettingLine) + " turnovers in " + str(under) + " games ")
                pushes = ("Pushed " + str(bettingLine) + " turnovers in " + str(push) + " games")
                overLabel.configure(text=overs)
                underLabel.configure(text=unders)
                if push >= 1:
                    pushLabel.configure(text=pushes)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " TOV/GP")
                    seasonAvgLabel.place(x=600, y=525)
                elif push < 1:
                    seasonAvgLabel.place(x=600, y=475)
                    seasonAvgLabel.configure(text="Average of " + str(avg) + " TOV/GP")

    def footballStats():
        def footballBack():
            labelFootball.destroy()
            nameLabel.destroy()
            nameEntry.destroy()
            statDropdown.destroy()
            statLabel.destroy()
            lineLabel.destroy()
            getline.destroy()
            submit.destroy()
            backButton.destroy()
            overLabel.destroy()
            pushLabel.destroy()
            underLabel.destroy()
            canvas.get_tk_widget().destroy()
            frame.destroy()
            topLabel.destroy()
            posLabel.destroy()
            ageLabel.destroy()
            teamLabel.destroy()
            playerpicLabel.destroy()
            chartName.destroy()
            seasonTotalName.destroy()
            seasonAvgLabel.destroy()
            home()

        label.destroy()
        selectLabel.destroy()
        selectHockey.destroy()
        selectBasketball.destroy()
        selectFootball.destroy()

        labelFootball = customtkinter.CTkLabel(root, text="Football Player Stats", font=('Arial', 26, 'bold'))
        labelFootball.pack(padx=10, pady=10)
        nameLabel = customtkinter.CTkLabel(root, text="Player Name:", font=('Arial', 14))
        nameLabel.place(x=10, y=100)

        name = StringVar()
        nameEntry = ttk.Combobox(root, width=25, values=nflPlayers, textvariable=name)
        nameEntry.place(x=100, y=100)

        stats = ['Passing Yards', 'Passing TDs', 'Passing Completions', 'Passing Attempts', 'Interceptions',
                 'Rushing TDs', 'Rushing Yards', 'Rushing Attempts', 'Receiving Yards', 'Receptions', "Receiving TDs"]
        stat = customtkinter.StringVar(value=stats[0])
        statDropdown = customtkinter.CTkOptionMenu(root, values=stats, variable=stat)
        statDropdown.place(x=100, y=140)

        statLabel = customtkinter.CTkLabel(master=root, text="Stat Type:", font=('Arial', 16))
        statLabel.place(x=10, y=140)

        possibleLines = ['0.0']
        line = customtkinter.StringVar(value=possibleLines[0])
        getline = customtkinter.CTkComboBox(root, width=100, variable=line, values=possibleLines)
        getline.place(x=102, y=182)

        lineLabel = customtkinter.CTkLabel(root, text="Line:", font=('Arial', 16))
        lineLabel.place(x=10, y=180)

        submit = customtkinter.CTkButton(root, text="Get Stats",
                                         command=lambda: getFootballStats(name.get(), stat.get(), line.get()))
        submit.place(x=25, y=225)

        backButton = customtkinter.CTkButton(root, text="Go Back", command=footballBack, width=25)
        backButton.place(x=5, y=5)

        def searchBox(event):
            value = event.widget.get()
            if value == '':
                nameEntry['values'] = nflPlayers

            else:
                data = []

                for item in nflPlayers:
                    if value.lower() in item.lower():
                        data.append(item)
                nameEntry['values'] = data

        nameEntry.bind('<KeyRelease>', searchBox)

        def getFootballStats(playerName, statPicked, bettingLine):
            overLabel.configure(text=" ")
            underLabel.configure(text=" ")
            pushLabel.configure(text=" ")
            seasonAvgLabel.configure(text="")
            seasonTotalName.configure(text='')
            chartName.configure(text="")
            canvas.get_tk_widget().destroy()
            frame.destroy()

            x = 0
            url = ""
            playerName = playerName.strip()
            for player in nflPlayers:
                player = player.strip()
                if playerName == player:
                    website2 = requests.get("https://www.pro-football-reference.com/" + nflPlayerLinks[x])
                    soup2 = BeautifulSoup(website2.content, "lxml")
                    info = soup2.find("div", id='meta')
                    teamname = info.find('a').get_text()
                    if nflPlayerPositions[x] == 'QB':
                        table = soup2.find("table", id='passing')
                        tbody = table.find('tbody')
                        rows = tbody.find_all('tr')
                        age = rows[-1].find('td', {'data-stat':'age'})
                        ageLabel.configure(text="Age: " + age.get_text())
                    elif nflPlayerPositions[x] in ['WR', 'TE']:
                        table = soup2.find("table", id='receiving_and_rushing')
                        tbody = table.find('tbody')
                        rows = tbody.find_all('tr')
                        age = rows[-1].find('td', {'data-stat': 'age'})
                        ageLabel.configure(text="Age: " + age.get_text())
                    elif nflPlayerPositions[x] == 'RB':
                        table = soup2.find("table", id='rushing_and_receiving')
                        tbody = table.find('tbody')
                        rows = tbody.find_all('tr')
                        age = rows[-1].find('td', {'data-stat': 'age'})
                        ageLabel.configure(text="Age: " + age.get_text())
                    teamLabel.configure(text= 'Team: ' + teamname)
                    posLabel.configure(text='Position: ' + nflPlayerPositions[x])
                    topLabel.configure(text=playerName)
                    if os.path.isfile(fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NFLPlayerPics\{player}.jpg'):
                        img = (
                            Image.open(fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NFLPlayerPics\{player}.jpg'))
                        resize = img.resize((130, 145))
                        imgtk = ImageTk.PhotoImage(resize)
                        playerpicLabel.configure(image=imgtk)
                        playerpicLabel.place(x=400, y=100)
                        label.image = imgtk
                    else:
                        image = soup2.find("img", attrs={'alt': "Photo of " + playerName})
                        if image is not None:
                            urllib.request.urlretrieve(image["src"],
                                                       fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NFLPlayerPics\{player}.jpg')
                            img = (Image.open(
                                fr'C:\Users\Admin\PycharmProjects\PlayerBettingStats\NFLPlayerPics\{player}.jpg'))
                            resize = img.resize((130, 145))
                            imgtk = ImageTk.PhotoImage(resize)
                            playerpicLabel.configure(image=imgtk)
                            label.image = imgtk
                            playerpicLabel.place(x=400, y=100)
                        elif image is None and website2.status_code != 429:
                            playerpicLabel.configure(image=None)
                    soup2 = BeautifulSoup(website2.content, "lxml")
                    content2 = soup2.find("div", id="bottom_nav_container")
                    uls = content2.find_all("ul")
                    i = 0
                    for curr in uls:
                        if i == 1:
                            y = curr.find_all("li")
                            for years in y:
                                if years.get_text() == "2023":
                                    url = ("https://www.pro-football-reference.com/" + years.find('a').get("href"))
                                    break
                        i += 1
                    break
                else:
                    x += 1
            if url == "":
                overLabel.place(x=250, y=375)
                overLabel.configure(text="That Player Doesn't Exist in Our Database!")
                return
            r = requests.get(url)
            overLabel.place(x=550, y=375)
            underLabel.place(x=550, y=425)

            soup = BeautifulSoup(r.content, "lxml")

            table = soup.find("table", id="stats")

            tbody = table.find("tbody")
            rows = tbody.find_all('tr')
            over = 0
            under = 0
            push = 0
            games = 0
            statTotal = 0
            last10stats = []
            last10games = []
            if nflPlayerPositions[x] in ['WR', 'TE']:
                if statPicked == "Receiving Yards":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec_yds'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1

                            statTotal += statnum
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec_yds'}):
                            if x >= games - 10:
                                if td.get_text() == '':
                                    statnum = 0
                                else:
                                    statnum = float(td.get_text())
                                last10stats.append(int(statnum))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rec yards in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rec yards in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rec yards in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec Yards/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec Yards/GP")

                elif statPicked == "Receptions":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(statnum)
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec'}):
                            if x >= games - 10:
                                if td.get_text() == '':
                                    statnum = 0
                                else:
                                    statnum = float(td.get_text())
                                last10stats.append(int(statnum))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " receptions in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " receptions in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " receptions in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec/GP")
                elif statPicked == "Receiving TDs":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec_td'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec_td'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rec TDs in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rec TDs in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rec TDs in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec TD/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec TD/GP")
                else:
                    overLabel.place(x=250, y=375)
                    overLabel.configure(text="Sorry! This player isn't eligible for that stat!")
                    seasonTotalName.configure(text="")

            elif nflPlayerPositions[x] == 'QB':
                seasonTotalName.configure(text="Season Totals")
                if statPicked == "Passing Yards":
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_yds'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_yds'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " pass yards in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " pass yards in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " pass yards in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Pass YDS/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Pass YDS/GP")
                elif statPicked == "Passing TDs":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_td'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_td'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " pass TDs in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " pass TDs in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " pass TDs in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Pass TDs/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Pass TDs/GP")

                elif statPicked == "Passing Completions":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_cmp'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_cmp'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " pass comps in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " pass comps in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " pass comps in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Pass Comps/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Pass Comps/GP")
                elif statPicked == "Passing Attempts":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_att'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_att'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " pass ATTs in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " pass ATTs in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " pass ATTs in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Pass ATTs/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Pass ATTs/GP")

                elif statPicked == "Interceptions":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_int'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'pass_int'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " interceptions in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " interceptions in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " interceptions in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " INTs/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " INTs/GP")

                elif statPicked == "Rushing Yards":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_yds'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_yds'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rush yards in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rush yards in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rush yards in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush YDs/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush YDs/GP")

                elif statPicked == "Rushing Attempts":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_att'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_att'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rush ATTs in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rush ATTs in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rush ATTs in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush YDs/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush YDs/GP")

                else:
                    overLabel.place(x=250, y=375)
                    overLabel.configure(text="Sorry! This player isn't eligible for that stat!")
                    seasonTotalName.configure(text="")

            elif nflPlayerPositions[x] == 'RB':
                if statPicked == "Receiving Yards":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec_yds'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec_yds'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rec yards in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rec yards in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rec yards in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec Yards/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec Yards/GP")

                elif statPicked == "Receptions":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " receptions in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " receptions in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " receptions in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec/GP")
                elif statPicked == "Receiving TDs":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec_td'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rec_td'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rec TDs in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rec TDs in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rec TDs in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec TD/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rec TD/GP")

                elif statPicked == "Rushing Yards":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_yds'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_yds'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rush yards in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rush yards in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rush yards in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush YDs/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush YDs/GP")

                elif statPicked == "Rushing Attempts":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_att'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_att'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rush ATTs in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rush ATTs in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rush ATTs in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush YDs/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush YDs/GP")

                elif statPicked == "Rushing TDs":
                    seasonTotalName.configure(text="Season Totals")
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_td'}):
                            if td.get_text() == '':
                                statnum = 0
                            else:
                                statnum = float(td.get_text())
                            if statnum > float(bettingLine):
                                over += 1
                            elif statnum == float(bettingLine):
                                push += 1
                            else:
                                under += 1
                            games += 1
                            statTotal += float(td.get_text())
                    x = 0
                    for trb in rows:
                        for td in trb.find_all('td', {'data-stat': 'rush_td'}):
                            if x >= games - 10:
                                last10stats.append(int(td.get_text()))
                                last10games.append("Game " + str(x + 1))
                            x += 1
                    graphLast10(last10stats, float(bettingLine), last10games, statPicked)
                    avg = round(float(statTotal / games), 2)
                    overs = ("O" + str(bettingLine) + " rush TDs in " + str(over) + " games")
                    unders = ("U" + str(bettingLine) + " rush TDs in " + str(under) + " games ")
                    pushes = ("Pushed " + str(bettingLine) + " rush TDs in " + str(push) + " games")
                    overLabel.configure(text=overs)
                    underLabel.configure(text=unders)
                    if push >= 1:
                        pushLabel.configure(text=pushes)
                        pushLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush TDs/GP")
                        seasonAvgLabel.place(x=550, y=525)
                    elif push < 1:
                        seasonAvgLabel.place(x=550, y=475)
                        seasonAvgLabel.configure(text="Average of " + str(avg) + " Rush TDs/GP")
                else:
                    overLabel.place(x=250, y=375)
                    overLabel.configure(text="Sorry! This player isn't eligible for that stat!")
                    seasonTotalName.configure(text="")

    label = customtkinter.CTkLabel(root, text="Betting Player Cards", font=('Arial', 26, 'bold'))
    label.pack(padx=10, pady=10)

    selectLabel = customtkinter.CTkLabel(root, text="Please Select a Sport:", font=('Arial', 20))
    selectLabel.place(x=400, y=75)

    selectHockey = customtkinter.CTkButton(root, text="Hockey", command=hockeyStats, height=75, width=75)
    selectHockey.place(x=325, y=150)

    selectBasketball = customtkinter.CTkButton(root, text="Basketball", command=basketballStats, height=75, width=75)
    selectBasketball.place(x=465, y=150)

    selectFootball = customtkinter.CTkButton(root, text="Football", command=footballStats, height=75, width=75)
    selectFootball.place(x=605, y=150)


home()
root.mainloop()
