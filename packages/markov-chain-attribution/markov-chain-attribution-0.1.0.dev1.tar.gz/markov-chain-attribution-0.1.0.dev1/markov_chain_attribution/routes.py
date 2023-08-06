import os

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from LoginForm import User, Login
from MarkovChainBigQuery import MarkovChainBQ
from MarkovChainGoogleAnalytics import MarkovChainGA
from __init__ import app, update_folder

MARKOV_CHAIN = None


###### Base Path #####
@app.route('/')
def index():
    if (current_user.is_authenticated):
        return redirect(url_for("BQ_INIT"))
    form = Login()
    flash("Logging In")
    return render_template('index.html', form=form, title="Log In")


@app.route("/", methods=['POST'])
def login_func():
    form = Login(request.form)
    if (form.validate()):
        user = form.username.data
        pwd = form.password.data
        if (user == "admin" and pwd == "admin"):
            login_user(User('ffab050d330ffee6eb4647df96e8ef29786a90cd'))
            return redirect(url_for('BQ_INIT'))
        else:
            return redirect(url_for('index'))


@app.route('/logout')
def logout_func():
    logout_user()
    os.system('rm data.csv')
    return redirect(url_for('index'))


@app.route('/GA/')
def GA_INIT():
    global MARKOV_CHAIN
    if (not current_user.is_authenticated):
        flash("Login Required!!")
        return redirect(url_for('index'))
    print("Hello")
    update_folder()
    MARKOV_CHAIN = MarkovChainGA(app.config['UPLOAD_FOLDER'])
    return render_template('homepage.html', title="Markov Chain for Google Ananlytics")


@app.route('/BQ/')
def BQ_INIT():
    global MARKOV_CHAIN

    if (not current_user.is_authenticated):
        flash("Login Required!!")
        return redirect(url_for('index'))
    print("BQ_INIT")
    update_folder()
    MARKOV_CHAIN = MarkovChainBQ(app.config['UPLOAD_FOLDER'])
    return render_template('homepage.html', title="Markov Chain for Big Query")


@app.route('/GA/', methods=['POST'])
def save_data_ga():
    if (not current_user.is_authenticated):
        flash("Login Required!!")
        return redirect(url_for('index'))

    if ('flup' in request.files):
        for f in request.files.getlist('flup'):
            filepath = 'data.csv'
            f.save(filepath)
        errors = init_markov()
        if (errors != None):
            flash(errors)
            return redirect(url_for('GA_INIT'))
    return redirect(url_for('table_init'))


@app.route('/BQ/', methods=['POST'])
def save_data_bq():
    if (not current_user.is_authenticated):
        flash("Login Required!!")
        return redirect(url_for('index'))

    if ('flup' in request.files):
        for f in request.files.getlist('flup'):
            filepath = 'data.csv'
            f.save(filepath)
        errors = init_markov()
        if (errors != None):
            flash(errors)
            return redirect(url_for('BQ_INIT'))
    return redirect(url_for('table_init'))


@app.route('/table')
def table_init():
    if (not current_user.is_authenticated):
        flash("Login Required!!")
        return redirect(url_for('index'))

    return redirect(url_for('gen_table', value="conversion_sum"))


@app.route('/table/<value>')
def gen_table(value):
    if (not current_user.is_authenticated):
        flash("Login Required!!")
        return redirect(url_for('index'))
    params = table_data(value)
    return render_template('table.html', title=params['title'],
                           rows=params['rows'],
                           columns=params['columns'])


## Operation On Table
def table_data(button):
    global MARKOV_CHAIN
    # button = request.form['button']
    param = {}  ## Parameter Dictionary

    if (button == "conversion_sum" and hasattr(MARKOV_CHAIN, 'conversion_summary')):
        param['title'] = "Conversion Summary"
        param['columns'] = MARKOV_CHAIN.conversion_summary.columns.str.replace('_', ' ').str.capitalize()
        param['rows'] = zip(MARKOV_CHAIN.conversion_summary.index, MARKOV_CHAIN.conversion_summary.values)

    elif (button == "conversion_sum"):
        param['title'] = "Conversion Summary"
        param['columns'] = MARKOV_CHAIN.conversion_paths.columns.str.replace('_', ' ').str.capitalize()
        param['rows'] = zip(MARKOV_CHAIN.conversion_paths.index, MARKOV_CHAIN.conversion_paths.values)

    elif (button == 'removal_effect'):
        param['title'] = "Removal Effect"
        param['columns'] = MARKOV_CHAIN.removal_effect_matrix.columns.str.replace('_', ' ').str.capitalize()
        param['rows'] = zip(MARKOV_CHAIN.removal_effect_matrix.index, MARKOV_CHAIN.removal_effect_matrix.values)

    elif (button == 'first_touch'):
        param['title'] = "First Touch Conversion"
        param['columns'] = MARKOV_CHAIN.first_touch_conversion_attribution.columns.str.replace('_',
                                                                                               ' ').str.capitalize()
        param['rows'] = zip(MARKOV_CHAIN.first_touch_conversion_attribution.index,
                            MARKOV_CHAIN.first_touch_conversion_attribution.values)

    elif (button == 'last_touch'):
        param['title'] = "Last Touch Conversion"
        param['columns'] = MARKOV_CHAIN.last_touch_conversion_attribution.columns.str.replace('_', ' ').str.capitalize()
        param['rows'] = zip(MARKOV_CHAIN.last_touch_conversion_attribution.index,
                            MARKOV_CHAIN.last_touch_conversion_attribution.values)

    return param


## Markov Chain Initalization
@app.route('/init_markov')
def init_markov():
    global MARKOV_CHAIN
    flash("Reading Data File")
    try:
        MARKOV_CHAIN.read_file()
        MARKOV_CHAIN.transition_matrix()
        MARKOV_CHAIN.removal_effect()
        MARKOV_CHAIN.touch_conversion()
    except Exception as e:
        # return jsonify(result = "File Does not support!! Please try with different file")
        print(e)
