from flask import Flask, make_response, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = b'the_key_that_is_secret'
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.route('/hello/', methods=['GET', 'POST'])
@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name=None):
    timeOfDay = request.args.get('tod', '')
    if request.method == 'POST':
        thisdict = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964
        }        
        return thisdict
    else:
        resp = make_response(render_template('hello.html', name=name, timeOfDay=timeOfDay ))
        resp.headers['X-Something'] = 'A value'
    return resp

@app.route('/debug')
def debug():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return "debug"

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'