from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Initialize OAuth
oauth = OAuth(app)

# Configure OAuth providers
google = oauth.register(
    name='google',
    client_id='your_google_client_id',
    client_secret='your_google_client_secret',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/auth/google/callback',
    client_kwargs={'scope': 'openid profile email'}
)

facebook = oauth.register(
    name='facebook',
    client_id='your_facebook_client_id',
    client_secret='your_facebook_client_secret',
    authorize_url='https://www.facebook.com/dialog/oauth',
    authorize_params=None,
    access_token_url='https://graph.facebook.com/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/auth/facebook/callback',
    client_kwargs={'scope': 'email'}
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('auth_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/login/facebook')
def login_facebook():
    redirect_uri = url_for('auth_facebook', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def auth_google():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user
    return redirect(url_for('profile'))

@app.route('/auth/facebook/callback')
def auth_facebook():
    token = oauth.facebook.authorize_access_token()
    user = oauth.facebook.parse_id_token(token)
    session['user'] = user
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
