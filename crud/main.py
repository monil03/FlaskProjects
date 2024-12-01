from flask import Flask, render_template, url_for, redirect, request
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/') 
db = client['database_name'] #Enter your database name
collection = db['collection_name'] #Enter your collection name

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/post/')
def register():
	return render_template('adddata.html')

@app.route('/postdata/', methods=['POST'])
def post():
	user_data = {'name':request.form['name'], 'phone':request.form['phone'],'address':request.form['address']}
	result = collection.insert_one(user_data)
	if result.inserted_id:
		return render_template('success.html', message="Document inserted successfully.")
	else:
		return render_template('error.html', message="Failed to insert document.")

@app.route('/get/')
def get():
	fname = request.args.get('fname')
	find_data = collection.find({"name":fname})

	if collection.count_documents({"name": fname}) > 0:
		return render_template('getdata.html', data=find_data)
	else:
		return render_template('error.html', message="No data found for the given name.")

@app.route('/delete/')
def delete():
	dname = request.args.get('dname')
	query_filter = { "name": dname }
	result = collection.delete_one(query_filter)
	
	if result.deleted_count > 0:
		return render_template('success.html', message="Document deleted successfully.")
	else:
		return render_template('error.html', message="No document found to delete.")

	
	

@app.route('/update/')
def update():
	uname = request.args.get('uname')
	find_data = collection.find({"name":uname})
	if collection.count_documents({"name": uname}) == 0:
    # No document matched the filter
		return render_template('error.html', message="No document found to update.")
    
	return render_template('updatedata.html', data=find_data)

@app.route('/updatedata/', methods=['POST'])
def updatedata():
	uname = request.form.get('uname')

	phone = request.form.get('phone')
	address = request.form.get('address')

	query_filter = {'name' : uname}
	update_operation = { '$set' : 
		{ 'phone' : phone, 'address':address}
	}
	
	result = collection.update_one(query_filter, update_operation)

	if result.matched_count == 0:
	# No document matched the filter
		return render_template('error.html', message="No document found to update.")
	return render_template('success.html')



if __name__ == '__main__':
    app.run(debug=True)
	
	
