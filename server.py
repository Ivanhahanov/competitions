from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from flask.views import MethodView, View
from bson.objectid import ObjectId
from flags import Flag
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Competitions"
app.secret_key = 'ODM4YmE0NjQ3OWNiNDc2M2U0ZDYz'
mongo = PyMongo(app)

@app.route('/')
def index():
    tasks = mongo.db.tasks.find({})
    print(tasks)
    return render_template('tasks.html', tasks=tasks)

class Teams(View):
    template_name = 'teams.html'
    def dispatch_request(self):
        teams = []
        points = 0
        for team in mongo.db.teams.find():
            for task in team['compleat_tasks']:
                points += int(mongo.db.tasks.find({'_id': ObjectId(task)})[0]['points'])
            teams.append({'team_name':team['team_name'], 'points': points})
        print(points)
        return render_template(self.template_name, teams=teams)


class Tasks(MethodView):

    template_name = 'tasks.html'

    def get(self, task_id):
        if task_id is None:
            tasks = mongo.db.tasks.find({})
            print(tasks)
            return render_template(self.template_name, tasks=tasks)
        else:
            task = mongo.db.tasks.find({'_id': ObjectId(task_id)})
            return render_template('task_check.html', task=task[0])

    def post(self, task_id):
        session['team_id'] = '5d2365ad056233fd947669ee'
        flag = request.form['flag']
        task = mongo.db.tasks.find({'_id': ObjectId(task_id)})[0]
        right_flag = mongo.db.tasks.find({'_id': ObjectId(task_id)})[0]['flag']
        if flag == right_flag:
            print(flag)
            mongo.db.teams.update({'_id':ObjectId(session['team_id'])}, {'$push': {'compleat_tasks': task_id}})
            return render_template('task_check.html',task=task, answer=True)
        else:
            return render_template('task_check.html', task=task, answer=False)


class Add_Task(MethodView):

    template_name = 'create_tasks.html'

    def get(self):
        return render_template(self.template_name)


    def post(self):
        task={}
        task['task_name'] = request.form['task_name']
        task['task_description'] = request.form['task_description']
        task['points'] = request.form['points']
        task['flag'] = Flag().create_flag()
        task['task_id'] = mongo.db.tasks.find().count() + 1
        print(task)
        mongo.db.tasks.insert(task)
        return redirect(url_for('tasks'))

app.add_url_rule('/teams/', view_func=Teams.as_view('show_teams') )
task_view = Tasks.as_view('tasks')
app.add_url_rule('/tasks/',defaults={'task_id':None}, view_func=Tasks.as_view('tasks'), methods=['GET'])
app.add_url_rule('/tasks/<string:task_id>', view_func=Tasks.as_view('show_tasks'), methods=['GET','POST'])
app.add_url_rule('/add_task/', view_func=Add_Task.as_view('new_task'), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
