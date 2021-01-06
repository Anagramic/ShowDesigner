from PIL import Image
import numpy as np

def bin_to_dec(binary): 
    decimal = 0 
    for character in str(binary): 
        decimal = decimal*2 + int(character) 

    return(decimal)


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

print(bin_to_dec(conv(line,47)))
#image = Image.convert('HSV')
#image = np.array(image)