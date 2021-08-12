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


def check_3(x):
    if (len(x) !=4) or (x[1] not in reg_list) or (x[2] not in reg_list) or (x[3] not in reg_list):
        global error_flag
        error_flag = 1
        out = "Invalid Syntax. Error in Line" + str(count)
        o_list.append(out)
        return(False)

def mov(x):
    if len(x) !=3:
        global error_flag
        error_flag = 1
        out = "Invalid Syntax. Error in line" + str(count)
        o_list.append(out)
        return()
    if (x[1] in reg_list) and (x[2] in reg_list):
        reg_dict[x[1]] = int(reg_dict[x[2]])
        out = "00011" + "00000" + op_dict[x[1]] + op_dict[x[2]]
        o_list.append(out)
        
    elif (x[2] == "FLAGS") and (x[1] in reg_list):
        out = "00011" + "0000" + op_dict[x[1]] + op_dict[x[2]]
        o_list.append(out)
        
    elif (x[2][0] == "$") and (x[1] in reg_list):
        num = x[2][1:]
        try:
            num = int(num)
        except:
            global error_flag
            error_flag = 1
            out = "Invalid Immediate Value. Error in line" + str(count)
            o_list.append(out)
            return()
        
        if (num > 255) or (num < 0):
            global error_flag
            error_flag = 1
            out = "Invalid Immediate Value. Error in line" + str(count)
            o_list.append(out)
            
        else:
            reg_dict[x[1]] = int(num)
            bit_8 = convertbin(int(num))
            out = "00010" + op_dict[x[1]] + bit_8
            o_list.append(out)
            
    else:
        global error_flag
        error_flag = 1
        out = "Invalid Syntax. Error in Line" + str(count)
        o_list.append(out)
        


def add(x):
    if (check_3(x) == False):
        return()
    sum_reg = reg_dict[x[2]] + reg_dict[x[3]]
    if sum_reg > 65535:  # greatest 16 bit number
        reg_dict[x[1]]= 65535 & sum_reg
        reg_dict["FLAGS"]="1000"
        
    else:
        reg_dict[x[1]] = sum_reg
        reg_dict["FLAGS"]="0000"
        
        
    out = "00000" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)
    
    
def sub(x):
    if (check_3(x) == False):
        return()
    dif_reg = reg_dict[x[2]] - reg_dict[x[3]]    
    if dif_reg >=0:
        reg_dict[x[1]] = dif_reg
        reg_dict["FLAGS"]="0000" 
        
    else:
        reg_dict[x[1]] = 0
        reg_dict["FLAGS"]="1000"
        
    out = "00001" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)
    

def mul(x):
    if (check_3(x) == False):
        return()
    
    pro_reg = (reg_dict[x[2]])*(reg_dict[x[3]]) 
    if pro_reg < 65535:
        reg_dict[x[1]] = pro_reg
        reg_dict["FLAGS"]="0000"
    else:
         reg_dict[x[1]]= 65535 & pro_reg
         reg_dict["FLAGS"]="1000"
        
    out = "00110" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)


def div(x):
    if (len(x) !=3) or (x[1] not in reg_list) or (x[2] not in reg_list):
        global error_flag
        error_flag = 1
        out = "Invalid Syntax. Error in Line" + str(count)
        o_list.append(out)
        return()
    quot = (reg_dict[x[1]])//(reg_dict[x[2]])
    rem = (reg_dict[x[1]])%(reg_dict[x[2]])
    reg_dict["R0"] = quot
    reg_dict["R1"] = rem
    out = "00111" + "00000" + op_dict[x[1]] + op_dict[x[2]]
    o_list.append(out)
    reg_dict["FLAGS"]="0000"


def or_r(x):
    if (check_3(x) == False):
        return()
    
    or_reg = (reg_dict[x[2]])|(reg_dict[x[3]]) 
    reg_dict[x[1]] = or_reg
    out = "01011" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)
    reg_dict["FLAGS"]="0000"
    
    
def and_r(x):
    if (check_3(x) == False):
        return()
    
    and_reg = (reg_dict[x[2]])&(reg_dict[x[3]]) 
    reg_dict[x[1]] = and_reg
    out = "01100" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)
    reg_dict["FLAGS"]="0000"

def not_r(x):
    if (len(x) !=3) or (x[1] not in reg_list) or (x[2] not in reg_list):
        global error_flag
        error_flag = 1
        out = "Invalid Syntax. Error in Line" + str(count)
        o_list.append(out)
        return()
    
    reg_dict[x[1]] = ~(reg_dict[x[2]])
    out = "01101" + "00000" + op_dict[x[1]] + op_dict[x[2]]
    o_list.append(out)
    reg_dict["FLAGS"]="0000"


def xor(x):
    if (check_3(x) == False):
        return()
    
    not_a = ~(reg_dict[x[2]])
    a = reg_dict[x[2]]
    b = reg_dict[x[3]]
    not_b = ~(reg_dict[x[3]])
    xor_reg = ((a)&(not_b))|((not_a)&b)
    reg_dict[x[1]] = xor_reg
    out = "01010" + "00" + op_dict[x[1]] + op_dict[x[2]] + op_dict[x[3]]
    o_list.append(out)
    reg_dict["FLAGS"]="0000"


def rs(x):
    num = x[2][1:]
    if (int(num)>255) | (int(num<0)):
        out = "Error, imm out of range"
        
    else:
        shifted = (reg_dict[x[1]])>>(int(num))
        reg_dict[x[1]] = shifted
        bit_8 = convertbin(int(num))
        out = "01000" + op_dict[x[1]] + bit_8
    o_list.append(out)
    reg_dict["FLAGS"]="0000"


def ls(x):
    num = x[2][1:]
    if (int(num)>255) | (int(num<0)):
        out = "Error, imm out of range"
    else: 
        shifted = (reg_dict[x[1]])<<(int(num))
        reg_dict[x[1]] = shifted
        bit_8 = convertbin(int(num))
        out = "01001" + op_dict[x[1]] + bit_8
    o_list.append(out) 
    reg_dict["FLAGS"]="0000"
    
def ld(x):
    if len(x)==3:
        if(x[2] in var_dict) and x[1] in op_dict and x[1]!="FLAGS":
            out="00100"+op_dict[x[1]]+convertbin(var_dict[x[2]])
            o_list.append(out)
        else:
            global error_flag
            error_flag=1
            out="Error in line " + str(count)+" Memory address doesnt exist"
            o_list.append(out)
            return()
    else:
        global error_flag
        error_flag=1
        out="Error in line "+str(count)+" Invalid syntax."
        o_list.append(out)
            

def st(x):
     if len(x)==3:
        if(x[2] in var_dict) and x[1] in op_dict and x[1]!="FLAGS":
            out="00101"+op_dict[x[1]]+convertbin(var_dict[x[2]])
            o_list.append(out)
        else:
            global error_flag
            error_flag=1
            out="Error in line " + str(count)+" Memory address doesnt exist"
            o_list.append(out)
            return()
     else:
        global error_flag
        error_flag=1
        out="Error in line "+str(count)+" Invalid syntax."
        o_list.append(out)
        

    
            
    
def cmp(x):
    if (len(x) !=3) or (x[1] not in reg_list) or (x[2] not in reg_list):
        global error_flag
        error_flag = 1
        out = "Invalid Syntax. Error in Line" + str(count)
        o_list.append(out)
        return()
    
    if(reg_dict[x[1]]>reg_dict[x[2]]):
        reg_dict["FLAGS"] ="0010"
        
    elif(reg_dict[x[1]]<reg_dict[x[2]]):
        reg_dict["FLAGS"] ="0100"
        
    elif(reg_dict[x[1]] == reg_dict[x[2]]):
        reg_dict["FLAGS"] ="0001"  
        
    out = "01110"+"00000" + op_dict[x[1]] + op_dict[x[2]]
    o_list.append(out)
        
def jmp(x):
    reg_dict["FLAGS"]="0000"
    temp_dict=dict(label_dict)
    for i in temp_dict:
        if i in label_dict:
            temp_dict[i]=label_dict[i][0]
    for i in temp_dict:
        if(x[1]==i):
            bit_8=convertbin(temp_dict[i])
            out="01111"+"000"+bit_8        
            o_list.append(out)
            return()
    out = "Error, no such label defined in line" + count
    o_list.append(out)
    global error_flag
    error_flag = 1
    
def jlt(x):
    if(reg_dict["FLAGS"]=="0100"):
        temp_dict=dict(label_dict)
        for i in temp_dict:
            if i in label_dict:
                temp_dict[i]=label_dict[i][0]
        for i in temp_dict:
            if(x[1]==i):
                bit_8=convertbin(temp_dict[i])
                out="10000"+"000"+bit_8
                o_list.append(out)
        out = "Error, no such label defined in line" + count
        o_list.append(out)
        global error_flag
        error_flag = 1
    
def jgt(x):
    if(reg_dict["FLAGS"]=="0010"):
        temp_dict=dict(label_dict)
        for i in temp_dict:
            if i in label_dict:
                temp_dict[i]=label_dict[i][0]
        for i in temp_dict:
            if(x[1]==i):
                bit_8=convertbin(temp_dict[i])
                out="10001"+"000"+bit_8
        o_list.append(out)
    
def je(x):
    if(reg_dict["FLAGS"]=="0001"):
        temp_dict=dict(label_dict)
        for i in temp_dict:
            if i in label_dict:
                temp_dict[i]=label_dict[i][0]
        for i in temp_dict:
            if(x[1]==i):
                bit_8=convertbin(temp_dict[i])
                out="10010"+"000"+bit_8
        o_list.append(out)    


def ins_func(x):
    
    
    if x[0] == "mov":
        
        mov(x)
        
    elif x[0] == "add":
       
        add(x)
            
    elif x[0] == "sub":
       
        sub(x)
            
    elif x[0] == "mul":
       
        mul(x)
            
    elif x[0] == "div":
       
        div(x)
            
    elif x[0] == "or":
        
        or_r(x)
        
    elif x[0] == "and":
       
        and_r(x)
            
    elif x[0] == "not":
       
        not_r(x)
            
    elif x[0] == "xor":
        
        xor(x)
            
    elif x[0] == "rs":
       
        rs(x)
            
    elif x[0] == "ls":
        
        ls(x)
    
    elif x[0] == "cmp":
        cmp(x)
        
    elif x[0] == "jmp":
        jmp(x)
        
    elif x[0] == "jlt":
        jlt(x)
        
    elif x[0] == "jgt":
        jgt(x)
        
    elif x[0] == "je":
        je(x)


reg_dict = {"R0" : 0, "R1" : 0, "R2" : 0, "R3" : 0, "R4" : 0, "R5" :0, "R6" : 0, "FLAGS" : "0000"}
op_dict = {"R0" : "000", "R1" : "001", "R2" : "010", "R3" : "011", "R4" : "100", "R5" : "101", "R6" : "110", "FLAGS" : "111"}
reg_list = ["R0", "R1", "R2", "R3", "R4", "R5", "R6"]
var_dict = {}
label_dict={}
ins_list=["add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]
firstCount=-1
#firstAbsoluteCount=0
count = 0
var_flag=0 #var in beginning
hlt_flag=0 #hlt in end
error_flag=0   #when a fucntion is returning some error

o_list=[]
fi = open('input.txt', 'r+')
inpu = fi.read()
inpu = inpu.split('\n')
inp = []
for i in inpu:
    if(i!=""):
        inp.append(i)

for i in range(0,len(inp)):  #firts pass
    
    labelError=0
    varError=0
    x = inp[i].split(' ')

    x = own_split(x)
    print(x[0])
    firstCount+=1
    #firstAbsoluteCount+=1
    
    if(x[0][-1]==":"):
        if(x[0][0:-1] not in ins_list and x[0][0:-1] not in var_dict ):
            label_dict[x[0][0:-1]]=[firstCount,x[1:]]
        else:
           
            labelError=i+1
            error_flag=1
            break
            
    if(x[0]=="var"):
        
        if len(x) >1:
       
            if(x[1]  not in ins_list and x[1] not in label_dict):
                firstCount-=1
                var_dict[x[1]]=0
            else:
                error_flag=1
                varError=i+1
                break
        else:
            error_flag = 1
            varError = i+1
            break
        
            
            
for key in var_dict:
    var_dict[key]=firstCount+1
    firstCount+=1
    
    
    

for i in range(0,len(inp)):  #second pass
    
    
    x = inp[i].split(' ')

    x = own_split(x)
    
    count+=1
    print(x[0])
    if(error_flag==1):
        if(count==labelError):
            out="invalid label name in line  "+ count
            o_list.append(out)
            break
        elif(count==varError):
            out="inavlid var name in line "+ count
            o_list.append(out)
            break

           
    if(hlt_flag==0):  #if we havent encountered hlt instruction yet
        
        if x[0][-1] == ":" :  #label
            ins_func(x[1:])
            var_flag=1
       
    
        elif (x[0] == "var") :
            if(var_flag==1):
                print("Error in line ",count,". Variables must be defined in beginning")
                break
        
        elif(x[0]=="hlt"):
            var_flag=1
            hlt_flag=1
            
           
        elif(x[0] not in ins_list) :
            var_flag=1
            out = "invalid instruction name in line " + str(count)
            o_list.append(out)
            break
    
        else:
            var_flag=1
            ins_func(x)
    else:
        print("Error in line ",count-1,". Hlt instruction should be in end.")
        break
    
    
fi.close()     
for i in range(0,len(o_list)):
    print(o_list[i])   
if(hlt_flag!=1)and(error_flag!=1):
    print("Error.Hlt instruction not found")

        
          
           




print(" ")

print(" ")
print(reg_dict)
print(count)
