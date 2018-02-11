# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:49:52 2018

@author: user
"""

#arr = os.listdir('.')

from traffic_light import *
from car import *

main_fileend = '_main.set.txt'

import tkinter as tk


mainsingleList=['road_length','safe_distance', 'time_step', 'reaction_time', 'record_time', 'max_run_time', 'reaction_time_flag', 'monitor_location']

def set_main():
    def main_close():
        mwin.destroy()
    def main_save():
        savename = save_e.get()
        c = open(savename+main_fileend, 'w')
        for i in range(len(mainsingleList)):
            c.write(mainsingleList[i]+'\t'+str(entryList[i].get())+'\n')
        c.close()
    def main_load():
        try:
            savename = load_e.get()
            f = open(savename+main_fileend, 'r')
            f = f.readlines()
            
            for i in range(len(mainsingleList)):
                g = f[i].split()
                entryList[i].delete(0, 'end')
                entryList[i].insert(0, g[1])
        except:
            print('Open file fail!!')
    mwin = tk.Tk()
    mwin.title('main set')
    
    tk.Label(mwin, text = 'road length').grid(row = 0, column = 0)
    tk.Label(mwin, text = 'safe distance').grid(row = 1, column = 0)
    tk.Label(mwin, text = 'time step').grid(row = 2, column = 0)
    tk.Label(mwin, text = 'reaction time').grid(row = 3, column = 0)
    tk.Label(mwin, text = 'record time').grid(row = 4, column = 0)
    tk.Label(mwin, text = 'max run time').grid(row = 5, column = 0)
    tk.Label(mwin, text = 'const. reaction time').grid(row = 6, column = 0)
    tk.Label(mwin, text = 'monitor location').grid(row = 7, column = 0)
    
    
    entryList=[]
    for i in range(len(mainsingleList)):
        e = tk.Entry(mwin, width = 10)
        e.grid(row = i, column = 1)
        entryList.append(e)
    
    save_e = tk.Entry(mwin)
    save_l = tk.Label(mwin, text = main_fileend)
    save_b = tk.Button(mwin, text = 'save', command=main_save)
    save_e.grid(row = 20, column = 0)
    save_l.grid(row = 20, column = 1)
    save_b.grid(row = 20, column = 2)
    load_e = tk.Entry(mwin)
    load_l = tk.Label(mwin, text = main_fileend)
    load_b = tk.Button(mwin, text = 'load', command=main_load)
    load_e.grid(row = 21, column = 0)
    load_l.grid(row = 21, column = 1)
    load_b.grid(row = 21, column = 2)
    
    tk.Button(mwin, text = 'quit', command = main_close).grid(row = 9, column = 1)
    
    mwin.mainloop()

def create_dir():
    eL = []
    def q():
        dwin.destroy()
    def create_d():
        s = str(eL[0].get())
        start = float(eL[1].get()) 
        step = float(eL[2].get())
        n = int(eL[3].get())
        for i in range(n):
            n = './'+s+str(start+step*i)
            os.mkdir(n)
    dwin = tk.Tk()
    dwin.title('main set')
    tk.Label(dwin, text = '文字:').grid(row = 0, column = 0)
    tk.Label(dwin, text = '開始:').grid(row = 1, column = 0)
    tk.Label(dwin, text = '間格:').grid(row = 2, column = 0)
    tk.Label(dwin, text = '數量:').grid(row = 3, column = 0)
    for i in range(4):
        e = tk.Entry(dwin, width = 7)
        e.grid(row = i, column = 1)
        eL.append(e)
    b1 = tk.Button(dwin, text = '產生', command = create_d).grid(row = 4, column = 0)
    b2 = tk.Button(dwin, text = '離開', command = q).grid(row = 4, column = 1)
    dwin.mainloop()

win = tk.Tk()
win.title('main')
win.geometry('200x200')

b1 = tk.Button(win, text = 'light', command = set_light).pack(pady = 10)
b2 = tk.Button(win, text = 'car', command = set_car).pack(pady = 10)
b3 = tk.Button(win, text = 'main_set', command = set_main).pack(pady = 10)
b3 = tk.Button(win, text = 'create folder', command = create_dir).pack(pady = 10)


win.mainloop()
