import json

import flask, csv
import numpy
from flask import render_template, request

app = flask.Flask(__name__)


def read_csv(file):
    readfile_csv = csv.reader(open(file))
    ll = list(readfile_csv)[1:]
    if len(ll) > 10:
        list_num = list(numpy.sort(numpy.random.choice(len(ll), size=10, replace=False)))
        questions_list = []
        for i in list_num:
            questions_list.append(ll[i])
        ll = questions_list

    return ll


@app.route('/jug/<exam_type>/<name>', methods=['POST'])
def jug(exam_type, name):

    readfile_csv = list(csv.reader(open(f"./static/{exam_type}.csv")))
    file_standard_answer = []
    for i in readfile_csv:
        file_standard_answer.append((i[0], list(i[-1].replace(" ", ""))))
    answer = list(request.form.lists())

    standard_answer = []
    for i in answer:
        standard_answer.append((int(i[0][6:]), i[1]))

    print(file_standard_answer)
    print(standard_answer)

    score = 0
    for i in standard_answer:
        if file_standard_answer[i[0]][1] == i[1]:
            if readfile_csv[i[0]][1] == "多选题":
                score += 5
            else:
                score += 2

    return name+": "+str(score)


@app.route('/exam')
def exam():
    name = request.args.get("name")
    exam_type = request.args.get("exam_type")
    list = read_csv(f"./static/{exam_type}.csv")

    return render_template("exam.html", list=list, exam_type=exam_type, name=name)


@app.route("/")
def index():
    """

    :return:
    :rtype:
    """
    # read_csv("./static/pythonn.csv")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8077, debug=True)
