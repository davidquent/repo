import sys
import logging
import pandas as pd
from utils import MysqlCon

file_handler = logging.FileHandler('./erp.log', encoding='utf-8')
logging.basicConfig(level=logging.INFO, handlers={file_handler}, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y '
                                                                                                           '%I:%M:%S')

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)
pd.set_option('display.width', 1000)

df_columns = ['ID', 'fabric code', 'fabric color', 'quantity', 'date', 'sent by', 'received by', 'cut', 'style']


# 主窗口
def main():
    print()
    print(" Welcome to ERP ".center(50, '*'))
    print("0.录入      1.查询".center(48))
    print("2.删除      3.修改".center(48))
    print("4.退出      5.批录".center(48))
    print(' Hello    David '.center(50, '*'))
    print()
    _tuple = ('data_entry', 'query', 'delete', 'modify', 'systemexit', 'undefined')
    readselect(_tuple)


def _processselect(select_src: str, selectlist: list) -> str:
    """
    读取输入的选择项/内容和选择列表，根据输入内容返回挑选的值
    若在列表里，根据列表序号返回对应的值
    若不在列表中，则返回输入的内容
    select_src: 输入的选择项或内容
    selectlist：被选择的列表
    """
    try:
        if int(select_src) in range(len(selectlist)):
            select_src = selectlist[eval(select_src)]
    except Exception:
        pass
    return select_src


def _selecthandler(selectstr: str):
    selectlist = ['fabric_code', 'fabric_color', 'quantity', 'sent_by', 'received_by', 'sent_date', 'cut', 'style',
                  'id']
    if selectstr not in selectlist:
        pass
    else:
        if selectstr == 'fabric_code':
            fab = input("请输入面料编号  0:3RD  1:BOS  2:AGD  3:BUH  4:ALG  5:YV  6:AVO :> ")
            fablist = ['3RD LINING', 'BOS', 'AGD', 'BUH', 'ALG', 'YV', 'AVO']
            if fab.isdigit():
                if int(fab) < len(fablist):
                    val = _processselect(fab, fablist)
                else:
                    print("输入错误！")
                    return 'c'
            else:
                val = fab.upper()
            print(f"\033[1;33m{val}\033[0m")
        elif selectstr == 'sent_by':
            sent_by = input("请输入寄出方 0:宇创  1:晓月  2:中澳  3:启涛  4:兴荣 :> ")
            sentlist = ['宇创', '晓月', '中澳', '启涛', '兴荣']
            val = _processselect(sent_by, sentlist)
        elif selectstr == 'received_by':
            received_by = input("请输入目的地 0:启涛  1:龙腾  2:龙鑫  3:盛世  4:友卉  5:喜讯 :> ")
            receivedlist = ['启涛', '龙腾', '龙鑫', '盛世', '友卉', '喜讯']
            val = _processselect(received_by, receivedlist)
        elif selectstr == 'sent_date':
            val = input("请输入要查询的值(e.g 20220506)：>")
        elif selectstr.lower() == 'id':
            val = input("请输入ID:> ")
            if not val.isalnum():
                return
        elif selectstr.lower() == 'cut':
            val = input("请输入cut:> ")
        elif selectstr.lower() == 'style':
            val = input("请输入款号:> ")
        else:
            val = input(f"请输入：{selectstr}> ").upper()
        return val


def data_entry():
    while True:
        year = input("请输入年份(默认2022年）：") or '2022'
        month = input("请输入月份(默认5月）：") or '5'
        date = input("请输入日期：")

        # 拼接日期字符串
        datestr = '-'.join((year, month, date))

        # 数据字典
        data = {}

        selectlist = ['fabric_code', 'fabric_color', 'quantity', 'sent_by', 'received_by', 'cut', 'style']
        n = 0
        for i in selectlist:
            val = _selecthandler(i)
            data[i] = val
            n += 1
        break

    if 'c' in data.values():
        print("\033[1;33m数据有错，中止储存，返回开始菜单\033[0m")
        return

    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    args = tuple(data.values())
    sql_first = "ALTER TABLE fabric_delivery_info AUTO_INCREMENT =1"

    # str_to_date函数将datestr字符串转为mysql的日期数据类型
    sql = f'INSERT INTO fabric_delivery_info({keys},sent_date) VALUES({values},str_to_date("{datestr}", "%%Y-%%m-%%d"))'
    try:
        mysqlcon.executesql(sql_first)
        rows, res = mysqlcon.executesql(sql, args)
        if rows:
            print('\033[1;33m数据插入成功\033[0m')
        else:
            print('\033[1;33m操作失败\033[0m')
    except Exception as E:
        # print(E)
        logging.exception(E)
        pass


def query():
    column_selected = input("请选择要查询的列：  0.面料编号   1.寄出方   2.接收方   3.cut    4.款号   5.日期   6.id:> ")
    columnlist = ['fabric_code', 'sent_by', 'received_by', 'cut', 'style', 'sent_date', 'id']
    column = _processselect(column_selected, columnlist)
    # column = columnlist[eval(column)]
    val = _selecthandler(column)
    sqloperator = input("请输入操作符号(e.g =, <, >) ： ")
    if 0 == len(val):
        print("查询条件为 空值，请重新查询")
        return
    sql = f"select * from fabric_delivery_info where {column} {sqloperator} '{val}'"
    confirm = input(f"即将执行的SQL语句是 \033[1;33m{sql} , 请确认 Y/n (默认Y) :\033[0m") or 'Y'
    if confirm.upper() == 'N':
        print('\033[1;33m取消操作\033[0m')
        return
    rows, res = mysqlcon.executesql(sql)
    df = pd.DataFrame(res, columns=df_columns)
    if len(df):
        print('\033[1;33m')
        print(df)
        print('\033[0m')
    else:
        print('\033[1;33m查无记录\033[0m')


def delete():
    column_selected = input("请选择要依据的列：  0.id   1.寄出方   2.接收方   3.cut    4.款号   5.日期:> ")
    columnlist = ['id', 'sent_by', 'received_by', 'cut', 'style', 'sent_date']
    column = _processselect(column_selected, columnlist)
    val = _selecthandler(column)
    sqloperator = input("请输入操作符号(e.g =, <, >) ： ")
    if column == 'id':
        val = int(val)
    try:
        sql = f"delete from fabric_delivery_info where {column} {sqloperator} '{val}'"
    except Exception as e1:
        logging.warning(e1)
        print('错误')
        return
    confirm = input(f"即将执行的SQL语句是 \033[1;33m{sql} , 请确认 Y/n (默认Y) :\033[0m") or 'Y'
    if confirm.upper() == 'N':
        print('\033[1;33m取消操作\033[0m')
        return
    rows, res = mysqlcon.executesql(sql)
    if rows:
        print(f'\033[1;33m{rows} 行数据删除成功\033[0m')
    else:
        print('\033[1;33m查无记录\033[0m')


def undefined():
    print('功能待开发')
    pass


def modify():
    updatecolumn = input("请选择要更新数值的列：  0.面料编号  1.面料颜色   2.数量   3.日期   4.寄出方   5.接收方   6.cut   7.款号:> ")
    updatecolumnlist = ['fabric_code', 'fabric_color', 'quantity', 'date', 'sent_by', 'received_by', 'cut', 'style']
    upcolumn = _processselect(updatecolumn, updatecolumnlist)
    newval = _selecthandler(upcolumn)

    column_selected = input("请选择要依据的列：  0.id   1.寄出方   2.接收方   3.cut    4.款号   5.日期:> ")
    columnlist = ['id', 'sent_by', 'received_by', 'cut', 'style', 'sent_date']
    column = _processselect(column_selected, columnlist)
    val = _selecthandler(column)
    sqloperator = input("请输入操作符号(e.g =, <, >) ： ")
    if column == 'id':
        val = int(val)
    try:
        sql = f"update fabric_delivery_info set {upcolumn} = '{newval}' where {column}{sqloperator} '{val}'"
    except Exception as e2:
        logging.warning(e2)
        print('错误')
        return
    confirm = input(f"即将执行的SQL语句是 \033[1;33m{sql} , 请确认 Y/n (默认Y) :\033[0m") or 'Y'
    if confirm.upper() == 'N':
        print('\033[1;33m取消操作\033[0m')
        return
    rows, res = mysqlcon.executesql(sql)
    if rows:
        print(f'\033[1;33m{rows} 行数据更新成功\033[0m')
    else:
        print('\033[1;33m查无记录\033[0m')


# 系统退出
def systemexit():
    print("\033[1;33mByeBye!\033[0m")
    try:
        mysqlcon.con.close()
    except Exception as e2:
        print(e2)
        pass
    logging.info('退出系统')
    sys.exit()


def readselect(func: tuple):
    while True:
        try:
            selectnumber = int(input("Select the function number:> "))
        except Exception as E:
            logging.error(E)
            print(E)
            print('\033[1;33m输入错误，请重新选择\033[0m')
            continue
        if selectnumber in range(len(func)):
            eval(func[selectnumber])()
            break
        else:
            print("\033[1;33mWrong select, try again!\033[0m")
            break


if __name__ == '__main__':

    sql_kwargs = {'user': 'david', 'password': 'david', 'database': 'erp'}

    try:
        mysqlcon = MysqlCon(**sql_kwargs)
        if mysqlcon:
            print("ERP 登录成功")
            logging.info('登陆系统')
    except Exception as e:
        mysqlcon = None
        print(e)

    while mysqlcon:
        main()
