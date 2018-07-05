from bs4 import BeautifulSoup

MONTH = '01'
month = '01'

# def read_html_for_month(month):
URL = 'inputs/SalariosAbertos2017/HTML/HTML_ativos_2017_{}/todos.html'.format(month)
with open(URL) as fp:
    soup = BeautifulSoup(fp, "lxml")

    # return soup

rows = soup.find_all('tr')

results = {}
current = None

for row in rows:
    current_tab = row.find(class_='cabecalho')
    net_income_tab = row.find(class_='tabela_remun_liq')
    if current_tab is not None:
        current = current_tab.string.strip()
        total = 0
    elif net_income_tab is not None:
        unique_income_tab = net_income_tab.find(class_='remun_unica')
        right_income_tab = net_income_tab.find(class_='remun_dir')
        if unique_income_tab is not None:
            value = unique_income_tab.getText().strip()
        elif right_income_tab is not None:
            value = right_income_tab.getText().strip()
        # TODO check for corner cases
        if value[:2] == u'R$':
            total += float(value[2:].replace('.', '').replace(',', '.'))
        elif value[:3] == u'-R$':
            total -= float(value[3:].replace('.', '').replace(',', '.'))
        elif value in results:
            total += results[value]

with open('outputs/output_values_month_{}.txt'.format(MONTH), 'w') as f:
    for key, value in results.items():
        f.write(key + '\t' +  str(value) + '\n')