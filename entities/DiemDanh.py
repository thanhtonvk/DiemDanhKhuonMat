class DiemDanh:
    # Id integer primary key autoincrement,
    # NgayDiemDanh date,
    # IdHocSinh integer not null
    def __init__(self):
        pass

    def __int__(self, Id, NgayDiemDanh, GioDiemDanh, IdHocSinh, TenHocSinh, Lop):
        self.Id = Id
        self.NgayDiemDanh = NgayDiemDanh
        self.IdHocSinh = IdHocSinh
        self.Lop = Lop
        self.GioDiemDanh = GioDiemDanh
