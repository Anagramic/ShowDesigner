from PIL import Image
import numpy as np
def interpl(bits):
    binRef = {(0,0,0,1,1,0,1):0, '0011001':'1', '0010011':'2', '0111101':'3', '0100011':'4', '0110001':'5', '0101111':'6', '0111011':'7', '0110111':'8', '0001011':'9'}
    return(binRef[bits])

def interpr(bits):
    BinRef = {'1110010':'0', '1100110':'1', '1101100':'2', '1000010':'3', '1011100':'4', '1001110':'5', '1010000':'6', '1000100':'7', '1001000':'8', '1110100':'9'}
    return(BinRef[bits])


def bits_to_number(bits):
    temp = str(bits)
    bits = []
    #print(temp)
    
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
        for _ in range(7):
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
#print(line)

#print(bits_to_number(conv(line,97)))
bits = conv(line,97)
print(bits)
number = bits_to_number(bits)
print(number)
#image = Image.convert('HSV')
#image = np.array(image)