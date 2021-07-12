import tkinter as tk
import MainWindow as mw

screen = tk.Tk()
screen.geometry("650x450")
screen.title("İplik Metraj Hesaplama")
mainWindow = mw.MainWindow(screen)
screen.protocol("WM_DELETE_WINDOW",mainWindow.OnClose)
screen.mainloop()