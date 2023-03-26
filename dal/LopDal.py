import sqlite3
from entities.Lop import Lop
from config import config


class LopDal:
    def __init__(self):
        pass

    def add(self, lop: Lop):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute("insert into Lop(TenLop,GVCN) values(?,?)", (lop.TenLop, lop.GVCN,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return False

    def update(self, lop: Lop, Id: int):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute("update Lop set TenLop = ?, GVCN = ? where Id = ?", (lop.TenLop, lop.GVCN, Id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return False

    def delete(self, Id: int):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute("DELETE FROM Lop where Id = ?", (Id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return False

    # conn.execute("""create table Lop(
    #     Id integer primary key autoincrement,
    #     TenLop text,
    #     GVCN text
    # )""")
    # conn.execute("""create table HocSinh(
    #     Id integer primary key autoincrement,
    #     HoTen text,
    #     Lop integer not null,
    #     KhuonMat1 text,
    #     KhuonMat2 text,
    #     KhuonMat3 text,
    #     EmbFace1 text,
    #     EmbFace2 text,
    #     EmbFace3 text
    # )""")
    def get(self):
        lops = []
        try:
            conn = sqlite3.connect(config.DATABASE)
            cur = conn.cursor()
            cur.execute("select Lop.Id,TenLop,GVCN,count(HocSinh.Id) from Lop,HocSinh where Lop.Id = HocSinh.Lop")
            rows = cur.fetchall()
            for row in rows:
                lop = Lop()
                lop.Id = row[0]
                lop.TenLop = row[1]
                lop.GVCN = row[2]
                lop.SoHocSinh = row[3]
                lops.append(lop)
            conn.close()
            return lops
        except Exception as e:
            print('err ', e)
            return lops
