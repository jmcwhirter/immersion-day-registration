from flask import Flask, render_template, flash, redirect
from forms import RegisterForm
import os
import boto3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('registrations')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = RegisterForm()

    if form.validate_on_submit():
        flash('Login requested for name {}, email {}'.format(
            form.name.data, form.email.data))
        table.put_item(
           Item={
                'name': form.name.data,
                'email': form.email.data
            }
        )
        return redirect('/')

    return render_template('register.html', title='Register', form=form)

if __name__ == "__main__":
    app.run(debug=True)
