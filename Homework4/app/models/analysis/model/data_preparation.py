from Homework4.app.models.sqlite.sqlite_database import *


def parse_string_to_float(num):
    if num == ',':
        return 0.0
    else:
        return float(num.replace('.', '').replace(',', '.'))


def get_data(db_path, ticker, from_date, to_date):
    data = get_sqlite_ticker_data(db_path, ticker, from_date, to_date)
    data = pd.DataFrame(data=data,
                        columns=['Date',
                                 'Price',
                                 'Max',
                                 'Min',
                                 'AvgPrice',
                                 'chg',
                                 'Volume',
                                 'TurnoverBEST',
                                 'TurnoverTotal'])
    data.sort_values('Date', inplace=True, ascending=True)
    data.set_index('Date', inplace=True)

    data['Price'] = data['Price'].apply(lambda x: parse_string_to_float(x))
    data['Max'] = data['Max'].apply(lambda x: parse_string_to_float(x))
    data['Min'] = data['Min'].apply(lambda x: parse_string_to_float(x))

    if data.dtypes['Volume'] == 'int64' or data.dtypes['Volume'] == 'int32':
        data['Volume'] = data['Volume'].astype('float64')
    else:
        data['Volume'] = data['Volume'].apply(lambda x: x.replace(',', '')).astype('float')

    data = data.filter(['Price', 'Max', 'Min', 'Volume'])
    return data
