from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import *
from app import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='Lat Clinic', template_mode='bootstrap4', index_view=MyAdmin())


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.VaiTro == VaiTro.QuanTri


class AuthenticatedNurse(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.VaiTro == VaiTro.YTa


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/')


class MyProductView(AuthenticatedAdmin):
    column_list = ['id_PK', 'id_BN', 'TrieuChung', 'ChuanDoanBenh', 'NgayKham']
    can_export = True
    column_searchable_list = ['TrieuChung']
    column_editable_list = ['TrieuChung', 'ChuanDoanBenh']
    edit_modal = True


class QLQuyDinh(AuthenticatedAdmin):
    column_list = ['id_QD', 'TenQD', 'NoiDungQD']
    can_export = True
    column_searchable_list = ['TenQD']
    column_editable_list = ['TenQD', 'NoiDungQD']
    edit_modal = True


class QLThuoc(AuthenticatedAdmin):
    column_list = ['id_Thuoc', 'TenThuoc', 'SoLuong', 'NgayNhap', 'HSD', 'CachDung', 'DonGia', 'id_DVT', 'tenDVT']
    can_export = True
    column_searchable_list = ['TenThuoc']
    column_editable_list = ['CachDung', 'SoLuong']
    edit_modal = True


class QLHoaDon(AuthenticatedAdmin):
    column_list = ['id_HD', 'id_TN', 'NgayThanhToan', 'TienThuoc', 'TongTien']
    can_export = True
    column_searchable_list = ['NgayThanhToan']
    edit_modal = True


class ThongKeTST(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/tansuat.html', mon_stats=dao.thuoc_thongke())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.VaiTro.value == 4


class ThongKeDoanhThu(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html', stats=dao.doanhthu_thongke())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.VaiTro.value == 4


# class MyStatsView(AuthenticatedUser):
#     @expose("/")
#     def index(self):
#         return self.render('admin/stats.html', stats=dao.revenue_stats(), mon_stats=dao.revenue_mon_stats())


# admin.add_view(MyStatsView(name='Thống kê báo cáo'))
admin.add_view(ThongKeDoanhThu(name='BCCTK doanh thu'))
admin.add_view(ThongKeTST(name='BCTK tần suất thuốc'))
admin.add_view(QLQuyDinh(QuyDinh, db.session))
admin.add_view(QLThuoc(Thuoc, db.session))
admin.add_view(QLHoaDon(HoaDon, db.session))
admin.add_view(AuthenticatedAdmin(NguoiDung, db.session))
admin.add_view(MyProductView(PhieuKham, db.session))
admin.add_view(AuthenticatedNurse(DanhSachKham, db.session))
admin.add_view(MyLogoutView(name='Đăng xuất'))
