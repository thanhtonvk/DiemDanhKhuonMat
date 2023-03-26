from entities.HocSinh import HocSinh
from config import config
import sqlite3


class HocSinhDal:
    def __init__(self):
        pass

    def add(self, hocSinh: HocSinh):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute(
                "insert into HocSinh(HoTen,Lop,KhuonMat1,KhuonMat2,KhuonMat3,EmbFace1,EmbFace2,EmbFace3) values(?,?,?,?,?,?,?,?)",
                (hocSinh.HoTen, hocSinh.Lop, hocSinh.KhuonMat1, hocSinh.KhuonMat2, hocSinh.KhuonMat3,
                 hocSinh.EmbFace1,
                 hocSinh.EmbFace2, hocSinh.EmbFace3,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return False

    def update(self, hocSinh: HocSinh, Id: int):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute(
                "update HocSinh set HoTen = ?, Lop = ?,KhuonMat1 = ?,KhuonMat2 = ?,KhuonMat3 = ?,EmbFace1 = ?,EmbFace2 = ?, EmbFace3 = ?, where Id = ?",
                (hocSinh.HoTen, hocSinh.Lop, hocSinh.KhuonMat1, hocSinh.KhuonMat2, hocSinh.KhuonMat3,
                 hocSinh.EmbFace1,
                 hocSinh.EmbFace2, hocSinh.EmbFace3, Id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return False

    def delete(self, Id: int):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute("DELETE FROM HocSinh where Id = ?", (Id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return False

    # Id integer primary key autoincrement,
    # HoTen text,
    # Lop integer not null,
    # KhuonMat1 text,
    # KhuonMat2 text,
    # KhuonMat3 text,
    # EmbFace1 text,
    # EmbFace2 text,
    # EmbFace3 text
    def get_by_class(self, idLop: int):
        hocSinhs = []
        try:
            conn = sqlite3.connect(config.DATABASE)
            cur = conn.cursor()
            cur.execute("select * from HocSinh where HocSinh.Lop = ?", (idLop,))
            rows = cur.fetchall()
            for row in rows:
                hocSinh = HocSinh()
                hocSinh.Id = row[0]
                hocSinh.HoTen = row[1]
                hocSinh.Lop = row[2]
                hocSinh.KhuonMat1 = row[3]
                hocSinh.KhuonMat2 = row[4]
                hocSinh.KhuonMat3 = row[5]
                hocSinh.EmbFace1 = row[6]
                hocSinh.EmbFace2 = row[7]
                hocSinh.EmbFace3 = row[8]
                hocSinhs.append(hocSinh)
            conn.close()
            return hocSinhs
        except Exception as e:
            print('err ', e)
            return hocSinhs

    def get_all(self):
        hocSinhs = []
        try:
            conn = sqlite3.connect(config.DATABASE)
            cur = conn.cursor()
            cur.execute("select * from HocSinh")
            rows = cur.fetchall()
            for row in rows:
                hocSinh = HocSinh()
                hocSinh.Id = row[0]
                hocSinh.HoTen = row[1]
                hocSinh.Lop = row[2]
                hocSinh.KhuonMat1 = row[3]
                hocSinh.KhuonMat2 = row[4]
                hocSinh.KhuonMat3 = row[5]
                hocSinh.EmbFace1 = row[6]
                hocSinh.EmbFace2 = row[7]
                hocSinh.EmbFace3 = row[8]
                hocSinhs.append(hocSinh)
            conn.close()
            return hocSinhs
        except Exception as e:
            print('err ', e)
            return hocSinhs
