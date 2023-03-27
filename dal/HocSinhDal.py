import sqlite3

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from config import config
from entities.HocSinh import HocSinh


def add(hocSinh: HocSinh):
    try:
        conn = sqlite3.connect(config.DATABASE)
        conn.execute(
            "insert into HocSinh(Id,HoTen,Lop,KhuonMat1,KhuonMat2,KhuonMat3,EmbFace1,EmbFace2,EmbFace3) values(?,?,?,?,?,?,?,?,?)",
            (hocSinh.Id, hocSinh.HoTen, hocSinh.Lop, hocSinh.KhuonMat1, hocSinh.KhuonMat2, hocSinh.KhuonMat3,
             hocSinh.EmbFace1, hocSinh.EmbFace2, hocSinh.EmbFace3,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print('err ', e)
        return False


def update(hocSinh: HocSinh, Id: int):
    try:
        conn = sqlite3.connect(config.DATABASE)
        conn.execute(
            "update HocSinh set HoTen = ?, Lop = ?,KhuonMat1 = ?,KhuonMat2 = ?,KhuonMat3 = ?,EmbFace1 = ?,"
            "EmbFace2 = ?, EmbFace3 = ?, where Id = ?",
            (hocSinh.HoTen, hocSinh.Lop, hocSinh.KhuonMat1, hocSinh.KhuonMat2, hocSinh.KhuonMat3,
             hocSinh.EmbFace1,
             hocSinh.EmbFace2, hocSinh.EmbFace3, Id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print('err ', e)
        return False


def delete(Id: int):
    try:
        conn = sqlite3.connect(config.DATABASE)
        conn.execute("DELETE FROM HocSinh where Id = ?", (Id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print('err ', e)
        return False


def tim_kiem_hoc_sinh(embbeding: np.ndarray):
    hocSinh = None
    conn = sqlite3.connect(config.DATABASE)
    cur = conn.cursor()
    cur.execute("select * from HocSinh")
    rows = cur.fetchall()
    for row in rows:
        emb1 = np.frombuffer(row[6], dtype='float').reshape(1, -1)
        emb2 = np.frombuffer(row[7], dtype='float').reshape(1, -1)
        emb3 = np.frombuffer(row[8], dtype='float').reshape(1, -1)
        if cosine_similarity(embbeding, emb1) >= config.FACE_THRESHOLD or cosine_similarity(embbeding,
                                                                                            emb3) >= config.FACE_THRESHOLD or cosine_similarity(
            embbeding, emb2) >= config.FACE_THRESHOLD:
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
            break
    return hocSinh


def get_ds_hoc_sinh_theo_lop(idLop: int):
    hocSinhs = []
    try:
        conn = sqlite3.connect(config.DATABASE)
        cur = conn.cursor()
        cur.execute(
            "select HocSinh.Id,HoTen,Lop.TenLop,KhuonMat1,KhuonMat2,KhuonMat3,EmbFace1,EmbFace2,EmbFace3 from HocSinh,Lop where HocSinh.Lop = Lop.Id and HocSinh.Lop = ?",
            (idLop,))
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
    except Exception as e:
        print('err ', e)
    return hocSinhs


def get_all():
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
    except Exception as e:
        print('err ', e)
    return hocSinhs
