"""
Handles expanding SQL shorthand to full SQL strings.
"""
from typing import List, Dict


def __parse_blob(blob_string: str) -> List[str]:
    return blob_string.split(' ')


def __retrieve_key_by_value(dictionary: Dict, value: str):
    for key, val in dictionary.items():
        if value == val:
            return key
    return None


def __replace_blob(config: Dict, blob_list: List[str]) -> List[str]:
    sql = list()
    for item in blob_list:
        key = __retrieve_key_by_value(config, item)
        if key is not None:
            sql.append(key)
        else:
            sql.append(item)
    return sql


def __generate_insert(sql_list: List[str]) -> str:
    sql_list.pop(0)
    result = "INSERT INTO `{0}` (".format(sql_list.pop(0))
    assert len(sql_list) % 2 == 0
    partition = len(sql_list) // 2
    sql_list_one = sql_list[:partition]
    sql_list_two = sql_list[partition:]
    if len(sql_list_one) == 1:
        result += "`{0}`".format(sql_list_one[0])
    else:
        for x in sql_list_one:
            result += "`{0}`,".format(x)
    result += ") VALUES ("
    if len(sql_list_two) == 1:
        result += "'{0}'".format(sql_list_two[0])
    else:
        for x in sql_list_two:
            result += "'{0}',".format(x)
    return result + ");"


def __generate_update(sql_list: List[str]) -> str:
    sql_list.pop(0)
    assert len(sql_list) % 2 == 0
    result = "UPDATE `{0}` SET ".format(sql_list.pop(0))
    x = 0
    while x < len(sql_list):
        result += "`{0}` = '{1}'".format(sql_list[x], sql_list[x+1])
        x += 2
    result += "WHERE ({1}{2}{3});".format(sql_list[0], sql_list[1], sql_list[2], sql_list[3])
    return result


def __generate_delete(sql_list: List[str]) -> str:
    sql_list.pop(0)
    return "DELETE FROM `{0}` WHERE ({1}{2}{3});".format(sql_list[0], sql_list[1], sql_list[2], sql_list[3])


def __generate_sql(sql_list: List[str]) -> str:
    if sql_list[0] == 'I':
        return __generate_insert(sql_list)
    elif sql_list[0] == 'U':
        return __generate_update(sql_list)
    elif sql_list[0] == 'D':
        return __generate_delete(sql_list)


def expand_sql(config, blob: str) -> str:
    """
    Expand out an SQL string based on the a dictionary of replacements.

    :param blob: An SQL shorthand blob string.
    :param config: A config mapping.
    :return: An SQL string produced from the given blob.
    """
    sql_list = __parse_blob(blob)
    sql = __replace_blob(config, sql_list)
    return __generate_sql(sql)
