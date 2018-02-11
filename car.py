# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 23:04:26 2018

@author: user
"""
car_fileend = '_car.set.txt'

import tkinter as tk
from random import *

class car:
    const_reaction_time = 1
    constant_reaction_time_flag = False
    def __init__(self, length_, v_max_, a_speedup_, a_speeddown_, create_time_, v_ini_, x_ini_, side_):
        self.length = length_
        self.v_max = v_max_
        self.a_speedup = a_speedup_
        self.a_speeddown = a_speeddown_
        self.create_time = create_time_
        self.v_ini = v_ini_
        self.x_ini = x_ini_
        self.side = side_
        self.reaction_count = 0
        self.last_x = self.x_ini-1
        if self.v_ini > 1:
            self.v_ini = 1
        if self.v_ini < 0:
            self.v_ini = 0
        
    def show(self):
        s = self.__str__()
        print(s)
    
    def save_str(self):
        if self.side == 0:
            s = 'A'
        else:
            s = 'B'
        s = s+'\t'+str(self.length)
        s = s+'\t'+str(self.v_max)
        s = s+'\t'+str(self.a_speedup)
        s = s+'\t'+str(self.a_speeddown)
        s = s+'\t'+str(self.create_time)
        s = s+'\t'+str(self.v_ini)
        s = s+'\t'+str(self.x_ini)
        return s
        
    def __str__(self):
        if self.side == 0:
            t = 'A '
        else:
            t = 'B '
        s = t+str([round(self.v_max, 2), round(self.a_speedup, 2), -round(self.a_speeddown, 2)])
        s = s+'@'+str(round(self.create_time, 1))+'-'+str(round(self.x_ini, 1))+'-'+str(round(self.v_ini, 1))
        return s
    
    def __lt__(self, other):
        if self.side == other.side:
            if self.create_time == other.create_time:
                return self.x_ini > other.x_ini
            return self.create_time < other.create_time
        return self.side < other.side
    def __gt__(self, other):
        if self.side == other.side:
            if self.create_time == other.create_time:
                return self.x_ini < other.x_ini
            return self.create_time > other.create_time
        return self.side > other.side
    def __eq__(self, other):
        if self.side == other.side:
            if self.x_ini == other.x_ini:
                return self.create_time == other.create_time
            return False
        return False
    
    def simulation_init(self, x_, lf, index_, v_):
        self.x = x_
        self.v = v_
        self.a = 0
        self.state = 0
        self.life_flag = lf
        self.index = index_
        self.reaction_time_func()
        
    def set_index(self, front):
        if front:
            self.index = front.index+1
        else:
            self.index = 0
        self.reaction_time_func()
            
    def reaction_time_func(self):
        if self.index < 0:
            self.reaction_time = 0
            return
        if self.constant_reaction_time_flag == 1:
            self.reaction_time = self.const_reaction_time
        elif self.constant_reaction_time_flag == 0:
            if self.index > 5:
                self.reaction_time = 2
            else:
                self.reaction_time = -0.1*self.index+2.5
     
    def set_reaction_time_flag(self, fg):
        car.constant_reaction_time_flag = fg

    def set_reaction_time(self, rt):
        car.const_reaction_time = rt
      
car_data_a = []
car_data_b = []
entryRandList = []

vm_rand_flag = 0
vi_rand_flag = 0

def set_car():
    global car_data_a, car_data_b, entryRandList
    
    def show():
        for i in car_data_a:
            print(i)
    
    def close():
        cwin.destroy()
    
    def del_car_a():
        global car_data_a, car_data_b, entryRandList
        cs = lba.curselection()
        for i in range(len(cs)-1, -1, -1):
            lba.delete(cs[i], cs[i])
            car_data_a.pop(cs[i])
        show()
    
    def del_car_b():
        global car_data_a, car_data_b, entryRandList
        cs = lbb.curselection()
        for i in range(len(cs)-1, -1, -1):
            lbb.delete(cs[i], cs[i])
            car_data_b.pop(cs[i])
    
    def add_car_main(s):
        global car_data_a, car_data_b, entryRandList
        t = car(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7])
        index = 0
        if s[7] == 0:
            car_data = car_data_a
            lb = lba
        else:
            car_data = car_data_b
            lb = lbb
        
        for i in range(len(car_data)):
            if t > car_data[i]:
                index = index+1
                continue
            break
        car_data.insert(index, t)
        lb.insert(index, str(t))
    
    def add_car_a():
        s = []
        for i in range(7):
            t = entryList[i].get()
            s.append(float(t))
        s.append(0)
        add_car_main(s)
        
    def add_car_b():
        s = []
        for i in range(7):
            t = entryList[i].get()
            s.append(float(t))
        s.append(1)
        add_car_main(s)
        
        
    def car_save():
        global car_data_a, car_data_b, entryRandList
        savename = save_e.get()
        c = open(savename+car_fileend, 'w')
        for i in range(len(car_data_a)):
            c.write(car_data_a[i].save_str())
            c.write('\n')
        for i in range(len(car_data_b)):
            c.write(car_data_b[i].save_str())
            c.write('\n')
        c.close()
        
    def car_load():
        global car_data_a, car_data_b, entryRandList
        try:
            savename = load_e.get()
            f = open(savename+car_fileend, 'r')
            f = f.readlines()
            car_data_a.clear()
            car_data_b.clear()
            s = lba.size()
            lba.delete(0, s)
            s = lbb.size()
            lbb.delete(0, s)
            for i in range(len(f)):
                g = f[i].split()
                t = []
                for j in range(1, 8):
                    t.append(float(g[j]))
                if g[0] == 'A':
                    t.append(0)
                else:
                    t.append(1)
                add_car_main(t)
        except:
            print('Open file fail!!')
            
    def get_rand_data(index):
        global entryRandList
        s = entryRandList[index].get()
        if s:
            return float(s)
        else:
            return 0
    
    def set_vm_rand():
        global vm_rand_flag
        if vm_rand_flag == 0:
            vm_rand_flag = 1
            randBvm.config(text = '常態分佈')
        elif vm_rand_flag == 1:
            vm_rand_flag = 0
            randBvm.config(text = '隨機分佈')
    def set_vi_rand():
        global vi_rand_flag
        if vi_rand_flag == 0:
            vi_rand_flag = 1
            randBvi.config(text = '常態分佈')
        elif vi_rand_flag == 1:
            vi_rand_flag = 0
            randBvi.config(text = '隨機分佈')
    #length_, v_max_, a_speedup_, a_speeddown_, create_time_, v_ini_, x_ini_, side_
    def handle_rand_add(side):
        global car_data_a, car_data_b, entryRandList, vi_rand_flag, vm_rand_flag
        l = get_rand_data(0)
        asu = get_rand_data(1)
        asd = get_rand_data(2)
        x_i = get_rand_data(3)
        v_m0 = get_rand_data(4)
        v_m1 = get_rand_data(5)
        v_i0 = get_rand_data(6)
        v_i1 = get_rand_data(7)
        cre_num = int(get_rand_data(10))
        cre_f = get_rand_data(8)
        cre_s = get_rand_data(9)
        
        for i in range(cre_num):
            if vm_rand_flag == 1:
                vm = round(uniform(v_m0, v_m1), 3)
            else:
                vm = round(gauss((v_m0+v_m1)/2., (v_m1-v_m0)/6.), 3)
            if vi_rand_flag == 1:
                vi = round(uniform(v_i0, v_i1), 3)
            else:
                vi = round(gauss((v_i0+v_i1)/2., (v_i1-v_i0)/6.), 3)
            ct = cre_f+cre_s*i
            car_s = [l, vm, asu, asd, ct, vi, x_i, side]
            add_car_main(car_s)
            
    def add_car_ar():
        handle_rand_add(0)
    def add_car_br():
        handle_rand_add(1)
        
    def  select_all_a():
        lba.select_set(0, 'end')
    def  select_all_b():
        lbb.select_set(0, 'end')
    def unselect_all_a():
        lba.select_clear(0, 'end')
    def unselect_all_b():
        lbb.select_clear(0, 'end')
    def revselect_all_a():
        cs = lba.curselection()
        n = lba.size()
        for i in range(n):
            if i in cs:
                lba.select_clear(i, i)
            else:
                lba.select_set(i, i)
    def revselect_all_b():
        cs = lbb.curselection()
        n = lbb.size()
        for i in range(n):
            if i in cs:
                lbb.select_clear(i, i)
            else:
                lbb.select_set(i, i)
    #traffic_light_data
    cwin = tk.Tk()
    cwin.title('car')
    #cwin.geometry('700x300')
    
    qb = tk.Button(cwin, text = 'quit', command = close).grid(row = 0, column = 3)
    L = tk.Label(cwin, text = '汽車列表\n[Vmax,+A,-A]@createtime-Xini-Vini').grid(row = 1, column = 2, columnspan = 4)
    
    sba = tk.Scrollbar(cwin)
    lba = tk.Listbox(cwin, width=30, height=10, selectmode=tk.MULTIPLE, yscrollcommand = sba.set)
    sba.config(command = lba.yview)
    sbb = tk.Scrollbar(cwin)
    lbb = tk.Listbox(cwin, width=30, height=10, selectmode=tk.MULTIPLE, yscrollcommand = sbb.set)
    sbb.config(command = lbb.yview)
    #lb = tk.Listbox(lwin, width=20)
    
    lba.grid(row = 2, column = 0, columnspan = 3, sticky = tk.E)
    sba.grid(row = 2, column = 3, sticky = tk.N+tk.S+tk.W)
    lbb.grid(row = 2, column = 4, columnspan = 3)
    sbb.grid(row = 2, column = 7, sticky = tk.N+tk.S+tk.W)
    
    b1 = tk.Button(cwin, text = '刪除', command = del_car_a)
    b3 = tk.Button(cwin, text = '全選', command = select_all_a)
    b4 = tk.Button(cwin, text = '取消選取', command = unselect_all_a)
    b5 = tk.Button(cwin, text = '反向選取', command = revselect_all_a)
    b2 = tk.Button(cwin, text = '刪除', command = del_car_b)
    b6 = tk.Button(cwin, text = '全選', command = select_all_b)
    b7 = tk.Button(cwin, text = '取消選取', command = unselect_all_b)
    b8 = tk.Button(cwin, text = '反向選取', command = revselect_all_b)
    b1.grid(row = 3, column = 0)
    b3.grid(row = 3, column = 1)
    b4.grid(row = 3, column = 2)
    b5.grid(row = 3, column = 3)
    b2.grid(row = 3, column = 4)
    b6.grid(row = 3, column = 5)
    b7.grid(row = 3, column = 6)
    b8.grid(row = 3, column = 7)
    
    
    tk.Label(cwin, text = 'length').grid(row = 4, column = 0)
    tk.Label(cwin, text = 'v_max').grid(row = 4, column = 1)
    tk.Label(cwin, text = 'a_speedup').grid(row = 4, column = 2)
    tk.Label(cwin, text = 'a_speeddown').grid(row = 4, column = 3)
    tk.Label(cwin, text = 'create time').grid(row = 4, column = 4)
    tk.Label(cwin, text = 'v_ini').grid(row = 4, column = 5)
    tk.Label(cwin, text = 'x_ini').grid(row = 4, column = 6)
    
    entryList = []
    for i in range(7):
        e = tk.Entry(cwin, width = 10)
        e.grid(row = 5, column = i)
        entryList.append(e)
    iba = tk.Button(cwin, text = '加入a', command = add_car_a)
    ibb = tk.Button(cwin, text = '加入b', command = add_car_b)
    iba.grid(row = 6, column = 3)
    ibb.grid(row = 6, column = 4)
    
    tk.Label(cwin, text = '亂數產生').grid(row = 7, column = 0, columnspan = 7)
    tk.Label(cwin, text = 'length:').grid(row = 8, column = 0, sticky = tk.E)
    tk.Label(cwin, text = 'a_speedup:').grid(row = 9, column = 0, sticky = tk.E)
    tk.Label(cwin, text = 'a_speeddown:').grid(row = 10, column = 0, sticky = tk.E)
    tk.Label(cwin, text = 'x_ini:').grid(row = 11, column = 0, sticky = tk.E)
    
    
    for i in range(4):
        e = tk.Entry(cwin, width = 7)
        e.grid(row = 8+i, column = 1)
        entryRandList.append(e)
    
    
    tk.Label(cwin, text = 'v_max:').grid(row = 8, column = 2, sticky = tk.E)
    tk.Label(cwin, text = 'v_ini:').grid(row = 9, column = 2, sticky = tk.E)
    tk.Label(cwin, text = 'create time. from:').grid(row = 10, column = 2, sticky = tk.E)
    
    tk.Label(cwin, text = 'to').grid(row = 8, column = 4)
    tk.Label(cwin, text = 'to').grid(row = 9, column = 4)
    tk.Label(cwin, text = 'step:').grid(row = 10, column = 4, sticky = tk.E)
    tk.Label(cwin, text = 'number:').grid(row = 11, column = 4, sticky = tk.E)
    
    rowcolumnList = [(8, 3), (8, 5), (9, 3), (9, 5), (10, 3), (10, 5), (11, 5)]
    
    for i in range(len(rowcolumnList)):
        e = tk.Entry(cwin, width = 7)
        e.grid(row = rowcolumnList[i][0], column = rowcolumnList[i][1])
        entryRandList.append(e)
    branda = tk.Button(cwin, text = '加入a', command = add_car_ar)
    branda.grid(row = 11, column = 2)
    brandb = tk.Button(cwin, text = '加入b', command = add_car_br)
    brandb.grid(row = 11, column = 3)
    
    randBvm = tk.Button(cwin, text = '隨機分佈', command = set_vm_rand)
    randBvi = tk.Button(cwin, text = '隨機分佈', command = set_vi_rand)
    randBvm.grid(row = 8, column = 6)
    randBvi.grid(row = 9, column = 6)
    
    save_e = tk.Entry(cwin)
    save_l = tk.Label(cwin, text = car_fileend)
    save_b = tk.Button(cwin, text = 'save', command=car_save)
    save_e.grid(row = 15, column = 1, columnspan = 2)
    save_l.grid(row = 15, column = 3)
    save_b.grid(row = 15, column = 4)
    load_e = tk.Entry(cwin)
    load_l = tk.Label(cwin, text = car_fileend)
    load_b = tk.Button(cwin, text = 'load', command=car_load)
    load_e.grid(row = 16, column = 1, columnspan = 2)
    load_l.grid(row = 16, column = 3)
    load_b.grid(row = 16, column = 4)
    
    cwin.mainloop()