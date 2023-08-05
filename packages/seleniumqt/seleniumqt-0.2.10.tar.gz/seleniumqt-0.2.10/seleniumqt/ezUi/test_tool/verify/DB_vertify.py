#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import socket
# import psycopg2
import MySQLdb
from util.sys import ini_file

logger = logging.getLogger(__name__)


def run(conn, data_base_conf, sql_in, exp_out, requirement):
    err_info = None
    try:
        bl, e = query_sql(conn, sql_in, data_base_conf)
        print(bl)
        s = data_base_conf.split(':')[1] + '|' + data_base_conf.split(':')[-1] + '|' + sql_in[1]
        k = str(sql_in[6]) + 'day' \
            + '|' + str(sql_in[3]).split('=')[1].replace("'", "") \
            + '|<' + requirement \
            + str(sql_in[2]).split('=')[1].replace("'", "") + '>'

        bl_out = 0
        if 'count' in sql_in[0].lower():
            bl_out = str(bl) + '笔'

        if 'sum' in sql_in[0].lower():
            bl_out = str(bl) + '元'

        ini_file.write_case(s, k, bl_out)

        if type(bl) is int and bl > 0:
            ini_file.write_case('testResult', 'pass', 'true')

        for i in str(exp_out[0]):
            if str(i) not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                err_info = ('[INFO:]***执行失败***',
                            e,
                            '设置错误',
                            '预期查询数量错误%s,实际查询记录%s' % (exp_out, str(bl)))
                logger.info(err_info)
                break
        else:
            if bl >= int(exp_out):
                logger.info('查询执行成功::有%s条查询记录', str(bl))

                return True, '执行通过', err_info

            err_info = ('[INFO:]***验证失败***',
                        e,
                        '未满足预期',
                        '预期查询数量大于%s,实际查询记录%s,查询地址%s' % (exp_out, bl, data_base_conf))

        logger.info('查询执行失败::%s', err_info[3])
    except Exception as e:
        logger.info(e)

    return False, '执行失败', err_info


def net_is_used(data_base_conf):
    db_conf = data_base_conf.split(':')
    db_ip = db_conf[1]
    db_port = int(db_conf[5])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((db_ip, db_port))
        s.shutdown(2)
        return True, db_ip
    except:
        logger.info('%s:%d is unused' % (db_ip, db_port))
        return False, db_ip


def connect_db(data_base_conf):
    try:

        db_conf = data_base_conf.split(':')

        if db_conf[0] != 'DB' or len(db_conf) != 7:
            return 0, '数据库链接参数错误'
        db_ip = db_conf[1]
        db_name = db_conf[2]
        db_pwd = db_conf[3]
        db_schemas = db_conf[4]
        port = int(db_conf[5])
        db_ = db_conf[6]
        logger.info('连接数据库' + str(db_conf))
        # if db_ == 'psycopg2':
        #     conn = psycopg2.connect(host=db_ip,
        #                             port=port,
        #                             database=db_schemas,
        #                             user=db_name,
        #                             password=db_pwd)
        if db_ == 'MySQLdb':
            conn = MySQLdb.connect(db_ip,
                                   db_name,
                                   db_pwd,
                                   db_schemas,
                                   charset='utf8')

    except Exception as e:
        logger.info(e)
    else:
        return conn, db_schemas
    return None, None


def close_db_connection(conn):
    conn.commit()
    conn.close()


def query_sql(conn, sql_in, data_base_conf):
    db_conf = data_base_conf.split(':')
    db_ = db_conf[6]

    sql = ''
    if db_ == 'psycopg2':
        sql = '''SELECT %s FROM %s WHERE %s AND %s AND %s AND %s>=(now() - interval '%sD');''' % (sql_in)
    if db_ == 'MySQLdb':
        sql = '''SELECT %s FROM %s WHERE %s AND %s AND %s AND %s>DATE_SUB(NOW(), INTERVAL %s*1440 MINUTE);''' % (sql_in)

    sql = sql.replace("ALL='***' AND", '')
    sql = sql.replace("ALL='___' AND", '')
    logger.info(sql)

    try:
        cur = conn.cursor()
        for i in range(3):
            cur.execute(sql)
            rows = cur.fetchall()
            print(rows)
            if len(rows) == 1 and len(rows[0]) == 1:
                if rows[0][0] is None:
                    return 0, None
                return rows[0][0], None
    except Exception as e:
        logger.info("Error: %s" % e)
        return '[time_out]', e


if __name__ == '__main__':
    # '''
    # 27
    # ['ICBC', 'POST', 'CMBCHINA', 'CMBC', 'SHB',
    # 'HXB', 'GDB', 'CEB', 'BOCO', 'CIB',
    # 'PINGANBANK', 'BOC', 'SPDB', 'UNIONPAY', 'WAP',
    # 'UNIONPAYWAP', 'UNIONPAY_WAP', 'BCCB', 'BJRCB', 'ABC',
    # 'ECITIC', 'CCB', 'SDB', '', 'CBHB', 'P2P', None]
    # '''
    #
    # host = '172.21.209.130'
    # port = '5432'
    # user = 'monitor'
    # password = 'jnDNNDDY2q'
    # database = 'federated'
    #
    # conn = psycopg2.connect(host=host,
    #                         port=port,
    #                         database=database,
    #                         user=user,
    #                         password=password)
    # logger.info("Opened database successfully")
    #
    # cur = conn.cursor()
    # '''
    #
    # '''
    # # sl = "SELECT count(*) FROM bc_online_pay_order as n WHERE bank_code='BOCO' AND mode='B2C' AND status='SUCCESS' AND n.bank_back_date_time>=CURRENT_DATE-30;"
    # # cur.execute("SELECT DISTINCT(bank_code) "
    # #             "FROM bc_online_pay_order as n "
    # #             "WHERE n.create_date_time>=CURRENT_DATE-366")
    # # cur.execute(
    # #     "SELECT count(*) FROM bc_online_pay_order as n WHERE bank_code='BOCO' AND mode='B2C' AND status='SUCCESS' AND n.create_date_time>=CURRENT_DATE-32")
    #
    # sl = "SELECT count(*) FROM bc_online_pay_order as n WHERE bank_code='CIB' AND mode='B2B' AND status='SUCCESS' AND n.bank_back_date_time>=CURRENT_DATE-30;"
    #
    # cur.execute(sl)
    #
    # rows = cur.fetchall()
    # for row in rows:
    #     logger.info(row[0])
    #
    # logger.info("Operation done successfully")
    # conn.close()

    t = None

    if t != None:
        print(3)
