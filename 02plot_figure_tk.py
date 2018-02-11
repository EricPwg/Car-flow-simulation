# -*- coding: utf-8 -*-

from plot_figure_func import *

import tkinter as tk
import os

dir_list = ['.']
simu_list = []
select_list = []
Ltext = ''
cur_p = '.'

def load_dir():
    global cur_p
    cs = lbm.curselection()
    cur_p = dir_list[cs[0]]
    s = os.scandir(cur_p)
    s = list(s)
    simu_list.clear()
    n = lbm.size()
    lb.delete(0, n)
    for i in s:
        if i.is_dir():
            simu_list.append(i.name)
    for i in range(len(simu_list)):
        lb.insert(i, simu_list[i])

dot_flag = True
def set_draw_dot():
    global dot_flag
    if dot_flag:
        dot_flag = False
        b9.config(text = '不顯示輔助標記')
    else:
        dot_flag = True
        b9.config(text = '顯示輔助標記')
def draw():
    global dot_flag, Lrun1
    n_fail = 0
    fail_list = []
    n = len(select_list)
    alpha = float(ae.get())
    for i in range(len(select_list)):
        try:
            plot_figure(simu_list[select_list[i]], dot_flag, alpha, cur_p)
        except:
            n_fail = n_fail+1
            fail_list.append(simu_list[select_list[i]])
    Lrun1.config(text = '失敗專案數量:'+str(n_fail)+'\n'+str(fail_list))
    print('Done')


def select_lb_update():
    global simu_list, select_list, lbs
    s = lbs.size()
    lbs.delete(0, s)
    for i in range(len(select_list)):
        lbs.insert(i, simu_list[select_list[i]])

def add_simu():
    global simu_list, select_list
    cs = lb.curselection()
    for i in cs:
        if not i in select_list:
            select_list.append(i)
    select_list.sort()
    select_lb_update()
    
def delete_simu():
    cs = lbs.curselection()
    for i in range(len(cs)-1, -1, -1):
        select_list.pop(cs[i])
    select_lb_update()
    
def select_all_a():
    lb.select_set(0, 'end')

def select_all_s():
    lbs.select_set(0, 'end')

def unselect_all_a():
    lb.select_clear(0, 'end')

def unselect_all_s():
    lbs.select_clear(0, 'end')

def revselect_all_a():
    cs = lb.curselection()
    n = lb.size()
    for i in range(n):
        if i in cs:
            lb.select_clear(i, i)
        else:
            lb.select_set(i, i)

def revselect_all_s():
    cs = lbs.curselection()
    n = lbs.size()
    for i in range(n):
        if i in cs:
            lbs.select_clear(i, i)
        else:
            lbs.select_set(i, i)

win = tk.Tk()
win.title('draw')


tk.Label(win, text = '檔案列表').grid(row = 0, column = 1)
tk.Label(win, text = '專案列表').grid(row = 0, column = 5)
tk.Label(win, text = '選擇專案').grid(row = 0, column = 10)

b1 = tk.Button(win, text = '>>>', command = add_simu)
b2 = tk.Button(win, text = '<<<', command = delete_simu)

sbm = tk.Scrollbar(win)
lbm = tk.Listbox(win, width=20, height=10, selectmode=tk.SINGLE, yscrollcommand = sbm.set)
sbm.config(command = lbm.yview)

sb = tk.Scrollbar(win)
lb = tk.Listbox(win, width=20, height=10, selectmode=tk.MULTIPLE, yscrollcommand = sb.set)
sb.config(command = lb.yview)

sbs = tk.Scrollbar(win)
lbs = tk.Listbox(win, width=20, height=10, selectmode=tk.MULTIPLE, yscrollcommand = sbs.set)
sbs.config(command = lbs.yview)

lbm.grid(row = 1, column = 0, rowspan = 5, columnspan = 3, sticky = tk.E)
sbm.grid(row = 1, column = 3, rowspan = 5, sticky = tk.N+tk.S)

lb.grid(row = 1, column = 4, rowspan = 5, columnspan = 3)
sb.grid(row = 1, column = 7, rowspan = 5, sticky = tk.N+tk.S)

b1.grid(row = 2, column = 8)
b2.grid(row = 3, column = 8)

lbs.grid(row = 1, column = 9, rowspan = 5, columnspan = 3)
sbs.grid(row = 1, column = 12, rowspan = 5, sticky = tk.N+tk.S)


b = tk.Button(win, text = 'load', command = load_dir).grid(row = 6, column = 2)

b3 = tk.Button(win, text = '全選', command = select_all_a)
b4 = tk.Button(win, text = '取消選取', command = unselect_all_a)
b5 = tk.Button(win, text = '反向選取', command = revselect_all_a)
b6 = tk.Button(win, text = '全選', command = select_all_s)
b7 = tk.Button(win, text = '取消選取', command = unselect_all_s)
b8 = tk.Button(win, text = '反向選取', command = revselect_all_s)
b3.grid(row = 6, column = 4)
b4.grid(row = 6, column = 5)
b5.grid(row = 6, column = 6)
b6.grid(row = 6, column = 9)
b7.grid(row = 6, column = 10)
b8.grid(row = 6, column = 11)



b9 = tk.Button(win, text = '顯示輔助標記', command = set_draw_dot)
b10 = tk.Button(win, text = 'start draw', command = draw)
b9.grid(row = 2, column = 13)
b10.grid(row = 3, column = 13)

tk.Label(win, text='透明度:').grid(row = 4, column = 13)
ae = tk.Entry(win, width = 5)
ae.grid(row = 4, column = 14)
ae.insert(0, 0.5)

Lrun1 = tk.Label(win, text=Ltext)
Lrun1.grid(row = 11, column = 0, columnspan = 10)

s = os.scandir('.')
s = list(s)
for i in s:
    if i.is_dir():
        dir_list.append(i.name)
for i in range(len(dir_list)):
    lbm.insert(i, dir_list[i])

win.mainloop()
