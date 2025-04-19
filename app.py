from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

approved_voters = {
    "ID001": "Alice",
    "ID002": "Bob",
    "ID003": "Charlie",
    "ID004": "David"
}

voted_voters = set()
candidates = {
    "Candidate A": 0,
    "Candidate B": 0,
    "Candidate C": 0
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        if voter_id in voted_voters:
            return render_template('index.html', error="You have already voted.")
        elif voter_id in approved_voters:
            session['voter_id'] = voter_id
            return redirect(url_for('vote'))
        else:
            return render_template('index.html', error="Invalid Voter ID.")
    return render_template('index.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    voter_id = session.get('voter_id')
    if not voter_id or voter_id in voted_voters:
        return redirect(url_for('index'))

    if request.method == 'POST':
        choice = request.form['candidate']
        if choice in candidates:
            candidates[choice] += 1
            voted_voters.add(voter_id)
            session.pop('voter_id', None)
            return render_template('vote.html', success="Your vote has been cast.")
        else:
            return render_template('vote.html', error="Invalid candidate.")
    
    return render_template('vote.html', candidates=candidates)

@app.route('/results')
def results():
    return render_template('results.html', candidates=candidates)

if __name__ == "__main__":
    app.run(debug=True)
