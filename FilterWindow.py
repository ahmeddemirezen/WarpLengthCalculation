import tkinter as tk
from tkinter.constants import DISABLED, LEFT, NORMAL, S, TOP, W


class FilterWindow:
    def __init__(self, screen):
        mainFrame = tk.Frame(screen)
        mainFrame.pack(side=TOP)

        self.MainFrame(mainFrame)

    def MainFrame(self, mainFrame):
        self.entries = {}
        self.lEntries = {}
        self.cButtons = {}
        self.cbVariables = {}

        for i in range(11):
            self.cbVariables[i] = tk.IntVar()
            self.cButtons[i] = tk.Checkbutton(
                mainFrame, command=self.UpdateMainFrame, variable=self.cbVariables[i])
            self.cButtons[i].grid(row=i, column=0)
            a = tk.Checkbutton(mainFrame)

        self.labels = ["İplik Numarası",	"Renk Kodu", "1 gram İpin metrajı (m)",	"Toplam Bobin Sayısı",	"Tel Sayısı",
                       "Ort. Bobin Ağırlığı(g)",	"Band Sayısı",	"Bobin Sayısı",	"Artan Bobin",	"Max Uzunluk",	"Yeni İplik Numarası"]
        for i in range(11):
            sV = tk.StringVar()
            sV.set(self.labels[i])
            self.lEntries[i] = tk.Entry(
                mainFrame, textvariable=sV, state=DISABLED)
            self.lEntries[i].grid(row=i, column=1)

        for i in range(11):
            self.entries[i] = tk.Entry(mainFrame, state=DISABLED)
            self.entries[i].grid(row=i, column=2)

    def UpdateMainFrame(self):
        for i in range(11):
            if(self.cbVariables[i].get() == 1):
                self.entries[i]["state"] = NORMAL
            else:
                self.entries[i]["state"] = DISABLED

    def GetFilter(self):
        result = {}
        for i in self.labels:
            result[i] = ""
        for i in range(11):
            if(self.cbVariables[i].get() == 1):
                result[self.labels[i]] = str(self.entries[i].get())
        return result
