from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Double
from app import db, app
from flask_login import UserMixin
import enum
from datetime import datetime


class VaiTro(enum.Enum):
    NguoiDung = 0
    BenhNhan = 1
    YTa = 2
    BacSi = 3
    QuanTri = 4
    ThuNgan = 5


class NguoiDung(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    HoTen = Column(String(60), nullable=False)
    DiaChi = Column(String(200), nullable=False)
    NamSinh = Column(Integer, nullable=False)
    GioiTinh = Column(String(5), nullable=False)
    username_sdt = Column(String(10), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg")
    VaiTro = Column(Enum(VaiTro), default=VaiTro.BenhNhan)

    def __str__(self):
        return self.HoTen


class BacSi(NguoiDung):
    id_BS = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    HocVi = Column(String(100), nullable=False)
    NgayTruc = Column(DateTime, nullable=False)
    id_ND = relationship('PhieuKham', backref='BacSi', lazy=True)


class BenhNhan(NguoiDung):
    id_BN = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    danhSachKham = relationship('DanhSachKham', backref='BenhNhan', lazy=True)
    id2 = relationship('HoaDon', backref='BenhNhan', lazy=True)
    id3 = relationship('HoSoBenhNhan', backref='BenhNhan', lazy=True)
    id4 = relationship('PhieuKham', backref='BenhNhan', lazy=True)
    id5 = relationship('LichKham', backref='datlichkham', lazy=True)


class YTa(NguoiDung):
    id_YTa = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    NgayTruc = Column(DateTime, nullable=False)
    id_ND = relationship("DanhSachKham", backref='YTa', lazy=True)


class QuanTri(NguoiDung):
    id_QT = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    id_update = relationship('CapNhatThuoc', backref='QuanTri', lazy=True)
    id1 = relationship('CapNhatQuyDinh', backref='QuanTri', lazy=True)


class ThuNgan(NguoiDung):
    id_TN = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    id_HD = relationship('HoaDon', backref='ThuNgan', lazy=True)


class DonViThuoc(db.Model):
    id_DVT = Column(Integer, primary_key=True, autoincrement=True)
    TenDonVi = Column(String(20), nullable=False)
    chiTietPhieuKham = relationship('ChiTietPhieuKham', backref='DonViThuoc', lazy=True)


class Thuoc(db.Model):
    id_Thuoc = Column(Integer, primary_key=True, autoincrement=True)
    TenThuoc = Column(String(100), nullable=False)
    SoLuong = Column(Integer, nullable=False)
    NgayNhap = Column(DateTime, nullable=False)
    HSD = Column(DateTime, nullable=False)
    CachDung = Column(String(500), nullable=False)
    DonGia = Column(Float, nullable=False)
    id_DVT = Column(Integer, ForeignKey(DonViThuoc.id_DVT), nullable=False)
    chiTietPhieuKham = relationship('ChiTietPhieuKham', backref='Thuoc', lazy=True)
    id1 = relationship('CapNhatThuoc', backref='Thuoc', lazy=True)

    id_DVTBL = Column(Integer, ForeignKey(DonViThuoc.id_DVT), nullable=False)
    GiaBanLe = Column(Float, nullable=False)


class DanhSachKham(db.Model):
    id_DSKham = Column(Integer, primary_key=True, autoincrement=True)
    NgayLapDSKham = Column(DateTime, nullable=False)
    id_BN = Column(Integer, ForeignKey(BenhNhan.id_BN), nullable=False)
    id_YT = Column(Integer, ForeignKey(YTa.id_YTa), nullable=False)


class PhieuKham(db.Model):
    id_PK = Column(Integer, primary_key=True, autoincrement=True)
    id_BN = Column(Integer, ForeignKey(BenhNhan.id_BN), nullable=False)
    id_BS = Column(Integer, ForeignKey(BacSi.id_BS), nullable=False)
    TrieuChung = Column(String(300), nullable=False)
    NgayKham = Column(DateTime, nullable=False)
    ChuanDoanBenh = Column(String(500), nullable=False)
    chiTietPhieuKham = relationship('ChiTietPhieuKham', backref='PhieuKham', lazy=True)
    id1 = relationship('HoaDon', backref='PhieuKham', lazy=True)


class ChiTietPhieuKham(db.Model):
    id_CTPK = Column(Integer, primary_key=True, autoincrement=True)
    id_PK = Column(Integer, ForeignKey(PhieuKham.id_PK), nullable=False)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc), nullable=False)
    SoLuong = Column(String(300), nullable=False)
    id_DVTBL = Column(Integer, ForeignKey(DonViThuoc.id_DVT), nullable=False)
    GiaThuocBanLe = Column(Float, nullable=False)


class CapNhatThuoc(db.Model):
    id_CNT = Column(Integer, primary_key=True, autoincrement=True)
    id_Thuoc = Column(Integer, ForeignKey(Thuoc.id_Thuoc))
    id_QT = Column(Integer, ForeignKey(QuanTri.id))
    NoiDung = Column(String(500), nullable=False)
    NgayCapNhat = Column(DateTime, nullable=False)


class QuyDinh(db.Model):
    id_QD = Column(Integer, primary_key=True, nullable=False)
    TenQD = Column(String(200), nullable=False)
    NoiDungQD = Column(String(100), nullable=False)

    capNhatQD = relationship('CapNhatQuyDinh', backref='QuyDinh', lazy=True)


class CapNhatQuyDinh(db.Model):
    id_CNQĐ = Column(Integer, primary_key=True, autoincrement=True)
    id_QĐ = Column(Integer, ForeignKey(QuyDinh.id_QD))
    id_QT = Column(Integer, ForeignKey(QuanTri.id))
    NoiDung = Column(String(500), nullable=False)
    NgayCapNhat = Column(DateTime, nullable=False)


class HoSoBenhNhan(db.Model):
    id_HSBN = Column(Integer, primary_key=True, autoincrement=True)
    id_BN = Column(Integer, ForeignKey(BenhNhan.id))
    id_PhieuKham = Column(Integer, ForeignKey(PhieuKham.id_PK))
    GhiChu = Column(String(500), nullable=False)


class HoaDon(db.Model):
    id_HD = Column(Integer, primary_key=True, autoincrement=True)
    id_BN = Column(Integer, ForeignKey(BenhNhan.id_BN))
    id_TN = Column(Integer, ForeignKey(ThuNgan.id_TN))
    id_PK = Column(Integer, ForeignKey(PhieuKham.id_PK))
    NgayThanhToan = Column(DateTime, nullable=False)
    TienKham = Column(Float, default=100)
    TienThuoc = Column(Float, nullable=False)
    TongTien = Column(Float, nullable=False)


class LichKham(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_BN = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    HoTen = Column(String(60), nullable=False)
    DVKham = Column(String(50), nullable=False)
    NgayKham = Column(DateTime, nullable=False)
    TrieuChung = Column(String(300), nullable=False)
    SDT = Column(String(10), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        import hashlib
        
        u = QuanTri(HoTen="Võ Thùy Linh", DiaChi="TpHCM", NamSinh="2003", GioiTinh="Nu", username_sdt="0792366301",
                    password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                    avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                    VaiTro=VaiTro.QuanTri)

        u1 = QuanTri(HoTen="Nguyễn Dương Ngọc Thảo", DiaChi="Long An", NamSinh="2003", GioiTinh="Nu",
                     username_sdt="0835073539",
                     password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                     avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                     VaiTro=VaiTro.QuanTri)

        u2 = QuanTri(HoTen="Nguyễn Vân Anh", DiaChi="TpHCM", NamSinh="2003", GioiTinh="Nu", username_sdt="0932694738",
                     password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                     avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                     VaiTro=VaiTro.QuanTri)

        u3 = BacSi(HoTen="Nguyễn Tường Lam", DiaChi="TpHCM", NamSinh="1996", GioiTinh="Nu", username_sdt="0987510332",
                   password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                   avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                   VaiTro=VaiTro.BacSi, HocVi="Ths.Bs Chuyên khoa II", NgayTruc='2023-12-27')

        u4 = BacSi(HoTen="Nguyễn Hải Đăng", DiaChi="TpHCM", NamSinh="1993", GioiTinh="Nam", username_sdt="0367235691",
                   password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                   avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                   VaiTro=VaiTro.BacSi, HocVi="Bác sĩ đa khoa 2", NgayTruc='2023-12-24')

        u5 = BenhNhan(HoTen="Trần An Khang", DiaChi="TpHCM", NamSinh="2010", GioiTinh="Nam", username_sdt="0375375727",
                      password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                      avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                      VaiTro=VaiTro.BenhNhan)

        u6 = BenhNhan(HoTen="Hồ Việt Lĩnh", DiaChi="TpHCM", NamSinh="2006", GioiTinh="Nam", username_sdt="0352979178",
                      password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                      avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                      VaiTro=VaiTro.BenhNhan)

        u7 = BenhNhan(HoTen="Trần Thị Ngọc Mơ", DiaChi="TpHCM", NamSinh="1997", GioiTinh="Nu",
                      username_sdt="0982356134",
                      password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                      avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                      VaiTro=VaiTro.BenhNhan)

        u8 = BenhNhan(HoTen="Phạm Trung Nguyên", DiaChi="TpHCM", NamSinh="1999", GioiTinh="Nam",
                      username_sdt="0827614599",
                      password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                      avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                      VaiTro=VaiTro.BenhNhan)

        u9 = YTa(HoTen="Nguyễn Ngọc Như Anh", DiaChi="TpHCM", NamSinh="1990", GioiTinh="Nu", username_sdt="0793567289",
                 password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                 avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                 VaiTro=VaiTro.YTa, NgayTruc='2023-12-26')
        u10 = ThuNgan(HoTen="Lê Phương Nhi", DiaChi="TpHCM", NamSinh="1994", GioiTinh="Nu",
                      username_sdt="0872351901",
                      password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                      avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                      VaiTro=VaiTro.ThuNgan)
        u11 = ThuNgan(HoTen="Lê Anh Tuấn", DiaChi="TpHCM", NamSinh="1991", GioiTinh="Nam",
                      username_sdt="0923912088",
                      password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                      avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                      VaiTro=VaiTro.ThuNgan)
        u12 = YTa(HoTen="Nguyễn Mai Anh Khuê", DiaChi="TpHCM", NamSinh="1997", GioiTinh="Nu",
                  username_sdt="0915620018",
                  password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                  avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                  VaiTro=VaiTro.YTa, NgayTruc='2023-12-24')
        db.session.add_all([u, u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12])
        t = DonViThuoc(TenDonVi='Viên')
        t1 = DonViThuoc(TenDonVi='Chai')
        t2 = DonViThuoc(TenDonVi='Gói')
        t3 = DonViThuoc(TenDonVi='Vỉ')
        t4 = DonViThuoc(TenDonVi='Hộp')
        db.session.add_all([t, t1, t2, t3, t4])


        db.session.commit()
