import sys
import os
from PIL import Image, ImageDraw, ImageOps

first_digit_codes = {0: ['A','A','A','A','A','A'],
                     1: ['A','A','B','A','B','B'],
                     2: ['A','A','B','B','A','B'],
                     3: ['A','A','B','B','B','A'],
                     4: ['A','B','A','A','B','B'],
                     5: ['A','B','B','A','A','B'],
                     6: ['A','B','B','B','A','A'],
                     7: ['A','B','A','B','A','B'],
                     8: ['A','B','A','B','B','A'],
                     9: ['A','B','B','A','B','A']}

digit_code = {'A': {0: [0,0,0,1,1,0,1],
                    1: [0,0,1,1,0,0,1],
                    2: [0,0,1,0,0,1,1],
                    3: [0,1,1,1,1,0,1],
                    4: [0,1,0,0,0,1,1],
                    5: [0,1,1,0,0,0,1],
                    6: [0,1,0,1,1,1,1],
                    7: [0,1,1,1,0,1,1],
                    8: [0,1,1,0,1,1,1],
                    9: [0,0,0,1,0,1,1]},
                     
              'B': {0: [0,1,0,0,1,1,1],
                    1: [0,1,1,0,0,1,1],
                    2: [0,0,1,1,0,1,1],
                    3: [0,1,0,0,0,0,1],
                    4: [0,0,1,1,1,0,1],
                    5: [0,1,1,1,0,0,1],
                    6: [0,0,0,0,1,0,1],
                    7: [0,0,1,0,0,0,1],
                    8: [0,0,0,1,0,0,1],
                    9: [0,0,1,0,1,1,1]},
                     
              'C': {0: [1,1,1,0,0,1,0],
                    1: [1,1,0,0,1,1,0],
                    2: [1,1,0,1,1,0,0],
                    3: [1,0,0,0,0,1,0],
                    4: [1,0,1,1,1,0,0],
                    5: [1,0,0,1,1,1,0],
                    6: [1,0,1,0,0,0,0],
                    7: [1,0,0,0,1,0,0],
                    8: [1,0,0,1,0,0,0],
                    9: [1,1,1,0,1,0,0]}}

# q: what mens <= ?
# a: <= means less than or equal to


def barcode_part(number, type):
    if type == 'A':
        return digit_code['A'][number]
    elif type == 'B':
        return digit_code['B'][number]
    elif type == 'C':
        return digit_code['C'][number]
    else:
        return None

def check_digit(number):
    number = str(number)
    if len(number) == 12:
        sum1 = 0
        sum2 = 0
        for i in range(0,12,2):
            sum1 += int(number[i])
        for i in range(1,12,2):
            sum2 += int(number[i])
        sum2 = sum2 * 3
        sum = sum1 + sum2
        if sum % 10 == 0:
            return 0
        else:
            return 10 - (sum % 10)
    else:
        return None
    
def barcode_generator(number):
    number = str(number)
    if len(number) == 13:
        first_digit = number[0]
        number = number[1:]
        first_digit = first_digit_codes[int(first_digit)]
        barcode = []
        barcode.extend([1,0,1])
        for i in range(0,6):
            barcode.extend(barcode_part(int(number[i]), first_digit[i]))
        
        barcode.extend([0,1,0,1,0])
        
        for i in range(7,12):
            barcode.extend(barcode_part(int(number[i]), 'C'))

        barcode.extend([1,0,1])
        
        return barcode
    else:
        return None

def barcode_image_generator(number):
    barcode = barcode_generator(number)
    if barcode:
        barcode_width = len(barcode)
        barcode_height = 50
        barcode_image = Image.new('RGB', (barcode_width, barcode_height), 'white')
        draw = ImageDraw.Draw(barcode_image)
        for i in range(len(barcode)):
            if barcode[i] == 1:
                draw.line((i, 0, i, barcode_height), fill='black')
        
        barcode_image = barcode_image.resize((barcode_width*10, barcode_height*10), Image.NEAREST)
        #q: how to i add a border to the image?
        #a: use ImageOps.expand()
        barcode_image = ImageOps.expand(barcode_image, border=10, fill='white')
        return barcode_image
    else:
        return None




number = 123456789012
if __name__ == '__main__':
    print(number)
    if len(str(number)) == 12:
        number = str(number) + str(check_digit(number))
        print(number)
    barcode = barcode_generator(int(number))
    print(barcode)
    barcode_image = barcode_image_generator(int(number))
    barcode_image.show()
    barcode_image.save(f'barcode{str(number)}.png')
