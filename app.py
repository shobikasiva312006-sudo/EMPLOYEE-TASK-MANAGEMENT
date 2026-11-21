from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

employees = {}
projects = {}
tasks = []
WORKFLOW = ["Analysis", "Design", "Coding", "Testing", "Deployment"]

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Task Manager</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial; background:#0f172a; color:white; padding:15px;}
.card{background:#1e293b; padding:20px; border-radius:15px; margin:12px 0;}
input,button{padding:10px; border-radius:8px; border:none; margin:5px;}
button{background:#38bdf8; font-weight:bold; cursor:pointer;}
.del{background:#ef4444; color:white; padding:5px 10px; font-size:12px;}
.task{padding:10px; background:#334155; border-radius:10px; margin:6px 0; display:flex; justify-content:space-between; align-items:center;}
.row{display:flex; justify-content:space-between; align-items:center; background:#334155; padding:8px; border-radius:8px; margin:4px 0;}
</style>
</head>
<body>
<h1>📱 Task Manager - With Delete</h1>

<div class="card">
<h3>Add Employee</h3>
<form method="post" action="/add_emp">
<input name="eid" placeholder="ID E101" required>
<input name="name" placeholder="Name" required>
<input name="role" placeholder="Role" required>
<button>Add</button>
</form>
</div>

<div class="card">
<h3>Add Project</h3>
<form method="post" action="/add_pro">
<input name="pid" placeholder="Project ID P1" required>
<input name="pname" placeholder="Project Name" required>
<button>Create</button>
</form>
</div>

<div class="card">
<h3>Assign / Finish Task</h3>
<form method="post" action="/assign">
<input name="eid" placeholder="Emp ID" required>
<input name="pid" placeholder="Project ID" required>
<button>Assign Task</button>
</form>
<form method="post" action="/finish">
<input name="eid" placeholder="Emp ID to Finish" required>
<button style="background:#22c55e">Finish & Auto Next Task</button>
</form>
</div>

<div class="card">
<h3>Employees</h3>
{% for id,e in employees.items() %}
<div class="row">
<span>{{id}} - {{e['name']}} ({{e['role']}}) | Completed: {{e['completed']}}</span>
<a href="/delete_emp/{{id}}"><button class="del">Delete</button></a>
</div>
{% endfor %}

<h3>Projects</h3>
{% for id,p in projects.items() %}
<div class="row">
<span>{{id}} - {{p['name']}} | Pending: {{p['pending']}}</span>
<a href="/delete_pro/{{id}}"><button class="del">Delete</button></a>
</div>
{% endfor %}

<h3>Live Tasks</h3>
{% for t in tasks %}
<div class="task">
<span>{{t['eid']}} -> {{t['task']}} ({{t['pid']}}) - {{t['status']}}</span>
<a href="/delete_task/{{loop.index0}}"><button class="del">X</button></a>
</div>
{% endfor %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, employees=employees, projects=projects, tasks=tasks)

@app.route("/add_emp", methods=["POST"])
def add_emp():
    employees[request.form['eid']] = {"name": request.form['name'], "role": request.form['role'], "completed": 0}
    return redirect("/")

@app.route("/add_pro", methods=["POST"])
def add_pro():
    projects[request.form['pid']] = {"name": request.form['pname'], "pending": WORKFLOW.copy()}
    return redirect("/")

@app.route("/assign", methods=["POST"])
def assign():
    eid = request.form['eid']; pid = request.form['pid']
    if pid in projects and projects[pid]["pending"]:
        tasks.append({"eid": eid, "pid": pid, "task": projects[pid]["pending"][0], "status": "Working"})
    return redirect("/")

@app.route("/finish", methods=["POST"])
def finish():
    eid = request.form['eid']
    for t in tasks:
        if t["eid"] == eid and t["status"] == "Working":
            t["status"] = "Done"
            employees[eid]["completed"] += 1
            pid = t["pid"]
            if projects[pid]["pending"]: projects[pid]["pending"].pop(0)
            if projects[pid]["pending"]:
                tasks.append({"eid": eid, "pid": pid, "task": projects[pid]["pending"][0], "status": "Working"})
            break
    return redirect("/")

# DELETE FUNCTIONS
@app.route("/delete_emp/<eid>")
def delete_emp(eid):
    if eid in employees: del employees[eid]
    return redirect("/")

@app.route("/delete_pro/<pid>")
def delete_pro(pid):
    if pid in projects: del projects[pid]
    return redirect("/")

@app.route("/delete_task/<int:index>")
def delete_task(index):
    if 0 <= index < len(tasks): tasks.pop(index)
    return redirect("/")

app.run(debug=True)




