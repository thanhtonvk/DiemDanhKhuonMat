import os
import random

import cv2
from flask import Flask, render_template, request, redirect

from config.constants import Constants
from dal import LopDal, HocSinhDal, DiemDanhDal
from dal.DiemDanhDal import add_diem_danh
from dal.HocSinhDal import tim_kiem_hoc_sinh
from entities.HocSinh import HocSinh
from entities.Lop import Lop
from modules.face_detection import FaceDetection
from modules.face_recognition import FaceRecognition

app = Flask(__name__)
app.config['UPLOAD_VIDEO'] = './faces/'

face_recognition = FaceRecognition()
face_detection = FaceDetection()


@app.route('/', methods=['GET'])
def index():
    lops = LopDal.get()
    return render_template('lop/index.html', lops=lops)


@app.route('/lop/add', methods=['GET', 'POST'])
def add_lop():
    if request.method == 'GET':
        return render_template('lop/create.html')
    if request.method == 'POST':
        lop = Lop()
        lop.TenLop = request.form['TenLop']
        lop.GVCN = request.form['GVCN']
        rs = LopDal.add(lop)
        print(rs)
        if rs:
            return redirect('/')
        return render_template('lop/create.html')
    return render_template('lop/create.html')


@app.route('/lop/edit/<int:id>', methods=['GET', 'POST'])
def edit_lop(id: int):
    if request.method == 'GET':
        for lop in LopDal.get():
            if lop.Id == id:
                return render_template('lop/edit.html', lop=lop)
    if request.method == 'POST':
        lop = Lop()
        lop.TenLop = request.form['TenLop']
        lop.GVCN = request.form['GVCN']
        rs = LopDal.update(lop, id)
        print(rs)
        if rs:
            return redirect('/')
        return render_template('lop/edit.html')
    return render_template('lop/edit.html')


@app.route('/lop/delete/<int:id>', methods=['GET'])
def delete_lop(id: int):
    rs = LopDal.delete(id)
    return redirect('/')


@app.route('/hoc-sinh/get/<int:id>', methods=['GET'])
def get_hoc_sinh(id: int):
    Constants.IDLOP = id
    hocSinhs = HocSinhDal.get_ds_hoc_sinh_theo_lop(id)
    return render_template('hoc-sinh/index.html', hocSinhs=hocSinhs)


@app.route('/hoc-sinh/add', methods=['GET', 'POST'])
def add_hoc_sinh():
    if request.method == 'POST':
        hocSinh = HocSinh()
        hocSinh.HoTen = request.form['HoTen']
        hocSinh.Lop = request.form['Lop']
        hocSinh.Id = random.randint(10000, 99999)
        f = request.files['file']
        file_name = f.filename
        try:
            os.mkdir(app.config['UPLOAD_VIDEO'] + "/videos/" + str(hocSinh.Id))
            save_path = os.path.join(app.config['UPLOAD_VIDEO'] + "/videos/" + str(hocSinh.Id), file_name)
        except:
            print('err')
        f.save(save_path)
        list_of_faces, list_of_embed = face_recognition.save_face_from_video(hocSinh.Id, save_path)
        if len(list_of_faces) == 3:
            hocSinh.KhuonMat1 = list_of_faces[0]
            hocSinh.KhuonMat2 = list_of_faces[1]
            hocSinh.KhuonMat3 = list_of_faces[2]
            hocSinh.EmbFace1 = list_of_embed[0].tobytes()
            hocSinh.EmbFace2 = list_of_embed[1].tobytes()
            hocSinh.EmbFace3 = list_of_embed[2].tobytes()
            rs = HocSinhDal.add(hocSinh)
            if rs:
                print('ok')
                return redirect('/hoc-sinh/get/' + str(Constants.IDLOP))
    lops = LopDal.get()
    return render_template('hoc-sinh/create.html', lops=lops)


@app.route('/hoc-sinh/add-auto', methods=['GET', 'POST'])
def add_hoc_sinh_auto():
    lops = LopDal.get()
    if request.method == 'POST':
        hocSinh = HocSinh()
        hocSinh.HoTen = request.form['HoTen']
        hocSinh.Lop = request.form['Lop']
        hocSinh.Id = random.randint(10000, 99999)
        f = request.files['file']
        file_name = f.filename
        try:
            os.mkdir(app.config['UPLOAD_VIDEO'] + "/videos/" + str(hocSinh.Id))
            save_path = os.path.join(app.config['UPLOAD_VIDEO'] + "/videos/" + str(hocSinh.Id), file_name)
        except:
            print('err')
        f.save(save_path)
        list_of_faces, list_of_embed = face_recognition.save_face_from_video(hocSinh.Id, save_path)
        if len(list_of_faces) == 3:
            hocSinh.KhuonMat1 = list_of_faces[0]
            hocSinh.KhuonMat2 = list_of_faces[1]
            hocSinh.KhuonMat3 = list_of_faces[2]
            hocSinh.EmbFace1 = list_of_embed[0].tobytes()
            hocSinh.EmbFace2 = list_of_embed[1].tobytes()
            hocSinh.EmbFace3 = list_of_embed[2].tobytes()
            rs = HocSinhDal.add(hocSinh)
            if rs:
                return render_template('hoc-sinh/create-auto.html', lops=lops)
    return render_template('hoc-sinh/create-auto.html', lops=lops)


@app.route('/hoc-sinh/edit/<int:id>', methods=['GET', 'POST'])
def edit_hoc_sinh(id: int):
    if request.method == 'POST':
        hocSinh = HocSinh()
        for hocsinh in HocSinhDal.get_all():
            if hocsinh.Id == id:
                hocSinh = hocsinh
                break
        hocSinh.HoTen = request.form['HoTen']
        hocSinh.Lop = request.form['Lop']
        f = request.files['file']
        file_name = f.filename
        try:
            os.mkdir(app.config['UPLOAD_VIDEO'] + "/videos/" + str(hocSinh.Id))
        except:
            print('err')
        save_path = os.path.join(app.config['UPLOAD_VIDEO'] + "/videos/" + str(hocSinh.Id), file_name)
        f.save(save_path)
        list_of_faces, list_of_embed = face_recognition.save_face_from_video(hocSinh.Id, save_path)
        if len(list_of_faces) == 3:
            hocSinh.KhuonMat1 = list_of_faces[0]
            hocSinh.KhuonMat2 = list_of_faces[1]
            hocSinh.KhuonMat3 = list_of_faces[2]
            hocSinh.EmbFace1 = list_of_embed[0].tobytes()
            hocSinh.EmbFace2 = list_of_embed[1].tobytes()
            hocSinh.EmbFace3 = list_of_embed[2].tobytes()
            rs = HocSinhDal.update(hocSinh, id)
            if rs:
                return redirect('/hoc-sinh/get/' + str(Constants.IDLOP))
    lops = LopDal.get()
    for hocsinh in HocSinhDal.get_all():
        if hocsinh.Id == id:
            return render_template('/hoc-sinh/edit.html', data={'hocSinhs': hocsinh, 'lops': lops})


@app.route('/hoc-sinh/delete/<int:id>', methods=['GET'])
def delete_hoc_sinh(id):
    rs = HocSinhDal.delete(id)
    return redirect('/hoc-sinh/get/' + str(Constants.IDLOP))


@app.route('/diem-danh/get/<int:id>', methods=['GET'])
def get_diem_danh(id):
    ds_diem_danh = DiemDanhDal.get_trang_thai_diem_danh(id)
    Constants.IDLOP = id
    return render_template('diem-danh/index.html', diemDanhs=ds_diem_danh)


@app.route('/diem-danh/hinhanh', methods=['GET', 'POST'])
def diem_danh():
    if request.method == 'GET':
        return render_template('diem-danh/diemdanh.html')
    if request.method == 'POST':
        f = request.files['file']
        file_name = f.filename
        print(file_name)
        save_path = os.path.join(app.config['UPLOAD_VIDEO'] + "/images/", file_name)
        f.save(save_path)
        # load image
        frame = cv2.imread(save_path)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bboxes = face_detection.detect(frame)
        if len(bboxes) > 0:
            for idx, box in enumerate(bboxes):
                box = list(map(int, box))
                x_min, y_min, x_max, y_max = box
                face = frame[y_min:y_max, x_min:x_max]
                hoc_sinh = tim_kiem_hoc_sinh(face_recognition.feature_extractor(face))
                print(hoc_sinh.HoTen)
                if hoc_sinh is not None:
                    add_diem_danh(hoc_sinh.Id)
        return redirect('/')
    return render_template('diem-danh/diemdanh.html')


@app.route('/diem-danh/xuat-file', methods=['GET'])
def xuat_file():
    from datetime import datetime
    ds_diem_danh = DiemDanhDal.get_trang_thai_diem_danh(Constants.IDLOP)
    ngay_hien_tai = datetime.today().strftime('%Y_%m_%d')
    f = open('./export/'+str(Constants.IDLOP)+'_' + ngay_hien_tai + '.csv', encoding='utf-8', mode='a')
    for diem_danh in ds_diem_danh:
        f.write(f"{diem_danh.IdHocSinh},{diem_danh.TenHocSinh},{diem_danh.NgayDiemDanh},{diem_danh.GioDiemDanh},{diem_danh.TrangThai}\n")
    f.close()
    return render_template('diem-danh/index.html', diemDanhs=ds_diem_danh)
if __name__ == '__main__':
    app.run(host='localhost', port=5000)
