from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods = ['GET'])
def show_index_html():
    return render_template('wordle-solver.html')

@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
        pay = request.form['pay']
        print ("Pay is " + pay)
        return "Data sent. Please check your program log"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)