from flask import Flask, render_template, request
import service

service.init()

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    term = ["大一上學期", "大一下學期", "大二上學期"]
    term_subject = [
        ["計算機概論", "微積分(一)", "電路學(一)", "邏輯設計"],
        ["微積分(二)", "電路學(二)", "電機機械(一)", "計算機程式設計"],
        ["資料結構", "電子學(一)", "電子學實習(一)", "電機機械實習"]
    ]

    subject = {}
    for index, element in enumerate(term):
        buffer = {}
        for sub in term_subject[index]:
            buffer[sub] = sub
        subject[element] = buffer

    return render_template('index.html', **locals())


@app.route('/result', methods=['POST'])
def result():
    data = request.values.to_dict()
    person_grade, pred_a, pred_b, pred_c = service.predict(data)
    return render_template('result.html', **locals())


MODE = 'deployment'

if __name__ == "__main__":
    if MODE == 'development':
        app.run(host='0.0.0.0', port=8080, debug=True)
    elif MODE == 'deployment':
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
