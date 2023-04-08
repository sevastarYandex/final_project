from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
from flask_login import login_user, logout_user, login_required, LoginManager
import os
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_name = 'db/music_db.db.db'


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def init_data():
    if os.path.exists(db_name):
        os.remove(db_name)
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    people = [('Scott', 'Ridley', 21, 'captain', 'research engineer',
               'module_1', 'scott_chief@mars.org', '123', 'Washington'),
              ('Armstrong', 'Neil', 22, 'sailor', 'research engineer',
               'module_1', 'arm_neil@mars.org', '123', 'Wapakoneta, Ohio'),
              ('Gagarin', 'Yuri', 22, 'sailor', 'tester',
               'module_1', 'yura_mi_vse_p@mars.org', '123', 'Moskva'),
              ('Tito', 'Dennis', 20, 'sailor', 'tester',
               'module_2', 'tito_ti@mars.org', '123', 'New York')]
    for info in people:
        user = User()
        user.surname = info[0]
        user.name = info[1]
        user.age = info[2]
        user.position = info[3]
        user.speciality = info[4]
        user.address = info[5]
        user.email = info[6]
        user.set_password(info[7])
        user.city_from = info[8]
        db_sess.add(user)
    jobs = [(1, 'Deployment of residental modules 1 and 2', 15,
             '2, 3', None, False),
            (2, 'Exploration of mineral resources', 13,
             '1, 4', None, False),
            (3, 'Development of management system', 20,
             '2, 4', None, False)]
    for info in jobs:
        job = Jobs()
        job.team_leader = info[0]
        job.job = info[1]
        job.work_size = info[2]
        job.collaborators = info[3]
        if info[4] is None:
            job.start_date = datetime.datetime.now()
        else:
            job.start_date = info[4]
        job.is_finished = info[5]
        db_sess.add(job)
    departments = [('First', 1, '2, 3', 'first@mars.org'),
                   ('Second', 2, '1, 4', 'second@mars.org'),
                   ('Third', 3, '2, 4', 'third@mars.org')]
    for info in departments:
        dep = Department()
        dep.title = info[0]
        dep.chief = info[1]
        dep.members = info[2]
        dep.email = info[3]
        db_sess.add(dep)
    db_sess.commit()


def main():
    init_data()
    api = Api(app)
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:jobs_id>')
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


def set_pict(place):
    req = f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-' \
              f'98533de7710b&geocode={place}, 1&format=json'
    resp = requests.get(req)
    if not resp:
        return '...'
    js = resp.json()
    top = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    pos = top['Point']['pos'].replace(' ', '%2C')
    req = f"https://static-maps.yandex.ru/1.x/?ll={pos}&l=sat&z=12&size=600,450"
    resp = requests.get(req)
    if not resp:
        return '...'
    with open(DONT, 'wb') as wfile:
        wfile.write(resp.content)


@app.route('/users_show/<int:user_id>')
def show(user_id):
    user = mpt(f'/api/users/{user_id}', requests.get, if_p=False)['user']
    name = user['name'] + ' ' + user['surname']
    town = user['city_from']
    set_pict(town)
    return render_template('show.html', title='Hometown', name=name, town=town)


@app.route('/')
@app.route('/index')
def jobs():
    db_sess = db_session.create_session()
    data = []
    for job in db_sess.query(Jobs).all():
        job_id = str(job.id)
        title = job.job
        lead_id = job.team_leader
        lead = db_sess.query(User).filter(User.id == lead_id).first()
        lead_str = f'{lead.surname} {lead.name}'
        dur_int = job.work_size
        dur_str = f'{dur_int} hours'
        if dur_int == 1:
            dur_str = dur_str[:-1]
        collab = job.collaborators
        if job.is_finished:
            finished = 'Yes'
        else:
            finished = 'No'
        data.append((title, lead_str, dur_str, collab, finished, job_id))
    return render_template('index.html', title='Works log', data=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    logout_user()
    title = 'Register form'
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title=title,
                                   form=form,
                                   message="Passwords are not equal")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title=title,
                                   form=form,
                                   message='This email is already busy')
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.modified_date = datetime.datetime.now()
        if user.age < 0:
            return render_template('register.html', title=title,
                                   form=form,
                                   message='Age must be non-negative')
        if db_sess.query(User).filter(User.hashed_password == user.hashed_password).first():
            return render_template('register.html', title=title,
                                   form=form,
                                   message='This password is already used')
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message='Wrong login or password',
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.leader.data
        job.collaborators = form.collaborators.data
        job.work_size = form.work_size.data
        job.is_finished = form.is_finished.data
        job.start_date = datetime.datetime.now()
        leader = db_sess.query(User).filter(User.id == form.leader.data).first()
        if not leader:
            return render_template('add_job.html', title='Add job', form=form,
                                   message='Wrong team leader id')
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Add job', form=form)


if __name__ == '__main__':
    main()
