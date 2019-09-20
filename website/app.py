from flask import Flask, render_template, flash, redirect
import flask_s3
from forms import RegisterForm
import os
import boto3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['FLASKS3_BUCKET_NAME'] = os.environ.get("BUCKET")
app.config['FLASKS3_FILEPATH_HEADERS'] = {
    r'.css$': {
        'Content-Type': 'text/css',
    }
}
s3 = flask_s3.FlaskS3(app)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('registrations')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = RegisterForm()

    if form.validate_on_submit():
        table.put_item(
           Item={
                'name': form.name.data,
                'email': form.email.data
            }
        )
        flash('Got it!')
        return redirect('/dev')

    return render_template('register.html', title='Register', form=form)

@app.route('/init', methods=['GET'])
def init():
    flask_s3.create_all(app)
    return redirect('/dev')

if __name__ == "__main__":
    app.run(debug=True)
