def hien_phieu_tam_thoi(PhieuKham):
    HoTen, TrieuChung, LoaiBenh, id = "", "", "", []
    if PhieuKham:
        HoTen = PhieuKham["thongTinKhamBenh"]["tenBenhNhan"]
        TrieuChung = PhieuKham["thongTinKhamBenh"]["trieuChung"]
        LoaiBenh = PhieuKham["thongTinKhamBenh"]["duDoanBenh"]
        id = [int(i) for i in PhieuKham["cacLoaiThuoc"]]

    return {
        "HoTen": HoTen,
        "TrieuChung": TrieuChung,
        "LoaiBenh": LoaiBenh,
        "id": id
    }