################################
#.bag-file to video
import numpy as np
import pyrealsense2 as rs
import cv2

#Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_device_from_file("Bag-file.bag")  #Here you insert the name of the bag-file that you want to convert to a mp4


pipeline.start(config)

#Create a video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_filename = 'output_video.mp4'
output_video = cv2.VideoWriter(output_filename, fourcc, 30.0, (640, 480)) #Frames per second and output resolution. Can be changed if needed

try:
    while True:
        
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            break

        color_image = np.asanyarray(color_frame.get_data())

        #Convert RGB to BGR color representation
        color_image_bgr = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)

        #Write the frame to the video file
        output_video.write(color_image_bgr)

        #Display the resulting frame
        cv2.imshow('RealSense Video', color_image_bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the pipeline and release resources
    pipeline.stop()
    output_video.release()
    cv2.destroyAllWindows()

