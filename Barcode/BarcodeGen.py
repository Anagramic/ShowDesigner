from PIL import Image, ImageDraw
import random as r
def draw(code):
    width = 97
    height = 10
    img = Image.new( 'RGB', (width,height), "white") # create a new white image
    pixels = img.load() # create the pixel map
    
    for h in range(height):
        for w in range(width):
            if code[w-1] == '1':
                pixels[w-1,h-1] = (0,0,0)
    
    img.save(dec+".png")

            


def getNew():
    return(str(r.randint(100000,999999)))

OddP = {'0':'0001101', '1':'0011001', '2':'0010011', '3':'0111101', '4':'0100011', '5':'0110001', '6':'0101111', '7':'0111011', '8':'0110111', '9':'0001011'}
dec = getNew()

binary = []
for i in range (len(dec)):
    binary.append(OddP[dec[i-1]])

LHS = ''.join(binary)
#apply two's compliment
binary = []
for i in range(len(LHS)):
    if LHS[i-1] == '0':
        binary.append('1')
    else:
        binary.append('0')

RHS = ''.join(binary)

code = str("1010"+LHS+'01010'+RHS+"0101")
draw(code)
print(len(code))
