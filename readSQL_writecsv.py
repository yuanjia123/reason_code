import csv
import psycopg2
class IO_rw(object):

    def __init__(self):
        self.csvfile = open("test.csv", "w")
        self.writer = csv.writer(self.csvfile)

        self.conn = psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")
        self.cur = self.conn.cursor()

    def process_item(self):

        self.cur.execute("select * from temp")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
            self.writer.writerow(row)
        self.cur.close()

    def close_spider(self):
        self.conn.close()
        self.csvFile.close()
if __name__ == '__main__':
    r = IO_rw()
    r.process_item()
    r.close_spider()
