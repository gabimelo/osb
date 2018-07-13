import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def read_html_for_month(month):
    month = str(month)
    if len(month) == 1:
        month = '0' + month
    URL = 'inputs/SalariosAbertos2017/HTML/HTML_ativos_2017_{}/todos.html'.format(month)
    with open(URL) as fp:
        soup = BeautifulSoup(fp, "lxml")

    return soup


def get_income(net_income_tab):
    unique_income_tab = net_income_tab.find(class_='remun_unica')
    right_income_tab = net_income_tab.find_all(class_='remun_dir')
    value = None
    if unique_income_tab is not None:
        a_tab = unique_income_tab.find('a')
        if a_tab is not None:
            value = a_tab.getText().strip()
        else:
            value = unique_income_tab.getText().strip()
        if value[:8] == u'ausência':
            value = None
    if right_income_tab is not None and value is None:
        value = right_income_tab[-1].getText().strip()
    # TODO check for corner cases
    if value[:2] == u'R$':
        value = float(value[2:].replace('.', '').replace(',', '.'))
    elif value[:3] == u'-R$':
        value = -float(value[3:].replace('.', '').replace(',', '.'))
    else:
        value = value

    return value


def get_structured_data_from_soup(soup, month):
    rows = soup.find_all('tr')
    section = None
    results = []

    for row in rows:
        section_tab = row.find(class_='cabecalho')
        net_income_tab = row.find(class_='tabela_remun_liq')
        if section_tab is not None:
            section = section_tab.string.strip()
        elif net_income_tab is not None:
            nome_valor_tab = row.find(class_='nome_valor').getText().strip()
            cargo_valor_tab = row.find(class_='cargo_valor').getText().strip()
            funcao_valor_tab = row.find(class_='funcao_valor').getText().strip()
            value = get_income(net_income_tab)
            if section is not None:
                results.append([section, nome_valor_tab,
                                cargo_valor_tab, funcao_valor_tab,
                                value, month])

    return results


def write_to_csv(data):
    columns = ['setor', 'matricula', 'cargo', 'funcao', 'salario', 'mes']
    df = pd.DataFrame(np.array(data), columns=columns)
    with open('outputs/structured_data.csv', 'a') as f:
        df.to_csv(f)


def main():
    open('outputs/structured_data.csv', 'w').close()
    for month in range(1, 13):
        soup = read_html_for_month(month)
        data = get_structured_data_from_soup(soup, month)
        write_to_csv(data)


if __name__ == '__main__':
    main()
