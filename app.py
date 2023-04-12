from flask import Flask, render_template, request, jsonify
from time import time


app = Flask(__name__)

start_time = 0
end_time = 0

@app.route("/", methods=['GET', 'POST'])
def home():
    global start_time
    start_time = time()
    return render_template('index.html')

@app.route("/leader", methods=['GET', 'POST'])
def leader():
    index = request.form['index']

    with open('scores.txt', 'r') as file:
        content = file.readlines()

    scores = [line.strip().split(':') for line in content]
    scores.sort(key=lambda x: int(x[1]))

    return jsonify(scores[int(index)])

@app.route("/endtime", methods=['GET', 'POST'])
def endtime():
    global end_time
    end_time = time()

    return jsonify()

@app.route("/addscore", methods=['GET', 'POST'])
def score():
    global end_time
    global start_time
    username = request.form['username']
    guesses = request.form['guesses']
    print(username)
    print("ADDING SCORE")
    print(start_time)
    score = int(end_time-start_time)+int(guesses)*15
    with open('scores.txt', 'a') as file:
        print("SCORE ADDED")
        file.write(username+":"+str(score)+"\n")

    return jsonify()




@app.route("/cleer", methods=['GET', 'POST'])
def cleer():
    with open('scores.txt', 'w') as file:
            file.write('person1:100\nperson2:100\nperson3:100\nperson4:100\nperson5:100\n')
    return jsonify()


if __name__ == '__main__':
    app.run(debug=True)
'''

'''