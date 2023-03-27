import sqlite3
from datetime import date
from datetime import datetime

from config import config
from dal.HocSinhDal import get_ds_hoc_sinh_theo_lop
from entities.DiemDanh import DiemDanh
from entities.TrangThaiDiemDanh import TrangThaiDiemDanh


def kiem_tra_diem_danh(idHocSinh: int):
    today = date.today()
    ngay_hien_tai = today.strftime("%d/%m/%Y")
    query = "select * from DiemDanh where DiemDanh.IdHocSinh = ? and NgayDiemDanh = ?"
    conn = sqlite3.connect(config.DATABASE)
    cur = conn.cursor()
    cur.execute(query, (idHocSinh, ngay_hien_tai))
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    return False


def add_diem_danh(idHocSinh: int):
    if not kiem_tra_diem_danh(idHocSinh):
        today = date.today()
        ngay_hien_tai = today.strftime("%d/%m/%Y")
        now = datetime.now()
        gio_hien_tai = now.strftime("%H:%M:%S")
        query = "insert into DiemDanh(GioDiemDanh,NgayDiemDanh,IdHocSinh) values(?,?,?)"
        conn = sqlite3.connect(config.DATABASE)
        conn.execute(query, (gio_hien_tai, ngay_hien_tai, idHocSinh,))
        conn.commit()
        conn.close()


def get_trang_thai_diem_danh(idLop: int):
    ds_hoc_sinh = get_ds_hoc_sinh_theo_lop(idLop)

    ds_diem_danh = get_diem_danh_theo_lop_hom_nay(idLop)
    ds_trang_thai = []
    for hoc_sinh in ds_hoc_sinh:
        trang_thai_diem_danh = TrangThaiDiemDanh()
        trang_thai_diem_danh.IdHocSinh = hoc_sinh.Id
        trang_thai_diem_danh.TenHocSinh = hoc_sinh.HoTen
        trang_thai_diem_danh.TrangThai = "Chưa điểm danh"
        for diem_danh in ds_diem_danh:
            if hoc_sinh.Id == diem_danh.IdHocSinh:
                trang_thai_diem_danh.TrangThai = "Đã điểm danh"
                trang_thai_diem_danh.NgayDiemDanh = diem_danh.NgayDiemDanh
                trang_thai_diem_danh.GioDiemDanh = diem_danh.GioDiemDanh
        ds_trang_thai.append(trang_thai_diem_danh)
    return ds_trang_thai


def get_diem_danh_theo_lop(idLop: int, ngay):
    query = """select DiemDanh.Id, NgayDiemDanh, GioDiemDanh, IdHocSinh, HocSinh.HoTen, TenLop
            from DiemDanh,
                 HocSinh,
                 Lop
            where DiemDanh.IdHocSinh = HocSinh.Id
                and Lop.Id = HocSinh.Lop
              and HocSinh.Lop = ?
              and NgayDiemDanh = ?"""
    diem_danhs = []
    try:
        conn = sqlite3.connect(config.DATABASE)
        cur = conn.cursor()
        cur.execute(query, (idLop, ngay))
        rows = cur.fetchall()
        for row in rows:
            diem_danh = DiemDanh()
            diem_danh.Id = row[0]
            diem_danh.NgayDiemDanh = row[1]
            diem_danh.GioDiemDanh = row[2]
            diem_danh.IdHocSinh = row[3]
            diem_danh.TenHocSinh = row[4]
            diem_danh.Lop = row[5]
            diem_danhs.append(diem_danh)
        conn.close()
        return diem_danhs
    except Exception as e:
        print(e)
        return diem_danhs


def get_diem_danh_theo_lop_hom_nay(idLop: int):
    query = """select DiemDanh.Id, NgayDiemDanh, GioDiemDanh, IdHocSinh, HocSinh.HoTen, TenLop
            from DiemDanh,
                 HocSinh,
                 Lop
            where DiemDanh.IdHocSinh = HocSinh.Id and HocSinh.Lop = Lop.Id
              and HocSinh.Lop = ?
              and NgayDiemDanh = ?"""
    diem_danhs = []
    try:
        today = date.today()
        ngay_hien_tai = today.strftime("%d/%m/%Y")
        conn = sqlite3.connect(config.DATABASE)
        cur = conn.cursor()
        cur.execute(query, (idLop, ngay_hien_tai))
        rows = cur.fetchall()
        for row in rows:
            diem_danh = DiemDanh()
            diem_danh.Id = row[0]
            diem_danh.NgayDiemDanh = row[1]
            diem_danh.GioDiemDanh = row[2]
            diem_danh.IdHocSinh = row[3]
            diem_danh.TenHocSinh = row[4]
            diem_danh.Lop = row[5]
            diem_danhs.append(diem_danh)
        conn.close()
        return diem_danhs
    except Exception as e:
        print(e)
        return diem_danhs


if __name__ == '__main__':
    print(get_diem_danh_theo_lop_hom_nay(1))
