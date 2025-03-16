import psycopg2
import pandas as pd
import json

def printRed(skk): print("\033[91m {}\033[00m" .format(skk))
def printGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def printYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def printLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def printPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def printCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def printLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def printBlack(skk): print("\033[98m {}\033[00m" .format(skk))


def clean_data(type, data):
    # type is either "user_pos_data" or "gaze_data"
    # data is in JSON format, representing 1 sample

    # Different flow for each type of data
    cleaned_data = {}
    if type == "user_pos_data":
        cleaned_data = data.copy()
        cleaned_data = pd.DataFrame(cleaned_data).fillna(-1)
        cleaned_data = cleaned_data.groupby(['left_user_position_validity','right_user_position_validity']).agg(lambda x: tuple(x)).reset_index()
        cleaned_data = json.loads(cleaned_data.to_json(orient='records'))[0]
    if type == "gaze_data":
        try:
            cleaned_data = json.dumps(data)
            # This is a very hacky way to fill NaN values. A more elegant way is more than welcome to replace this part.
            cleaned_data = cleaned_data.replace("NaN", "-1").replace("[NaN, NaN]", "[-1, -1]").replace("[NaN, NaN, NaN]", "[-1, -1, -1]")
            cleaned_data = json.loads(cleaned_data)
        except Exception as e:
            print(e)
    return cleaned_data


def insert_row(conn,
                schema="public",
                table="",
                columns=[],
                data=()):
    """ Insert multiple rows into the specified table  """
    cols = ", ".join(columns)
    vals = ",".join(len(columns)*["%s"])
    sql = f"INSERT INTO {schema}.{table}({cols}) VALUES("+ vals +");"
    try:
        with  conn.cursor() as cur:
            # execute the INSERT statement
            cur.execute(sql, data)
        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def calibrate(eyetracker):
    if eyetracker is None:
        return# <BeginExample>
    import time
    import tobii_research as tr
    calibration = tr.ScreenBasedCalibration(eyetracker)

    # Enter calibration mode.
    calibration.enter_calibration_mode()
    print("Entered calibration mode for eye tracker with serial number {0}.".format(eyetracker.serial_number))

    # Define the points on screen we should calibrate at.
    # The coordinates are normalized, i.e. (0.0, 0.0) is the upper left corner and (1.0, 1.0) is the lower right corner.
    points_to_calibrate = [(0.5, 0.5), (0.1, 0.1), (0.1, 0.9), (0.9, 0.1), (0.9, 0.9)]

    for point in points_to_calibrate:
        print("Show a point on screen at {0}.".format(point))

        # Wait a little for user to focus.
        time.sleep(0.7)

        print("Collecting data at {0}.".format(point))
        if calibration.collect_data(point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
            # Try again if it didn't go well the first time.
            # Not all eye tracker models will fail at this point, but instead fail on ComputeAndApply.
            calibration.collect_data(point[0], point[1])

    print("Computing and applying calibration.")
    calibration_result = calibration.compute_and_apply()
    print("Compute and apply returned {0} and collected at {1} points.".
        format(calibration_result.status, len(calibration_result.calibration_points)))

    # Analyze the data and maybe remove points that weren't good.
    recalibrate_point = (0.1, 0.1)
    print("Removing calibration point at {0}.".format(recalibrate_point))
    calibration.discard_data(recalibrate_point[0], recalibrate_point[1])

    # Redo collection at the discarded point
    print("Show a point on screen at {0}.".format(recalibrate_point))
    calibration.collect_data(recalibrate_point[0], recalibrate_point[1])

    # Compute and apply again.
    print("Computing and applying calibration.")
    calibration_result = calibration.compute_and_apply()
    print("Compute and apply returned {0} and collected at {1} points.".
        format(calibration_result.status, len(calibration_result.calibration_points)))

    # See that you're happy with the result.

    # The calibration is done. Leave calibration mode.
    calibration.leave_calibration_mode()
    print("Left calibration mode.")# <EndExample>
