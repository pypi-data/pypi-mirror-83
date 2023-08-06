# TODO: description header

from .supplier import Supplier, ScappamentoError
import pandas as pd


def update():
    supplier_name = 'MEPA'
    mepa = Supplier(supplier_name)

    print(mepa)

    # Config
    config_path = 'C:\\Ready\\ReadyPro\\Archivi\\scappamento.ini'
    key_list = ['excel_filename',
                'ref_excel_filename']

    mepa.load_config(key_list, config_path)

    [excel_filename,
     ref_excel_filename] = mepa.val_list

    # Do stuff

    xls = pd.read_excel(excel_filename, header=None)
    'Access||Accu Case||Acorn||ADAM Professional Audio'

    if 'field' not in xls:
        pass

    # TODO: properly generate file from Ready Pro, start chipping away at file issues

    # # CREDENTIALS AND URLs
    # config = configparser.ConfigParser()
    # with open('MEPA.ini') as f:
    #     config.read_file(f)
    #
    #     user = config['acquistinretepa.it']['user']
    #     password = config['acquistinretepa.it']['password']
    #     login_url = config['acquistinretepa.it']['login_url']
    #
    # with session() as s:
    #     s.get(login_url)
    #
    # # PACKAGE ASSEMBLY IMMUTABLE
    #
    # conn = msq.connect(host=host, database=database, user=user, password=password)
    # with open(final_path + sql_filename) as f:
    #     query = f.read()
    #
    # results = pandas.read_sql_query(query, conn)
    #
    # results.to_csv(final_path + csv_filename, sep=';', index=False)
    #
    # conn.close()


if __name__ == '__main__':
    update()
