from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import wordle_solver

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
wordle_db = SQLAlchemy(app)
ws = wordle_solver.wordle_solver()

class wordle(wordle_db.Model):
    id = wordle_db.Column(wordle_db.Integer, primary_key=True)
    str = wordle_db.Column(wordle_db.String(200), nullable=False)
    valid = wordle_db.Column(wordle_db.String(20), nullable=False)
    color = wordle_db.Column(wordle_db.String(20), nullable=False)
    date_created = wordle_db.Column(wordle_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<entry %r>' % self.id
    
def read_db():
    all = wordle.query.order_by(wordle.date_created).all()
    greens=[]; yellows=[]; used=[]
    for entry in all:
        if entry.color=='g': greens += [entry]
        elif entry.color=='y': yellows += [entry]
        elif entry.color=='u': used += [entry]
    return greens, yellows, used

def initialize_ws(greens, yellows, used):
    for g in greens:
        if g.valid=='true': ws.add_green(g.str)
    for y in yellows:
        if y.valid=='true': ws.add_yellow(y.str)
    for u in used: ws.add_used(u.str)

@app.route('/', methods=['POST', 'GET'])
def show_index_html():
    if request.method == 'POST':
        the_id = request.form['my_id']

        # check which form submitted
        # only incorporate valid responses into wordle solver
        if the_id=='g':
            green = request.form['green']
            if len(green)==5: valid='true'; ws.add_green(green)
            else: valid = 'false'
            new_green = wordle(str=green, valid=valid, color=the_id)
            if green=='': return redirect('/')

            try:
                wordle_db.session.add(new_green)
                wordle_db.session.commit()
                return redirect('/')
            except:
                return "there was an issue adding your green"
            
        elif the_id=='y':
            yellow = request.form['yellow']
            if len(yellow)==5: valid='true'; ws.add_yellow(yellow)
            else: valid = 'false'
            new_yellow = wordle(str=yellow, valid=valid, color=the_id)
            if yellow=='': return redirect('/')

            try:
                wordle_db.session.add(new_yellow)
                wordle_db.session.commit()
                return redirect('/')
            except:
                return "there was an issue adding your yellows"
            
        elif the_id=='u':
            use = request.form['use']
            ws.add_used(use)
            new_use = wordle(str=use, valid='true', color=the_id)
            if use=='': return redirect('/')

            try:
                wordle_db.session.add(new_use)
                wordle_db.session.commit()
                return redirect('/')
            except:
                return "there was an issue adding your used letters"
            
        elif the_id=='reset':
            all = wordle.query.order_by(wordle.date_created).all()
            for entry in all:

                try:
                    wordle_db.session.delete(entry)
                    wordle_db.session.commit()
                except:
                    return 'there was a problem deleting that entry'
                
            ws.reset()
            greens=[]; yellows=[]; used=[]
            possible = enumerate(ws.get_possible(), 1)
            return render_template('wordle-solver.html', greens=greens, yellows=yellows, used=used, possible=possible)

    else:
        greens, yellows, used = read_db()
        initialize_ws(greens, yellows, used)
        possible = enumerate(ws.get_possible(), 1)
        return render_template('wordle-solver.html', greens=greens, yellows=yellows, used=used, possible=possible)
    
@app.route('/delete/<int:id>')
def delete(id):
    
    # if a valid entry is being deleted, then reinitialize the wordle solver
    entry_to_delete = wordle.query.get_or_404(id)
    try:
        wordle_db.session.delete(entry_to_delete)
        wordle_db.session.commit()
        if entry_to_delete.valid=='true':
            ws.reset()
            greens, yellows, used = read_db()
            initialize_ws(greens, yellows, used)
        return redirect('/')
    except:
        return 'there was a problem deleting that entry'

if __name__ == '__main__':
    app.run(debug=True)
