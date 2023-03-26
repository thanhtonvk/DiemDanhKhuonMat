class HocSinh:

    # Id integer primary key autoincrement,
    # HoTen text,
    # Lop integer not null,
    # KhuonMat1 text,
    # KhuonMat2 text,
    # KhuonMat3 text,
    # EmbFace1 text,
    # EmbFace2 text,
    # EmbFace3 text
    def __init__(self, Id, HoTen, Lop, KhuonMat1, KhuonMat2, KhuonMat3, EmbFace1, EmbFace2, EmbFace3):
        self.Id = Id
        self.HoTen = HoTen
        self.Lop = Lop
        self.KhuonMat1 = KhuonMat1
        self.KhuonMat2 = KhuonMat2
        self.KhuonMat3 = KhuonMat3
        self.EmbFace1 = EmbFace1
        self.EmbFace2 = EmbFace2
        self.EmbFace3 = EmbFace3
    def __init__(self):
        pass


