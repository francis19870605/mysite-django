# import pymysql
# pymysql.install_as_MySQLdb()
#
# # 打开数据库连接
# db = pymysql.connect("192.168.23.200", "root", "nihao123!", "blog")
#
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()
#
# # 使用execute方法执行SQL语句
# cursor.execute("SELECT VERSION()")
#
# # 使用fetchone()方法获取一条数据
# data = cursor.fetchone()
# print("DataBase version : %s " % data)
#
# # 关闭数据库
# db.close()
