import sqlite3
if __name__ == '__main__':
    conn = sqlite3.connect('../database/database.sqlite')
    conn.execute("""create table Lop(
        Id integer primary key autoincrement,
        TenLop text,
        GVCN text
    )""")
    conn.execute("""create table HocSinh(
        Id integer primary key autoincrement,
        HoTen text,
        Lop integer not null,
        KhuonMat1 text,
        KhuonMat2 text,
        KhuonMat3 text,
        EmbFace1 text,
        EmbFace2 text,
        EmbFace3 text
    )""")
    conn.execute("""
    create table DiemDanh(
        Id integer primary key autoincrement,
        GioDiemDanh text,
        NgayDiemDanh text,
        IdHocSinh integer not null 
    )
    """)
