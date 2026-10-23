"""Create static, print-quality QR assets. Requires Pillow, qrcode and zxing-cpp.

All codes link directly to the business website, without a QR redirect service.
"""
from pathlib import Path
import base64
from io import BytesIO
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont
import zxingcpp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/qr'
OUT.mkdir(parents=True, exist_ok=True)
URL = 'https://bennystreeservices.com/'
BOX = 40
GREEN = '#183b27'
qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=BOX, border=4)
qr.add_data(URL)
qr.make(fit=True)
matrix = qr.get_matrix()
size = len(matrix)
logo = Image.open(ROOT / 'assets/originals/logo.png').convert('RGB')
logo_width = 7 * BOX
plate_width = 9 * BOX
logo = logo.resize((logo_width, logo_width), Image.Resampling.LANCZOS)
logo_buffer = BytesIO()
logo.save(logo_buffer, format='PNG')
encoded_logo = base64.b64encode(logo_buffer.getvalue()).decode()


def save_qr(branded):
    name = 'bennys-website-qr' if branded else 'bennys-website-qr-plain'
    color = GREEN if branded else '#000000'
    canvas = Image.new('RGB', (size * BOX, size * BOX), 'white')
    draw = ImageDraw.Draw(canvas)
    paths = []
    for y, row in enumerate(matrix):
        for x, dark in enumerate(row):
            if dark:
                draw.rectangle((x * BOX, y * BOX, (x + 1) * BOX - 1, (y + 1) * BOX - 1), fill=color)
                paths.append(f'M{x} {y}h1v1h-1z')
    overlay = ''
    if branded:
        start = (canvas.width - plate_width) // 2
        draw.rectangle((start, start, start + plate_width - 1, start + plate_width - 1), fill='white')
        logo_start = (canvas.width - logo_width) // 2
        canvas.paste(logo, (logo_start, logo_start))
        p = (size - 9) / 2
        l = (size - 7) / 2
        overlay = f'<rect x="{p}" y="{p}" width="9" height="9" fill="white"/><image x="{l}" y="{l}" width="7" height="7" href="data:image/png;base64,{encoded_logo}"/>'
    canvas.save(OUT / f'{name}.png', dpi=(300, 300), optimize=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size * BOX}" height="{size * BOX}" viewBox="0 0 {size} {size}" role="img" aria-labelledby="title desc"><title id="title">Benny’s Tree Service website QR code</title><desc id="desc">Scan to open {URL}</desc><rect width="{size}" height="{size}" fill="white"/><path d="{''.join(paths)}" fill="{color}" shape-rendering="crispEdges"/>{overlay}</svg>'''
    (OUT / f'{name}.svg').write_text(svg, encoding='utf-8')
    return canvas


branded = save_qr(True)
plain = save_qr(False)
card = Image.new('RGB', (1800, branded.height + 650), 'white')
draw = ImageDraw.Draw(card)
bold = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 78)
regular = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 44)
small = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 36)

def center(text, y, font, fill):
    draw.text((card.width / 2, y), text, font=font, fill=fill, anchor='mt')

center('Benny’s Tree Service', 75, bold, GREEN)
center('Scan to visit our website', 195, regular, '#425348')
card.paste(branded, ((card.width - branded.width) // 2, 280))
y = 280 + branded.height
center('bennystreeservices.com', y + 30, regular, GREEN)
center('Free estimates  |  Call or text (708) 296-8946', y + 105, small, '#425348')
card.save(OUT / 'bennys-website-qr-print-card.png', dpi=(300, 300), optimize=True)

# Decode the final branded images, not just the underlying unobstructed QR.
checks = 0
for name, image in [('branded', branded), ('plain', plain), ('print card', card)]:
    for width in ([image.width, 800, 400, 280] if name != 'print card' else [image.width, 900, 600]):
        resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
        results = zxingcpp.read_barcodes(resized)
        assert any(result.text == URL for result in results), f'Failed scan: {name} at {width}px'
        checks += 1
    jpeg = BytesIO()
    image.resize((600, round(image.height * 600 / image.width)), Image.Resampling.LANCZOS).save(jpeg, 'JPEG', quality=80)
    jpeg.seek(0)
    assert any(result.text == URL for result in zxingcpp.read_barcodes(Image.open(jpeg))), f'Failed compressed scan: {name}'
    checks += 1
print(f'PASS: {checks} scan checks, including the logo, reduced sizes and JPEG compression. Target: {URL}')
print(f'QR size: {branded.width} x {branded.height}. Print card: {card.width} x {card.height}.')
