#coding: utf-8
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import psycopg2


def db_get(cnt, bank_code, mode, CURRENT_DATE):
    host = '172.21.209.220'
    port = '5432'
    user = 'monitor'
    password = 'jnDNNDDY2q'
    database = 'federated'

    conn = psycopg2.connect(host=host,
                            port=port,
                            database=database,
                            user=user,
                            password=password)
    print("Opened database successfully")

    cur = conn.cursor()

    sl = "SELECT " + cnt + " FROM bc_online_pay_order as n WHERE bank_code='" + bank_code + "' AND mode='" + mode + "' AND status='SUCCESS' AND n.bank_back_date_time>=CURRENT_DATE-" + CURRENT_DATE + ";"
    print(sl)
    cur.execute(sl)

    rows = cur.fetchall()
    for row in rows:
        print(row)
        print('.' * 8)

    print("Operation done successfully")
    conn.close()


if __name__ == '__main__':

    print(sys.argv)
    if len(sys.argv) < 4:
        print("argv must more 4")
    elif sys.argv[3] not in ['B2B', 'B2C']:
        print("mode must B2C or B2B")
    elif sys.argv[4][0] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        print("_DATE must int")
    else:
        db_get(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
