class DiemDanh:
    # Id integer primary key autoincrement,
    # NgayDiemDanh date,
    # IdHocSinh integer not null
    def __int__(self, Id=0, NgayDiemDanh=0, GioDiemDanh=0, IdHocSinh=0, TenHocSinh=0, Lop=0):
        self.Id = Id
        self.NgayDiemDanh = NgayDiemDanh
        self.IdHocSinh = IdHocSinh
        self.Lop = Lop
        self.GioDiemDanh = GioDiemDanh
