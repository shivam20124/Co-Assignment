# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 16:20:18 2021

@author: shiva
"""

def own_split(x):
    lis = []
    for i in range(0, len(x)):
        if x[i] != "":
            lis.append(x[i])
    return(lis)
  


def convertbin(n):
    y = ""
    y  = bin(n)
    y = y[2:]
    l = len(y)
    out = ("0")*(8-l) + y
    return out

def mov(x):
    if x[2][0] == "R":
        reg_dict[x[1]] = int(reg_dict[x[2]])
        out = "00011" + "00000" + op_dict[x[1]] + op_dict[x[2]]
        o_list.append(out)
    else:
        num = x[2][1:]
        if (int(num) > 255):
            print("error")
            return("error")
        reg_dict[x[1]] = int(num)
        bit_8 = convertbin(int(num))
        out = "00010" + op_dict[x[1]] + bit_8
        o_list.append(out)


def add(x):
    sum_reg = reg_dict[x[2]] + reg_dict[x[3]]
    #if sum_reg > 65535:
        
    reg_dict[x[1]] = sum_reg
    out = "00000" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)
    
    
def sub(x):
    dif_reg = reg_dict[x[2]] - reg_dict[x[3]]    
    if dif_reg >=0:
        reg_dict[x[1]] = dif_reg
        out = "00001" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
        o_list.append(out)
    else:
        reg_dict[x[1]] = 0
    

def mul(x):
    pro_reg = (reg_dict[x[2]])*(reg_dict[x[3]]) 
    if pro_reg < 256:
        reg_dict[x[1]] = pro_reg
        out = "00110" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
        o_list.append(out)


def div(x):
    quot = (reg_dict[x[1]])//(reg_dict[x[2]])
    rem = (reg_dict[x[1]])%(reg_dict[x[2]])
    reg_dict["R0"] = quot
    reg_dict["R1"] = rem
    out = "00111" + "00000" + op_dict[x[1]] + op_dict[x[2]]
    o_list.append(out)


def or_r(x):
    or_reg = (reg_dict[x[2]])|(reg_dict[x[3]]) 
    reg_dict[x[1]] = or_reg
    out = "01011" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)
    
    
def and_r(x):
    and_reg = (reg_dict[x[2]])&(reg_dict[x[3]]) 
    reg_dict[x[1]] = and_reg
    out = "01100" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)


def not_r(x):
    reg_dict[x[1]] = ~(reg_dict[x[2]])
    out = "01101" + "00000" + op_dict[x[1]] + op_dict[x[2]]
    o_list.append(out)


def xor(x):
    not_a = ~(reg_dict[x[2]])
    a = reg_dict[x[2]]
    b = reg_dict[x[3]]
    not_b = ~(reg_dict[x[3]])
    xor_reg = ((a)&(not_b))|((not_a)&b)
    reg_dict[x[1]] = xor_reg
    out = "01010" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)


def rs(x):
    num = x[2][1:]
    shifted = (reg_dict[x[1]])>>(int(num))
    reg_dict[x[1]] = shifted
    bit_8 = convertbin(int(num))
    out = "01000" + op_dict[x[1]] + bit_8
    o_list.append(out)


def ls(x):
    num = x[2][1:]
    shifted = (reg_dict[x[1]])<<(int(num))
    reg_dict[x[1]] = shifted
    bit_8 = convertbin(int(num))
    out = "01001" + op_dict[x[1]] + bit_8
    o_list.append(out)

count = 0;

def ins_func(x):
    global count 
    
    if x[0] == "mov":
        count += 1
        mov(x)
        
    elif x[0] == "add":
        count +=1
        add(x)
            
    elif x[0] == "sub":
        count +=1
        sub(x)
            
    elif x[0] == "mul":
        count +=1
        mul(x)
            
    elif x[0] == "div":
        count +=1
        div(x)
            
    elif x[0] == "or":
        count +=1
        or_r(x)
        
    elif x[0] == "and":
        count += 1
        and_r(x)
            
    elif x[0] == "not":
        count += 1
        not_r(x)
            
    elif x[0] == "xor":
        count += 1
        xor(x)
            
    elif x[0] == "rs":
        count +=1
        rs(x)
            
    elif x[0] == "ls":
        count += 1
        ls(x)


reg_dict = {"R0" : 0, "R1" : 0, "R2" : 0, "R3" : 0, "R4" : 0, "R5" :0, "R6" : 0, "FLAGS" : "0000"}
op_dict = {"R0" : "000", "R1" : "001", "R2" : "010", "R3" : "011", "R4" : "100", "R5" : "101", "R6" : "110", "FLAGS" : "111"}
var_count = {}

o_list=[]
fi = open('input.txt', 'r+')
inp = fi.read()
inp = inp.split('\n')
for i in range(0,len(inp)):
    
    
    x = inp[i].split(' ')

    x = own_split(x)
    print(x)
    
    
    if x[0][-1] == ":":
        #label wala function
        continue
    
    if (x[0] == "var"):
        var_count[x[1]] = count
    
    else:
        ins_func(x)

fi.close()
        

                    
           


for i in range(0,len(o_list)):
    print(o_list[i])

print(" ")
print(var_count)
print(" ")
print(reg_dict)
print(count)

