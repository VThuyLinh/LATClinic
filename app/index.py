import math
from itertools import groupby

from flask import render_template, request, redirect, jsonify, session
from flask_login import current_user
from sqlalchemy import func

from app.models import *
import dao
from app import app, login, admin
import utils
from flask_login import login_user, logout_user, login_required


@app.route("/")
def Home():
    return render_template('index.html')


@app.route("/login1", methods=['get','post'])
def dnn():
    err_msg = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        vaitro = request.form.get('vaitro')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            next = request.args.get('/')
            return redirect('/' if next is None else next)
        else:
            err_msg = "Sai mật khẩu hoặc sai tên người dùng"
    return render_template('login1.html', err_msg=err_msg)

@app.route('/login', methods=["get", "post"])
def process_user_login():
    err_msg = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        vaitro = request.form.get('vaitro')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            next = request.args.get('/')
            return redirect('/' if next is None else next)
        else:
            err_msg = "Sai mật khẩu hoặc sai tên người dùng"
    return render_template('login.html', err_msg=err_msg)


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user and username.__eq__(QuanTri.username_sdt):
        login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             diachi=request.form.get('address'),
                             ns=request.form.get('birthday'),
                             gt=request.form.get('GT'),
                             password=password,
                             avatar=request.files.get('avatar'))

            except Exception as ex:
                print(ex)
                err_msg = str(ex)
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/bookschedule')
@login_required
def bookschedule():
    return render_template("bookschedule.html")


@app.route('/api/check', methods=["post"])
@login_required
def CheckMK():
    matkhau = request.json.get("matkhau")

    try:
        if dao.check_MK(matkhau):
            return jsonify({"message": "Xác Minh Thành Công", 'status': 200})
        else:
            return jsonify({"message": "Xác Minh Thất Bại", 'status': 400})
    except Exception as ex:
        return jsonify({"message": str(ex), 'status': 500})


@app.route('/api/bookschedule', methods=["post"])
@login_required
def add_ngayKham():
    NgayKham = request.json.get("NgayKham")
    HoTen = request.json.get("HoTen")
    DVKham = request.json.get("DVKham")
    DiaChi = request.json.get("DiaChi")
    TrieuChung = request.json.get("TrieuChung")
    SDT = request.json.get("SDT")
    GioiTinh = request.json.get("GioiTinh")
    NamSinh = request.json.get("NamSinh")
    try:
        dao.add_booking(Hoten=HoTen, sdt=SDT, diachi=DiaChi, ngayKham=NgayKham, trieuchung=TrieuChung, dvkham=DVKham,
                        namsinh=NamSinh, gioitinh=GioiTinh)
    except Exception as ex:
        return jsonify({"message": str(ex), 'status': 500}), 404
    else:
        return jsonify({"message": "Lịch khám đã được đặt thành công! Vui lòng đến đúng giờ", 'status': 200}), 200


@app.route("/banggia")
def banggia():
    return render_template("banggia.html")


@app.route("/hoadon")
def hoadon():
    return render_template("hoadon.html")


@app.route("/dichvu")
def dichvu():
    return render_template("dichvu.html")


@app.route('/api/luutamthoi', methods=["post"])
def luutamthoi():
    data = request.json

    phieuKham = session.get("PhieuKham")

    if phieuKham is None:
        phieuKham = {}

    HoTen = data.get("HoTen")
    TrieuChung = data.get("TrieuChung")
    LoaiBenh = data.get("LoaiBenh")
    id = data.get("id")

    phieuKham['thongTinKhamBenh'] = {
        'tenBenhNhan': HoTen,
        'trieuChung': TrieuChung,
        'duDoanBenh': LoaiBenh
    }

    if phieuKham.get("cacLoaiThuoc") is None:
        phieuKham["cacLoaiThuoc"] = {}

    for i in id:
        phieuKham["cacLoaiThuoc"][str(i)] = {
            "tenThuoc": dao.get_Thuoc()[0][0].tenThuoc
        }
    session["PhieuKham"] = phieuKham

    return utils.hien_phieu_tam_thoi(phieuKham)


@app.route("/lapphieukham")
def lappk():
    key = request.args.get('key')
    hsbn = request.args.get('hsbn')
    return render_template("lapphieukham.html", Thuoc=dao.get_Thuoc(key), DonViThuoc=dao.get_DonViThuoc(),
                           NguoiDung=dao.get_NguoiDung(), PhieuKham=utils.hien_phieu_tam_thoi(session.get("PhieuKham")),
                           HoSoBenhNhan=dao.get_HSBN(hsbn))


@app.route('/api/lapphieukham', methods=['post'])
def lpk():
    TrieuChung = request.json.get("TrieuChung")
    NgayKham = request.json.get("NgayKham")
    ChuanDoanBenh = request.json.get("ChuanDoanBenh")
    HoTen = request.json.get("HoTen")

    if request.method.__eq__('POST'):
        try:
            if dao.add_PK(hoten=HoTen, trieuchung=TrieuChung, ngaykham=NgayKham,
                          chuandoanbenh=ChuanDoanBenh):
                return jsonify({"message": "Phiếu khám đã được tạo thành công! Vui lòng đến đúng giờ", 'status': 200})
            else:
                return jsonify({"message": "Phiếu khám không được tạo ", 'status': 300})
        except Exception as ex:
            return jsonify({"message": str(ex), 'status': 500}), 404
        else:
            return jsonify({"message": "Phiếu khám đã được tạo thành công! Vui lòng đến đúng giờ", 'status': 500}), 200


@app.route('/danhsachkham')
def doctor():
    return render_template('danhsachkham.html', DanhSachKham=dao.getDSK())


@app.route('/findmedicine')
def findm():
    return render_template('findmedicine.html', Thuoc=dao.get_Thuoc(), DonViThuoc=dao.get_DVT())


@app.route("/ctpk")
def ctpk():
    return render_template("chitietphieukham.html")


@app.route('/hosobenhnhan')
def hsbn():
    return render_template('hsbn.html', PhieuKham=dao.get_PK(), NguoiDung=dao.get_ND(),
                           ChiTietPhieuKham=dao.get_CTPK(), BacSi=dao.get_BS(), HoSoBenhNhan=dao.get_HSBN())


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/account')
def acc():
    return render_template('thongtinND.html')


@app.route('/test')
def thu():
    return render_template('test.html')


@app.route('/logout')
def process_logout_user():
    logout_user()
    return redirect('/')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)





if __name__ == '__main__':
    app.run(debug=True)
