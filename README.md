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
## II. CÁC BƯỚC TẠO VÀ LƯU CHỮ KÝ TRONG PDF
### 1. Tạo khóa RSA và chứng chỉ
#### Tạo khóa riêng
```openssl genrsa -out private_key.pem 2048```
#### Tạo chứng chỉ
```openssl req -x509 -new -nodes -key private_key.pem -sha256 -days 365 -out certificate.pem -subj "/CN=Nguyen Trung Hieu/O=UIT/C=VN"```
### 2. Tạo file và ký file PDF.
#### Tạo file `sign_pdf.py`

#### Trong terminal (VSCODE) chạy lệnh:
```python sign_pdf.py```

#### Kết quả:
<img width="2588" height="46" alt="image" src="https://github.com/user-attachments/assets/108150b5-e091-48e7-8942-1fd20bab56cb" />

#### File signed.pdf có chữ ký hợp lệ:
<img width="3071" height="1431" alt="image" src="https://github.com/user-attachments/assets/47bf969a-1047-46e7-a3cc-053f5d42df31" />

#### Nêu rõ:
- Trường ```md_algorithm="sha256"``` cho biết thuật toán băm (hash) sử dụng là: `SHA-256 (Secure Hash Algorithm 256-bit)`. Đây là thuật toán băm chuẩn của họ `SHA-2`, tạo ra chuỗi 256 bit (32 byte).
- `SimpleSigner` trong thư viện `pyHanko` mặc định sử dụng `PKCS#1 v1.5 padding` khi ký RSA. Đây là kiểu đệm chuẩn trong chữ ký số PDF/PAdES, tương thích với Adobe Acrobat.
- Độ dài khóa sử dụng: `RSA 2048-bit`
- Chữ ký PKCS#7 được lưu trong trường `/Contents` của dictionary chữ ký (SigDict) trong file PDF.
## III. XÁC THỰC CHỮ KÝ TRÊN PDF ĐÃ KÝ
#### Bước 1: Tạo file `verify_pdf.py`
Các bước kiểm tra:
1. Đọc Signature dictionary: Truy xuất trường /Contents (chữ ký PKCS#7) và /ByteRange (vùng dữ liệu được ký).
2. Tính lại hash ByteRange: Dùng SHA-256 để băm vùng dữ liệu được ký và so sánh với messageDigest trong chữ ký.
3. Giải mã và xác thực chữ ký PKCS#7: Dùng khóa công khai trong chứng thư số để kiểm tra tính toàn vẹn của chữ ký.
4. Kiểm tra chuỗi chứng chỉ: Xác thực chứng thư người ký có được cấp bởi CA tin cậy (trust_roots).
5. Kiểm tra OCSP/CRL (nếu có): Đảm bảo chứng thư chưa bị thu hồi.
6. Kiểm tra timestamp token (nếu có): Xác minh thời điểm ký và máy chủ TSA.
7. Phân tích incremental update: Phát hiện các thay đổi (sửa đổi, điền form, thêm trang...) sau khi ký.
8. Ghi kết quả ra file log: Ghi toàn bộ quá trình xác thực và kết quả hợp lệ / không hợp lệ vào verify_log.txt.
#### Bước 2: Tạo file pdf giả mạo: `tampered.pdf`
Ở bài tập này em đã tạo một file `tamper_by_byte.py` để thay đổi byte trực tiếp trong vùng được ký `(ByteRange)`: dễ làm, chắc chắn làm vỡ chữ ký vì thay đổi dữ liệu mà chữ ký đã băm.

Script này đọc `signed.pdf`, tìm mảng `/ByteRange [ a b c d ]` trong PDF, chọn 1 vị trí nằm trong đoạn đã kí (ví dụ offset a + 50) rồi lật 1 bit ở đó, lưu file mới `tampered.pdf`. Vì đã thay đổi nội dung nằm trong `ByteRange`, chữ ký sẽ không hợp lệ nữa.

Chạy lệnh ```python tamper_by_byte.py``` để tạo ra file `tampered.pdf` giả mạo (đã thay đổi byte của chữ ký). 

#### Bước 3: Chạy file `verify_pdf.py` và kiểm chứng kết quả xác thực:
Kết quả sau khi chạy file `verify_pdf.py` để xác thực `tampered.pdf` được ghi log để tiện theo dõi:

<img width="2628" height="535" alt="image" src="https://github.com/user-attachments/assets/ce0fe664-30f6-42ed-a5c7-30525392f856" />

<img width="3064" height="1426" alt="image" src="https://github.com/user-attachments/assets/016d67b5-dea3-472b-a937-fd648c665bd2" />

#### Kết quả cho thấy tuy nội dung file chưa bị chỉnh sửa nhưng chữ ký KHÔNG HỢP LỆ nên kết luận "Chữ ký không hợp lệ hoặc file đã bị chỉnh sửa".

<img width="1824" height="876" alt="image" src="https://github.com/user-attachments/assets/5387c7f3-ab7c-4b7f-9b1c-d77d4c2fd6d4" />

## THE END
