import cv2
from .gaze_tracking import GazeTracking


def analyzeFrames(videoPath=0):
    gaze = GazeTracking()
    video_stream = cv2.VideoCapture(videoPath)
    frame_count = 0
    looking_down = 0
    
    while True:
        # We get a new frame from the video_stream
        frame_captured, frame = video_stream.read()
        
        if not frame_captured:
            break

        frame_count += 1
        
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)
    
        frame = gaze.annotated_frame()
        text = ""
    
        if gaze.is_blinking():
            text = "Blinking"
            looking_down += 1
        else:
            if gaze.is_above():
                text = "Looking above"
            elif gaze.is_below():
                text = "Looking below"
                looking_down += 1             
            elif gaze.is_vertical_center():
                text = "Looking center"

        if videoPath == '0':
            cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        
            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        
            cv2.imshow("Demo", frame)
        
            # Esc key to stop
            if cv2.waitKey(1) == 27:
                break
    
    print("Total Frames: " + str(frame_count))
    print("Negative Frames: " + str(looking_down))
    print("Confidence: " + str((1-looking_down/frame_count)*100))


# Driver Code 
if __name__ == '__main__':

  analyzeFrames()