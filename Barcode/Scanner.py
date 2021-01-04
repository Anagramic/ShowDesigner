from PIL import Image
import numpy as np

def bin_to_dec(binary):
    i=0
    length = len(str(binary)) -1
    dec = 0
    while binary != '':
        if binary[length] == 1:
            dec += 2^i
            del binary[length]
        
        i+=1

    return(dec)


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


image=Image.open("1.jpg")
image = image.convert('HSV')#makes it b+w
#image.show()
width, height = image.size

line = []
pix = image.load()

for i in range(width):
    line.append(list(pix[i,height/2])[2])

for i in range(len(line)):
    
    if int(line[i]) > 127:
        line[i] = 0
    
    else:
        line[i] = 1

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

print(bin_to_dec(conv(line,47)))






#image = Image.convert('HSV')
#image = np.array(image)