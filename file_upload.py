import os
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'secret'

BASE_PATH = os.path.abspath(os.environ.get('HOME'))
ALLOWED_EXTENSIONS = {'mp4'}


def file_is_allowed(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part.')
            return redirect(request.url)

        file = request.files.get('file')

        if file.filename == '':
            flash("No file was selected.")
            return redirect(request.url)

        if file and file_is_allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(BASE_PATH, '\Desktop\WhereToUploadTo', filename))
            flash("File uploaded successfully.")
            return redirect(url_for('download'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
