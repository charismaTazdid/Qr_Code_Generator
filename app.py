from flask import Flask, request, make_response, render_template_string
import qrcode
import io
import os

app = Flask(__name__)


@app.route('/qrcode', methods=['GET'])
def generate_qrcode():
    # get the URL string from the query parameter
    url = request.args.get('url')

    # generate the QR code image
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # create a byte stream to save the image
    img_bytes = io.BytesIO()
    img.save(img_bytes, 'PNG')
    img_bytes.seek(0)

    # extract the filename from the URL
    filename = os.path.basename(url) + '.png'

    # create a response object with the HTML page and headers
    html = f'<html><body><h1>Download QR code for {url}</h1><p>Click <a href="/download?url={url}">here</a> to download the QR code image.</p></body></html>'
    response = make_response(render_template_string(html))
    response.headers['Content-Type'] = 'text/html'

    return response


@app.route('/download', methods=['GET'])
def download_qrcode():
    # get the URL string from the query parameter
    url = request.args.get('url')

    # generate the QR code image
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # create a byte stream to save the image
    img_bytes = io.BytesIO()
    img.save(img_bytes, 'PNG')
    img_bytes.seek(0)

    # extract the filename from the URL
    filename = os.path.basename(url) + '.png'

    # create a response object with the image data and headers
    response = make_response(img_bytes.read())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


if __name__ == '__main__':
    app.run(debug=True)
