def execute(eyetracker):
    if eyetracker is not None:
        eye_images(eyetracker)
    else:
        print("No tracker with eye images to run example.")


# <BeginExample>

import sys
import base64
import time
import tobii_research as tr

if sys.version_info[0] == 3:
    # Python 3
    from tkinter import Tk, PhotoImage
else:
    from Tkinter import Tk, PhotoImage


def eye_image_callback(eye_image_data):
    print("System time: {0}, Device time {1}, Camera id {2}".format(eye_image_data['system_time_stamp'],
                                                                    eye_image_data['device_time_stamp'],
                                                                    eye_image_data['camera_id']))

    image = PhotoImage(data=base64.standard_b64encode(eye_image_data['image_data']))
    print("{0} width {1}, height {2}".format(image, image.width(), image.height()))


def eye_images(eyetracker):
    root = Tk()
    print("Subscribing to eye images for eye tracker with serial number {0}.".format(eyetracker.serial_number))
    eyetracker.subscribe_to(tr.EYETRACKER_EYE_IMAGES, eye_image_callback, as_dictionary=True)

    # Wait for eye images.
    time.sleep(10)

    eyetracker.unsubscribe_from(tr.EYETRACKER_EYE_IMAGES, eye_image_callback)
    print("Unsubscribed from eye images.")
    root.destroy()
# <EndExample>

# def execute(eyetracker):
#  gaze_data(eyetracker)
 
 
#  # <BeginExample>
# import logging
# import time
# import tobii_research as tr
 
# global_gaze_data = None

# def gaze_data_callback(gaze_data):
#     global global_gaze_data 
#     global_gaze_data = gaze_data


# def buffer_overflow_notifications_callback(notification_data):
#     logging.error("Buffer overflow occurred at system time:")


# def gaze_data(eyetracker):
#     global global_gaze_data

#     print("Subscribing to gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))
#     eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

#     # # listen for buffer overflow notifications (to see e.g. if the gaze callback is too slow)
#     # eyetracker.subscribe_to(
#     # # tr.EYETRACKER_NOTIFICATION_STREAM_BUFFER_OVERFLOW,
#     # # buffer_overflow_notifications_callback,
#     # as_dictionary=True
#     # )

#     # Wait while some gaze data is collected.
#     time.sleep(5)

#     eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
#     print("Unsubscribed from gaze data.")

#     print("Last received gaze package:")
#     print(global_gaze_data)
#     # <EndExample>

# def gaze_data_callback(gaze_data):
#     # Print gaze points of left and right eye
#     print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
#         gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
#         gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

found_eyetrackers = tr.find_all_eyetrackers()

my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)


execute(my_eyetracker)
# # my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

# # time.sleep(20)


# # my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)