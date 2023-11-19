import os.path
import pandas as pd
from flask import Flask, render_template, redirect, request, url_for, make_response

app = Flask(__name__, template_folder="templates")

polls_df = pd.read_csv("poll_test.csv")



@app.route("/")
def index():
    df = pd.read_csv('poll_test.csv')
    df.drop(columns=['Unnamed: 0'],axis=1, inplace=True)
    polls_df2 = df.groupby('poll_id').max().reset_index()
    return render_template("index.html", polls=polls_df2) 




@app.route("/polls/<id>")
def polls(id):
    polls_df = pd.read_csv("poll_test.csv")
    poll = polls_df[polls_df['poll_id']==int(id)]
    return render_template("show_poll.html", poll=poll)




@app.route("/options", methods=["GET","POST"])
def options():
    if request.method == "GET":
        return render_template("options.html")
    elif request.method == "POST":
        global no_of_options
        no_of_options = request.form['Number']
        no_of_options = int(no_of_options)
        return redirect(url_for("create_polls"))



@app.route("/polls", methods=["GET","POST"])
def create_polls():
    if request.method == "GET":
        no_of_options_above = no_of_options
        return render_template("new_poll.html", no_of_options= no_of_options_above)
    elif request.method == "POST":
        poll = request.form['Poll']
        options_dict = {}
        for i in range(1,no_of_options+1):
            options_dict[i] = request.form.get(f'option{i}', '')
        print(options_dict)
        df = pd.DataFrame(options_dict, index=['Values']).transpose().reset_index()
        df.columns = ['poll_option_no', 'poll_option']
        df['poll_name'] = poll
        df['poll_vote'] = 0
        max_df = pd.read_csv('poll_test.csv')
        try:
            df['poll_id'] = max(max_df['poll_id']) + 1
        except:
            df['poll_id'] = 1
        df = df[['poll_id','poll_name','poll_option_no', 'poll_option','poll_vote']]
        df.to_csv('poll_test.csv', mode='a', header=False)
        return redirect(url_for("index"))




@app.route("/vote/<id>/<option>")
def vote(id, option):
    # if request.cookies.get(f"vote_{id}_cookie") is None:
        polls_df = pd.read_csv("poll_test.csv")
        polls_df.loc[(polls_df['poll_id'] == int(id)) & (polls_df['poll_option_no'] == int(option)), 'poll_vote'] += 1
        polls_df.to_csv("poll_test.csv")
        return redirect(url_for("polls", id=id))
        # response = make_response(redirect(url_for("polls", id=id)))
        # response.set_cookie(f"vote_{id}_cookie", str(option))
        # return response
    # else:
        # return render_template("repeat.html")



@app.route("/clean")
def clean():
    columns = ['poll_id', 'poll_name', 'poll_option_no', 'poll_option', 'poll_vote']
    df = pd.DataFrame(columns=columns)
    df.to_csv('poll_test.csv')
    return render_template('clean.html')


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)