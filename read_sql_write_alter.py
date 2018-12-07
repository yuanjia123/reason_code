import csv
import psycopg2
class IO_rw(object):

    def __init__(self):
        self.csvfile = open("test——1.csv", "w")
        self.writer = csv.writer(self.csvfile)

        self.conn = psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")
        self.cur = self.conn.cursor()

    def process_item(self):

        self.cur.execute("select * from temp_1")
        rows = self.cur.fetchall()
        for row in rows[:500]:
            row = list(row)      #数据库查到的数据是typle 类型，不可以修改。所以转成list类型， 然后把第一个元素拿到以后， 进行修改， 再放到csv里面去
            row[0] = row[0].split('的微博_')[0]
            print(row)
            self.writer.writerow(row)
        self.cur.close()

    def close_spider(self):
        self.conn.close()
        self.csvfile.close()
if __name__ == '__main__':
    r = IO_rw()
    r.process_item()
   # r.close_spider()
