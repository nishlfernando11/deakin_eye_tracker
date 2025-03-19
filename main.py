import socketio
import keyboard
from utilities import *
import tobii_research as tr
import time
import json
import psycopg2
import pylsl

sio = socketio.Client()

"""
Config
"""
DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "experiments"
DB_USER = "experiments"
DB_PASSWORD = "experiments"

count_gaze = 0
count_user = 0
"""
Callbacks
"""
def gaze_data_callback(gaze_data):
    global eye_tracker_data
    global round_id
    global conn
    global outlet
    global count_gaze
    count_gaze += 1

    # Preprocess
    gaze_data = clean_data("gaze_data", gaze_data)
    
    # Assume that there will be 1 call to gaze_data_callback per 1 call to user_pos_data_callback.
    # If there are 2 or more calls to gaze_data_callback before user_pos_data_callback is called, raise an error that the subscription is out of sync.
    if "gaze_data" in eye_tracker_data:
        raise Exception("!!! Subscription is out of sync !!!")

    # Check if user position data have been added. If there are user position data, append user position data to gaze data and save to database.
    # It could be harder if we subscribe to more data than the current EYETRACKER_GAZE_DATA and EYETRACKER_USER_POSITION_GUIDE.
    # Refresh eye_tracker_data for the next row insert in database.
    # For reference, columns to be inserted in database are ["event_time","unix_timestamp","lsl_timestamp","round_id","eye_tracker_data"]
    eye_tracker_data["gaze_data"] = gaze_data
    if "user_pos_data" in eye_tracker_data:
        data = json.dumps(eye_tracker_data)
        # Push data to Postgres
        insert_row(conn,
            schema="public",
            table="eye_tracker_data",
            columns=eye_tracker_cols,
            data=(
                    time.time(),
                    time.time(),
                    pylsl.local_clock(),
                    round_id,
                    data
            ))
        # Push data to LSL stream
        # print("Pushing sample to LSL stream:", data)
        outlet.push_sample([data])
        eye_tracker_data = {}


def user_pos_data_callback(user_pos_data):
    global eye_tracker_data
    global round_id
    global conn
    global outlet
    global count_user
    count_user += 1

    # Preprocess
    user_pos_data = clean_data("user_pos_data", user_pos_data)
    
    # Assume that there will be 1 call to gaze_data_callback per 1 call to user_pos_data_callback.
    # If there are 2 or more calls to user_pos_data_callback before gaze_data_callback is called, raise an error that the subscription is out of sync.
    if "user_pos_data" in eye_tracker_data:
        raise Exception("!!! Subscription is out of sync !!!")

    # Check if gaze data have been added. If there are gaze data, append gaze data to user position data and save to database.
    # It could be harder if we subscribe to more data than the current EYETRACKER_GAZE_DATA and EYETRACKER_USER_POSITION_GUIDE.
    # Refresh eye_tracker_data for the next row insert in database.
    # For reference, columns to be inserted in database are ["event_time","unix_timestamp","lsl_timestamp","round_id","eye_tracker_data"]
    eye_tracker_data["user_pos_data"] = user_pos_data
    if "gaze_data" in eye_tracker_data:
        data = json.dumps(eye_tracker_data)
        # Push data to Postgres
        insert_row(conn,
            schema="public",
            table="eye_tracker_data",
            columns=eye_tracker_cols,
            data=(
                    time.time(),
                    time.time(),
                    pylsl.local_clock(),
                    round_id,
                    data
            ))
        # Push data to LSL stream
        # print("Pushing sample to LSL stream:", data)
        outlet.push_sample([data])
        eye_tracker_data = {}


"""
Start
"""
# Manually input round_id
# round_id = str(input("Please put in the Round ID: "))

# Initialize the stream outlet once
info = pylsl.StreamInfo(name="Eye_Tracker_Stream", type="Event", channel_count=1, nominal_srate=0, channel_format='string')
outlet = pylsl.StreamOutlet(info)
print("Stream outlet created.")

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


#start data collection
eye_tracker_cols = ["event_time","unix_timestamp","lsl_timestamp","round_id","eye_tracker_data"]
eye_tracker_data = {}
my_eyetracker = None

@sio.event
def connect():
    print('connection established')

@sio.on("start_game")
def eye_tracker_start(data):
    global my_eyetracker
    #find device
    found_eyetrackers = tr.find_all_eyetrackers()
    my_eyetracker = found_eyetrackers[0]
    round_id = data.get("round_id","round_1")
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
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    my_eyetracker.subscribe_to(tr.EYETRACKER_USER_POSITION_GUIDE, user_pos_data_callback, as_dictionary=True)
    # my_eyetracker.subscribe_to(tr.EYETRACKER_EYE_IMAGES, eye_image_data_callback, as_dictionary=True)
    # my_eyetracker.subscribe_to(tr.EYETRACKER_EYE_OPENNESS_DATA, eye_openness_data_callback, as_dictionary=True)
    # my_eyetracker.subscribe_to(tr.EYETRACKER_EXTERNAL_SIGNAL, ext_signal_data_callback, as_dictionary=True)
    print('message received with ', data)

@sio.on("end_game")
def eye_tracker_stop():
    global my_eyetracker
    global conn
    global count_gaze
    global count_user
    print(f"Eye tracker data collection ended. Gaze instances: {count_gaze} | User position instances: {count_user}")
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_USER_POSITION_GUIDE, user_pos_data_callback)
    conn.close()
    print('disconnected from server')

sio.connect('http://localhost:80')
sio.wait()
if keyboard.is_pressed("esc"):
    print(f"Data collection ended.")
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_USER_POSITION_GUIDE, user_pos_data_callback)
