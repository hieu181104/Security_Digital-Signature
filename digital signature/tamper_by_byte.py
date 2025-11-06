# tamper_by_byte.py
import re
from pathlib import Path

SIGNED = Path("signed.pdf")       # input: file đã ký
TAMPERED = Path("tampered.pdf")   # output: file bị sửa

data = SIGNED.read_bytes()

# tìm mảng /ByteRange [ a b c d ]
m = re.search(rb"/ByteRange\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\]", data)
if not m:
    raise SystemExit("Không tìm thấy /ByteRange trong PDF. Kiểm tra tên field hoặc file.")

a, b, c, d = (int(m.group(i)) for i in range(1,5))
print("ByteRange offsets:", a, b, c, d)

# chọn vị trí để thay đổi: nằm trong khoảng a..a+b (vùng băm đầu)
# tránh vị trí quá gần đầu xref/objects, lấy a + min(50, b-1)
if b <= 10:
    raise SystemExit("Vùng ByteRange quá nhỏ, không thể thay đổi an toàn.")
pos = a + min(50, b - 1)
print("Sẽ thay đổi byte tại offset:", pos)

# tạo bytes mới bằng cách lật bit thấp nhất (xor 1) của byte đó
lst = bytearray(data)
lst[pos] = lst[pos] ^ 0x01

TAMPERED.write_bytes(bytes(lst))
print("Đã tạo tampered file:", TAMPERED.resolve())