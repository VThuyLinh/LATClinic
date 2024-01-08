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
    VaiTro = Column(Enum(VaiTro), default=VaiTro.NguoiDung)

    def __str__(self):
        return self.name


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
    id5= relationship('LichKham', backref='datlichkham', lazy=True)

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
    tendvt=relationship('DonViThuoc', backref='Thuoc', lazy=True)


class DanhSachKham(db.Model):
    id_DSKham = Column(Integer, primary_key=True, autoincrement=True)
    id_BN = Column(Integer, ForeignKey(BenhNhan.id_BN), nullable=False)
    id_YT = Column(Integer, ForeignKey(YTa.id_YTa), nullable=False)
    NgayLapPhieuKham = Column(DateTime, nullable=False)


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
    id_DonVi = Column(Integer, ForeignKey(DonViThuoc.id_DVT), nullable=False)
    Gia = Column(String(500), nullable=False)


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

        db.session.commit()
