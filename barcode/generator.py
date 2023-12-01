
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
    
def barcode_generator(number):
    number = str(number)
    if len(number) == 13:
        first_digit = number[0]
        number = number[1:]
        first_digit = first_digit_codes[int(first_digit)]
        barcode = []
        barcode.append(first_digit)
        for i in range(0,6):
            barcode.append(barcode_part(int(number[i+1]), first_digit[i]))
        barcode.append(barcode_part(int(number[6]), 'C'))
        for i in range(7,12):
            barcode.append(barcode_part(int(number[i+1]), 'C'))
        return barcode
    else:
        return None

        