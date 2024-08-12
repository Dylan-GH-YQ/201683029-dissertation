# -*- coding: utf-8 -*-


from tkinter import *
from tkinter import messagebox
import time
root=Tk()
root.title('GoBang')
SIZE=17
win_flag=0
w=Canvas(root,width=SIZE*30,height=SIZE*30,background='Green')
w.pack()
for num in range(1,SIZE):
    w.create_line(num*30,30,num*30,(SIZE-1)*30,width=2)
for num in range(1,SIZE):
    w.create_line(30,num*30,(SIZE-1)*30,num*30,width=2)

color_flag=1 
STEP=0 
matrix = [[0 for i in range(SIZE+2)] for i in range(SIZE+2)] 
min_x=0 
min_y=0
max_x=0
max_y=0

def fresh_outline_rectangle(x,y): 
    global min_x
    global max_x
    global min_y
    global max_y
    global STEP
    if (STEP == 0):  
        min_x = x
        min_y = y
        max_x = x
        max_y = y
#        STEP = 1
    else:
        if(x<min_x):
            min_x=x
        elif(x>max_x):
            max_x=x
        if(y<min_y):
            min_y=y
        elif(y>max_y):
            max_y=y
#    w.create_rectangle(30*min_x,30*min_y,30*max_x,30*max_y,fill='blue',outline='blue')

        

 

shape_score = { (0,1,0):5,          
                (0,1,1,-1):10,       
                (-1,1,1,0):10,       
                (0,1,1,0):20,        
                (-1,1,1,1,0):20,     
                (0,1,1,1,-1):20,     
                (0,1,1,1,0):45,      
                (-1,1,1,1,1,0):60,   
                (0,1,1,1,1,-1):60,   
                (0,1,1,1,1,0):120,   
                (0,1,1,1,1,1,0):300, 
                (0,1,1,1,1,1,-1):300,
                (-1,1,1,1,1,1,0):300,
                (-1,1,1,1,1,1,-1):300,
                (-1,1,1,1,1,1,1,-1):300,
                (-1,1,1,1,1,1,1,1,-1):300,
                }


def evaluate_each(list_ad,list_xw,list_ze,list_cq):  
    score_ad=shape_score.get(tuple(list_ad),0) 
    score_xw = shape_score.get(tuple(list_xw),0)
    score_ze = shape_score.get(tuple(list_ze),0)
    score_cq = shape_score.get(tuple(list_cq),0)
    rank=[score_ad,score_xw,score_ze,score_cq] 
    rank.sort()
    rank.reverse()
    score = rank[0]+rank[1] 
    return  score


def get_list(mx, my,color): 
    global matrix
    list1 = []
    tx = mx
    ty = my
    while (matrix[tx][ty] == color):
        list1.append(1) 
        tx = tx + 1 
        ty = ty
    if (matrix[tx][ty] == -color or tx == 0 or ty == 0 or tx >= SIZE or ty >= SIZE):
        list1.append(-1)
    else:
        list1.append(0)
    list1.pop(0) 
    list2 = []
    tx = mx
    ty = my
    while (matrix[tx][ty] == color):
        list2.append(1)
        tx = tx - 1
        ty = ty
    if (matrix[tx][ty] == -color or tx == 0 or ty == 0 or tx >= SIZE or ty >= SIZE):
        list2.append(-1)
    else:
        list2.append(0)
    list2.reverse()
    list_ad = list2 + list1
    list1 = []
    tx = mx
    ty = my
    while (matrix[tx][ty] == color):
        list1.append(1)
        tx = tx
        ty = ty + 1
    if (matrix[tx][ty] == -color or tx == 0 or ty == 0 or tx >= SIZE or ty >= SIZE):
        list1.append(-1)
    else:
        list1.append(0)
    list1.pop(0)
    list2 = []
    tx = mx
    ty = my
    while (matrix[tx][ty] == color):
        list2.append(1)
        tx = tx
        ty = ty - 1
    if (matrix[tx][ty] == -color or tx == 0 or ty == 0 or tx >= SIZE or ty >= SIZE):
        list2.append(-1)
    else:
        list2.append(0)
    list2.reverse()
    list_xw = list2 + list1
    list1 = []
    tx = mx
    ty = my
    while (matrix[tx][ty] == color):
        list1.append(1)
        tx = tx + 1
        ty = ty + 1
    if (matrix[tx][ty] == -color or tx == 0 or ty == 0 or tx >= SIZE or ty >= SIZE):
        list1.append(-1)
    else:
        list1.append(0)
    list1.pop(0)
    list2 = []
    tx = mx
    ty = my
    while (matrix[tx][ty] == color):
        list2.append(1)
        tx = tx - 1
        ty = ty - 1
    if (matrix[tx][ty] == -color or tx == 0 or ty == 0 or tx >= SIZE or ty >= SIZE):
        list2.append(-1)
    else:
        list2.append(0)
    list2.reverse()
    list_ze = list2 + list1
    list1 = []
    tx = mx
    ty = my
    while (matrix[tx][ty] == color):
        list1.append(1)
        tx = tx + 1
        ty = ty - 1
    if (matrix[tx][ty] == -color or tx == 0 or ty == 0 or tx >= SIZE or ty >= SIZE):
        list1.append(-1)
    else:
        list1.append(0)
    list1.pop(0)
    list2 = []
    tx = mx
    ty = my
    while (matrix[tx][ty] == color):
        list2.append(1)
        tx = tx - 1
        ty = ty + 1
    if (matrix[tx][ty] == -color or tx == 0 or ty == 0 or tx >= SIZE or ty >= SIZE):
        list2.append(-1)
    else:
        list2.append(0)
    list2.reverse()
    list_cq = list2 + list1
    return [list_ad, list_xw, list_ze, list_cq]


def first_step():
    if(matrix[SIZE//2][SIZE//2]==0):
        down_chess(SIZE//2,SIZE//2)
    else:
        down_chess(SIZE//2,SIZE//2+1)

def is_out(min_x,min_y,max_x,max_y):
    if(min_x-2<1): 
        temp_min_x=1
    else:
        temp_min_x=min_x-2
    if(min_y-2<1):
        temp_min_y=1
    else:
        temp_min_y=min_y-2
    if(max_x+2>=SIZE):
        temp_max_x=SIZE
    else:
        temp_max_x=max_x+2
    if(max_y+2>=SIZE):
        temp_max_y=SIZE
    else:
        temp_max_y=max_y+2
    return [temp_min_x,temp_min_y,temp_max_x,temp_max_y]
    
def ai_go(): 
    global min_x
    global max_x
    global min_y
    global max_y
    global color_flag
    global matrix
    global matrix_copy
    time_start=time.time()
    evaluate_matrix=[[0 for i in range(SIZE+2)] for i in range(SIZE+2)]  
    if(STEP==1):
        first_step()
    else: 
#        for i in range(SIZE+2):
#            matrix_copy[i]=matrix[i].copy()
        temp_min_x1,temp_min_y1,temp_max_x1,temp_max_y1=is_out(min_x,min_y,max_x,max_y)
        evaluate_matrix=[[0 for i in range(SIZE+2)] for i in range(SIZE+2)]  
        evaluate_matrix2=[[0 for i in range(SIZE+2)] for i in range(SIZE+2)] 
        Max=-100000
        for i in range(temp_min_x1,temp_max_x1+1):
            for j in range(temp_min_y1,temp_max_y1+1):
                cut_flag=0 
                evaluate_matrix2=[[0 for i in range(SIZE+2)] for i in range(SIZE+2)]  
                if(matrix[i][j]==0):              
                    matrix[i][j]=color_flag  
                    temp_min_x2,temp_min_y2,temp_max_x2,temp_max_y2=is_out(temp_min_x1,temp_min_y1,temp_max_x1,temp_max_y1)
                    for ii in range(temp_min_x2,temp_max_x2+1):
                        for jj in range(temp_min_y2,temp_max_y2+1):
                            if(matrix[ii][jj]==0): 
                                matrix[ii][jj]=-color_flag
                                [list_ad, list_xw, list_ze, list_cq] = get_list(ii, jj,-color_flag)
                                evaluate_matrix2[ii][jj]=-evaluate_each(list_ad, list_xw, list_ze, list_cq)*2+0.1 
                                [list_ad, list_xw, list_ze, list_cq] = get_list(i, j,color_flag)
                                evaluate_matrix2[ii][jj]=evaluate_matrix2[ii][jj]+evaluate_each(list_ad, list_xw, list_ze, list_cq)
                                matrix[ii][jj]=0
                                #alpha-beta
                                if(evaluate_matrix2[ii][jj]<Max):
                                    
                                    evaluate_matrix[i][j]=evaluate_matrix2[ii][jj]
                                    cut_flag = 1
                                                                  

                        if(cut_flag == 1):
                            break
                    #min
                    
                    if(cut_flag == 0):
                        Min=1000000
                        for ii in range(temp_min_x2,temp_max_x2+1):
                            for jj in range(temp_min_y2,temp_max_y2+1):
                                if(evaluate_matrix2[ii][jj]<Min and matrix[ii][jj]==0 and evaluate_matrix2[ii][jj]!=0):
                                    Min=evaluate_matrix2[ii][jj]
                        evaluate_matrix[i][j]=Min
                    
                        if(Max < Min):
                            Max = Min
                            candidate_x=i
                            candidate_y=j
                    matrix[i][j]=0

        '''
        #max                        
        Max2=-100000
        candidate_x=0
        candidate_y=0
        for i in range(temp_min_x1,temp_max_x1+1):
            for j in range(temp_min_y1,temp_max_y1+1):
                if(evaluate_matrix[i][j]>Max2 and matrix[i][j]==0 and evaluate_matrix[i][j]!=0 ):
                    Max2=evaluate_matrix[i][j]
                    candidate_x=i
                    candidate_y=j
        
            
        print("Max:",Max2)
        print("Minx:",temp_min_x1,"Miny:",temp_min_y1)
        for a in range(SIZE+2):
            print(evaluate_matrix[a])
        
        print("MATRIX:")
        for a in range(SIZE+2):
            print(matrix[a])
        print(candidate_x,candidate_y)
        print("matrix(x,y):",matrix[candidate_x][candidate_y])
        #matrix[candidate_x][candidate_y] = color_flag
        '''
        down_chess(candidate_x,candidate_y)
        time_end=time.time()
        print('Time cost:',round(time_end-time_start,4),'second')
        

def action(event): 
    mx=event.x
    my=event.y
    if(mx%30<15):
        xin_x=mx//30*30
    else:
        xin_x=mx//30*30+30
    if(my%30<15):
        xin_y=my//30*30
    else:
        xin_y=my//30*30+30
    int_x=xin_x//30
    int_y=xin_y//30
    if(matrix[int_x][int_y]==0 and win_flag==0):
        down_chess(int_x,int_y)
        if(win_flag==0):
            ai_go()  
        

def down_chess(int_x,int_y): 
    global matrix
    global color_flag
    global STEP
    global win_flag
    if(int_x!=0 and int_y!=0 and int_x<SIZE and int_y<SIZE and matrix[int_x][int_y]==0):
        matrix[int_x][int_y]=color_flag
        fresh_outline_rectangle(int_x,int_y)
        x1,y1=(int_x*30-15),(int_y*30-15)
        x2,y2=(int_x*30+15),(int_y*30+15)
        STEP=STEP+1
        if(color_flag==1):
            w.create_oval(x1,y1,x2,y2,fill='black')
            #label=Label(root,text=str(STEP),bg='black',fg="white") 
            #label.place(x=x1+5,y=y1+3) 
        else:
            w.create_oval(x1,y1,x2,y2,fill='white',width=2)
            #label=Label(root,text=str(STEP),bg='white',fg="black")
            #label.place(x=x1+5,y=y1+3)
        [list_ad, list_xw, list_ze, list_cq] = get_list(int_x, int_y, color_flag)
        if(sum(list_ad[1:-1])>=5 or sum(list_xw[1:-1])>=5 or sum(list_ze[1:-1])>=5 or sum(list_cq[1:-1])>=5):
            if(color_flag==1):
                messagebox.showinfo(title='Game Over', message='Black_Win OVO')   
                win_flag=1
            else:
                messagebox.showinfo(title='Game Over', message='White_Win OVO') 
                win_flag=-1
        color_flag = -color_flag

    else:
        pass
first_step()
w.bind("<Button-1>",action)
mainloop()
