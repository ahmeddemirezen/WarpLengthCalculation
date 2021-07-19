import os
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
import FilterWindow as fw
from tkinter.constants import BOTTOM, DISABLED, LEFT, NORMAL, RIGHT, TOP


class MainWindow:

    def __init__(self, screen):
        # Variables
        self.dataLabels = ["İplik Numarası", "Renk Kodu", "Lot Numarası",
                           "1 gram İpin metrajı (m)", "Toplam Bobin Sayısı",
                           "Tel Sayısı", "Ort. Bobin Ağırlığı(g)",
                           "Yaklaşık Bobin Başı Fire (g)", "Band Sayısı",
                           "Bobin Sayısı", "Artan Bobin", "Toplam Fire (g)",
                           "Max Uzunluk",  "Yeni İplik Numarası"]
        self.isFWindowOpen = False

        self.myScreen = screen

        bottomGroup = tk.Frame(screen)
        bottomGroup.pack(side=BOTTOM, fill="x", padx=10, pady=10)

        resultFrame = tk.Frame(bottomGroup)
        resultFrame.pack(side=BOTTOM)

        warnFrame = tk.Frame(bottomGroup)
        warnFrame.pack(side=BOTTOM)

        buttonFrame = tk.Frame(bottomGroup)
        buttonFrame.pack(side=BOTTOM)

        leftGroup = tk.Frame(screen)
        leftGroup.pack(side=LEFT, fill="both", expand=True, padx=10, pady=10)

        calcHeaderFrame = tk.Frame(leftGroup)
        calcHeaderFrame.pack(side=TOP)

        calcFrame = tk.Frame(leftGroup)
        calcFrame.pack(side=TOP)

        rightGroup = tk.Frame(screen)
        rightGroup.pack(side=RIGHT, fill="both", expand=True, padx=10, pady=10)

        infoHeaderFrame = tk.Frame(rightGroup)
        infoHeaderFrame.pack(side=TOP)

        infoFrame = tk.Frame(rightGroup)
        infoFrame.pack(side=TOP)

        self.CalcFrame(calcFrame)
        self.InfoFrame(infoFrame)
        self.ResultFrame(resultFrame)
        self.ButtonFrame(buttonFrame)
        self.WarningFrame(warnFrame)

        # Header
        calcHeader = tk.Label(calcHeaderFrame, text="Hesaplama Bilgileri")
        calcHeader.pack(pady=20)

        infoHeader = tk.Label(infoHeaderFrame, text="İplik Bilgileri")
        infoHeader.pack(pady=20)

    def CalcFrame(self, calcFrame):

        self.oneUnitRopeLabel = tk.Label(
            calcFrame, text="1 gram İpin metrajı (m)")
        self.oneUnitRopeLabel.grid(row=0, column=0)

        self.oneUnitRopeEntry = tk.Entry(calcFrame)
        self.oneUnitRopeEntry.grid(row=1, column=0)

        self.bobbinCountLabel = tk.Label(calcFrame, text="Toplam Bobin Sayısı")
        self.bobbinCountLabel.grid(row=2, column=0)

        self.bobbinCountEntry = tk.Entry(calcFrame)
        self.bobbinCountEntry.grid(row=3, column=0)

        self.ropeyarnLabel = tk.Label(calcFrame, text="Tel Sayısı")
        self.ropeyarnLabel.grid(row=4, column=0)

        self.ropeyarnEntry = tk.Entry(calcFrame)
        self.ropeyarnEntry.grid(row=5, column=0)

        self.bobbinWeightLabel = tk.Label(
            calcFrame, text="Ort. Bobin Ağırlığı (g)")
        self.bobbinWeightLabel.grid(row=6, column=0)

        self.bobbinWeightEntry = tk.Entry(calcFrame)
        self.bobbinWeightEntry.grid(row=7, column=0)

        self.meanBobbinWasteLabel = tk.Label(
            calcFrame, text="Yaklaşık Bobin Başı Fire (g)")
        self.meanBobbinWasteLabel.grid(row=8, column=0)

        self.meanBobbinWasteEntry = tk.Entry(calcFrame)
        self.meanBobbinWasteEntry.grid(row=9, column=0)

    def InfoFrame(self, infoFrame):

        self.ropeLabel = tk.Label(
            infoFrame, text="İplik Numarası")
        self.ropeLabel.grid(row=0, column=0)

        self.ropeEntry = tk.Entry(infoFrame)
        self.ropeEntry.grid(row=1, column=0)

        vlist = ["DN", "DTEX", "NE"]
        self.ropeCombo = ttk.Combobox(
            infoFrame, state='readonly', values=vlist)
        self.ropeCombo.set("İp Türü Seçin")
        self.ropeCombo.grid(row=1, column=1, padx=5)

        self.colorCodeLabel = tk.Label(infoFrame, text="Renk Kodu")
        self.colorCodeLabel.grid(row=2, column=0)

        self.colorCodeEntry = tk.Entry(infoFrame)
        self.colorCodeEntry.grid(row=3, column=0)

        self.lotNumberLabel = tk.Label(infoFrame, text="Lot Numarası")
        self.lotNumberLabel.grid(row=4, column=0)

        self.lotNumberEntry = tk.Entry(infoFrame)
        self.lotNumberEntry.grid(row=5, column=0)

    def ResultFrame(self, resultFrame):
        self.entries = {}
        self.labelNames = self.dataLabels[8:]

        for i in range(2):
            for k in range(6):
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
            buttonFrame, command=self.Filter, text="Grafik Seçenekleri", state=NORMAL)
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
                    bobbinAmount * float(self.oneUnitRopeEntry.get()) * (float(self.bobbinWeightEntry.get()) - float(self.meanBobbinWasteEntry.get())))
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
                self.entries[3].set((float(self.entries[2].get())*float(self.bobbinWeightEntry.get())) + (
                    float(bobbinAmount)*float(self.meanBobbinWasteEntry.get())))
                self.entries[4].set(totalLength)
                self.entries[5].set(
                    str("{:.2f}".format(newRopeVal)) + self.ropeCombo.get())

                self.exportButton['state'] = NORMAL
            else:
                self.warningLabel["fg"] = "red"
                self.warningText.set("Hata")
                self.exportButton['state'] = DISABLED

        except AttributeError:
            self.entries[0].set("-----")
            self.entries[1].set("-----")
            self.entries[2].set("-----")
            self.entries[3].set("-----")
            self.entries[4].set("-----")
            self.entries[5].set("-----")
            self.exportButton['state'] = DISABLED
            self.warningLabel["fg"] = "red"
            self.warningText.set("Hata")

    def Export(self):
        result = self.WriteData()
        result.to_excel('data.xlsx', sheet_name='sheet1', index=False)

        self.warningLabel["fg"] = "green"
        self.warningText.set("Dışa Aktarım Başarılı.")
        self.exportButton["state"] = DISABLED

    def Filter(self):
        try:
            if(self.isFWindowOpen == False):
                self.filterScene = tk.Toplevel(self.myScreen)
                self.filterScene.title("Grafik Seçenekleri")
                self.filterScene.geometry("400x450+850+50")
                self.filterWindow = fw.FilterWindow(self.filterScene)
                self.filterScene.protocol(
                    "WM_DELETE_WINDOW", self.filterOnClose)
                self.isFWindowOpen = True

        except AttributeError:
            pass

    def WriteData(self):
        dfRead = self.ReadData()

        r1 = [str(self.ropeEntry.get())+str(self.ropeCombo.get()), "c"+str(self.colorCodeEntry.get().upper()), "L"+str(self.lotNumberEntry.get().upper()), float(self.oneUnitRopeEntry.get()),
              float(self.bobbinCountEntry.get()), float(self.ropeyarnEntry.get()), float(self.bobbinWeightEntry.get()), float(self.meanBobbinWasteEntry.get())]
        r2 = [float(self.entries[0].get()), float(self.entries[1].get()), float(
            self.entries[2].get()), float(self.entries[3].get()), float(self.entries[4].get()), str(self.entries[5].get())]
        r = r1 + r2

        myDict = {}

        for count, element in enumerate(self.dataLabels):
            myDict[element] = [r[count]]

        df = pd.DataFrame(myDict)

        result = pd.concat([dfRead, df])

        return result

    def ReadData(self):
        if(os.path.isfile('data.xlsx')):
            return pd.read_excel("data.xlsx")
        else:
            pd.DataFrame().to_excel('data.xlsx')
            return pd.read_excel("data.xlsx")

    def OnClose(self):
        plt.close()
        self.myScreen.destroy()

    def filterOnClose(self):
        self.isFWindowOpen = False
        self.filterScene.destroy()

    def roundToUp(self, number):
        result = number
        if((number - int(number)) > 0):
            result = int(number) + 1
        return float(result)
