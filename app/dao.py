from app.models import *
import hashlib
from app import app, db
import cloudinary.uploader
from sqlalchemy import func
from flask_login import current_user


def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)


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




def check_MK(matkhau):
    return current_user.password == (str(hashlib.md5(matkhau.strip().encode('utf-8')).hexdigest()))


def get_Thuoc():
    return Thuoc.query.all()


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


def get_HSBN():
    return HoSoBenhNhan.query.all()


# def get_Thuoc(id_Thuoc, TenThuoc,SoLuong,id_DVT, CachDung):
#     thuoc = Thuoc.query
#
#     if TenThuoc:
#         tt = Thuoc.filter(Thuoc.TenThuoc.contains(TenThuoc))
#
#     if cate_id:
#         products = products.filter(Product.category_id.__eq__(cate_id))
#
#     if page:
#         page = int(page)
#         page_size = app.config['PAGE_SIZE']
#         start = (page - 1)*page_size
#
#         return products.slice(start, start + page_size)
#
#     return products.all()


if __name__ == '__main__':
    with app.app_context():
        pass
