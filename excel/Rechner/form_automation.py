# creates a list of all formulas for an excel sheet and writes them to a file in the same directory
# the file is named "formulas.txt"
# this is a automation script for the excel sheet "Rechner" in which a working cpu is programmed whit ram
# this script is for creating a list of all formulas needed for the ram
# the list is used to create the ram in the excel sheet

# structure of the formulas:
#   =GANZZAHL(UND(NICHT(pos1);NICHT(pos2);...;NICHT(posn)))
#   =GANZZAHL(UND(pos1;NICHT(pos2);...;NICHT(posn)))
#   ...
#   =GANZZAHL(UND(pos1;pos2;...;posn))

# the list is created by iterating over all possible combinations of the positions for a binary counter
# this script creates a list of all formulas for the ram in the excel sheet "Rechner" using the number of bits in the counter, the position of the lowest bit and the position of the highest bit
# lowest bit and highest bit are given as excel cell coordinates in the form "A1", "B2", etc.
# all bits are assumed to be in the same row
# will generate all possible formulas for the combination of the bits in the given range


# write the formulas to a file
def save_formulas(formulas:list):
    with open('formulas.txt', 'w') as file:
        for formula in formulas:
            file.write(formula + '\n')


# generate all possible formulas for the given range of bits
def generate_formulas(bits:int, row:int, lowest:str, highest:str):
    formulas = []
    for i in range(2**bits):
        formula = '=GANZZAHL(UND('
        for j in range(bits):
            # Calculate the column letter(s)
            column = ''
            temp = j
            while temp >= 0:
                column = chr(ord('A') + temp % 26) + column
                temp = temp // 26 - 1

            if i & (1 << j):
                formula += column + str(row) + ';'
            else:
                formula += 'NICHT(' + column + str(row) + ');'
        formula = formula[:-1] + '))'
        formulas.append(formula)
    return formulas


# main function
def main():
    bits = 8
    row = 1
    lowest = 'A'
    highest = 'H'
    formulas = generate_formulas(bits, row, lowest, highest)
    print(formulas)
    save_formulas(formulas)

if __name__ == '__main__':
    main()
