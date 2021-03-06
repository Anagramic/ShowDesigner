from PIL import Image
import numpy as np
#The encoding for the left side of the barcode
def interpl(bits):
    binRef = {(0,0,0,1,1,0,1):'0', (0,0,1,1,0,0,1):'1', (0,0,1,0,0,1,1):'2', (0,1,1,1,1,0,1):'3', (0,1,0,0,0,1,1):'4', (0,1,1,0,0,0,1):'5', (0,1,0,1,1,1,1):'6', (0,1,1,1,0,1,1):'7', (0,1,1,0,1,1,1):'8', (0,0,0,1,0,1,1):'9'}
    return(binRef[bits])

#The ENcoding for the right side of the barcode
def interpr(bits):
    BinRef = {(1,1,1,0,0,1,0):'0', (1,1,0,0,1,1,0):'1', (1,1,0,1,1,0,0):'2', (1,0,0,0,0,1,0):'3', (1,0,1,1,1,0,0):'4', (1,0,0,1,1,1,0):'5', (1,0,1,0,0,0,0):'6', (1,0,0,0,1,0,0):'7', (1,0,0,1,0,0,0):'8', (1,1,1,0,1,0,0):'9'}
    return(BinRef[bits])

#Where a binary string is converted into a number, guards and the other way of encoding the smae number(interpl + interpr)
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
    
    for _ in range(4):
        Lguard.append(bits[0])
        del bits[0] 
    

    for _ in range(6):
        digit=[]
        
        for _ in range(7):
            digit.append(bits[0])
            del bits[0]
        
        LHS.append(interpl(tuple(digit)))
    
    for _ in range(5):
        Mguard.append(bits[0])
        del bits[0]

    for _ in range(6):
        digit=[]
        for _ in range(7):
            digit.append(bits[0])
            del bits[0]
        
        RHS.append(interpr(tuple(digit)))
    
    for _ in range(4):
        Rguard.append(bits[0])
        del bits[0]
    
    #if ''.join([str(x) for x in Lguard]) != '1010':
    #    print("Left guard incorrect")
    
    #if ''.join([str(x) for x in Mguard]) != '01010':
    #    print("Mid guard incorrect")
    
    #if ''.join([str(x) for x in Rguard]) != '0101':
    #    print("Right guard incorrect")
    
    #if LHS != RHS:
    #    print("Discrepancy between left and right side")
    
    return(''.join(LHS))

#take a load of one's followed by lots of 0' and so forth and returns the length of those repeats in a list always starting with a one
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
            rep = 1
    encode.append(rep)
    return(encode)


def conv(pixels,digits):   
    num = []
    
    #its imidiate guess of how many pixels to to expect
    length = 0
    #clumps becomes a dictioanry encoded version in a list of dictionarys format
    clumps = dict_encode(pixels)
    #print(clumps)



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
 
        #if reps != 0:
        #print(length)
        #length = clump/reps
        #print(length)
    #print("!")
    #print(num)
    #print("!")

    
    #if len(num) != digits:
        #print(f"Wrong number of digits {len(num)} vs {digits}")
    #    pass
    
    return(num)       

def read_image(image):

    try:
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
        #print(line)

        #print(bits_to_number(conv(line,97)))
        bits = conv(line,97)
        print("".join([str(x) for x in bits]))
        number = bits_to_number(bits)
        return(number)

    except Exception:
        return("Failed to read barcode ")

#manual way of using a file on the machine to scan
def main(pic):
    image=Image.open(pic)
    return(read_image(image))

#if __name__=="__main__":
#    print(main("Test 1.1.jpg"))