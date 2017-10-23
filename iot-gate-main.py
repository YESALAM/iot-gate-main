from flask import Flask


from flask import flash
from flask import render_template
from flask import request
from wtforms import Form, TextField
from wtforms import validators

from time import sleep


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    vrn = TextField('Vrn:', validators=[validators.required(), validators.Length(min=6, max=35)])
    nop = TextField('Nop:', validators=[validators.required(), validators.Length(min=3, max=35)])
    purpose = TextField('Purpose:', validators=[validators.required(), validators.Length(min=6, max=35)])
    access = TextField('Access:', validators=[validators.required(), validators.Length(min=3, max=35)])


@app.route('/',methods=['GET','POST'])
def hello_world():
    form = ReusableForm(request.form)

    print
    form.errors
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['vrn']
        email = request.form['nop']
        print
        name, " ", email, " ", password

        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('hello.html', form=form)

@app.route('/readtag',methods=['GET'])
def readTag():
    sleep(20)
    return '{result:"verygood"}'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
