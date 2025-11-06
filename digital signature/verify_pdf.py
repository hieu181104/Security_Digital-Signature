# =====================
# 🔒 VERIFY PDF
# =====================
from pyhanko.sign import validation
from pyhanko.sign.validation.status import SignatureStatus
from pyhanko.sign.diff_analysis import ModificationLevel
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.keys import load_cert_from_pemder
from pyhanko_certvalidator import ValidationContext
import hashlib, datetime, io, os
from datetime import timezone, timedelta
import traceback

# === Cấu hình đường dẫn ===
PDF_PATH = r"D:\Visual Studio Code - Folders\digital signature\tampered.pdf"
CERT_FILE = r"D:\Visual Studio Code - Folders\digital signature\certificate.pem"
LOG_FILE = r"D:\Visual Studio Code - Folders\digital signature\verify_log.txt"
FIELD_NAME = "SigField1"

# === Tạo ValidationContext ===
trusted_cert = load_cert_from_pemder(CERT_FILE)
vc = ValidationContext(trust_roots=[trusted_cert])

# === Chuẩn bị log ===
log = io.StringIO()
def log_print(msg):
    print(msg)
    log.write(msg + "\n")

log_print("=== XÁC THỰC CHỮ KÝ PDF ===")
log_print(f"🕒 Thời gian xác thực: {datetime.datetime.now()}")
log_print(f"📄 File kiểm tra: {PDF_PATH}")
log_print("====================================")

try:
    # === Đọc file PDF ===
    with open(PDF_PATH, "rb") as f:
        reader = PdfFileReader(f)
        embedded_sigs = reader.embedded_signatures

        if not embedded_sigs:
            log_print("❌ Không tìm thấy chữ ký nào trong PDF.")
            raise SystemExit()

        sig = embedded_sigs[0]
        sig_name = sig.field_name or FIELD_NAME
        log_print(f"🔍 Phát hiện chữ ký: {sig_name}")
        log_print("====================================")

        # === Đọc Signature dictionary ===
        sig_dict = sig.sig_object
        contents = sig_dict.get('/Contents')
        byte_range = sig_dict.get('/ByteRange')

        log_print(f"/Contents: {len(contents)} bytes")
        log_print(f"/ByteRange: {byte_range}")

        # === Tính lại hash ===
        f.seek(0)
        data = f.read()
        ranges = list(byte_range)
        signed_data = data[ranges[0]:ranges[0]+ranges[1]] + data[ranges[2]:ranges[2]+ranges[3]]
        digest = hashlib.sha256(signed_data).hexdigest()
        log_print(f"SHA256(ByteRange): {digest[:64]}... ✅")

        # === Xác thực chữ ký ===
        status: SignatureStatus = validation.validate_pdf_signature(sig, vc)

        log_print("====================================")
        log_print("🔒 KẾT QUẢ XÁC THỰC CHỮ KÝ:")
        log_print(status.pretty_print_details())

        # === Thông tin người ký ===
        signer_cert = status.signing_cert
        if signer_cert:
            subj = signer_cert.subject.human_friendly
            log_print("\n📜 Thông tin người ký:")
            log_print(f"  Chủ thể (Subject): {subj}")

            sha1_fp = signer_cert.sha1_fingerprint.hex() if hasattr(signer_cert.sha1_fingerprint, 'hex') else signer_cert.sha1_fingerprint
            sha256_fp = signer_cert.sha256_fingerprint.hex() if hasattr(signer_cert.sha256_fingerprint, 'hex') else signer_cert.sha256_fingerprint
            log_print(f"  SHA1: {sha1_fp}")
            log_print(f"  SHA256: {sha256_fp}")
        else:
            log_print("⚠️ Không đọc được người ký.")

        # === Thời gian ký ===
        if status.signer_reported_dt:
            vn_tz = timezone(timedelta(hours=7))
            local_time = status.signer_reported_dt.astimezone(vn_tz)
            log_print(f"\n🕒 Thời gian ký: {local_time}")
        else:
            log_print("⚠️ Không có timestamp RFC3161.")

        # === Kiểm tra sửa đổi ===
        mod_level = getattr(status, "modification_level", None)
        if mod_level == ModificationLevel.NONE:
            log_print("✅ File chưa bị chỉnh sửa.")
        elif mod_level == ModificationLevel.FORM_FILLING:
            log_print("⚠️ File có thay đổi nhỏ sau khi ký.")
        else:
            log_print("❌ File đã bị chỉnh sửa sau khi ký!")

        log_print("====================================")

    # === Tổng kết ===
    if status.bottom_line:
        log_print("✅ Chữ ký hợp lệ và tài liệu còn nguyên vẹn!")
    else:
        log_print("❌ Chữ ký không hợp lệ hoặc file đã bị chỉnh sửa.")

except Exception as e:
    log_print("⚠️ LỖI TRONG QUÁ TRÌNH XÁC THỰC:")
    log_print(str(e))
    log_print(traceback.format_exc())

# === Lưu log ===
with open(LOG_FILE, "w", encoding="utf-8") as out:
    out.write(log.getvalue())

log_print(f"\n📄 Log đã được lưu tại: {LOG_FILE}")
