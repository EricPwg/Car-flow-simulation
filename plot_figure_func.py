# -*- coding: utf-8 -*-7

import sys
import numpy as np
import matplotlib.pyplot as plt

def plot_figure(simulation_id, dot_flag, plot_red_alpha, p):
    if dot_flag:
        plot_speed_down_flag = 1   #0 for no, 1 for yes
        plot_red_flag = 1      #0 for no, 1 for yes
        plot_front_flag = 1    #0 for no, 1 for yes
    else:
        plot_speed_down_flag = 0   #0 for no, 1 for yes
        plot_red_flag = 0      #0 for no, 1 for yes
        plot_front_flag = 0    #0 for no, 1 for yes
    plot_red_alpha = 0.5  #number of 0~1
    
    
    
    
    car_infor_num = 5
    
    car_aF = open(p+'\\'+simulation_id+'\\'+simulation_id+'_Car_As.txt', 'r')
    car_bF = open(p+'\\'+simulation_id+'\\'+simulation_id+'_Car_Bs.txt', 'r')
    light_F = open(p+'\\'+simulation_id+'\\'+simulation_id+'_light_state.txt', 'r')
    infor_F = open(p+'\\'+simulation_id+'\\'+simulation_id+'_base_infor.txt', 'r')
    car_infor_aF = open(p+'\\'+simulation_id+'\\'+simulation_id+'_base_inforA.txt', 'r')
    car_infor_bF = open(p+'\\'+simulation_id+'\\'+simulation_id+'_base_inforB.txt', 'r')
    car_aF = car_aF.readlines()
    car_bF = car_bF.readlines()
    car_infor_aF = car_infor_aF.readlines()
    car_infor_bF = car_infor_bF.readlines()
    light_F = light_F.readlines()
    infor_F = infor_F.readlines()
    num_car_a = int((len(car_aF[0].split())-1)/car_infor_num)
    num_car_b = int((len(car_bF[0].split())-1)/car_infor_num)
    num_light = int(len(light_F[0].split())-1)
    
    road_length = float(infor_F[0].split()[1])
    finish_time = float(infor_F[7].split()[1])
    record_time = float(infor_F[5].split()[1])
    
    loc_s=[]
    weigth_s=[]
    green_ts=[]
    red_ts=[]
    
    
    for i in range(num_light):
        loc= float(light_F[0].split()[i+1])
        w = float(light_F[1].split()[i+1])
        weigth_s.append(w)
        green_x = []
        red_x=[]
        for j in range(2, len(light_F)):
            g = light_F[j].split()
            if float(g[i+1]) == 0:
                red_x.append(float(g[0]))
            else:
                green_x.append(float(g[0]))
        green_ts.append(green_x)
        red_ts.append(red_x)
        loc_s.append(loc)
             
    fig, ax = plt.subplots()
    for i in range(len(green_ts)):
        gx=green_ts[i]
        rx=red_ts[i]
        loc = loc_s[i]
        ax.plot(gx, [loc for i in range(len(gx))], 'g|')
        ax.plot(rx, [loc for i in range(len(rx))], 'r|')
    
    ax.plot([0, finish_time, finish_time, 0, 0], [0, 0, road_length, road_length, 0], 'k--', alpha=0.5)
    
    colorL = ['r', 'g', 'y', 'k', 'c']
    for i in range(num_car_a):
        t=[]
        x=[]
        tr=[]
        xr=[]
        tf=[]
        xf=[]
        td=[]
        xd=[]
        for j in range(len(car_aF)):
            g = car_aF[j].split()
            if int(g[i*car_infor_num+5]) == 0:
                continue
            t.append(float(g[0]))
            x.append(float(g[i*car_infor_num+1]))
            if j != len(car_aF)-1:
                gn = car_aF[j+1].split()
                if float(g[i*car_infor_num+3]) >= 0 and float(gn[i*car_infor_num+3]) < 0:
                    td.append(float(g[0]))
                    xd.append(float(g[i*car_infor_num+1]))
                if int(g[i*car_infor_num+4]) == 22 and int(gn[i*car_infor_num+4]) == 21:
                    if float(gn[i*car_infor_num+2]) == 0:
                        tr.append(float(g[0]))
                        xr.append(float(g[i*car_infor_num+1]))
                    else:
                        tf.append(float(g[0]))
                        xf.append(float(g[i*car_infor_num+1]))
                if int(g[i*car_infor_num+4]) == 32 and int(gn[i*car_infor_num+4]) == 31:
                    tr.append(float(g[0]))
                    xr.append(float(g[i*car_infor_num+1]))
        if plot_red_flag == 1:
            ax.plot(tr, xr, colorL[i%len(colorL)]+'x', alpha=plot_red_alpha)
        if plot_front_flag == 1:
            ax.plot(tf, xf, colorL[i%len(colorL)]+'o', alpha=plot_red_alpha)
        if plot_speed_down_flag == 1:
            ax.plot(td, xd, colorL[i%len(colorL)]+'v', alpha=plot_red_alpha)
        ax.plot(t, x, colorL[i%len(colorL)])
    ax.set_title(simulation_id)
    ax.set_ylabel('distance')
    ax.set_xlabel('time')
    fig.savefig(p+'\\'+simulation_id+'\\'+simulation_id+'_Car_As.png')
        
    fig, ax = plt.subplots()
    for i in range(len(green_ts)):
        gx=green_ts[i]
        rx=red_ts[i]
        loc = loc_s[i]
        ax.plot(gx, [loc for i in range(len(gx))], 'g|')
        ax.plot(rx, [loc for i in range(len(rx))], 'r|')
    ax.plot([0, finish_time, finish_time, 0, 0], [0, 0, road_length, road_length, 0], 'k--', alpha=0.5)
    
    for i in range(num_car_b):
        t=[]
        x=[]
        tr=[]
        xr=[]
        tf=[]
        xf=[]
        td=[]
        xd=[]
        for j in range(len(car_bF)):
            g = car_bF[j].split()
            if int(g[i*car_infor_num+5]) == 0:
                continue
            t.append(float(g[0]))
            x.append(float(g[i*car_infor_num+1]))
            if j != len(car_bF)-1:
                gn = car_bF[j+1].split()
                if float(g[i*car_infor_num+3]) >= 0 and float(gn[i*car_infor_num+3]) < 0:
                    td.append(float(g[0]))
                    xd.append(float(g[i*car_infor_num+1]))
                if int(g[i*car_infor_num+4]) == 22 and int(gn[i*car_infor_num+4]) == 21:
                    if float(gn[i*car_infor_num+2]) == 0:
                        tr.append(float(g[0]))
                        xr.append(float(g[i*car_infor_num+1]))
                    else:
                        tf.append(float(g[0]))
                        xf.append(float(g[i*car_infor_num+1]))
                if int(g[i*car_infor_num+4]) == 32 and int(gn[i*car_infor_num+4]) == 31:
                    tr.append(float(g[0]))
                    xr.append(float(g[i*car_infor_num+1]))
        if plot_red_flag == 1:
            ax.plot(tr, xr, colorL[i%len(colorL)]+'x', alpha=plot_red_alpha)
        if plot_front_flag == 1:
            ax.plot(tf, xf, colorL[i%len(colorL)]+'o', alpha=plot_red_alpha)
        if plot_speed_down_flag == 1:
            ax.plot(td, xd, colorL[i%len(colorL)]+'v', alpha=plot_red_alpha)
        ax.plot(t, x)
    ax.set_title(simulation_id)
    ax.set_xlabel('time')
    ax.set_ylabel('distance')
    fig.savefig(p+'\\'+simulation_id+'\\'+simulation_id+'_Car_Bs.png')
