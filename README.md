# Security Digital Signature
## THÔNG TIN CÁ NHÂN
##### Họ và tên: Nguyễn Trung Hiếu
##### Lớp: K58KTP
##### MSSV: K225480106019
## BÀI TẬP 2 - AN TOÀN VÀ BẢO MẬT THÔNG TIN
## I. MỤC TIÊU VÀ CÔNG CỤ
Phân tích và thực hiện việc nhúng, xác thực chữ ký số trong file PDF

Bài làm sử dụng các công cụ:
- OpenSSL – sinh cặp khóa và chứng thư số tự ký (self-signed)
- PyPDF2 / pikepdf – thao tác PDF và nhúng vùng chữ ký
- hashlib, base64 – băm dữ liệu và mã hóa chữ ký
- Python – viết script
## III. CÁC BƯỚC TẠO VÀ LƯU CHỮ KÝ TRONG PDF
### 1. Tạo khóa RSA và chứng chỉ
#### Tạo khóa riêng
```openssl genrsa -out private_key.pem 2048```
#### Tạo chứng chỉ
```openssl req -x509 -new -nodes -key private_key.pem -sha256 -days 365 -out certificate.pem -subj "/CN=Nguyen Trung Hieu/O=UIT/C=VN"```
### 2. Tạo file và ký file PDF.
Tạo file `sign_pdf.py`

Trong terminal (VSCODE) chạy lệnh:
```python sign_pdf.py```

Kết quả:
<img width="2588" height="46" alt="image" src="https://github.com/user-attachments/assets/108150b5-e091-48e7-8942-1fd20bab56cb" />

#### File signed.pdf có chữ ký hợp lệ:
<img width="3071" height="1431" alt="image" src="https://github.com/user-attachments/assets/47bf969a-1047-46e7-a3cc-053f5d42df31" />

#### Nêu rõ:
- Trường md_algorithm="sha256" cho biết thuật toán băm (hash) sử dụng là: SHA-256 (Secure Hash Algorithm 256-bit). Đây là thuật toán băm chuẩn của họ SHA-2, tạo ra chuỗi 256 bit (32 byte).
- SimpleSigner trong thư viện pyHanko mặc định sử dụng PKCS#1 v1.5 padding khi ký RSA. Đây là kiểu đệm chuẩn trong chữ ký số PDF/PAdES, tương thích với Adobe Acrobat.
- Độ dài khóa sử dụng: RSA 2048-bit
- Chữ ký PKCS#7 được lưu trong trường /Contents của dictionary chữ ký (SigDict) trong file PDF.
### 3. Xác thực chữ ký trên PDF đã ký
