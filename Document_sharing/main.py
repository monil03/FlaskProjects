from flask import Flask, render_template, request, jsonify
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError


app = Flask(__name__)
s3 = boto3.client('s3',aws_access_key_id='your-key',
    aws_secret_access_key='your-secret-key',
    region_name='your-region'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file = request.files['up_file']  # Get the file from the request

        s3.upload_fileobj(file, 'your-bucket-name', file.filename)
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'your-bucket-name',
                                                            'Key': 'your-filename'},
                                                    ExpiresIn=100)
        return response
        

if __name__ == '__main__':
    app.run(debug=True)
