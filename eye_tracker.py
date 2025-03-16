import tobii_research as tr
import keyboard
import time
import json
import psycopg2
import pylsl
from utilities import *

"""
Config
"""
DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "experiments"
DB_USER = "experiments"
DB_PASSWORD = "experiments"


"""
Callbacks
"""
def gaze_data_callback(gaze_data):
    global eye_tracker_data
    global conn


def user_pos_data_callback(user_pos_data):
    global eye_tracker_data
    global conn


"""
Start
"""
#find device
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)
all_gaze_output_frequencies = my_eyetracker.get_all_gaze_output_frequencies()
initial_gaze_output_frequency = my_eyetracker.get_gaze_output_frequency()
all_eye_tracking_modes = my_eyetracker.get_all_eye_tracking_modes()
print("There are {0} Hz frequencies. The eye tracker's initial gaze output frequency is {1} Hz.".format(all_gaze_output_frequencies, initial_gaze_output_frequency))
print("All eye tracking modes: ", all_eye_tracking_modes)
print("Eye tracker capabilities: ",my_eyetracker.device_capabilities)

# Calibrate eye tracker
# calibrate(my_eyetracker)

# Connect database
try:
    conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
    )
    printGreen("Database connected.")
except Exception as e:
    printRed(f"Unable to establish a connection with database hosted on {DB_HOST}. Exception: {e}")


#start data collection until the escape key "esc" is pressed
eye_tracker_cols = ["event_time","unix_timestamp","lsl_timestamp","round_id","eye_tracker_data"]
is_ongoing = True
eye_tracker_data = {}
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
# my_eyetracker.subscribe_to(tr.EYETRACKER_EYE_IMAGES, eye_image_data_callback, as_dictionary=True)
# my_eyetracker.subscribe_to(tr.EYETRACKER_EYE_OPENNESS_DATA, eye_openness_data_callback, as_dictionary=True)
# my_eyetracker.subscribe_to(tr.EYETRACKER_EXTERNAL_SIGNAL, ext_signal_data_callback, as_dictionary=True)
my_eyetracker.subscribe_to(tr.EYETRACKER_USER_POSITION_GUIDE, user_pos_data_callback, as_dictionary=True)
while is_ongoing:
    if keyboard.is_pressed("esc"):
        is_ongoing = False
        conn.close()
        print("Ended.")
        time.sleep(2)   # Wait to finalize inserting data into db
        my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
        # my_eyetracker.unsubscribe_from(tr.EYETRACKER_EYE_IMAGES, eye_image_data_callback)
        # my_eyetracker.unsubscribe_from(tr.EYETRACKER_EYE_OPENNESS_DATA, eye_openness_data_callback)
        # my_eyetracker.unsubscribe_from(tr.EYETRACKER_EXTERNAL_SIGNAL, ext_signal_data_callback)
        my_eyetracker.unsubscribe_from(tr.EYETRACKER_USER_POSITION_GUIDE, user_pos_data_callback)

    # insert_row(conn,
    #         schema="public",
    #         table="eye_tracker_data",
    #         columns=eye_tracker_cols,
    #         data=data)