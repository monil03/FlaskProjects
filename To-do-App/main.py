from flask import Flask,render_template,request


app=Flask(__name__)
to_do=[]

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/add",methods=['POST'])
def add():
    task_name=request.form.get('task')
    to_do.append({'Task':task_name,'Done':False})
    print(to_do)
    return render_template('index.html')

@app.route("/get",methods=['get'])
def view():
    print(to_do)
    return render_template('index.html', data=to_do)
    
@app.route("/update/<int:id>",methods=['get','post'])
def update(id):
    temp = to_do[id]
    if request.method=="POST":
        update_task=request.form['utask']
        temp['Task']=update_task 
        return render_template('index.html', data=to_do)
    
    else:
        return render_template('update.html', data=to_do,index=id)

    
@app.route("/delete/<int:id>",methods=['get','post'])
def delete(id):
    to_do.pop(id)
    return render_template('index.html', data=to_do)

    
@app.route("/check/<int:id>")
def check(id):
    to_do[id]['Done']=True
    return render_template('index.html', data=to_do)

    



app.run(debug=True)

