MONTH = 1

with open('inputs/input_month_{}.txt'.format(MONTH)) as f:
     read_data = f.read()

by_line = read_data.split('\n')

remove = True

def should_remove(i):
    global remove
    if by_line[i][:4] == u'após':
        if remove:
            remove = False
            return True
        else:
            remove = True
            return False
    return False

indexes_to_remove = [i for i in range(len(by_line)) if should_remove(i)]

for index in sorted(indexes_to_remove, reverse=True):
    del by_line[index]

for i in range(len(by_line)-1, 0, -1):
    if by_line[i][:4] == u'após':
        value = by_line[i].split('\t')[1]
        by_line[i-1] += value
        del by_line[i]
    elif by_line[i][:2] == 'R$':
        by_line[i-1] += by_line[i]
        del by_line[i]

results = {}
current = None

for i in range(len(by_line)):
    if len(by_line[i].split('\t')) == 1:
        if by_line[i] in results:
            total += results[by_line[i]]
        elif by_line[i][:6] == "nota: ":
            if by_line[i].split('\t')[-1][:2] == u'R$':
                total += float(by_line[i]\
                               .split('\t')[-1][2:]\
                               .replace('.', '')\
                               .replace(',', '.'))
            if by_line[i].split('\t')[-1][:3] == u'-R$':
                total -= float(by_line[i]\
                               .split('\t')[-1][3:]\
                               .replace('.', '')\
                               .replace(',', '.'))
        else:
            if current is not None:
                results[current] = total
            current = by_line[i]
            total = 0
    else:
        if by_line[i].split('\t')[-1][:2] == u'R$':
            total += float(by_line[i]\
                           .split('\t')[-1][2:]\
                           .replace('.', '')\
                           .replace(',', '.'))
        if by_line[i].split('\t')[-1][:3] == u'-R$':
            total -= float(by_line[i]\
                           .split('\t')[-1][3:]\
                           .replace('.', '')\
                           .replace(',', '.'))

with open('outputs/output_values_month_{}.txt'.format(MONTH), 'w') as f:
    for key, value in results.items():
        f.write(key + '\t' +  str(value) + '\n')
