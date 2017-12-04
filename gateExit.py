import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import requests
import json

continue_reading = True


def redLight():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    print "LED on"
    GPIO.output(23, GPIO.HIGH)
    time.sleep(5)
    print "LED off"
    GPIO.output(23, GPIO.LOW)

def greeLight():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    print "LED on"
    GPIO.output(18, GPIO.HIGH)
    time.sleep(5)
    print "LED off"
    GPIO.output(18, GPIO.LOW)

def redLightFlash():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    print "LED on"
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)

def continous_redLight():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(23, GPIO.HIGH)


def submitData(payload):
    base_url = "http://ec2-52-90-129-59.compute-1.amazonaws.com:5000"
    final_url = base_url+"/gateexit"

    response = requests.post(final_url,data=payload)

    json_response = response.text
    print json_response
    js = json.loads(json_response)
    result = js['result']
    return result



# Capture SIGINT for cleanup when the script is aborted
def end_read():
    global continue_reading
    #print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to gate Exit Program"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    continous_redLight()
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
	

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        #status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

	suid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
        # Check if authenticated
        #if status == MIFAREReader.MI_OK:
        #    MIFAREReader.MFRC522_Read(8)
        #    MIFAREReader.MFRC522_StopCrypto1()
	payload = {'uuid':suid}
	result = submitData(payload)
	if result == 'ok':		
	    print 'ok to Exit'
	    greeLight()
	elif result == 'already':
	    print 'You have exited already '
	    greeLight()
	elif result == 'notok':
	    print 'Something Wrong! Please wait for a gaurd to talk to you'
	    redLightFlash()
        #else:
        #    print "Authentication error"
        #    redLight()
