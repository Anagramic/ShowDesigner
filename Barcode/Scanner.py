from PIL import Image
import numpy as np

def conv(li,d):   
    num = []
    
    for i in range(d):
        start = li[int((len(li)/d)*(i-1))]
        end = li[int((len(li)/d)*i)]
        ones =0
        zeros =0
        
        for pxl in range(start,end):
            print(pxl)
            
            if pxl == 0:
                zeros+=1
    
            else:
                ones+=1
        
        if zeros>ones:
            num.append(0)
        
        else:
            num.append(1)
    print(num)
    #return(str(''.join(num)))       


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
        line[i] = 1
    
    else:
        line[i] = 0

while True: 
    i=line[0]
    
    if i ==1:
        del line[0]
    
    else:
        break

while True: 
    i=line[len(line)-1]
    
    if i ==1:
        del line[len(line)-1]
    
    else:
        break
#print(line)

print(conv(line,47))






#image = Image.convert('HSV')
#image = np.array(image)