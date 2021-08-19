# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 20:53:39 2021

@author: AKSHITA
"""
from sys import stdin

mem=['0000000000000000']*256 #initialising memory

pc=0
reg_file=[0]*8
halt=False
ins_list=[]
op_dict={"00000":add,"00001":sub,"00010":mov_im,
         "00011":mov_reg,"00100":load,"00101":store,"00110":mul,"00111":div,
         "01000":rs,"01001":ls,"01010":xor,"01011":Or,"01100":And,"01101":invert,
         "01110":cmp,"01111":jmp,"10000":jlt,"10001":jgt,"10010":je,"10011":hlt}



def load(s):    
    reg=int(s[5:8],2)
    mem_add=int(s[8:],2)
    reg_file[reg]=int(mem[mem_add],2)
    global pc
    pc+=1
    reg_file[7]=0

def store(s):
    reg=int(s[5:8],2)
    mem_add=int(s[8:],2)
    val=convertBin(reg_file[reg],16)
    mem[mem_add]=val
    global pc
    pc+=1
    reg_file[7]=0    


def rs(s):
    reg=int(s[5:8],2)
    imm=int(s[8:],2)
    reg_file[reg]=reg_file>>imm
    global pc
    pc+=1
    reg_file[7]=0
    
    
def ls(s):
    reg=int(s[5:8],2)
    imm=int(s[8:],2)
    reg_file[reg]=reg_file<<imm
    global pc
    pc+=1
    reg_file[7]=0
    
    
def cmp(s):
    reg1=int(s[10:13],2)
    reg2=int(s[13:],2)
    val1=reg_file[reg1]
    val2=reg_file[reg2]
    if(val1==val2):
        reg_file[7]=1
    elif(val1>val2):
        reg_file[7]=2
    else:
        reg_file[7]=3
    global pc
    pc+=1

def jmp(s):
    mem_add=int(s[8:],2)
    pc=mem_add
    reg_file[7]=0  
    
    
       
    
    
def convertBin(n,b):
    y=bin(n)
    y=y[2:]
    l=len(y)
    y="0"*(b-l)+ str(y)
    return y
    


    
    
for line in stdin:
    ins_list.append(line)
    
for i in range(0,len(ins_list)):
    mem[i]=ins_list[i]
    

while(halt==False):
    curr_ins=mem[pc]
    print(convertBin(pc,8),end=" ")
    op_dict[curr_ins[0:5]](curr_ins)
    for i in reg_file:
        print(convertBin(i,16),end=" ")
    print("\n")
   

for i in mem:
    print(i)
   
