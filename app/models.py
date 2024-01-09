import enum

from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean, Enum, DATETIME, Double, ForeignKey,INTEGER
from sqlalchemy.orm import relationship
from app import db,app


# User
class UserRoleEnum(enum.Enum):
    KHACH_HANG = 1
    LE_TAN = 2
    QUAN_LY = 3
class KhachHangRoleEnum(enum.Enum):
    NOI_DIA = 1
    NUOC_NGOAI = 2
class TrangThaiDatThuePhongEnum(enum.Enum):
    DAT_PHONG = 1
    THUE_PHONG = 2
    DA_THANH_TOAN = 3
    HUY_PHONG = 4
class User(db.Model, UserMixin):
    id = Column(String(45), primary_key=True, nullable=False)
    username = Column(String(45), unique=True, nullable=True)
    password = Column(String(45), nullable=True)
    ten = Column(String(45), nullable=False)
    ho = Column(String(22), nullable=False)
    gioi_tinh = Column(Boolean, nullable=False, default=False)
    ngay_sinh = Column(DATETIME, nullable=True)
    cccd = Column(String(45), nullable=False, unique=True)
    dia_chi = Column(String(255), nullable=True)
    sdt = Column(String(255), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.KHACH_HANG)
    nhan_vien = relationship("NhanVien",backref="User", lazy=True)
    khach_hang = relationship("KhachHang", backref="User", lazy=True)



# nhan vien

class NhanVien(db.Model):
    id = Column(String(45), ForeignKey(User.id), primary_key=True, nullable=False)
    luong = Column(Double, nullable=False, default=0)
    cac_ca_lam_viec = relationship("BangPhanCong", backref="NhanVien", lazy=True)
    le_tan = relationship("LeTan",backref="NhanVien",lazy=True)


# Cap Quan Ly
class CapQuanLy(db.Model):
    id = Column(String(45), primary_key=True, nullable=False)
    cap_quan_ly = Column(String(45), nullable=False)
    cac_quan_ly = relationship("QuanLy", backref="CapQuanLy", lazy=True)


# QuanLy
class QuanLy(db.Model):
    id = Column(String(45), ForeignKey(NhanVien.id), primary_key=True, nullable=False)
    id_cap_quan_ly = Column(String(45),ForeignKey( CapQuanLy.id) ,nullable=False)


# ca lam viec

class CaLamViec(db.Model):
    id = Column(String(45), primary_key=True, nullable=False)
    thoi_gian_bat_dau = Column(DATETIME, nullable=False)
    thoi_gian_ket_thuc = Column(DATETIME, nullable=False)
    cac_nhan_vien = relationship("BangPhanCong", backref="CaLamViec", lazy=True)


# BAN PHAN CONG CALAMVIEC-NHANVIEN
class BangPhanCong(db.Model):
    id_calamviec = Column(String(45), ForeignKey(CaLamViec.id), primary_key=True, nullable=False)
    id_nhanvien = Column(String(45), ForeignKey(NhanVien.id), primary_key=True, nullable=False)


# tiennghi
class TienNghi(db.Model):
    id = Column(String(45), primary_key=True, nullable=False)
    ten = Column(String(45), nullable=False)
    tinh_trang = Column(Boolean, nullable=False, default=True)
    gia_tien = Column(Double, nullable=False, default=0)
    cac_phong = relationship("Phong_TienNghi", backref="TienNghi", lazy=True)


# loai phong
class LoaiPhong(db.Model):
    id = Column(String(45), primary_key=True, nullable=False)
    loai_phong = Column(String(45), nullable=False)
    mo_ta = Column(String(255), default="")
    gia_tien = Column(Double, nullable=False, default=0)
    cac_phong = relationship("Phong", backref="LoaiPhong", lazy=True)
    cac_dich_vu = relationship("LoaiPhong_DichVu", backref="LoaiPhong", lazy=True)


# dich vu
class DichVu(db.Model):
    id = Column(String(45), primary_key=True, nullable=False)
    ten = Column(String(45), nullable=False)
    tinh_trang = Column(Boolean, nullable=False, default=True)
    gia_tien = Column(Double, nullable=False, default=0)
    cac_loai_phong = relationship("LoaiPhong_DichVu",backref="DichVu",lazy=True)
    cac_khach_hang_dang_ky = relationship("KhachHang_DichVu", backref="DichVu", lazy=True)
    hinh_anh_dich_vu = relationship("HinhAnh_DichVu", backref="DichVu", lazy=True)


# loaiphong -- dichvu
class LoaiPhong_DichVu(db.Model):
    id_loai_phong = Column(String(45), ForeignKey(LoaiPhong.id), primary_key=True, nullable=False)
    id_dich_vu = Column(String(45), ForeignKey(DichVu.id), primary_key=True, nullable=False)


# PHONG
class Phong(db.Model):
    id = Column(String(45), primary_key=True, nullable=False)
    tinh_trang = Column(Boolean, nullable=False, default=True)
    so_luong_nguoi_o= Column(INTEGER, nullable=False)
    id_loai_phong = Column(String(45), ForeignKey(LoaiPhong.id), nullable=False)
    cac_tien_nghi = relationship("Phong_TienNghi", backref="Phong" , lazy=True)
    cac_bang_dat_phong = relationship("BangDatPhong", backref="Phong", lazy=True)
    cac_bang_thue_phong = relationship("BangThuePhong", backref="Phong", lazy=True)
    hinh_anh_phong = relationship("HinhAnh_Phong", backref="Phong", lazy=True)

# Phong -- TienNghi


class Phong_TienNghi(db.Model):
    id_phong = Column(String(45), ForeignKey(Phong.id), primary_key=True, nullable=False)
    id_tiennghi = Column(String(45), ForeignKey(TienNghi.id), primary_key=True, nullable=False)

# letan
class LeTan(db.Model):
    id = Column(String(45), ForeignKey(NhanVien.id), primary_key=True, nullable=False)
    cac_bang_dat_phong = relationship("BangDatPhong",backref="LeTan", lazy=True)
    cac_bang_thue_phong = relationship("BangThuePhong", backref="LeTan", lazy=True)
    cac_hoa_don = relationship("HoaDon", backref="LeTan", lazy=True)
# khachhang
class KhachHang(db.Model):
    id = Column(String(45), ForeignKey(User.id), primary_key=True, nullable=False)
    cac_bang_dat_phong = relationship("BangDatPhong",backref="KhachHang", lazy=True)
    loai_khach = Column(Enum(KhachHangRoleEnum), default=KhachHangRoleEnum.NOI_DIA)
    nguoi_dat = relationship("BangNguoiDat", backref="KhachHang", lazy=True)
    nguoi_thue = relationship("BangNguoiThue", backref="KhachHang", lazy=True)
    cac_dich_vu_dang_ky = relationship("KhachHang_DichVu", backref="KhachHang", lazy=True)

# khach hang - phong - letan
class BangDatPhong(db.Model):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    id_le_tan = Column(String(45), ForeignKey(LeTan.id))
    id_khach_hang = Column(String(45), ForeignKey(KhachHang.id), nullable=False)
    id_phong = Column(String(45), ForeignKey(Phong.id), primary_key=True, nullable=False)
    thoi_gian_dat = Column(DATETIME, primary_key=True, nullable=False)
    thoi_gian_tra = Column(DATETIME, nullable=False)
    trang_thai = Column(Enum(TrangThaiDatThuePhongEnum), default=TrangThaiDatThuePhongEnum.DAT_PHONG)
    nguoi_dat_phong = relationship("BangNguoiDat", backref="BangDatPhong", lazy=True)

# phong - letan
class BangThuePhong(db.Model):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    id_le_tan = Column(String(45), ForeignKey(LeTan.id), nullable=False)
    id_phong = Column(String(45), ForeignKey(Phong.id), primary_key=True, nullable=False)
    thoi_gian_nhan = Column(DATETIME, primary_key=True, nullable=False)
    thoi_gian_tra = Column(DATETIME, nullable=False)
    trang_thai = Column(Enum(TrangThaiDatThuePhongEnum), default=TrangThaiDatThuePhongEnum.THUE_PHONG)
    nguoi_thue_phong = relationship("BangNguoiThue", backref="BangThuePhong", lazy=True)
    hoa_don_phong = relationship("HoaDon",backref="BangThuePhong", lazy= True)



# id bang dat phong
class BangNguoiDat(db.Model):
    id_khach_hang = Column(String(45), ForeignKey(KhachHang.id),primary_key=True)
    id_bang_dat_phong = Column(INTEGER,ForeignKey(BangDatPhong.id),primary_key=True)


# id bang thue phong
class BangNguoiThue(db.Model):
    id_khach_hang = Column(String(45), ForeignKey(KhachHang.id),primary_key=True)
    id_bang_thue_phong = Column(INTEGER,ForeignKey(BangThuePhong.id),primary_key=True)

# hoa Don Phong
class HoaDon(db.Model):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    id_le_tan = Column(String(45), ForeignKey(LeTan.id), nullable=False)
    id_bang_thue_phong = Column(INTEGER, ForeignKey(BangThuePhong.id), nullable=False)
    tien_tong = Column(Double, nullable=False)
    cac_dich_vu_khach_hang_su_dung = relationship("KhachHang_DichVu", backref="HoaDon", lazy=True)


#Chi Tiet Hoa Don Dich Vu
class KhachHang_DichVu(db.Model):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    id_khach_hang = Column(String(45), ForeignKey(KhachHang.id))
    id_dich_vu = Column(String(45), ForeignKey(DichVu.id))
    ngay_dang_ky_su_dung = Column(DATETIME)
    gia_tien = Column(Double, nullable=False)
    id_hoa_don = Column(INTEGER, ForeignKey(HoaDon.id), nullable=False)

# hinhanh
class HinhAnh(db.Model):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    duong_dan = Column(String(255), nullable=False)
    ghi_chu = Column(String(255), default="")
    hinh_anh_dich_vu = relationship("HinhAnh_DichVu", backref="HinhAnh", lazy=True)
    hinh_anh_phong = relationship("HinhAnh_Phong", backref="HinhAnh", lazy=True)

# hinhanh-dichvu
class HinhAnh_DichVu(db.Model):
    id_dich_vu = Column(String(45), ForeignKey(DichVu.id), nullable=False)
    id_hinh_anh = Column(INTEGER, ForeignKey(HinhAnh.id), primary_key=True, nullable=False)

# hinhanh - loaiphong
class HinhAnh_Phong(db.Model):
    id_loai_phong = Column(String(45), ForeignKey(Phong.id), nullable=False)
    id_hinh_anh = Column(INTEGER, ForeignKey(HinhAnh.id), primary_key=True, nullable=False)
if __name__ == "__main__":
    with app.app_context():
        db.session.commit()
        # db.create_all()
