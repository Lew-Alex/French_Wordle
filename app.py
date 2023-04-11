from flask import Flask, render_template, request, jsonify
from words import is_french_word, ans
from random import randint
from time import time


app = Flask(__name__)

word = ans[randint(0, len(ans)-1)]
letters = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'], ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'], ['ENTRER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'DELETE']]


rows = [[[], [], False], [[], [], False], [[], [], False], [[], [], False], [[], [], False], [[], [], False]]

done = False
side_nav = False

start_time = 0
score = 0

def is_character(input):
    return isinstance(input, str) and len(input) == 1 and input.isalpha()
    

def check(index):
    global done
    global word
    global start_time
    global score
    row = rows[index][0]
    row_str = ''.join(row)


    if row_str == 'cleer':
        with open('scores.txt', 'w') as file:
            file.write('')

    if not is_french_word(row_str):
        return [False, jsonify([-1, index])]
        print("NOT A WORD")

    rows[index][2] = True

    l = [5]
    if row_str == word:
        score = int(time()-start_time)+(index+1)*15
        print("\n\n\n\n\n THIS IS A SCORE:"+str(score)+"\n\n\n\n\n\n")
        
        done = True
        for i in range(len(word)): 
            l.append(str(index)+str(i))
            l.append(word[i].upper())
            l.append('green')
        return [True, jsonify(l)]
    else:
        for i in range(len(row_str)):
            l.append(str(index)+str(i))
            l.append(row_str[i].upper())
            if row_str[i] == word[i]:
                l.append('green')
            elif row_str[i] in word and (row_str.count(row_str[i]) == word.count(row_str[i]) or row_str.index(row_str[i]) == i):
                l.append('f3c237')
            else:
                l.append('474747')
        return [False, jsonify(l)]
            



@app.route("/", methods=['GET', 'POST'])
def home():
    global rows
    global word
    global done
    global side_nav
    global start_time
    print(done)
    if request.method == 'POST' and done == False:
        post_id = request.form['id']

        keypress = request.form['keypress']
        count = 0
        for i in rows:
            if not i[2]:
                if is_character(keypress): 
                    if len(i[0]) < 5: i[0].append(str(keypress))
                    else: i[0][4] = str(keypress)

                    print(i[0])
                    return jsonify([1, str(min((count), 5))+str(len(i[0])-1), keypress.upper(), "121213"])
                elif keypress == 'backspace': 
                    if (len(i[0]) > 0): i[0].pop()
                    return jsonify([1, str(count)+str(len(i[0])), "", "121213"])
                elif keypress == 'enter': 
                    print(rows)
                    c = check(count)
                    if c[0]: done = True
                    return c[1]
                else: return jsonify(side_nav)
            count += 1
    elif request.method == 'GET':
        rows = [[[], [], False], [[], [], False], [[], [], False], [[], [], False], [[], [], False], [[], [], False]]
        word = ans[randint(0, len(ans)-1)]
        done = False
        start_time = time()
        print(f"START_TIME{start_time}")
        print("here")
        return render_template('index.html', letters=letters)
    else:
        return jsonify()

@app.route("/leader", methods=['GET', 'POST'])
def leader():
    index = request.form['index']
    print(index)

    with open('scores.txt', 'r') as file:
        content = file.readlines()

    scores = [line.strip().split(':') for line in content]
    scores.sort(key=lambda x: int(x[1]))

    print(scores[0])
    return jsonify(scores[int(index)])


@app.route("/addscore", methods=['GET', 'POST'])
def score():
    username = request.form['username']
    print(username)
    print("ADDING SCORE")
    with open('scores.txt', 'a') as file:
        file.write(username+":"+str(score)+"\n")

    return jsonify()





if __name__ == '__main__':
    app.run(debug=True)
'''

'''