a = '20x^18 + x + 2x^4'
e = '1'
b = a.split('+')
b = [i.split('^') for i in b if '^' in i]
max_v = 0
index_v = 0
for i in range(len(b)):
    if max_v <= int(b[i][1]):
        max_v = int(b[i][1])
        index_v = i
degree_b = int(b[index_v][1])
if len(b[index_v][0]) == 1:
    coef_b = 1
else:
    coef_b = b[index_v][0].replace('x', '*x').strip()
    coef_b = eval(coef_b.replace('x', e))

print(coef_b)
print(degree_b)


