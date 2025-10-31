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
Tạo file `generate_key_cert.sh`

Thực hiện:
```#!/bin/bash
echo "Đang tạo khóa và chứng chỉ..."
openssl genrsa -out private_key.pem 2048
openssl req -x509 -new -nodes -key private_key.pem \
    -subj "/CN=58KTPM Test CA/O=UIT/C=VN" \
    -sha256 -days 365 -out certificate.pem
echo "Hoàn tất! Đã tạo:"
echo "   - private_key.pem"
echo "   - certificate.pem"
```
### 2. Tạo file sign_pdf.py
