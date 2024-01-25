from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/task2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    status = db.Column(db.Boolean, default=False)


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = not task.status
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        new_title = request.form.get('new_title')
        if new_title:
            task.title = new_title
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit.html', task=task)


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
