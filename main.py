import html_reader
import aggregates_calculator

if __name__ == '__main__':
    for month in range(1,13):
        soup = html_reader.read_html_for_month(month)
        results = html_reader.get_values_from_soup(soup)
        html_reader.output_results(month, results)

    aggregates = {}
    for month in range(1, 13):
        aggregates = aggregates_calculator.get_aggregates(month, aggregates)
    aggregates_calculator.output_aggregates(aggregates)
