from PIL import Image
import numpy as np
def interpl(bits):
    binRef = {(0,0,0,1,1,0,1):'0', (0,0,1,1,0,0,1):'1', (0,0,1,0,0,1,1):'2', (0,1,1,1,1,0,1):'3', (0,1,0,0,0,1,1):'4', (0,1,1,0,0,0,1):'5', (0,1,0,1,1,1,1):'6', (0,1,1,1,0,1,1):'7', (0,1,1,0,1,1,1):'8', (0,0,0,1,0,1,1):'9'}
    return(binRef[bits])

def interpr(bits):
    BinRef = {(1,1,1,0,0,1,0):'0', (1,1,0,0,1,1,0):'1', (1,1,0,1,1,0,0):'2', (1,0,0,0,0,1,0):'3', (1,0,1,1,1,0,0):'4', (1,0,0,1,1,1,0):'5', (1,0,1,0,0,0,0):'6', (1,0,0,0,1,0,0):'7', (1,0,0,1,0,0,0):'8', (1,1,1,0,1,0,0):'9'}
    return(BinRef[bits])


def bits_to_number(bits):
#    temp = bits
#    bits = []
    #print(temp)
    
#    for i in range(len(temp)):
#        bits.append(temp[i-1])

    Lguard = []
    Mguard = []
    Rguard = []
    LHS    = []
    RHS    = []
    print(bits)
    for _ in range(4):
        Lguard.append(bits[0])
        del bits[0] 
    print(Lguard)
    

    for _ in range(6):
        digit=[]
        for _ in range(7):
            digit.append(bits[0])
            del bits[0]
        
        LHS.append(interpl(tuple(digit)))
    
    for _ in range(5):
        Mguard.append(bits[0])
        del bits[0]
    
    print(len(bits))
    print(bits)

    for _ in range(6):
        digit=[]
        for _ in range(7):
            digit.append(bits[0])
            del bits[0]
        
        RHS.append(interpr(tuple(digit)))
    
    for _ in range(4):
        Rguard.append(bits[0])
        del bits[0]
    
    if ''.join([str(x) for x in Lguard]) != '1010':
        print("Left guard incorrect")
    
    if ''.join([str(x) for x in Mguard]) != '01010':
        print("Mid guard incorrect")
    
    if ''.join([str(x) for x in Rguard]) != '0101':
        print("Right guard incorrect")
    
    if LHS != RHS:
        print("Discrepancy between left and right side")
    
    return(''.join(LHS))

def dict_encode(li):
    encode = []
    bit = 1
    rep = 0
    
    for i in li:
    
        if i == bit:
            rep += 1
    
        else:
            encode.append(rep)
            
            if bit == 1:
                bit = 0
            
            else:
                bit = 1
            rep = 0
    encode.append(rep)
    print(encode)
    return(encode)


def conv(pixels,digits):   
    #li is the stream of pixels as read by the program
    #digits is how many binary bits it should expect. normally 97
    num = []
    
    #its imidiate guess of how many pixels to to expect
    length = 0
    #li becomes a dictioanry encoded version in a list of dictionarys format
    clumps = dict_encode(pixels)


    bit = 1

    #for each clump of numbers, divide that by what one bit should be to see how many bars are there next to each other
    for clump in clumps:

        if len(num) == 0:
            length = clump

        reps = round(clump/length) #bars next to each other
        
        
        for _ in range( int(reps)):
            num.append(bit) # put a 1 or 0 in for each bar next to each other there is
        
        if bit == 1:
            bit = 0

        else:
            bit = 1
        
        length = clump/reps
    
    if len(num) != digits:
        print(f"Wrong number of digits {len(num)} vs {digits}")
    
    return(num)       


image=Image.open("test4.jpg")
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
    
    if line[0] ==0:
        del line[0]
    
    else:
        break

while True:  
    
    if line[len(line)-1] ==0:
        del line[len(line)-1]
    
    else:
        break
print(line)

#print(bits_to_number(conv(line,97)))
bits = conv(line,97)
print(bits)
number = bits_to_number(bits)
print(number)
#image = Image.convert('HSV')
#image = np.array(image)