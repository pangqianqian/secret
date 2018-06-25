# coding=utf-8

import mysql.connector


def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
    db = mysql.connector.connect(user="root", passwd="ldh0517", database="Feature", charset="utf8")
    print '连接上了!'
    return db


def createtable(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 如果存在表Sutdent先删除
    cursor.execute("DROP TABLE IF EXISTS fonts")
    cursor.execute("DROP TABLE IF EXISTS num_fonts")

    sql_fonts = '''CREATE TABLE fonts ( 
            char_chi VARCHAR(5) NOT NULL, 
            feature1 VARCHAR(40) NOT NULL,
            feature2 VARCHAR(20) NOT NULL,
            feature3 VARCHAR(20) NOT NULL,
            feature4 VARCHAR(20) NOT NULL,
            feature5 VARCHAR(20) NOT NULL)DEFAULT CHARSET=utf8'''

    sql_numfonts = ''' CREATE TABLE num_fonts (
                char_chi VARCHAR (5) NOT NULL,
                feature1 VARCHAR(40) NOT NULL,
                feature2 VARCHAR(20) NOT NULL,
                feature3 VARCHAR(20) NOT NULL,
                feature4 VARCHAR(20) NOT NULL,
                feature5 VARCHAR(20) NOT NULL)'''

    # 创建Sutdent表
    cursor.execute(sql_fonts)
    cursor.execute(sql_numfonts)

    print '建表成功！'


def insertdb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 　打开文件
    f = open('num_value.txt', 'r')
    while True:
        line = f.readline()
        if line == '':
            break
        else:
            # 处理每行
            line = line.strip('\n')
            line = line.split(',')
            char_chi = line[0]
            feature1 = line[1] + line[2] + line[3] + line[4]
            l = line[5].split(' ')
            feature2 = l[0]
            feature3 = l[1]
            feature4 = l[2]
            feature5 = l[3]

            try:
                # 执行sql语句
                cursor.execute("INSERT INTO num_fonts VALUES(%s,%s,%s,%s,%s,%s)",
                               [char_chi, feature1, feature2, feature3, feature4, feature5])
            except:
                # Rollback in case there is any error
                print '插入数据失败!'

    f.close()
    cursor.close()
    db.commit()
    print '插入数据成功！'


def querydb(db, feature):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    fs = feature.split(',')
    f1 = fs[0] + fs[1] + fs[2] + fs[3]
    print f1
    f = fs[4].split(' ')
    f2 = f[0]
    f3 = f[1]
    f3 = f[2]
    f4 = f[3]
    sql = "SELECT char_chi FROM num_fonts where feature1 = '%s' "
    try:
    # 执行SQL语句
        cursor.execute(sql % f1)
        # 获取所有记录列表
        results = cursor.fetchall()
        print results
    except:
        print "Error: unable to fecth data"


def closedb(db):
    db.close()


def main():
    db = connectdb()  # 连接MySQL数据库

    # createtable(db)  # 创建表
    # insertdb(db)  # 插入数据
    querydb(db, '1 1 1 ,3 3 3 ,1 0 1 0 ,2 2 2 2 ,0.97265625 0.96484375 0.5 0.4375')
    closedb(db)


if __name__ == '__main__':
    main()
