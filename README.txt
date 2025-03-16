- Python has to be exactly 3.10 for latest tobii-research package 2.1.0.
- Pip version used 25.0.1.
- To avoid conflicting Python versions, you can install different Python versions without adding it to PATH, then create a virtualenv with the command "virtualenv -p Python3.10 venv"
- SDK reference guide: https://developer.tobiipro.com/python/python-sdk-reference-guide.html
- Software required:
    - Tobii Pro Eye Tracker Manager
    - Tobii Eye Tracking Core: https://gaming.tobii.com/getstarted/?bundle=tobii-core-4c&manualdownload=true
    - Tobii Pro Spark runtime: https://s3.eu-west-1.amazonaws.com/tobiipro.eyetracker.manager/downloadable-content/drivers/Spark/TobiiProSparkRuntime_2.2.3.0_x64.msi/TobiiProSparkRuntime_2.2.3.0_x64.msi
    - Tobii Eye Tracker Browser
- Check requirements.txt for installed libraries and their version
- Looks like Tobii Pro Spark is only eligible to subscribe to EYETRACKER_GAZE_DATA and EYETRACKER_USER_POSITION_GUIDE. The property EyeTracker.device_capabilities can show in more details. According to Pro SDK guide, there are also EYETRACKER_EYE_IMAGES, EYETRACKER_EYE_OPENNESS_DATA, EYETRACKER_EXTERNAL_SIGNAL and other notification channels.
- A topic on eye tracker gaze filter: https://connect.tobii.com/s/article/Gaze-Filter-functions-and-effects?language=en_US

Nishani data collection github: https://github.com/nishlfernando11/physiodata/blob/main/EquivitalDongleExample/schema.sql