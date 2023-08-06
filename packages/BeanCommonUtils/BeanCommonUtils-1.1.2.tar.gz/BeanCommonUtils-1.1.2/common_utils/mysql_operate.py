# -*- coding: utf-8 -*-

import pymysql


class MysqlOperate:

    @classmethod
    def mysql_conn(cls, mysql_info):
        host = mysql_info['host']
        user_name = mysql_info['user_name']
        passwd = mysql_info['passwd']
        dbname = mysql_info['dbname']
        if mysql_info.__contains__('port'):
            port = mysql_info['port']
        else:
            port = 3306
        db = pymysql.connect(host, user_name, passwd, dbname, port, charset="utf8")
        cursor = db.cursor()
        return db, cursor

    @classmethod
    def mysql_insert(cls, mysql_info, query):
        db, cursor = cls.mysql_conn(mysql_info)
        cursor.execute(query)
        db.commit()
        db.close()

    @classmethod
    def mysql_insert_mul(cls, mysql_info, queries):
        db, cursor = cls.mysql_conn(mysql_info)
        for query in queries:
            cursor.execute(query)
            db.commit()

        db.close()

    @classmethod
    def new_mysql_insert(cls, mysql_info, sql_template, params=None):
        """
        替换原有的mysql_insert/update/delete方法，该方法的主要目的是防止sql注入
        :param mysql_info:
        :param sql_template: sql的模板
        :param params: 替换sql模板中的动态参数  parameters used with sql_template. (optional)
        :type params: tuple, list or dict
        :return:
        """
        db, cursor = cls.mysql_conn(mysql_info)
        cursor.execute(sql_template, params)
        db.commit()
        db.close()

    @classmethod
    def new_mysql_query(cls, mysql_info, query_template, params=None):
        """
        替换原有的mysql_query方法，该方法的主要目的是防止sql注入
        :param mysql_info:
        :param query_template: 查询sql的模板
        :param params: 替换sql模板中的动态参数
        :return:
        """
        db, cursor = cls.mysql_conn(mysql_info)
        cursor.execute(query_template, params)

        # 获取所有字段名称
        col_name_list = [tuple_data[0] for tuple_data in cursor.description]
        results = cursor.fetchall()
        result_list = []
        for row in results:
            result_list.append(row)

        db.close()
        return result_list, col_name_list
