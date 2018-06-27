aggregates = {}

for i in range(1,3):
    with open('output_values_month_{}.txt'.format(i)) as f:
        read_data = f.read()
        by_line = read_data.split('\n')
        for line in by_line:
            if line != '':
                key = line.split('\t')[0]
                value = line.split('\t')[1]
                if key in aggregates:
                    aggregates[key] += float(value)
                else:
                    aggregates[key] = float(value)


import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')
with open('total_results_on_year.txt', 'w') as f:
    for key, value in aggregates.items():
        f.write(key + u'\t R$' +  \
            locale.format('%.2f', value, 1) + '\n')