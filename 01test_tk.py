# -*- coding: utf-8 -*-

from main_simulation import *
from traffic_light import *
from car import *

import tkinter as tk
import os

simulation_id = 'test1'

main_fileend = '_main.set.txt'


def light_load(simulation_id):
    traffic_light_data = []
    arr = os.listdir('./'+simulation_id)
    for i in range(len(arr)):
        if light_fileend in arr[i]:
            filename = simulation_id+'/'+arr[i]
            continue
    try:
        f = open(filename, 'r')
        f = f.readlines()
        traffic_light_data.clear()
        
        for i in range(len(f)):
            g = f[i].split()
            s = []
            for j in range(5):
                s.append(g[j])
            t = traffic_light(s[0], s[1], s[2], s[3], s[4])
            traffic_light_data.append(t)
        return traffic_light_data
    except:
        print('Open file fail!!')
        
def car_load(simulation_id):
    car_data_a = []
    car_data_b = []
    arr = os.listdir('./'+simulation_id)
    for i in range(len(arr)):
        if car_fileend in arr[i]:
            filename = simulation_id+'/'+arr[i]
            continue
    try:
        f = open(filename, 'r')
        f = f.readlines()
        car_data_a.clear()
        car_data_b.clear()
        
        for i in range(len(f)):
            g = f[i].split()
            s = []
            for j in range(1, 8):
                s.append(float(g[j]))
            if g[0] == 'A':
                s.append(0)
            else:
                s.append(1)
            t = car(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7])
            if s[7] == 0:
                car_data_a.append(t)
            else:
                car_data_b.append(t)
        return [car_data_a, car_data_b]
    except:
        print('Open file fail!!')
        
def main_load(simulation_id):
    rL = []
    arr = os.listdir('./'+simulation_id)
    for i in range(len(arr)):
        if main_fileend in arr[i]:
            filename = simulation_id+'/'+arr[i]
            continue
    try:
        f = open(filename, 'r')
        f = f.readlines()
        for i in range(len(f)):
            g = f[i].split()
            rL.append(g[1])
        return rL
    except:
        print('Open file fail!!')

def simulation_once(simulation_id):
    data={}
    data['intersection'] = light_load(simulation_id)
    t = car_load(simulation_id)
    data['car_a'] = t[0]
    data['car_b'] = t[1]
    mainL = main_load(simulation_id)
    data['simulation_id'] = simulation_id
    data['road_length'] = int(mainL[0])
    data['safe_distance'] = float(mainL[1])
    data['time_step'] = float(mainL[2])
    data['reaction_time'] = float(mainL[3])
    data['record_time'] = float(mainL[4])
    data['max_run_time'] = float(mainL[5])
    data['const_reaction_time_flag'] = float(mainL[6])
    mL = []
    s = mainL[7].split(',')
    for i in s:
        mL.append(int(i))
    data['monitor_location']=mL
    car_simulate(data)

simu_list = []
select_list = []
Ltext = ''

def simu():
    global Ltext
    n_fail = 0
    fail_list = []
    n = len(select_list)
    for i in range(len(select_list)):
        try:
            simulation_once(simu_list[select_list[i]])
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
win.title('run simulation')
win.geometry('500x300')

tk.Label(win, text = '檔案列表').grid(row = 0, column = 1)
tk.Label(win, text = '選擇專案').grid(row = 0, column = 5)

b1 = tk.Button(win, text = '>>>', command = add_simu)
b2 = tk.Button(win, text = '<<<', command = delete_simu)

sb = tk.Scrollbar(win)
lb = tk.Listbox(win, width=20, height=10, selectmode=tk.MULTIPLE, yscrollcommand = sb.set)
sb.config(command = lb.yview)

sbs = tk.Scrollbar(win)
lbs = tk.Listbox(win, width=20, height=10, selectmode=tk.MULTIPLE, yscrollcommand = sbs.set)
sbs.config(command = lbs.yview)

lb.grid(row = 1, column = 0, rowspan = 5, columnspan = 3)
sb.grid(row = 1, column = 3, rowspan = 5, sticky = tk.N+tk.S)

b1.grid(row = 2, column = 4)
b2.grid(row = 3, column = 4)

lbs.grid(row = 1, column = 5, rowspan = 5, columnspan = 3)
sbs.grid(row = 1, column = 8, rowspan = 5, sticky = tk.N+tk.S)

b3 = tk.Button(win, text = '全選', command = select_all_a)
b4 = tk.Button(win, text = '取消選取', command = unselect_all_a)
b5 = tk.Button(win, text = '反向選取', command = revselect_all_a)
b6 = tk.Button(win, text = '全選', command = select_all_s)
b7 = tk.Button(win, text = '取消選取', command = unselect_all_s)
b8 = tk.Button(win, text = '反向選取', command = revselect_all_s)
b3.grid(row = 6, column = 0)
b4.grid(row = 6, column = 1)
b5.grid(row = 6, column = 2)
b6.grid(row = 6, column = 5)
b7.grid(row = 6, column = 6)
b8.grid(row = 6, column = 7)

b = tk.Button(win, text = 'start', command = simu).grid(row = 10, column = 3)


run_text = tk.StringVar()
Lrun1 = tk.Label(win, text=Ltext)
Lrun1.grid(row = 11, column = 0, columnspan = 5)

s = os.scandir('.')
s = list(s)
for i in s:
    if i.is_dir():
        simu_list.append(i.name)
for i in range(len(simu_list)):
    lb.insert(i, simu_list[i])

win.mainloop()
