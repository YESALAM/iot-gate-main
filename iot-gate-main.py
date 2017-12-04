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

import requests
import json

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
    result = ""
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
                result = '{"status":"ok","result":"'+suid+'"}'
                #end_read()
            else:
                #print "Authentication error"
                result = '{"status":"not authenticated"}'
                #end_read()
               
    return result

def submitData(payload):
    base_url = "http://ec2-52-90-129-59.compute-1.amazonaws.com:5000"
    final_url = base_url+"/register"

    response = requests.post(final_url,data=payload)

    json_response = response.text

    js = json.loads(json_response)
    result = js['result']
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

    if request.method == 'POST':
        name = request.form['name']
        vrn = request.form['vrn']
        nop = request.form['nop']
        purpose = request.form['purpose']
        access = request.form['access']
        uuid = request.form['token_id_button']

        #validation of POST data
        valid = 1
        inop = 0
        iaccess = 0
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
            if len(uuid) != 10:
                flash('Huh wrong uuid! Please try again')
                valid = 0

        #print name, " ", email, " ", password

        if valid == 1:
            # Send the data to server here.
            # yay success
            payload = {'name':name,'vrn':vrn,'nop':nop,'purpose':purpose,'access':access,'token_id_button':uuid}
            result = submitData(payload)
            if result == 'ok':
                flash('' + name + ' is Registered . Provide him the TAG Card')
            elif result== 'already':
                flash('Error: Card is already Registered ! Use another')
            else:
                flash('Error: Server Error')

        else:
            # Huh something wrong
            flash('Error: Correct error and try again. ')

    return render_template('hello.html', form=form)

@app.route('/readtag',methods=['GET'])
def readTag():
    #sleep(20)
    #return '{result:"verygood"}'
    return readyToread()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
