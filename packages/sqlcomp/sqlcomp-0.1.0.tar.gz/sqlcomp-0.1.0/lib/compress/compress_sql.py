"""
Handles compressing a full SQL string to a shorthand string.
"""
from typing import List, Dict


def __parse_sql(blob_string: str) -> List[str]:
    blob = blob_string.split(' ')
    blob = [x.replace('`', '') for x in blob]
    blob = [x.replace('(', '') for x in blob]
    blob = [x.replace(')', '') for x in blob]
    blob = [x.replace("'", '') for x in blob]
    blob = [x.replace(';', '') for x in blob]
    return blob


def __replace_sql(config: Dict, blob_list: List[str]) -> List[str]:
    sql = list()
    for item in blob_list:
        if item in config:
            sql.append(config[item])
        elif item == "'" or item == '"' or item == '(' or item == ')' or item == ';' \
                or item == 'INTO' or item == 'VALUES':
            pass
        elif item == 'INSERT':
            sql.append('I')
        elif item == 'UPDATE':
            sql.append('U')
        elif item == 'DELETE':
            sql.append('D')
        else:
            sql.append(item)
    return sql


def __generate_insert(sql_list: List[str]) -> str:
    sql_list.pop(0)
    result = "I"
    for x in sql_list:
        result += ' ' + x
    return result


def __generate_update(sql_list: List[str]) -> str:
    sql_list.pop(0)
    result = "U "
    for x in sql_list:
        result += x + ' '
    return result


def __generate_delete(sql_list: List[str]) -> str:
    sql_list.pop(0)
    result = "D "
    for x in sql_list:
        result += x + ' '
    return result


def __generate_blob(sql_list: List[str]) -> str:
    if sql_list[0].upper() == 'I':
        return __generate_insert(sql_list)
    elif sql_list[0].upper() == 'U':
        return __generate_update(sql_list)
    elif sql_list[0].upper() == 'D':
        return __generate_delete(sql_list)


def compress_sql(config, sql: str) -> str:
    """
    Compress from a full SQL string to a compressed version to shave off as many characters as is reasonable.

    :param sql: An SQL string to condense.
    :param config: A mapping of tables and variables.
    :return: A compressed SQL string.
    """
    blob_list = __parse_sql(sql)
    blob = __replace_sql(config, blob_list)
    return __generate_blob(blob)
