# coding=utf-8

import mysql.connector
import cmath
import numpy


class Database:
    def connectdb(self):
        print('连接到mysql服务器...')
        # 打开数据库连接
        # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
        db = mysql.connector.connect(host='ruanjianbei1.mysql.rds.aliyuncs.com', port=3306, user="root",
                                     passwd="Ruanjianbei1", database="Features", charset="utf8")
        print '连接上了!'
        return db

    def createtable(self, db):
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # 如果存在表Sutdent先删除
        # cursor.execute("DROP TABLE IF EXISTS fonts")
        # cursor.execute("DROP TABLE IF EXISTS num_fonts")

        # sql_fonts = '''CREATE TABLE fonts (
        #         char_chi VARCHAR(5) NOT NULL,
        #         feature1 VARCHAR(40) NOT NULL,
        #         feature2 VARCHAR(20) NOT NULL,
        #         feature3 VARCHAR(20) NOT NULL,
        #         feature4 VARCHAR(20) NOT NULL,
        #         feature5 VARCHAR(20) NOT NULL)DEFAULT CHARSET=utf8'''

        sql_numfonts = ''' CREATE TABLE num_fonts (
                    id VARCHAR(8) NOT NULL,
                    font VARCHAR (10) NOT NULL,
                    feature1 VARCHAR(40) NOT NULL,
                    feature2 VARCHAR(10) NOT NULL,
                    feature3 VARCHAR(10) NOT NULL,
                    feature4 VARCHAR(10) NOT NULL,
                    feature5 VARCHAR(10) NOT NULL)'''

        # 创建Sutdent表
        # cursor.execute(sql_fonts)
        cursor.execute(sql_numfonts)

        print '建表成功！'

    def insertdb(self, db):
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # 　打开文件
        f = open('num_value.txt', 'r')
        i = 0
        while True:
            line = f.readline()
            if line == '':
                break
            else:
                # 处理每行
                line = line.strip('\n')
                line = line.split(',')
                char_chi = line[0]
                feature1 = line[1].strip(' ') + ',' + line[2].strip(' ') + ',' + line[3].strip(' ') + ',' + line[
                    4].strip(' ')
                l = line[5].split(' ')
                feature2 = l[0]
                feature3 = l[1]
                feature4 = l[2]
                feature5 = l[3]
                print feature5

                try:
                    # 执行sql语句
                    cursor.execute("INSERT INTO num_fonts VALUES(%s,%s,%s,%s,%s,%s,%s)",
                                   [str(i), char_chi, feature1, feature2, feature3, feature4, feature5])
                except:
                    # Rollback in case there is any error
                    print '插入数据失败!'
                i += 1

        f.close()
        cursor.close()
        db.commit()
        print '插入数据成功！'

    def querydb(self, db, feature, choose):
        # choose=0,企业名称部分；choose=1,注册号部分
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        fs = feature.split(',')
        f = fs[0].strip(' ') + ',' + fs[1].strip(' ') + ',' + fs[2].strip(' ') + ',' + fs[3].strip(' ')
        if choose == 1:
            sql = "SELECT font from num_fonts WHERE feature1='%s'"
            # 执行SQL语句
            cursor.execute(sql % f)
            # 获取所有记录列表
            results = cursor.fetchall()
            if len(results) == 1:
                return results[0][0]
            else:
                sql = "SELECT * from eng_fonts WHERE feature1='%s'"
                s = "SELECT * from eng_fonts"
                return self.search(db, feature, sql, s)
        else:
            sql = "SELECT * from chi_fonts WHERE feature1='%s'"
            s = "SELECT * from chi_common"
            return self.search(db, feature, sql, s)

    def search(self, db, feature, sql, s):
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        fs = feature.split(',')
        f1 = fs[0].strip(' ') + ',' + fs[1].strip(' ') + ',' + fs[2].strip(' ') + ',' + fs[3].strip(' ')
        # print f1
        try:
            # 执行SQL语句
            cursor.execute(sql % f1)
            # 获取所有记录列表
            results = cursor.fetchall()
            if len(results) == 1:  # 单一匹配
                return results[0][1]
            elif len(results) > 1:  # 匹配出来多个
               # print self.Euclid_dis(fs[4], results)
                return self.Euclid_dis(fs[4], results)
            else:  # 匹配不出来的情况，用模糊匹配
                # print self.Fuzzy_match(db, s, feature)
                return self.Fuzzy_match(db, s, feature)
        except:
            print "Error: unable to fecth data1"

    def Euclid_dis(self, f, results):
        f = f.split(' ')
        f2 = float(f[0])
        f3 = float(f[1])
        f4 = float(f[2])
        f5 = float(f[3])
        mini = 10000000
        font = ""
        for i in results:
            x1 = i[3]
            x2 = i[4]
            x3 = i[5]
            x4 = i[6]
            dis = numpy.sqrt((f2 - x1) ** 2 + (f3 - x2) ** 2 + (f4 - x3) ** 2 + (f5 - x4) ** 2)
            if dis < mini:
                font = i[1]
        return font

    def Fuzzy_match(self, db, sql, feature):
        fs = feature.split(',')
        f1 = fs[0].strip(' ') + ',' + fs[1].strip(' ') + ',' + fs[2].strip(' ') + ',' + fs[3].strip(' ')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            l = []
            for i in results:
                k = 0
                for j in range(len(f1)):
                    if f1[j] != i[2][j]:
                        k += 1
                if k <= 2:  # 两个以内的被匹配出来
                    l.append(i)
            if len(l) == 1:
                return l[0][1]
            elif len(l) > 1:
                return self.Euclid_dis(fs[4], l)
            else:
                return '!'
        except:
            print "Error: unable to fecth data2"

    def closedb(self, db):
        db.close()


if __name__ == '__main__':
    db = Database()
    d = db.connectdb()
    db.createtable(d)
    db.insertdb(d)
    db.closedb(d)
