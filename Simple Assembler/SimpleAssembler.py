import sys

A = {'add': '10000', 'sub': '10001', 'mul': "10110",'xor': '11010', 'or': '11011', 'and': '11100'}
B = {'mov': '10010', 'ls': '11001'}
C = {"mov": "10011", "not": "11101", "cmp": "11110", "div": "10111"}
D = {"ld": "10100", "st": "10101"}
E = {"jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111"}
F = {"hlt": "01010"}
reg_add = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011','R4': '100', 'R5': '101', "R6": "110","FLAGS":"111"}
Cd = [A, B, C, D, E, F]
Var = []
cnt = 0

source_code = sys.stdin.read().rstrip()
lines = source_code.split("\n")

check = 0
hlt_chk=0
hlt_a=0
cnt1=0
check_var=0
check_var1=0

for line in lines:
    if line == '' :
        print('empty line')
        exit(0)
    instruction, *operands = line.split()
    chk_ins=0 
    cnt1+=1

    if instruction=="var":
        Var=operands.copy()

    if hlt_chk==1 :
        print('hlt not being used as the last instruction')
        exit(0)



    if instruction=='hlt' :
        hlt_chk=1

    for i in Cd :#Typo in instruction name
        if instruction in i.keys() :
            chk_ins=1
            break 
    #check the particular line
    
    if (chk_ins==0 and instruction[len(instruction)-1]==":"):
            chk_ins=1
    if(chk_ins==0 and instruction!='var') :
        print('Typos in instruction name')
        exit(0)

    for i in operands :#Typo in register 
        if i[0]=='R' :
            if int(i[1:])>6 :
                print('Typos in register name')
                exit(0)
        
    for i in operands :#Illegal immediate values
        if i[0]=='$' :
            xy = i[1:]
            xyz=int(xy)
            if xyz>255 or xyz<0 :
                print('Illegal Immediate values(more than 8 bits) ')

    if instruction in D.keys():#Use of undefined variables
        for i in Var:
            if i not in operands[len(operands)-1]:
                print("Undefined variable/label used in place of variable")
                exit(0)

    if instruction =='var' :
        check_var=1
    elif instruction!='var':
        check_var=0
        check_var1=1
    elif check_var==1 and check_var1==1 :
        print('variable error')
        exit(0)

if hlt_chk!=1 :
    print('missing hlt instruction')
    exit(0)



for line in lines :
    s=''
    instruction, *operands=line.split()
    if instruction[len(instruction)-1] ==":":
        if instruction[0:len(instruction)-1] in Var:
            print("Labels used instead of register ")
            exit(0)
        for i in operands:
            if i!=instruction:
                i,instruction=instruction,i
                operands=operands[1:]
                

                
                break
            else:
                continue
    
        
#TYPE-F
    if (instruction in F.keys() and operands == []):
        if (len(operands)>0):
            print("Invalid register use")
            exit(0)
        check=1
        hlt_chk=1
        s += F[instruction]+'0'*11
        sys.stdout.write(s)
        print()
 
# TYPE-A
    elif instruction in A.keys():
        check=1
        if(len(operands)!=3) :
            print('insufficient reg')
            exit(0)
        for i in range(0,len(operands)):
            if operands[i] not in reg_add.keys():
                print("Register name typo")
                exit(0)
        s += A[instruction]
        s += '00'
        for i in operands:
            s += reg_add[i]
        sys.stdout.write(s)
        print()
    
# TYPE-B 
    elif operands[len(operands)-1] not in reg_add.keys() and operands!=[] and instruction in B.keys() :
        check=1
        if operands[0] not in reg_add.keys():
            print("Register Name typo")
            exit(0)
        if (len(operands)!=2):
            print("Insufficient registers")
            exit(0)
        s += B[instruction]
        s += reg_add[operands[0]]
        s1= bin(int(operands[1][1:]))
        if len(s1[2:])>8 and 0<=int(operands[1][1:])<=255:
            print("Illegal value of Imm")
            exit(0)
        s += '0'*(8-len(s1)+2)
        s+=s1[2:]
        sys.stdout.write(s)
        print()

#TYPE-C       
    elif (instruction in C.keys() and operands[len(operands)-1] in reg_add.keys()) :
        check=1
        for i in range(0,len(operands)):
            if operands[i] not in reg_add.keys():
                print("Register name typo")
                exit(0)
        if len(operands)!=2:
            print("insufficient operands")
            exit(0)
            
        s += C[instruction]
        s += '00000'
        for i in operands:
            s += reg_add[i]
        sys.stdout.write(s)
        print()
    
#TYPE-D
    elif instruction in D.keys() :
        if (len(operands)!=2):
            print("Insufficient commands")
            exit(0)
        if operands[0] not in reg_add.keys():
            print("Register name typo")
        check=1
        s+=D[instruction]
        s+=reg_add[operands[0]]
        
        s1= bin(cnt1-1)
        
        s += '0'*(8-len(s1)+2)
        s+=s1[2:]
        sys.stdout.write(s)
        print()

#Type E
    elif instruction in E.keys() :
        if (len(operands)!=1):
            print()
        check=1
        s+=E[instruction]
        s+='0'*3
        s1=bin(cnt1-1)
        s+= '0'*(8-len(s1)+2)
        s+=s1[2:]
        sys.stdout.write(s)
        print()
