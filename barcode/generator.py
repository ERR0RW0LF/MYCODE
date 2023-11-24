
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

# q: what mens <= ?
# a: <= means less than or equal to

def first_digit(number):
    while number <= 9:
        return first_digit_codes[number]



        