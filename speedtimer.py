import time
import threading
import datetime
import random
import timeit
from tkinter import *
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

timer = 0
moves = ['R', 'U', 'F', 'D', 'L', 'B']
counter = 0
stop = True
scramble = ""
last5 = []
statitik = 0


def average_on_5_startup():
    global last5
    last5 = []
    solves = []
    with open("solves.csv", "r") as file:
        for line in file:
            line = line.split(",")
            line[-1] = line[-1].strip()
            solves.append(line)
    reverse = list(reversed(solves))
    for element in reverse:
        if element[0] == "Time":
            break
        last5.append(float(element[0]))
    last5 = list(reversed(last5))
    average_on_5()


def save_solve():
    global scramble
    with open("solves.csv", "a") as file:
        date = datetime.datetime.now()
        dt_string = date.strftime("%d/%m/%Y %H:%M:%S")
        file.write(str(round(counter, 2)) + "," + scramble + "," + dt_string + "\n")

def read_solves():
    df = pd.read_csv("solves.csv")
    df.sort_values("Datum")
    return df

def plot():
    global canvas
    global axis
    global fig
    solves = read_solves()
    fig = plt.Figure(figsize=(5, 3), dpi=100)
    axis = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, frameRight)
    canvas.get_tk_widget().pack(side=TOP)
    solves.plot(kind='line', ax=axis, legend=True)

def destroy():
    global canvas
    canvas.get_tk_widget().destroy()

def get_statistik(event=None):
    global statitik
    global last5
    if len(last5) > 0:
        if statitik % 2 == 0:
            button.config(width=64)
            frameRight.pack_forget()
            timeLabel.pack_forget()
            frameButtons.pack_forget()
            button.pack_forget()
            buttonX.pack_forget()
            scrambleLabel.pack_forget()
            averageLabel.pack_forget()
            statistikButton.pack_forget()
            solvesText.pack_forget()
            frameRight.pack(side=TOP)
            solvesText.pack(side=RIGHT)
            timeLabel.pack(side=TOP)
            frameButtons.pack(side=TOP)
            button.pack(side=LEFT)
            buttonX.pack(side=LEFT)
            scrambleLabel.pack(side=TOP)
            averageLabel.pack(side=TOP)
            statistikButton.pack(side=TOP)
            plot()
            statitik += 1
        elif statitik % 2 == 1:
            buttonX.pack_forget()
            solvesText.pack_forget()
            button.config(width=70)
            destroy()
            statitik += 1


def average_on_5():
    global last5
    average = 0
    while(len(last5) > 5):
        del last5[0]
    if len(last5) == 5:
        for i in last5:
            average += i
        average = round(average / 5, 2)
        averageLabel.config(text="Ao5: " + str(average))


def generate_scramble():
    global scramble
    scramble = ""
    lastMoveNumber = 6
    for i in range(15):
        moveNumber = random.randint(0, 5)
        while moveNumber == lastMoveNumber:
            moveNumber = random.randint(0, 5)
        lastMoveNumber = moveNumber

        move = moves[moveNumber]
        if random.randint(0,100) < 50:
            zahl = ""
        else:
            zahl = "2"
        if random.randint(0,100) < 50:
            richtung = ""
        else:
            richtung = "'"
        scramble += (zahl + move + richtung + " ")
    scrambleLabel.config(text=scramble)


def counter_label(label):
    global statitik
    def count():
        global counter
        counter += 0.1
        label.config(text=str(round(counter, 2)))
        if not stop:
            label.after(99, count)
        else:
            last5.append(counter)
            average_on_5()
            save_solve()
            generate_scramble()
            write_solves_text(False)
            if statitik % 2 == 1:
                destroy()
                plot()
    count()

def write_solves_text(all):
    solves = []
    with open("solves.csv", "r") as file:
        for index, line in enumerate(file):
            if index == 0:
                if all:
                    solvesText.insert('end', line)
                continue
            line = line.split(",")
            del line[1]
            solves.append(line)
    if all:
        for index2, i in enumerate(solves):
            append = " | ".join(i)
            solvesText.insert('end', str(index2 + 1) + ": " + append)
    else:
        append2 = " | ".join(solves[-1])
        solvesText.insert('end', str(len(solves)) + ": " + append2)

def delete_latest_solve(event=None):
    solves = []
    with open("solves.csv", "r") as file:
        for line in file:
            solves.append(line)
    with open("solves.csv", "w") as writeFile:
        writeFile.write("")
    del solves[-1]
    with open("solves.csv", "a") as appendFile:
        for solve in solves:
            for string in solve:
                appendFile.write(string)
    solvesText.delete("1.0", "end")
    write_solves_text(True)
    average_on_5_startup()
    canvas.get_tk_widget().destroy()
    plot()



def change_value(event=None):
    global stop
    global counter
    global timer
    if stop:
        stop = False
        counter = 0
        counter_label(timeLabel)
    else:
        stop = True


root = tk.Tk()
root.title("Speedcubing")
frameRight = tk.Frame(root, width=200)
frameButtons = tk.Frame(frameRight)

root.bind("<space>", change_value)
root.bind("<s>", get_statistik)
root.bind("r", delete_latest_solve)
scrambleLabel = tk.Label(frameRight, fg="green", font="Helvetica 16 bold italic")
averageLabel = tk.Label(frameRight, fg="green", font="Helvetica 16 bold italic")
averageLabel.config(text="Ao5: ")
statistikButton = tk.Button(frameRight, text="Statistics", width=70, command=lambda: get_statistik())
buttonX = tk.Button(frameButtons, text='X', width=5, command=delete_latest_solve)
timeLabel = tk.Label(frameRight, fg="green", font="Helvetica 16 bold italic")
button = tk.Button(frameButtons, text='Stop', width=70, command=change_value)
solvesText = tk.Text(frameRight, width=30, height=27.5)

#Pack
frameRight.pack(side=TOP)
#solvesText.pack(side=RIGHT)
timeLabel.pack(side=TOP)
frameButtons.pack(side=TOP)
button.pack(side=LEFT)
scrambleLabel.pack(side=TOP)
averageLabel.pack(side=TOP)
statistikButton.pack(side=TOP)

#Methoden
generate_scramble()
average_on_5_startup()
write_solves_text(True)
#Plot
fig = plt.Figure(figsize=(4, 2), dpi=100)
axis = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, frameRight)
root.mainloop()