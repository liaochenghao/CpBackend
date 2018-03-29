# coding: utf-8
from django.db import connection


def execute_custom_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows
