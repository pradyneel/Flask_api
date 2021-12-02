from users import *


#Task 1 : CRUD Operation for creating users

#route to get user info by id
@app.route('/users/<int:id>', methods=['GET'])
@check_for_token
def get_user_by_id(id):
    'Function to get users info from database'
    return_value = Users.GET(id)
    return jsonify(return_value)

#route to add new user
@app.route('/users', methods = ['POST'])
def add_user():
    request_data = request.get_json()#Getting data from client
    Users.POST(request_data["Name"], request_data["age"], request_data["city"], request_data["password"])
    response = Response("User added", 201, mimetype='application/json')
    return response

#route to Update User info
@app.route('/users/<int:id>', methods=['PUT'])
@check_for_token
def update_user_info(id):
    request_data = request.get_json()
    Users.PUT(id, request_data['Name'], request_data['age'], request_data['city'])
    response = Response("User info Updated", status = 200, mimetype = 'application/json')
    return response

#route to delete User by id
@app.route('/users/<int:id>', methods = ['DELETE'])
@check_for_token
def remove_user(id):
    Users.DELETE(id)
    response = Response("User Deleted", status = 200, mimetype='application/json')
    return response


#Task 2 : upload local files to server


#Files settings
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#route to upload file
@app.route('/file-upload', methods = ['POST'])
@check_for_token
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    
    file = request.files['file']

    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


if __name__ == "__main__":
    app.run(port=1234, debug = True)

