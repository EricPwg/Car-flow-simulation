# -*- coding: utf-8 -*-
'''
datatype
{
   intersection:[
       {location, 
        width, 
        greenlight_time, 
        redlight_time, 
        start_phase
       },...
   ],
   car:{
       a_speedup,
       a_speeddown,
       v_max,
       length
   },
   car_addition_a:[
     {
       a_speedup,
       a_speeddown,
       v_max,
       length,
       create_time,
       v_ini
     }, ...
   ], 
   car_addition_b:[
     {
       a_speedup,
       a_speeddown,
       v_max,
       length,
       create_time,
       v_ini
     }, ...
   ]
   car_number_a,
   car_number_b,
   mode,
   road_length,
   safe_distance,
   time_step,
   simulation_id,
   reaction_time,
   record_time,
   max_run_time

}
   
   
if mode == 0: ignore car_addition
if mode == 1: ignore car_number
'''


'''
car state
0:initial state
10:free speed up
11:free speed constant
21:speed constant because of front car
22:speed down because of front car
31:stop because of red light
32:speed down because of red light
'''

from os import system
from random import *
from numpy import *

from traffic_light import *
from car import *

def get_gau(down, up):
    r1 = uniform(0, 1)
    r2 = uniform(0, 1)
    r = sqrt(-2*log(r1))*cos(2*pi*r2)
    r = r*(up-down)/6.+(up+down)*0.5
    if r > up or r < down:
        return get_gau(down, up)
    else:
        return r
    

def write_infor(data, F, current_time):
    singleList=['road_length','safe_distance','time_step','simulation_id','reaction_time','record_time', 'max_run_time']
    for i in range(len(singleList)):
        F.write(singleList[i]+'\t'+str(data[singleList[i]])+'\n')
    F.write('finish_time\t'+str(current_time)+'\n')
    '''
    F.write('car_a_speedup\t'+str(data['car']['a_speedup'])+'\n')
    F.write('car_a_speeddown\t'+str(data['car']['a_speeddown'])+'\n')
    F.write('car_v_max\t'+str(data['car']['v_max'])+'\n')
    F.write('car_length\t'+str(data['car']['length'])+'\n')
    
    F.write('intersection_num\t')
    F.write(str(len(data['intersection']))+'\n')
    interList=['location', 'width', 'greenlight_time', 'redlight_time', 'start_phase']
    for i in range(len(interList)):
        F.write('intersection_'+interList[i])
        for j in range(len(data['intersection'])):
            F.write('\t'+str(data['intersection'][j][interList[i]]))
        F.write('\n')
    '''



def main_simulate_func(this_car, front_car, data):
    if this_car.life_flag == 0:
        return this_car
    if front_car:
        if this_car.state == 0:
            if this_car.index < 0:
                this_car.state = 10
            else:
                this_car.state = 1
        elif this_car.state == 1:
            if front_car.v > this_car.v:
                this_car.state = 3
                this_car.reaction_count = data['current_time']+this_car.reaction_time
        elif this_car.state == 3 or this_car.state == 23 or this_car.state == 33:
            if this_car.reaction_count < data['current_time']:
                this_car.state = 10
                this_car.index = -1
        elif this_car.state == 21:
            d = 0.5*this_car.v**2/this_car.a_speeddown
            dsf = (this_car.v**2)/(2*this_car.a_speeddown) - (front_car.v**2)/(2*front_car.a_speeddown)+2*data['safe_distance']
            dfc = data['direction']*(front_car.x-data['direction']*front_car.length-this_car.x)
            if d < data['next_intersection_dis'] and (d+2*(this_car.v*data['time_step']+0.5*this_car.a_speeddown*(data['time_step']**2))) >= data['next_intersection_dis'] and data['next_intersection_state'] == 0:
                this_car.state = 32
            elif front_car.v > this_car.v:
                this_car.state = 23
                this_car.reaction_count = data['current_time']+this_car.reaction_time
            elif front_car.v < this_car.v:
                if front_car.a >= 0:
                    this_car.state = 10
                    this_car.index = -1
                elif front_car.a < 0 and (dsf+2*(this_car.v*data['time_step']+0.5*this_car.a_speedup*data['time_step']**2)) >= dfc:
                    this_car.state = 22
            elif front_car.v == 0 and this_car.v == 0 and 0.5*dfc > dsf:
                this_car.state = 10
                this_car.index = -1
        elif this_car.state == 31 or this_car.state == 32:
            if data['next_intersection_state'] == 1:
                this_car.state = 33
                this_car.reaction_count = data['current_time']+this_car.reaction_time

        if this_car.state == 10:
            d = 0.5*this_car.v**2/this_car.a_speeddown
            dsf = (this_car.v**2)/(2*this_car.a_speeddown) - (front_car.v**2)/(2*front_car.a_speeddown)+2*data['safe_distance']
            dfc = data['direction']*(front_car.x-data['direction']*front_car.length-this_car.x)
            if d < data['next_intersection_dis'] and (d+2*(this_car.v*data['time_step']+0.5*this_car.a_speeddown*(data['time_step']**2))) >= data['next_intersection_dis'] and data['next_intersection_state'] == 0:
                this_car.state = 32
            elif (dsf+2*(this_car.v*data['time_step']+0.5*this_car.a_speedup*data['time_step']**2)) >= dfc:
                this_car.state = 22
            elif this_car.a_speedup == front_car.a_speedup:
                pass
                
#            elif (this_car.v**2)/(2*this_car.a_speeddown) < dfc + 2*(this_car.v*data['time_step']+0.5*this_car.a_speedup*data['time_step']**2):
            elif this_car.v > front_car.v and ((this_car.v-0*front_car.v)**2)/(2*this_car.a_speeddown) > dfc - 1*data['safe_distance']:
                this_car.state = 22
                
    else:
        if this_car.state == 0:
            this_car.state = 3
        elif this_car.state%10 == 3 :
            if this_car.reaction_count < data['current_time']:
                this_car.state = 10
                this_car.index = -1
        elif this_car.state == 21 or this_car.state == 22:
            this_car.state = 10
            this_car.index = -1
        elif this_car.state == 31 or this_car.state == 32:
            if data['next_intersection_state'] == 1:
                this_car.state = 33
                this_car.reaction_count = data['current_time']+this_car.reaction_time
        if this_car.state == 10:
            d = 0.5*this_car.v**2/this_car.a_speeddown
            if d < data['next_intersection_dis'] and (d+2*(this_car.v*data['time_step']+0.5*this_car.a_speeddown*(data['time_step']**2))) >= data['next_intersection_dis'] and data['next_intersection_state'] == 0:
                this_car.state = 32
               
    if this_car.state == 3 or this_car.state == 23 or this_car.state == 1 or this_car.state == 33:
        this_car.a = 0
        v_terminal = this_car.v
    elif this_car.state == 10:
        if this_car.v+this_car.a_speedup*data['time_step'] >= this_car.v_max:
            this_car.a = (this_car.v_max-this_car.v)/data['time_step']
            v_terminal = this_car.v_max
        else:
            this_car.a = this_car.a_speedup
            v_terminal = this_car.v+this_car.a*data['time_step']
    elif this_car.state == 21 or this_car.state == 31:
        this_car.a = 0
        v_terminal = this_car.v
    elif this_car.state == 22:
        if this_car.v-this_car.a_speeddown*data['time_step'] <= front_car.v:
            this_car.a = (front_car.v-this_car.v)/data['time_step']
            v_terminal = front_car.v
            this_car.state = 21
            this_car.set_index(front_car)
        else:
            this_car.a = -this_car.a_speeddown
            v_terminal = this_car.v+this_car.a*data['time_step']
    elif this_car.state == 32:
        if this_car.v-this_car.a_speeddown*data['time_step'] <= 0:
            this_car.a = (-this_car.v)/data['time_step']
            v_terminal = 0
            this_car.state = 31
            this_car.set_index('')
        else:
            this_car.a = -this_car.a_speeddown
            v_terminal = this_car.v+this_car.a*data['time_step']
    
    this_car.v = v_terminal
    this_car.last_x = this_car.x
    this_car.x = this_car.x+0.5*(this_car.v+v_terminal)*data['time_step']*data['direction']
    return this_car

def save_data(carAL, carBL, fileA, fileB, curtime):
    fileA.write(str(curtime))
    fileB.write(str(curtime))
    for i in carAL:
        x = str(round(i.x, 4))
        v = str(round(i.v, 4))
        a = str(round(i.a, 4))
        state = str(i.state)
        life_flag = str(i.life_flag)
        fileA.write('\t'+x+'\t'+v+'\t'+a+'\t'+state+'\t'+life_flag)
    fileA.write('\n')
    for i in carBL:
        x = str(round(i.x, 4))
        v = str(round(i.v, 4))
        a = str(round(i.a, 4))
        state = str(i.state)
        life_flag = str(i.life_flag)
        fileB.write('\t'+x+'\t'+v+'\t'+a+'\t'+state+'\t'+life_flag)
    fileB.write('\n')

def save_light(interL, interF, curtime):
    s=str(curtime)
    for i in range(len(interL)):
        s = s+'\t'+str(interL[i].state)
    s = s+'\n'
    interF.write(s)

def save_monitor(monitorList, monitor_location, side, f):
    maxL = []
    for i in range(len(monitorList)):
        maxL.append(len(monitorList[i][side]))
    maxN = max(maxL)
    for i in monitor_location:
        f.write(str(i)+',')
    f.write('\n')
    for i in range(maxN):
        for j in range(len(monitorList)):
            if i >= len(monitorList[j][side]):
                f.write(',')
            else:
                f.write(str(round(monitorList[j][side][i], 3))+',')
        f.write('\n')
    
    

def show(carL):
    for i in range(len(carL)):
        s='Car '+str(i)
        s = s+'\tx:'+str(carL[i].x)
        s = s+'\tv:'+str(carL[i].v)
        s = s+'\ta:'+str(carL[i].a)
        print(s)
        
def show_inter(interL):
    s=''
    for i in range(len(interL)):
        s = s+str(interL[i].state)+'\t'
    print('light state:'+s)

def simulate_ini(data, sd, side, road_length):
    if len(data) > 0:
        x = data[0].x_ini
        index = -1
    else:
        x = 0
        index = -1
    for i in range(len(data)):
        if data[i].create_time == 0:
            lf = 1
        else:
            data[i].simulation_init(data[i].x_ini, 0, -1, data[i].v_ini)
            continue
        if data[i].x_ini > x:
            v = 0
        else:
            x = data[i].x_ini
            index = -1
            v = data[i].v_ini*data[i].v_max
        data[i].simulation_init(x, lf, index, v)
        x = x-data[i].length-sd
        index = index+1
        if i == 0:
            continue
        if data[i].v == 0:
            continue
        vsf = sqrt((data[i-1].x-data[i-1].length-sd-data[i].x+(data[i-1].v**2)/(2*data[i-1].a_speeddown))*2*data[i].a_speeddown)
        if data[i].v > vsf:
            data[i].v = vsf
        
    if side == 1:
        for j in range(len(data)):
            data[j].x = -1*data[j].x+road_length
    return data

def car_simulate(data):
    print('Start simulation:'+data['simulation_id'])
    intersection=[]

    for i in data['intersection']:
        if i.start_phase >= i.greenlight_time:
            state = 0 #red
        else:
            state = 1 #green
        i.state_ini(state)
        intersection.append(i)
    intersection.sort()
    
    
    
#    write car base infor.
    collect_Fa = open(data['simulation_id']+'\\'+data['simulation_id']+'_base_inforA.txt', 'w')
    collect_Fb = open(data['simulation_id']+'\\'+data['simulation_id']+'_base_inforB.txt', 'w')
    car_infor_list=['car_num', 'length', 'v_max', 'a_speedup', 'a_speeddown', 'create_time']
    s = '\t'.join(car_infor_list)+'\n'
    collect_Fa.write(s)
    collect_Fb.write(s)
    
    #########################
    road_length = data['road_length']
    sd = data['safe_distance']
    car_a=data['car_a']
    car_b=data['car_b']
    
    if len(car_a) > 0:
        car_a[0].set_reaction_time_flag(data['const_reaction_time_flag'])
        car_a[0].set_reaction_time(data['reaction_time'])
    elif len(car_b) > 0:
        car_b[0].set_reaction_time_flag(data['const_reaction_time_flag'])
        car_b[0].set_reaction_time(data['reaction_time'])
    
    car_a.sort()
    car_b.sort()
    
    car_a = simulate_ini(car_a, sd, 0, road_length)
    car_b = simulate_ini(car_b, sd, 1, road_length)
    
    for i in range(len(car_a)):
        tt = car_a[i]
        s = [str(i),str(tt.length) , str(tt.v_max), str(tt.a_speedup), str(tt.a_speeddown), str(tt.create_time)]
        s = '\t'.join(s)
        s = s+'\n'
        collect_Fa.write(s)
        
    for i in range(len(car_b)):
        tt = car_b[i]
        s = [str(i),str(tt.length) , str(tt.v_max), str(tt.a_speedup), str(tt.a_speeddown), str(tt.create_time)]
        s = '\t'.join(s)
        s = s+'\n'
        collect_Fb.write(s)
    
    collect_Fa.close()
    collect_Fb.close()
    '''
    
    for i in range(data['car_number_a']):
        car_t = {'x':x, 'v':0, 'a':0, 'state':0, 'length':length, 'life_flag':1, 'create_time':0}
        car_t['v_max'] = data['car']['v_max']
        car_t['a_speedup'] = data['car']['a_speedup']
        car_t['a_speeddown'] = data['car']['a_speeddown']
        car_t['reaction_count'] = 0
        car_t['v_ini_flag'] = 0
        car_a.append(car_t)
        x = x-length-sd
        collect_Fa.write(str(i))
        for j in range(1, len(car_infor_list)):
            s = '\t'+str(car_t[car_infor_list[j]])
            collect_Fa.write(s)
        collect_Fa.write('\n')
    for ii in range(len(data['car_addition_a'])):
        i = data['car_addition_a'][ii]
        car_t = {'x':x, 'v':0, 'a':0, 'state':0, 'life_flag':0}
        car_t['length'] = i['length']
        car_t['v_max'] = i['v_max']
        car_t['a_speedup'] = i['a_speedup']
        car_t['a_speeddown'] = i['a_speeddown']
        car_t['reaction_count'] = 0
        car_t['create_time'] = i['create_time']
        car_t['v_ini_flag'] = i['v_ini_flag']
        car_a.append(car_t)
        x = x-length-sd
        collect_Fa.write('addi'+str(ii))
        for j in range(1, len(car_infor_list)):
            s = '\t'+str(car_t[car_infor_list[j]])
            collect_Fa.write(s)
        collect_Fa.write('\n')
    collect_Fa.close()
    
    x = data['road_length']
    for i in range(data['car_number_b']):
        car_t = {'x':x, 'v':0, 'a':0, 'state':0, 'length':length, 'life_flag':1, 'create_time':0}
        car_t['v_max'] = data['car']['v_max']
        car_t['a_speedup'] = data['car']['a_speedup']
        car_t['a_speeddown'] = data['car']['a_speeddown']
        car_t['reaction_count'] = 0
        car_t['v_ini_flag'] = 0
        car_b.append(car_t)
        x = x+length+sd
        collect_Fb.write(str(i))
        for j in range(1, len(car_infor_list)):
            s = '\t'+str(car_t[car_infor_list[j]])
            collect_Fb.write(s)
        collect_Fb.write('\n')
    for ii in range(len(data['car_addition_b'])):
        i = data['car_addition_b'][ii]
        car_t = {'x':x, 'v':0, 'a':0, 'state':0, 'life_flag':0}
        car_t['length'] = i['length']
        car_t['v_max'] = i['v_max']
        car_t['a_speedup'] = i['a_speedup']
        car_t['a_speeddown'] = i['a_speeddown']
        car_t['reaction_count'] = 0
        car_t['create_time'] = i['create_time']
        car_t['v_ini_flag'] = i['v_ini_flag']
        car_b.append(car_t)
        x = x+length+sd
        collect_Fb.write('addi'+str(ii))
        for j in range(1, len(car_infor_list)):
            s = '\t'+str(car_t[car_infor_list[j]])
            collect_Fb.write(s)
        collect_Fb.write('\n')
    collect_Fb.close()
    '''
    
    #mkdir open file
    
    file_a = open(data['simulation_id']+'\\'+data['simulation_id']+'_Car_As.txt', 'w')
    file_b = open(data['simulation_id']+'\\'+data['simulation_id']+'_Car_Bs.txt', 'w')
    file_light = open(data['simulation_id']+'\\'+data['simulation_id']+'_light_state.txt', 'w')
    file_infor = open(data['simulation_id']+'\\'+data['simulation_id']+'_base_infor.txt', 'w')
    
    s1 = 'location'
    s2 = 'width'
    for i in range(len(intersection)):
        s1 = s1+'\t'+str(intersection[i].location)
        s2 = s2+'\t'+str(intersection[i].width)
    s = s1+'\n'+s2+'\n'
    file_light.write(s)
    
    monitor_location = data['monitor_location']
    monitorList = []
    for i in range(len(monitor_location)):
        monitorList.append([[], []])
    
    #SIMULATION
    time_step = data['time_step']
    car_a_start=0
    car_b_start=0
    current_time = 0.
    counter = 0
    while 1:
        # save file and
        for i in range(len(car_a)):
            ii = car_a[i]
            if ii.life_flag == 0 and current_time <= ii.create_time and current_time+time_step > ii.create_time:
                ii.life_flag = 1
                if i == 0:
                    ii.x = 0
                    ii.v = ii.v_ini*ii.v_max
                elif car_a[i-1].life_flag == 0:
                    ii.x = 0
                    ii.v = ii.v_ini
                elif car_a[i-1].x-car_a[i-1].length-sd > 0:
                    vsf = sqrt((car_a[i-1].x-car_a[i-1].length-sd+(car_a[i-1].v**2)/(2*car_a[i-1].a_speeddown))*2*ii.a_speeddown)
                    if vsf > ii.v_ini*ii.v_max:
                        ii.v = ii.v_ini*ii.v_max
                        ii.x = 0
                        ii.state = 10
                    else:
                        ii.v = vsf
                        ii.x = 0
                        ii.state = 10
                else:
                    ii.x = car_a[i-1].x-car_a[i-1].length-sd
                    ii.v = 0
            car_a[i] = ii
        for i in range(len(car_b)):
            ii = car_b[i]
            if ii.life_flag == 0 and current_time <= ii.create_time and current_time+time_step > ii.create_time:
                ii.life_flag = 1
                if i == 0:
                    ii.x = data['road_length']
                    ii.v = ii.v_ini*ii.v_max
                elif car_b[i-1].life_flag == 0:
                    ii.x = data['road_length']
                    ii.v = ii.v_ini
                elif car_b[i-1].x+car_b[i-1].length+sd < data['road_length']:
                    vsf = sqrt((data['road_length']-(car_b[i-1].x+car_b[i-1].length+sd)+(car_b[i-1].v**2)/(2*car_b[i-1].a_speeddown))*2*ii.a_speeddown)
                    if vsf > ii.v_ini*ii.v_max:
                        ii.v = ii.v_ini*ii.v_max
                        ii.x = data['road_length']
                        ii.state = 10
                    else:
                        ii.v = vsf
                        ii.x = data['road_length']
                        ii.state = 10
                else:
                    ii.x = car_b[i-1].x+car_b[i-1].length+sd
                    ii.v = 0
            car_b[i] = ii
            
        if counter%(data['record_time']/time_step) == 0:
            save_data(car_a, car_b, file_a, file_b, current_time)     
            save_light(intersection, file_light, current_time)
            #print('t='+str(current_time))
            
        for i in range(car_a_start, len(car_a)):
            #get infor of next light
            car_cur = car_a[i]
            next_intersection_dis=intersection[0].location-intersection[0].width-car_cur.x
            next_intersection_state=intersection[0].state
            for j in range(1, len(intersection)):
                if intersection[j-1].location-intersection[j-1].width > car_cur.x:
                    break
                next_intersection_dis=intersection[j].location-intersection[j].width-car_cur.x
                next_intersection_state=intersection[j].state
            if i == 0:
                front_car = ""
            elif car_a[i-1].life_flag == 0:
                front_car = ""
            else:
                front_car = car_a[i-1]
            act_dict = {'direction':1, 'safe_distance':data['safe_distance']}
            act_dict['next_intersection_dis'] = next_intersection_dis
            act_dict['next_intersection_state'] = next_intersection_state
            act_dict['time_step'] = time_step
            act_dict['reaction_time'] = data['reaction_time']
            act_dict['time_step'] = data['time_step']
            act_dict['current_time'] = current_time
            car_a[i] = main_simulate_func(car_cur, front_car, act_dict)
                            
        for i in range(car_b_start, len(car_b)):
            #get infor of next light
            car_cur = car_b[i]
            next_intersection_dis=car_cur.x-(intersection[-1].location+intersection[-1].width)
            next_intersection_state=intersection[-1].state
            for j in range(-2, -len(intersection)-1, -1):
                if intersection[j+1].location+intersection[j+1].width < car_cur.x:
                    break
                next_intersection_dis=car_cur.x-(intersection[j].location+intersection[j].width)
                next_intersection_state=intersection[j].state
            if i == 0:
                front_car = ""
            elif car_b[i-1].life_flag == 0:
                front_car = ""
            else:
                front_car = car_b[i-1]
            act_dict = {'direction':-1, 'safe_distance':data['safe_distance']}
            act_dict['next_intersection_dis'] = next_intersection_dis
            act_dict['next_intersection_state'] = next_intersection_state
            act_dict['time_step'] = time_step
            act_dict['reaction_time'] = data['reaction_time']
            act_dict['time_step'] = data['time_step']
            act_dict['current_time'] = current_time
            car_b[i] = main_simulate_func(car_cur, front_car, act_dict)
            
        ######################
        for i in range(len(monitor_location)):
            this_loc = monitor_location[i]
            for j in car_a:
                if j.life_flag == 1 and j.last_x < this_loc and j.x >= this_loc:
                    monitorList[i][0].append(current_time)
            for j in car_b:
                if j.life_flag == 1 and j.last_x > this_loc and j.x <= this_loc:
                    monitorList[i][1].append(current_time)
                    
        for i in car_a:
            if i.x > data['road_length'] and i.life_flag == 1:
                i.life_flag = 0
                car_a_start = car_a_start+1
        for i in car_b:
            if i.x <0 and i.life_flag == 1:
                i.life_flag = 0
                car_b_start = car_b_start+1
                
        
        
      
        current_time = current_time+time_step
        counter = counter+1
        for i in intersection:
            T = i.greenlight_time+i.redlight_time
            if (current_time+i.start_phase)%T >= i.greenlight_time:
                i.state = 0
            else:
                i.state = 1
                
        #print(current_time)
        if current_time > data['max_run_time']:
        #if (car_a_start == len(car_a) and car_b_start == len(car_b)) or current_time > data['max_run_time']:
            save_data(car_a, car_b, file_a, file_b, current_time)
            save_light(intersection, file_light, current_time)
            file_a.close()
            file_b.close()
            file_light.close()
            print('End simulation!:')
            print('at time = '+str(current_time))
            #print('Car_A')
            #show(car_a)
            #print('Car_B')
            #show(car_b)
            #show_inter(intersection)
            print()
            break
    print(data['const_reaction_time_flag'])
    print(car_a[0].constant_reaction_time_flag)
    write_infor(data, file_infor, current_time)
    moniWA = open(data['simulation_id']+'\\'+data['simulation_id']+'_monitorA.csv', 'w')
    moniWB = open(data['simulation_id']+'\\'+data['simulation_id']+'_monitorB.csv', 'w')
    save_monitor(monitorList, monitor_location, 0, moniWA)
    save_monitor(monitorList, monitor_location, 1, moniWB)
    moniWA.close()
    moniWB.close()
    file_infor.close()
    collect_infor(data['simulation_id'], data['monitor_location'], data['road_length'], monitorList)
        
def collect_infor(simulation_id, monitor_location, road_length, monitorList):
    car_infor_num = 5

    car_aF = open(simulation_id+'\\'+simulation_id+'_Car_As.txt', 'r')
    car_bF = open(simulation_id+'\\'+simulation_id+'_Car_Bs.txt', 'r')
    light_F = open(simulation_id+'\\'+simulation_id+'_light_state.txt', 'r')
    infor_F = open(simulation_id+'\\'+simulation_id+'_base_infor.txt', 'r')
    base_Fa = open(simulation_id+'\\'+simulation_id+'_base_inforA.txt', 'r')
    base_Fb = open(simulation_id+'\\'+simulation_id+'_base_inforB.txt', 'r')
    car_aF = car_aF.readlines()
    car_bF = car_bF.readlines()
    light_F = light_F.readlines()
    infor_F = infor_F.readlines()
    base_Fa = base_Fa.readlines()
    base_Fb = base_Fb.readlines()
    num_car_a = int((len(car_aF[-1].split())-1)/car_infor_num)
    num_car_b = int((len(car_bF[-1].split())-1)/car_infor_num)
    num_light = int(len(light_F[-1].split())-1)
    
    road_length = float(infor_F[0].split()[1])
    
    
    collect_Fa = open(simulation_id+'\\'+simulation_id+'_count_inforA.txt', 'w')
    collect_Fb = open(simulation_id+'\\'+simulation_id+'_count_inforB.txt', 'w')
    all_Fa = open(simulation_id+'\\'+simulation_id+'_all_inforA.txt', 'w')
    all_Fb = open(simulation_id+'\\'+simulation_id+'_all_inforB.txt', 'w')
    
    s = base_Fa[0].split()
    all_Fa.write('\t'.join(s))
    s = base_Fb[0].split()
    all_Fb.write('\t'.join(s))
    all_Fa.write('\tstart_time\tend_time\tpass_time\tstop_red\tstop_front_car\tspeed_down\n')
    all_Fb.write('\tstart_time\tend_time\tpass_time\tstop_red\tstop_front_car\tspeed_down\n')
    collect_Fa.write('Car_num\tstart_time\tend_time\tpass_time\tstop_red\tstop_front_car\tspeed_down\n')
    collect_Fb.write('Car_num\tstart_time\tend_time\tpass_time\tstop_red\tstop_front_car\tspeed_down\n')
    
    error_point = {}
    
    print('Start reading infor. of Car As')
    print('total num='+str(num_car_a))
    for i in range(num_car_a):
        start_time=0
        end_time=0
        stop_red=0
        stop_front_car=0
        speed_down=0
        for j in range(len(car_aF)-1):
            g = car_aF[j].split()
            gn = car_aF[j+1].split()
            if len(g) < (i+1)*car_infor_num+1:
                continue
            if float(g[i*car_infor_num+1])<0:
                start_time = float(gn[0])
            if float(g[i*car_infor_num+1])<road_length:
                end_time = float(gn[0])
            if float(g[i*car_infor_num+3]) >= 0 and float(gn[i*car_infor_num+3]) < 0:
                speed_down = speed_down+1
            if int(g[i*car_infor_num+4]) == 32 and int(gn[i*car_infor_num+4]) == 31:
                stop_red = stop_red+1
            if int(g[i*car_infor_num+4]) == 22 and int(gn[i*car_infor_num+4]) == 21:
                if float(gn[i*car_infor_num+2]) == 0:
                    stop_red = stop_red+1
                else:
                    stop_front_car = stop_front_car+1
            if i < num_car_a-1:
                if (float(g[i*car_infor_num+1]) < float(g[(i+1)*car_infor_num+1])) and int(g[i*car_infor_num+5]) == 1:
                    error_point['a'+str(i)] = 1
        pass_time = end_time-start_time
        start_time = round(start_time, 4)
        end_time = round(end_time, 4)
        pass_time = round(pass_time, 4)
        s = base_Fa[i+1].split()
        all_Fa.write('\t'.join(s))
        all_Fa.write('\t'+str(start_time)+'\t'+str(end_time)+'\t'+str(pass_time)+'\t'+str(stop_red)+'\t'+str(stop_front_car)+'\t'+str(speed_down)+'\n')
        collect_Fa.write(str(i)+'\t'+str(start_time)+'\t'+str(end_time)+'\t'+str(pass_time)+'\t'+str(stop_red)+'\t'+str(stop_front_car)+'\t'+str(speed_down)+'\n')
        print('.', end='')
        if (i+1)%50 == 0:
            print()
    print()
    print('Start reading infor. of Car Bs')    
    print('total num='+str(num_car_b))
    for i in range(num_car_b):
        start_time=0
        end_time=0
        stop_red=0
        stop_front_car=0
        speed_down=0
        for j in range(len(car_bF)-1):
            g = car_bF[j].split()
            gn = car_bF[j+1].split()
            if len(g) < (i+1)*car_infor_num+1:
                continue
            if float(g[i*car_infor_num+1])>road_length:
                start_time = float(gn[0])
            if float(g[i*car_infor_num+1])>0:
                end_time = float(gn[0])
            if float(g[i*car_infor_num+3]) >= 0 and float(gn[i*car_infor_num+3]) < 0:
                speed_down = speed_down+1
            if int(g[i*car_infor_num+4]) == 32 and int(gn[i*car_infor_num+4]) == 31:
                stop_red = stop_red+1
            if int(g[i*car_infor_num+4]) == 21 and int(gn[i*car_infor_num+4]) == 23:
                if float(gn[i*car_infor_num+2]) == 0:
                    stop_red = stop_red+1
                else:   
                    stop_front_car = stop_front_car+1
            if i < num_car_b-1:
                if (float(g[i*car_infor_num+1]) > float(g[(i+1)*car_infor_num+1])) and int(g[i*car_infor_num+5]) == 1:
                    error_point['b'+str(i)] = 1
        pass_time = end_time-start_time
        start_time = round(start_time, 4)
        end_time = round(end_time, 4)
        pass_time = round(pass_time, 4)
        s = base_Fb[i+1].split()
        all_Fb.write('\t'.join(s))
        all_Fb.write('\t'+str(start_time)+'\t'+str(end_time)+'\t'+str(pass_time)+'\t'+str(stop_red)+'\t'+str(stop_front_car)+str(speed_down)+'\n')
        collect_Fb.write(str(i)+'\t'+str(start_time)+'\t'+str(end_time)+'\t'+str(pass_time)+'\t'+str(stop_red)+'\t'+str(stop_front_car)+str(speed_down)+'\n')
        print('.', end='')
        if (i+1)%50 == 0:
            print()
    print()
    print('Start Count monitor_location')
    infor_Fw = open(simulation_id+'\\'+simulation_id+'_base_infor.txt', 'a')
    for i in range(len(monitor_location)):
        counta = 0
        g = car_aF[-1].split()
        for j in range(num_car_a):
            h = float(g[j*car_infor_num+1])
            if h > monitor_location[i]:
                counta = counta+1
        countb=0
        g = car_bF[-1].split()
        for j in range(num_car_b):
            h = float(g[j*car_infor_num+1])
            if h < monitor_location[i]:
                countb = countb+1
        print('The numbers car pass through location x='+str(monitor_location[i])+' is a='+str(len(monitorList[i][0]))+' b='+str(len(monitorList[i][1])))
        infor_Fw.write('The numbers car pass through location x='+str(monitor_location[i])+' is a='+str(len(monitorList[i][0]))+' b='+str(len(monitorList[i][1]))+'\n')
    print('error_point:'+str(error_point))
    infor_Fw.write('error_point:'+str(error_point)+'\n')
    infor_Fw.close()
        
    collect_Fa.close()
    collect_Fb.close()
    