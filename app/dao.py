import datetime

from app.models import *
import hashlib
from app import app, db
import cloudinary.uploader
from sqlalchemy import func
from flask_login import current_user


def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)


def get_NguoiDung():
    return NguoiDung.query.all()


def get_name(HoTen):
    return NguoiDung.query.get(HoTen)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return NguoiDung.query.filter(NguoiDung.username_sdt.__eq__(username.strip()),
                                  NguoiDung.password.__eq__(password)).first()


def add_user(name, username, diachi, gt, ns, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = NguoiDung(HoTen=name, username_sdt=username, DiaChi=diachi, GioiTinh=gt, NamSinh=ns, password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        print(res)
        u.avatar = res['secure_url']

    db.session.add(u)
    db.session.commit()











def add_booking(Hoten=None, sdt=None, dvkham=None, ngayKham=None, trieuchung=None, diachi=None, namsinh=None,
                gioitinh=None):
    benhnhan = BenhNhan.query.filter(BenhNhan.username_sdt.__eq__(sdt)).first()
    u = LichKham(DVKham=dvkham, NgayKham=ngayKham, TrieuChung=trieuchung, SDT=sdt)
    if benhnhan:
        u.id_BN, u.HoTen = benhnhan.id, benhnhan.HoTen
    else:
        bn = BenhNhan(username_sdt=sdt, HoTen=Hoten,
                      password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), DiaChi=diachi,
                      NamSinh=namsinh, GioiTinh=gioitinh)
        db.session.add(bn)
        u.HoTen = Hoten
        u.datlichkham = bn
    db.session.add(u)
    db.session.commit()

    return u


def add_PK(hoten=None, ngaykham=None, trieuchung=None, chuandoanbenh=None):
    benhnhan = BenhNhan.query.filter(BenhNhan.HoTen.__eq__(hoten)).first()
    u = PhieuKham(NgayKham=ngaykham, ChuanDoanBenh=chuandoanbenh, TrieuChung=trieuchung)
    if benhnhan:
        u.id_BN = benhnhan.id
        u.id_BS = current_user.id
        db.session.add(u)
        db.session.commit()

    return benhnhan


def TongDT(month=6):
    return (db.session.query(func.sum(HoaDon.TongTien))
            .filter(func.extract('month', HoaDon.NgayThanhToan).__eq__(month))).first()


def doanhthu_thongke(month=6):
    query = (db.session.query(func.extract('day', HoaDon.NgayThanhToan),
                              func.count(HoaDon.id_BN), func.sum(HoaDon.TongTien),
                              func.sum(HoaDon.TongTien) / TongDT(month)[0] * 100)
             .join(BenhNhan, BenhNhan.id_BN.__eq__(HoaDon.id_BN))
             .filter(func.extract('month', HoaDon.NgayThanhToan).__eq__(month))
             .group_by(func.extract('day', HoaDon.NgayThanhToan))
             .order_by(func.extract('day', HoaDon.NgayThanhToan)))

    return query.all()


def thuoc_thongke(month=9):
    query = (db.session.query(Thuoc.TenThuoc, DonViThuoc.TenDonVi, func.sum(ChiTietPhieuKham.SoLuong),
                              func.count(ChiTietPhieuKham.id_Thuoc))
             .join(DonViThuoc, Thuoc.id_DVT.__eq__(DonViThuoc.id_DVT))
             .join(ChiTietPhieuKham, ChiTietPhieuKham.id_Thuoc.__eq__(Thuoc.id_Thuoc))
             .filter(func.extract("month", PhieuKham.NgayKham).__eq__(month))
             .group_by(Thuoc.TenThuoc, DonViThuoc.TenDonVi)
             .order_by(func.count(ChiTietPhieuKham.id_Thuoc), func.sum(ChiTietPhieuKham.SoLuong)))

    return query.all()


def check_MK(matkhau):
    return current_user.password == (str(hashlib.md5(matkhau.strip().encode('utf-8')).hexdigest()))


def get_Thuoc(key=None):
    thuoc = Thuoc.query
    if key:
        thuoc = thuoc.filter(Thuoc.TenThuoc.contains(key))
    return thuoc.all()


def get_HSBN(hsbn=None):
    hosoBN = (db.session.query(HoSoBenhNhan.id_HSBN,NguoiDung.HoTen,HoSoBenhNhan.GhiChu,PhieuKham.ChuanDoanBenh)
              .join(NguoiDung, NguoiDung.id.__eq__(HoSoBenhNhan.id_BN))
              .join(PhieuKham, PhieuKham.id_BN.__eq__(HoSoBenhNhan.id_BN))
              .group_by(HoSoBenhNhan.id_HSBN,NguoiDung.HoTen,HoSoBenhNhan.GhiChu,PhieuKham.ChuanDoanBenh))
    if hsbn:
        hosoBN = hosoBN.filter(NguoiDung.HoTen.contains(hsbn))
    return hosoBN.all()

def getDSK():
    DSK=(db.session.query(NguoiDung.HoTen,LichKham.DVKham,DanhSachKham.NgayLapPhieuKham,DanhSachKham.id_YT,LichKham.TrieuChung)
         .join(DanhSachKham.id_BN.__eq__(NguoiDung.id))
         .join(LichKham.id.__eq__(DanhSachKham.id_BN))
         .join(DanhSachKham.id_BN.__eq__(LichKham.id_BN))
         .group_by(NguoiDung.HoTen,LichKham.DVKham,DanhSachKham.NgayLapPhieuKham,DanhSachKham.id_YT, LichKham.TrieuChung))
    return DSK.all()


def get_DonViThuoc():
    return DonViThuoc.query.all()





def get_PK():
    return PhieuKham.query.all()


def get_CTPK():
    return ChiTietPhieuKham.query.all()


def get_BN():
    return BenhNhan.query.all()


def get_BS():
    return BacSi.query.all()


def get_ND():
    return NguoiDung.query.all()


def get_DVT():
    return DonViThuoc.query.all()


if __name__ == '__main__':
    with app.app_context():
        pass
