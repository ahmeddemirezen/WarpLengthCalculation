from datetime import date
import MainWindow as mw
import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL, TOP
import pandas as pd
import matplotlib.pyplot as plt


class FilterWindow:
    def __init__(self, screen):
        # Variables
        self.dataLabels = ["İplik Numarası", "Renk Kodu", "Lot Numarası",
                           "1 gram İpin metrajı (m)", "Toplam Bobin Sayısı",
                           "Tel Sayısı", "Ort. Bobin Ağırlığı(g)",
                           "Yaklaşık Bobin Başı Fire (g)", "Band Sayısı",
                           "Bobin Sayısı", "Artan Bobin", "Toplam Fire (g)",
                           "Max Uzunluk",  "Yeni İplik Numarası"]

        topFrame = tk.Frame(screen)
        topFrame.pack(side=TOP)

        mainFrame = tk.Frame(screen)
        mainFrame.pack(side=TOP)

        bottomFrame = tk.Frame(screen)
        bottomFrame.pack(side=TOP)

        self.TopFrame(topFrame)
        self.MainFrame(mainFrame)
        self.BottomFrame(bottomFrame)

    def MainFrame(self, mainFrame):
        self.entries = {}
        self.lEntries = {}
        self.cButtons = {}
        self.cbVariables = {}

        for i in range(len(self.dataLabels)):
            self.cbVariables[i] = tk.IntVar()
            self.cButtons[i] = tk.Checkbutton(
                mainFrame, command=self.UpdateMainFrame, variable=self.cbVariables[i])
            self.cButtons[i].grid(row=i, column=0)
            a = tk.Checkbutton(mainFrame)

        for i in range(len(self.dataLabels)):
            sV = tk.StringVar()
            sV.set(self.dataLabels[i])
            self.lEntries[i] = tk.Entry(
                mainFrame, textvariable=sV, state="readonly")
            self.lEntries[i].grid(row=i, column=1, padx=5)

        for i in range(len(self.dataLabels)):
            self.entries[i] = tk.Entry(mainFrame, state=DISABLED)
            self.entries[i].grid(row=i, column=2)

    def TopFrame(self, topFrame):
        self.comboHeaderLabel = tk.Label(topFrame, text="Veriler")
        self.comboHeaderLabel.grid(row=0, column=0, pady=5)

        self.comboBox = ttk.Combobox(
            topFrame, values=self.dataLabels[3:-1], state="readonly")
        self.comboBox.set("Band Sayısı")
        self.comboBox.grid(row=1, column=0, pady=5)

    def BottomFrame(self, bottomFrame):
        self.terminateButton = tk.Button(
            bottomFrame, text="Grafiğe Dök", command=self.Graph)
        self.terminateButton.grid(row=0, column=0)

    def UpdateMainFrame(self):
        for i in range(len(self.dataLabels)):
            if(self.cbVariables[i].get() == 1):
                self.entries[i]["state"] = NORMAL
            else:
                self.entries[i]["state"] = DISABLED
                sV = tk.StringVar()
                sV.set("")
                self.entries[i]["textvariable"] = sV

    def GetFilter(self):
        result = {}
        for i in self.dataLabels:
            result[i] = ""
        for i in range(len(self.dataLabels)):
            if(self.cbVariables[i].get() == 1):
                if(i == 1):
                    result[self.dataLabels[i]] = "c" + \
                        str(self.entries[i].get().upper())
                elif(i == 2):
                    result[self.dataLabels[i]] = "L" + \
                        str(self.entries[i].get().upper())
                else:
                    result[self.dataLabels[i]] = str(
                        self.entries[i].get().upper())
        return result

    def Graph(self):
        try:
            result = mw.MainWindow.ReadData(self)

            filterResult = self.GetFilter()

            for i, e in enumerate(filterResult):
                if(filterResult[e] != ""):
                    filtered = result.loc[result[e] == filterResult[e]]
                    result = pd.DataFrame(filtered)
            #? print method for debugging
            print(result)
            labelInput = self.comboBox.get()
            result[labelInput].plot()
            plt.ylabel(labelInput)
            plt.title(str(date.today()))
            plt.show()

        except AttributeError:
            result = self.ReadData()
            labelInput = self.comboBox.get()
            result[labelInput].plot()
            plt.ylabel(labelInput)
            plt.title(str(date.today()))
            plt.show()
