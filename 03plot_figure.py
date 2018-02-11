# -*- coding: utf-8 -*-7

simulation_id = 'v_ini_test'
plot_speed_down_flag = 1   #0 for no, 1 for yes
plot_red_flag = 1      #0 for no, 1 for yes
plot_front_flag = 1    #0 for no, 1 for yes
plot_red_alpha = 0.5  #number of 0~1
anmi_flag = 1
anmi_state_flag = 1
anmi_width_set = [15, 4.8]
anmi_step_time = 1 #1s 10 frames




car_infor_num = 5

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


car_aF = open(simulation_id+'\\'+simulation_id+'_Car_As.txt', 'r')
car_bF = open(simulation_id+'\\'+simulation_id+'_Car_Bs.txt', 'r')
light_F = open(simulation_id+'\\'+simulation_id+'_light_state.txt', 'r')
infor_F = open(simulation_id+'\\'+simulation_id+'_base_infor.txt', 'r')
car_infor_aF = open(simulation_id+'\\'+simulation_id+'_base_inforA.txt', 'r')
car_infor_bF = open(simulation_id+'\\'+simulation_id+'_base_inforB.txt', 'r')
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
fig.savefig(simulation_id+'\\'+simulation_id+'_Car_As.png', dpi = 200)
    
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
fig.savefig(simulation_id+'\\'+simulation_id+'_Car_Bs.png', dpi = 200)

if anmi_flag == 0:
    sys.exit()

fig, ax = plt.subplots()
fig.set_tight_layout(True)
fig.set_size_inches(anmi_width_set[0],  anmi_width_set[1])
ax.set_yticks([])

print('fig size: {0} DPI, size in inches {1}'.format(fig.get_dpi(), fig.get_size_inches()))
print(road_length)
p1, p2 = ax.plot([0, road_length], [20, 20],'k', [0, road_length], [-20, -20], 'k', linewidth=5)
plot_light_list=[]
for i in range(len(loc_s)):
    p, = ax.plot([loc_s[i]-weigth_s[i], loc_s[i]+weigth_s[i], loc_s[i]+weigth_s[i], loc_s[i]-weigth_s[i], loc_s[i]-weigth_s[i]], [20, 20, -20, -20, 20],linewidth=3)
    plot_light_list.append(p)

plot_list_a=[]
plot_list_b=[]
plot_state_list_a=[]
plot_state_list_b=[]
for i in range(num_car_a):
    car_length = float(car_infor_aF[i+1].split()[1])
    p, = ax.plot([0, -car_length], [-10, -10], '-|', color = colorL[i%len(colorL)])
    plot_list_a.append(p)
    p, = ax.plot([0], [-7], '.', color = colorL[i%len(colorL)])
    plot_state_list_a.append(p)
for i in range(num_car_b):
    car_length = float(car_infor_bF[i+1].split()[1])
    p, = ax.plot([road_length, road_length+car_length], [10, 10], '-|', color = colorL[i%len(colorL)])
    plot_list_b.append(p)
    p, = ax.plot([road_length], [13], '.', color = colorL[i%len(colorL)])
    plot_state_list_b.append(p)

ax.set_title(simulation_id+'\nT = 0s')
ax.set_xlabel('distance')

ax.set_ylim(-40, 40)

if anmi_state_flag == 0:
    for i in range(len(plot_state_list_a)):
        plot_state_list_a[i].set_visible(0)

def update(i):
    label = 'timestep {0}/{1}'.format(i, len(car_aF))
    print(label)
    aL = car_aF[i].split()
    bL = car_bF[i].split()
    lightL = light_F[i].split()
    r=()
    for j in range(len(plot_list_a)):
        car_length = float(car_infor_aF[j+1].split()[1])
        x = float(aL[j*car_infor_num+1])
        tp = plot_list_a[j].set_xdata([x, x-car_length])
        live_flag = int(aL[j*car_infor_num+5])
        if live_flag == 0:
            tp = plot_list_a[j].set_visible(0)
        else:
            tp = plot_list_a[j].set_visible(1)
        if anmi_state_flag == 1:
            tpp = plot_state_list_a[j].set_xdata([x-0.5*car_length])
            state = int(aL[j*car_infor_num+4])
            if state == 0 or state == 1:
                tpp = plot_state_list_a[j].set_marker('.')
            elif state%10 == 3:
                tpp = plot_state_list_a[j].set_marker('+')
            elif state%10 == 2:
                tpp = plot_state_list_a[j].set_marker('v')
            elif state == 31 or (state == 21 and float(aL[j*car_infor_num+2]) == 0):
                tpp = plot_state_list_a[j].set_marker('x')
            elif state == 10:
                if float(aL[j*car_infor_num+3]) == 0:
                    tpp = plot_state_list_a[j].set_marker('_')
                else:
                    tpp = plot_state_list_a[j].set_marker('^')
            else:
                tpp = plot_state_list_a[j].set_marker('o')
            if live_flag == 0:
                tpp = plot_state_list_a[j].set_visible(0)
            else:
                tpp = plot_state_list_a[j].set_visible(1)
            r = r+(tpp,)
        r = r+(tp,)
    for j in range(len(plot_list_b)):
        car_length = float(car_infor_bF[j+1].split()[1])
        x = float(bL[j*car_infor_num+1])
        tp = plot_list_b[j].set_xdata([x, x+car_length])
        live_flag = int(bL[j*car_infor_num+5])
        if live_flag == 0:
            tp = plot_list_b[j].set_visible(0)
        else:
            tp = plot_list_b[j].set_visible(1)
        if anmi_state_flag == 1:
            tpp = plot_state_list_b[j].set_xdata([x+0.5*car_length])
            state = int(bL[j*car_infor_num+4])
            if state == 0:
                tpp = plot_state_list_b[j].set_marker('.')
            elif state%10 == 3:
                tpp = plot_state_list_b[j].set_marker('+')
            elif state%10 == 2:
                tpp = plot_state_list_b[j].set_marker('v')
            elif state == 31 or (state == 21 and float(bL[j*car_infor_num+2]) == 0):
                tpp = plot_state_list_b[j].set_marker('x')
            elif state == 10:
                if float(bL[j*car_infor_num+3]) == 0:
                    tpp = plot_state_list_b[j].set_marker('_')
                else:
                    tpp = plot_state_list_b[j].set_marker('^')
            else:
                tpp = plot_state_list_b[j].set_marker('o')
            if live_flag == 0:
                tpp = plot_state_list_b[j].set_visible(0)
            else:
                tpp = plot_state_list_b[j].set_visible(1)
            r = r+(tpp,)
        r = r+(tp,)
    for j in range(len(plot_light_list)):
        s = float(lightL[j+1])
        if s == 1:
            plot_light_list[j].set_color('g')
        else:
            plot_light_list[j].set_color('r')
    ts = round(float(aL[0]), 3)
    ta = ax.set_title(simulation_id+'\nT = '+str(ts)+'s')
    r = r+(ta,)
    return r

an_step = int(anmi_step_time/record_time)
if an_step == 0:
    an_step = 1

anim = FuncAnimation(fig, update, frames=np.arange(0, len(car_aF), an_step), interval=100)
anim.save(simulation_id+'/'+simulation_id+'_animate.html', dpi=80, writer='imagemagick')