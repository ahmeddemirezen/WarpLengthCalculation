import os
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL, TOP


class MainWindow:
    def __init__(self, screen):

        mainFrame = tk.Frame(screen)
        mainFrame.pack(side=TOP)

        buttonFrame = tk.Frame(screen)
        buttonFrame.pack(side=TOP)

        warnFrame = tk.Frame(screen)
        warnFrame.pack(side=TOP)

        resultFrame = tk.Frame(screen)
        resultFrame.pack(side=TOP)

        self.MainFrame(mainFrame)
        self.ResultFrame(resultFrame)
        self.ButtonFrame(buttonFrame)
        self.WarningFrame(warnFrame)

    def MainFrame(self, mainFrame):
        self.ropeLabel = tk.Label(mainFrame, text="İplik Numarası")
        self.ropeLabel.grid(row=0, column=0)

        self.ropeEntry = tk.Entry(mainFrame)
        self.ropeEntry.grid(row=1, column=0)

        vlist = ["DN", "DTEX", "NE"]
        self.ropeCombo = ttk.Combobox(
            mainFrame, state='readonly', values=vlist)
        self.ropeCombo.set("İp Türü Seçin")
        self.ropeCombo.grid(row=1, column=1)

        self.oneUnitRopeLabel = tk.Label(
            mainFrame, text="1 gram İpin metrajı (m)")
        self.oneUnitRopeLabel.grid(row=2, column=0)

        self.oneUnitRopeEntry = tk.Entry(mainFrame)
        self.oneUnitRopeEntry.grid(row=3, column=0)

        self.bobbinCountLabel = tk.Label(mainFrame, text="Toplam Bobin Sayısı")
        self.bobbinCountLabel.grid(row=4, column=0)

        self.bobbinCountEntry = tk.Entry(mainFrame)
        self.bobbinCountEntry.grid(row=5, column=0)

        self.ropeyarnLabel = tk.Label(mainFrame, text="Tel Sayısı")
        self.ropeyarnLabel.grid(row=6, column=0)

        self.ropeyarnEntry = tk.Entry(mainFrame)
        self.ropeyarnEntry.grid(row=7, column=0)

        self.bobbinWeightLabel = tk.Label(
            mainFrame, text="Ort. Bobin Ağırlığı (kg)")
        self.bobbinWeightLabel.grid(row=8, column=0)

        self.bobbinWeightEntry = tk.Entry(mainFrame)
        self.bobbinWeightEntry.grid(row=9, column=0)

    def ResultFrame(self, resultFrame):
        self.entries = {}
        self.labelNames = ["Band Sayısı", "Bobin Sayısı",
                           "Artan Bobin", "Max Uzunluk", "Yeni İplik Numarası"]

        for i in range(2):
            for k in range(5):
                self.entries[k] = tk.StringVar()
                if(i == 0):
                    self.entries[k].set(self.labelNames[k])
                else:
                    self.entries[k].set("-----")
                rEntry = tk.Entry(resultFrame, state='readonly',
                                  textvariable=self.entries[k])
                rEntry.grid(row=i, column=k, pady=5)

    def ButtonFrame(self, buttonFrame):
        self.calcBotton = tk.Button(
            buttonFrame, text="Hesapla", command=self.Calculate)
        self.calcBotton.grid(row=1, column=0, padx=10, pady=10)

        self.exportButton = tk.Button(
            buttonFrame, text="Dışa Aktar", command=self.Export, state=DISABLED)
        self.exportButton.grid(row=1, column=1, padx=10, pady=10)

        self.graphButton = tk.Button(
            buttonFrame, command=self.Graph, text="Grafikler", state=DISABLED)
        self.graphButton.grid(row=1, column=2, padx=10, pady=10)

    def WarningFrame(self, warningFrame):
        self.warningText = tk.StringVar()
        self.warningLabel = tk.Label(
            warningFrame, fg='red', textvariable=self.warningText)
        self.warningLabel.grid(row=0, column=0)

    def Calculate(self):
        try:
            self.warningText.set("")
            if(self.ropeEntry.get().replace(" ", "") != "" and self.ropeCombo.get() != "İp Türü Seçin"):
                bandAmount = float(self.ropeyarnEntry.get()) / \
                    float(self.bobbinCountEntry.get())
                bandAmount = self.roundToUp(bandAmount)

                bobbinAmount = float(self.ropeyarnEntry.get()) / bandAmount
                bobbinAmount = self.roundToUp(bobbinAmount)

                totalLength = float(
                    bobbinAmount * float(self.oneUnitRopeEntry.get()) * ((float(self.bobbinWeightEntry.get()) * 1000) - 40))
                totalLength = totalLength / float(self.ropeyarnEntry.get())

                newRopeVal = 0
                if(self.ropeCombo.get() == "DN"):
                    newRopeVal = float(
                        9000 / float(self.oneUnitRopeEntry.get()))
                elif(self.ropeCombo.get() == "DTEX"):
                    newRopeVal = float(
                        10000 / float(self.oneUnitRopeEntry.get()))
                elif(self.ropeCombo.get() == "NE"):
                    newRopeVal = float(
                        1693 / float(self.oneUnitRopeEntry.get()))

                self.entries[0].set(float(bandAmount))
                self.entries[1].set(float(bobbinAmount))
                self.entries[2].set(
                    float(self.bobbinCountEntry.get()) - bobbinAmount)
                self.entries[3].set(totalLength)
                self.entries[4].set(
                    str("{:.2f}".format(newRopeVal)) + self.ropeCombo.get())

                self.exportButton['state'] = NORMAL
            else:
                self.warningLabel["fg"] = "red"
                self.warningText.set("Hata")
                self.exportButton['state'] = DISABLED

        except Exception as e:
            self.entries[0].set("-----")
            self.entries[1].set("-----")
            self.entries[2].set("-----")
            self.entries[3].set("-----")
            self.entries[4].set("-----")
            self.exportButton['state'] = DISABLED
            self.warningLabel["fg"] = "red"
            self.warningText.set("Hata")

    def Export(self):
        result = self.TakeData()
        result.to_excel('data.xlsx', sheet_name='sheet1', index=False)

        self.warningLabel["fg"] = "green"
        self.warningText.set("Dışa Aktarım Başarılı.")
        self.exportButton["state"] = DISABLED

    def Graph(self):
        pass
        #! need to add data to the excel file as number not as string

    def TakeData(self):
        if(os.path.isfile('data.xlsx')):
            dfRead = pd.read_excel("data.xlsx")

        l1 = ["İplik Numarası",
              "1 gram İpin metrajı (m)", "Toplam Bobin Sayısı", "Tel Sayısı", "Ort. Bobin Ağırlığı(kg)"]
        l2 = self.labelNames
        l = l1 + l2

        r1 = [str(self.ropeEntry.get())+str(self.ropeCombo.get()), str(self.oneUnitRopeEntry.get()),
              str(self.bobbinCountEntry.get()), str(self.ropeyarnEntry.get()), str(self.bobbinWeightEntry.get())]
        r2 = [str(self.entries[0].get()), str(self.entries[1].get()), str(
            self.entries[2].get()), str(self.entries[3].get()), str(self.entries[4].get())]
        r = r1 + r2

        myDict = {}

        for count, element in enumerate(l):
            myDict[element] = [r[count]]

        df = pd.DataFrame(myDict)

        result = pd.concat([dfRead, df])

        return result

    def roundToUp(self, number):
        result = number
        if((number - int(number)) > 0):
            result = int(number) + 1
        return float(result)
