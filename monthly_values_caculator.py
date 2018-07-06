from bs4 import BeautifulSoup

def read_html_for_month(month):
    month = str(month)
    if len(month) == 1:
        month = '0' + month
    URL = 'inputs/SalariosAbertos2017/HTML/HTML_ativos_2017_{}/todos.html'.format(month)
    with open(URL) as fp:
        soup = BeautifulSoup(fp, "lxml")

    return soup

def get_values_from_soup(soup):
    rows = soup.find_all('tr')

    results = {}
    current = None

    for row in rows:
        current_tab = row.find(class_='cabecalho')
        net_income_tab = row.find(class_='tabela_remun_liq')
        if current_tab is not None:
            if current is not None:
                results[current] = total
            current = current_tab.string.strip()
            total = 0
        elif net_income_tab is not None:
            unique_income_tab = net_income_tab.find(class_='remun_unica')
            right_income_tab = net_income_tab.find_all(class_='remun_dir')
            if unique_income_tab is not None:
                value = unique_income_tab.getText().strip()
            elif right_income_tab is not None:
                value = right_income_tab[-1].getText().strip()
            # TODO check for corner cases
            if value[:2] == u'R$':
                total += float(value[2:].replace('.', '').replace(',', '.'))
            elif value[:3] == u'-R$':
                total -= float(value[3:].replace('.', '').replace(',', '.'))
            elif value in results:
                total += results[value]

    return results

def output_results(month, results):
    with open('outputs/by_month/output_values_month_{}.txt'.format(month), 'w') as f:
        for key, value in results.items():
            f.write(key + '\t' +  str(value) + '\n')

def main():
    for month in range(1,13):
        soup = read_html_for_month(month)
        results = get_values_from_soup(soup)
        output_results(month, results)

if __name__ == '__main__':
    main()
