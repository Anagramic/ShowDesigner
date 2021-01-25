from PIL import Image
import numpy as np
def interpl(bits):
    binRef = {'0001101':'0', '0011001':'1', '0010011':'2', '0111101':'3', '0100011':'4', '0110001':'5', '0101111':'6', '0111011':'7', '0110111':'8', '0001011':'9'}
    return(binRef[bits])

def interpr(bits):
    BinRef = {'1110010':'0', '1100110':'1', '1101100':'2', '1000010':'3', '1011100':'4', '1001110':'5', '1010000':'6', '1000100':'7', '1001000':'8', '1110100':'9'}
    return(BinRef[bits])


def bits_to_number(bits):
    temp = str(bits)
    bits = []
    print(temp)
    
    for i in range(len(temp)):
        bits.append(temp[i-1])

    Lguard = []
    Mguard = []
    Rguard = []
    LHS    = []
    RHS    = []
    
    for i in range(4):
        Lguard.append(bits[0])
        del bits[0] 
    

    for i in range(6):
        digit=[]
        for bit in range(7):
            digit.append(bits[0])
            del bits[0]
        
        LHS.append(interpl(''.join(digit)))
    
    for i in range(5):
        Mguard.append(bits[0])
        del bits[0]
    
    for i in range(6):
        digit=[]
        for bit in range(7):
            digit.append(bits[0])
            del bits[0]
        
        RHS.append(interpr(''.join(digit)))
    
    for i in range(4):
        Rguard.append(bits[0])
        del bits[0]
    
    if ''.join(Lguard) != '1010':
        print("Left guard incorrect")
    
    if ''.join(Mguard) != '01010':
        print("Mid guard incorrect")
    
    if ''.join(Rguard) != '0101':
        print("Right guard incorrect")
    
    if LHS != RHS:
        print("Discrepancy between left and right side")
    
    return(''.join(LHS))

        

def conv(li,digits):   
    #method 1
    num = []
    
    for i in range(digits):
#        start = li[int((len(li)/d)*(i-1))]
#        end = li[int((len(li)/d)*i)]
        start = int((i/digits) * len(li))
        end = int(((i+1)/digits) * len(li))
        
        ones =0
        zeros =0
        
        for pxl in range(start,end):
            
            if li[pxl] == 0:
                zeros+=1
    
            else:
                ones+=1
        
        if zeros>ones:
            num.append('0')
        
        else:
            num.append('1')
    #method1 = num

    ##method2
    #num = []
    #(len(li)/dig)/2 = Mid
    #if Type(Mid) == 'float':
    #    mid += 0.5
   # 
   # for i in range(digits):
   #     num.append(li[mid+(len(li)/digits)*(i-1)])


    
    return(int(''.join(num)))       


image=Image.open("test1.jpg")
image = image.convert('HSV')#makes it b+w
#image.show()
width, height = image.size

line = []
pix = image.load()

#converts a tuple into one 0 to 255
for i in range(width):
    line.append(list(pix[i,height//2])[2])

#finds the whitest pixel and the darkest pixel and uses that to to judge if it is a black bar or a white bar
maximum = line[0]
minimum = line[0]

for i in line:
    if i >= maximum:
        maximum = i

    if i <= minimum:
        minimum = i


#decides if it is closer to black or white
for i in range(len(line)):
    
    if int(line[i]) > (maximum + minimum)//2 :
        line[i] = 0
    
    else:
        line[i] = 1

#trims the 0s off both ends
while True: 
    i=line[0]
    
    if i ==0:
        del line[0]
    
    else:
        break

while True: 
    i=line[len(line)-1]
    
    if i ==0:
        del line[len(line)-1]
    
    else:
        break
print(line)

print(bits_to_number(conv(line,97)))


#image = Image.convert('HSV')
#image = np.array(image)