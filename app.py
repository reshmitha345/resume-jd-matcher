from flask import Flask, render_template, request
import os
from matcher import extract_text_from_pdf, get_match_score, get_keyword_gap

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    resume_file = request.files['resume']
    jd_text = request.form['jd']

    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    resume_file.save(resume_path)

    resume_text = extract_text_from_pdf(resume_path)
    score = get_match_score(resume_text, jd_text)
    missing_keywords = get_keyword_gap(resume_text, jd_text)

    return render_template('index.html',
                           score=score,
                           missing=missing_keywords,
                           show_result=True)

if __name__ == '__main__':
    app.run(debug=True, port=3000)