# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 23:04:26 2018

@author: user
"""
light_fileend = '_light.set.txt'

import tkinter as tk

class traffic_light:
    def __init__(self, loc, w, gt, rt, sp):
        self.location = float(loc)
        self.width = float(w)
        self.greenlight_time = int(gt)
        self.redlight_time = int(rt)
        self.start_phase = int(sp)
        
    def state_ini(self, si):
        self.state = si
        
    def show(self):
        s = self.__str__()
        print(s)
    
    def save_str(self):
        s = str(self.location)
        s = s+'\t'+str(self.width)
        s = s+'\t'+str(self.greenlight_time)
        s = s+'\t'+str(self.redlight_time)
        s = s+'\t'+str(self.start_phase)
        return s
        
    def __unicode__(self):
        self.show()
        
    def __str__(self):
        s = str([self.greenlight_time, self.redlight_time, self.start_phase])
        s = s+'@'+str(round(self.location, 0))+'-'+str(round(self.width, 0))
        return s
    
    def __lt__(self, other):
        return self.location < other.location
    def __gt__(self, other):
        return self.location > other.location
    def __eq__(self, other):
        return self.location == other.location
      
traffic_light_data = []

def set_light():
    global traffic_light_data
    
    def show():
        for i in traffic_light_data:
            print(i)
    
    def close():
        lwin.destroy()
    
    def del_light():
        global traffic_light_data
        cs = lb.curselection()
        for i in range(len(cs)-1, -1, -1):
            lb.delete(cs[i], cs[i])
            traffic_light_data.pop(cs[i])
        show()
    def refresh():
        global traffic_light_data
        s = lb.size()
        lb.delete(0, s)
        for i in range(len(traffic_light_data)):
            lb.insert(i, str(traffic_light_data[i]))
            
            
    def edit_light():
        global traffic_light_data
        cs = lb.curselection()
        if len(cs) == 0:
            return
        def editcancel():
            ewin.destroy()
        def editok():
            s0 = eE0.get()
            s1 = eE1.get()
            s2 = eE2.get()
            if s0 and s0 != '*':
                for i in range(len(cs)):
                    traffic_light_data[cs[i]].greenlight_time = int(s0)
            if s1 and s1 != '*':
                for i in range(len(cs)):
                    traffic_light_data[cs[i]].redlight_time = int(s1)
            if s2 and s2 != '*':
                for i in range(len(cs)):
                    traffic_light_data[cs[i]].start_phase = int(s2)
            refresh()
            ewin.destroy()
                
        ewin = tk.Tk()
        ewin.title('edit light')
        tk.Label(ewin, text = 'green light time').grid(row = 0, column = 0)
        tk.Label(ewin, text = 'red light time').grid(row = 1, column = 0)
        tk.Label(ewin, text = 'start phase').grid(row = 2, column = 0)
        eE0 = tk.Entry(ewin, width = 7)
        eE1 = tk.Entry(ewin, width = 7)
        eE2 = tk.Entry(ewin, width = 7)
        eE0.grid(row = 0, column = 1)
        eE1.grid(row = 1, column = 1)
        eE2.grid(row = 2, column = 1)
        eE0s = str(traffic_light_data[cs[0]].greenlight_time)
        eE1s = str(traffic_light_data[cs[0]].redlight_time)
        eE2s = str(traffic_light_data[cs[0]].start_phase)
        for i in range(1, len(cs)):
            if traffic_light_data[cs[i]].greenlight_time != traffic_light_data[cs[0]].greenlight_time:
                eE0s = '*'
                break
        for i in range(1, len(cs)):
            if traffic_light_data[cs[i]].redlight_time != traffic_light_data[cs[0]].redlight_time:
                eE1s = '*'
                break
        for i in range(1, len(cs)):
            if traffic_light_data[cs[i]].start_phase != traffic_light_data[cs[0]].start_phase:
                eE2s = '*'
                break
        eE0.insert(0, eE0s)
        eE1.insert(0, eE1s)
        eE2.insert(0, eE2s)
        bE1 = tk.Button(ewin, text = 'Ok', command = editok)
        bE2 = tk.Button(ewin, text = 'cancel', command = editcancel)
        bE1.grid(row = 3, column = 0)
        bE2.grid(row = 3, column = 1)
        ewin.mainloop()
    
    def add_light_main(s):
        global traffic_light_data
        t = traffic_light(s[0], s[1], s[2], s[3], s[4])
        index = 0
        for i in range(len(traffic_light_data)):
            if t > traffic_light_data[i]:
                index = index+1
                continue
            break
        traffic_light_data.insert(index, t)
        lb.insert(index, str(t))
    
    def add_light():
        s = []
        for i in range(5):
            t = entryList[i].get()
            s.append(int(t))
        add_light_main(s)
        
        
    def light_save():
        savename = save_e.get()
        c = open(savename+light_fileend, 'w')
        for i in range(len(traffic_light_data)):
            c.write(traffic_light_data[i].save_str())
            c.write('\n')
        c.close()
        
    def light_load():
        global traffic_light_data
        try:
            savename = load_e.get()
            f = open(savename+light_fileend, 'r')
            f = f.readlines()
            traffic_light_data.clear()
            s = lb.size()
            lb.delete(0, s)
            
            for i in range(len(f)):
                g = f[i].split()
                t = []
                for j in range(5):
                    t.append(g[j])
                add_light_main(t)
        except:
            print('Open file fail!!')
                
    def select_all():
        lb.select_set(0, 'end')
    def unselect_all():
        lb.select_clear(0, 'end')
    def revselect_all():
        cs = lb.curselection()
        n = lb.size()
        for i in range(n):
            if i in cs:
                lb.select_clear(i, i)
            else:
                lb.select_set(i, i)
    
    #traffic_light_data
    lwin = tk.Tk()
    lwin.title('light')
    #lwin.geometry('400x300')
    
    qb = tk.Button(lwin, text = 'quit', command = close).grid(row = 0, column = 2)
    L = tk.Label(lwin, text = '紅綠燈列表\n[Tgreen,Tred,startphase]@loc-width').grid(row = 1, column = 0, columnspan = 5)
    
    sb = tk.Scrollbar(lwin)
    lb = tk.Listbox(lwin, width=20, height=10, selectmode=tk.MULTIPLE, yscrollcommand = sb.set)
    sb.config(command = lb.yview)
    #lb = tk.Listbox(lwin, width=20)
    
    lb.grid(row = 2, column = 1, columnspan = 2)
    sb.grid(row = 2, column = 3, sticky = tk.N+tk.S)
    
    b3 = tk.Button(lwin, text = '全選', command = select_all)
    b4 = tk.Button(lwin, text = '取消選取', command = unselect_all)
    b5 = tk.Button(lwin, text = '反向選取', command = revselect_all)
    eb = tk.Button(lwin, text = '編輯', command = edit_light)
    db = tk.Button(lwin, text = '刪除', command = del_light)
    b3.grid(row = 3, column = 0)
    b4.grid(row = 3, column = 1)
    b5.grid(row = 3, column = 2)    
    eb.grid(row = 3, column = 3)
    db.grid(row = 3, column = 4)
    
    tk.Label(lwin, text = 'location').grid(row = 4, column = 0)
    tk.Label(lwin, text = 'width').grid(row = 4, column = 1)
    tk.Label(lwin, text = 'green time').grid(row = 4, column = 2)
    tk.Label(lwin, text = 'red time').grid(row = 4, column = 3)
    tk.Label(lwin, text = 'start phase').grid(row = 4, column = 4)
    
    entryList = []
    for i in range(5):
        e = tk.Entry(lwin, width = 10)
        e.grid(row = 5, column = i)
        entryList.append(e)
    ib = tk.Button(lwin, text = '加入', command = add_light)
    ib.grid(row = 6, column = 2)
    
    save_e = tk.Entry(lwin)
    save_l = tk.Label(lwin, text = light_fileend)
    save_b = tk.Button(lwin, text = 'save', command=light_save)
    save_e.grid(row = 7, column = 0, columnspan = 2)
    save_l.grid(row = 7, column = 2)
    save_b.grid(row = 7, column = 3)
    load_e = tk.Entry(lwin)
    load_l = tk.Label(lwin, text = light_fileend)
    load_b = tk.Button(lwin, text = 'load', command=light_load)
    load_e.grid(row = 8, column = 0, columnspan = 2)
    load_l.grid(row = 8, column = 2)
    load_b.grid(row = 8, column = 3)
    
    lwin.mainloop()