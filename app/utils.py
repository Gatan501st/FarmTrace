import qrcode, os
from uuid import uuid4
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/qrcodes/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def generate_qr(data, filename):
    file_path = os.path.join(f'app/{UPLOAD_FOLDER}', filename)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(file_path)
    return file_path
