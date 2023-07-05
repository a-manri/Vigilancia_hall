import cv2

def record_video(duration, output_file):
    # Define the video capture object
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    output = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))

    # Calculate the end time based on the desired duration
    end_time = cv2.getTickCount() + (duration * cv2.getTickFrequency())

    # Start recording
    while cv2.getTickCount() < end_time:
        ret, frame = video_capture.read()

        if ret:
            output.write(frame)

        # Display the frame (optional)
        #cv2.imshow('Recording', frame)
        #cv2.waitKey(1)

    # Release the video capture and writer objects
    video_capture.release()
    output.release()

    # Destroy any OpenCV windows
    cv2.destroyAllWindows()

# Define the duration (in seconds) and output file name
duration = 5
output_file = 'videofunciona0mjpg.avi'

# Call the function to record the video
record_video(duration, output_file)
