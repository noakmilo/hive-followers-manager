from flask import Flask, render_template, request, redirect
from pick import pick
from beem import Hive
from beem.account import Account
from beem.exceptions import AccountDoesNotExistsException
from flask_bootstrap import Bootstrap
from builtins import max


def get_min_value(a, b):
    return min(a, b)

app = Flask(__name__)
hive = Hive()
bootstrap = Bootstrap(app)

def custom_max(*args):
    return max(args)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    account_name = request.form['account'].strip().lower()
    if account_name.startswith('@'):
        account_name = account_name[1:]
    limit = 1000000000  # Se establece un límite inicial de 100 resultados por página

    try:
        account = Account(account_name, blockchain_instance=hive)
    except Exception:
        return redirect('/')

    followers = account.get_followers()
    following = account.get_following()

    followers_set = set(followers)
    following_set = set(following)

    follows_followed_by = list(following_set - followers_set)
    follows_not_followed_by = list(followers_set - following_set)

    total_followers = len(followers)
    total_following = len(following)

    page = int(request.args.get('page', 1))
    start = (page - 1) * limit
    end = start + limit
    followers_page = followers[start:end]
    following_page = following[start:end]

    if len(followers_page) == 0:
        return render_template('index.html', message="No followers information available.")

    if len(following_page) == 0:
        return render_template('index.html', message="No following information available.")

    total_pages = total_followers // limit
    if total_followers % limit != 0:
        total_pages += 1

    return render_template('index.html', followers=followers, following=following,
                           follows_followed_by=follows_not_followed_by, follows_not_followed_by=follows_followed_by,
                           total_pages=total_pages, current_page=page, max=max, account_name=account_name,
                           total_followers=total_followers, total_following=total_following)

if __name__ == '__main__':
    app.run(debug=True)
