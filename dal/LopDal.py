import sqlite3

from config import config
from entities.Lop import Lop


def add(lop: Lop):
    try:
        conn = sqlite3.connect(config.DATABASE)
        conn.execute("insert into Lop(TenLop,GVCN) values(?,?)", (lop.TenLop, lop.GVCN,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print('err ', e)
        return False


def update(lop: Lop, Id: int):
    try:
        conn = sqlite3.connect(config.DATABASE)
        conn.execute("update Lop set TenLop = ?, GVCN = ? where Id = ?", (lop.TenLop, lop.GVCN, Id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print('err ', e)
        return False


def delete(Id: int):
    try:
        conn = sqlite3.connect(config.DATABASE)
        conn.execute("DELETE FROM Lop where Id = ?", (Id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print('err ', e)
        return False


def get():
    lops = []
    try:
        conn = sqlite3.connect(config.DATABASE)
        cur = conn.cursor()
        cur.execute("select Lop.Id,TenLop,GVCN from Lop")
        rows = cur.fetchall()
        for row in rows:
            lop = Lop(row[0],row[1],row[2])
            lops.append(lop)
        conn.close()
        return lops
    except Exception as e:
        print('err ', e)
        return lops
