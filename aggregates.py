def get_aggregates(month, aggregates):
    with open('outputs/output_values_month_{}.txt'.format(month)) as f:
        read_data = f.read()

    by_line = filter(None, read_data.split('\n'))
    for line in by_line:
        key = line.split('\t')[0]
        value = line.split('\t')[1]
        if key in aggregates:
            aggregates[key] += float(value)
        else:
            aggregates[key] = float(value)

    return aggregates

def output_aggregates(aggregates):
    import locale
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')
    with open('outputs/total_results_on_year.txt', 'w') as f:
        for key, value in aggregates.items():
            f.write(key + u'\t R$' + locale.format('%.2f', value, 1) + '\n')


if __name__ == '__main__':
    aggregates = {}
    for month in range(1, 13):
        aggregates = get_aggregates(month, aggregates)
    output_aggregates(aggregates)
