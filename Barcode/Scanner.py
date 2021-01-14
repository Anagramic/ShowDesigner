from PIL import Image
import numpy as np

def bits_to_number(bits):
    LHS = []
    RHS = []
    binRef = {'0':'0001101', '1':'0011001', '2':'0010011', '3':'0111101', '4':'0100011', '5':'0110001', '6':'0101111', '7':'0111011', '8':'0110111', '9':'0001011'}
    temp = []
    for i in range(4):
        x = bits[0]
        temp.pop(x)
        del x
    joined = str(''.join(temp))
    if joined != "1010":
        print("Unexpected starting digits of "+joined)
    

    for number in range(6): #6 numbers to find
        temp = []
        for bit in range(7): #1 number is represented by 7 bits
            temp.pop(bits[0])
        LHS.append(binRef[''.join(temp)])
    
    temp = []
    for i in range(5):
        temp.pop(bits[0])
    joined = str(''.join(temp))
    if joined != "01010":
        print("Unexpected starting digits of "+joined)
    
    for number in range(6): #6 numbers to find
        temp = []
        
        for bit in range(7): #1 number is represented by 7 bits
            
            if bits[0] == '1':
                temp.append('0')
            
            else:
                temp.append('1')
            del bits[0]
    

        RHS.append(binRef[''.join(temp)])
    for i in range(4):
        temp.pop(bits[0])
    
    joined = str(''.join(temp))        
    if joined != "0101":
        print("Unexpected starting digits of "+joined)
    right = ''.join(RHS)
    left = ''.join(LHS)
    
    if left != right:
        print("Unexpected discrepancy between the left and right side")
    
    return(LHS)
    
    

    
        
            


        


def conv(li,digits):   
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
    
    return(int(''.join(num)))       


image=Image.open("482282.png")
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
#print(line)

print(bits_to_number(conv(line,97)))


#image = Image.convert('HSV')
#image = np.array(image)