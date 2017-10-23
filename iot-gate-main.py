from flask import Flask


from flask import flash
from flask import render_template
from flask import request
from wtforms import Form, TextField
from wtforms import validators

from time import sleep

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read():
    global continue_reading
    #print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def readyToread():
    global continue_reading
    continue_reading = True
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    result = "";
    while continue_reading:

        # Scan for cards
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            #print "Card detected"
            end_read()

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print "Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3])
            suid = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            # This is the default key for authentication
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)


            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
                result = "{status:'ok',result:'"+suid+"'}"
                #end_read()
            else:
                #print "Authentication error"
                result = "{status:'not authenticated'}"
                #end_read()
               
    return result

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
    #sleep(20)
    #return '{result:"verygood"}'
    return readyToread()

if __name__ == '__main__':
    app.run()
