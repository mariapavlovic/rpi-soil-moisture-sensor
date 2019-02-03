import RPi.GPIO as GPIO
import time
import smtplib

channel = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)


def send_email(message):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('raspberrypi2k19@gmail.com', 'thisisrpi')
    sender = 'raspberrypi2k19@gmail.com'
    recipient = 'mariapavlovic0@gmail.com'
    header = 'To:' + recipient + '\n' + 'From:' \
            + sender + '\n' + 'Subject: Soil Update! \n'
    content = header + message
    mail.sendmail(sender, recipient, content)
    mail.close()


def print_gpio_input(ch, is_cb):
    state_change = True
    if GPIO.input(ch):
        if not is_cb and state_change:
            print("out of water")
            message = "out of water"
            send_email(message)
            state_change = False
    else:
        if not is_cb and state_change:
            print("in water")
            message = "has water"
            send_email(message)
            state_change = False


def callback(channel):
    print_gpio_input(channel, True)


GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=100)
GPIO.add_event_callback(channel, callback)


while True:
    print_gpio_input(channel, False)
    time.sleep(0.10)
