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

    print form.errors
    if request.method == 'POST':
        name = request.form['name']
        vrn = request.form['vrn']
        nop = request.form['nop']
        purpose = request.form['purpose']
        access = request.form['access']
        uuid = request.form['token_id_button']

        #validation of POST data
        valid = 1
        try:
            inop = int(nop)
        except ValueError:
            flash('Please corrent the No of People field')
            valid = 0

        try:
            iaccess = int(access)
        except ValueError:
            flash('Please select a correct option to required area')
            valid = 0


        if valid == 1:
            if name == '':
                flash('Please fill the "Name" field')
                valid = 0
            if vrn == '' or len(vrn) < 5:
                flash('Please fill correct Vehicle Registration No.')
                valid = 0
            if inop < 0:
                flash('Please corrent the No of People field')
                valid = 0
            if iaccess < 0 or iaccess > 11:
                flash('Please select a correct option to required area')
                valid = 0
            if len(uuid) != 8:
                flash('Huh wrong uuid! Please try again')
                valid = 0

        #print name, " ", email, " ", password

        if valid == 1:
            # Send the data to server here.
            # yay success
            flash('' + name + ' is Registered . Provide him the TAG Card')
        else:
            # Huh something wrong
            flash('Error: Correct error and try again. ')

    return render_template('hello.html', form=form)

@app.route('/readtag',methods=['GET'])
def readTag():
    sleep(1)
    return '{"status":"ok","result":"verygood"}'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
