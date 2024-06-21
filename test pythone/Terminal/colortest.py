def print_format_table():
	"""
	prints table of formatted text format options
	"""
	for style in range(8):
		for fg in range(30, 38):
			s1 = ''
			for bg in range(40, 48):
				format = ';'.join([str(style), str(fg), str(bg)])
				s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
			print(s1)
		print('\n')


print_format_table()



import sys
for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")

for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")

print(u"\u001b[1m BOLD \u001b[0m\u001b[4m Underline \u001b[0m\u001b[7m Reversed \u001b[0m")

print(u"\u001b[1m\u001b[4m\u001b[7m BOLD Underline Reversed \u001b[0m")

print(u"\u001b[1m\u001b[31m Red Bold \u001b[0m")
print(u"\u001b[4m\u001b[44m Blue Background Underline \u001b[0m")