#!/usr/bin/env python

#Image Processing with ROS and OpenCV

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

def callback(image_msg):
    
    try:
        # We first convert the ROS image message image_msg to OpenCV format using the imgmsg_to_cv2 function.
        cv_image = bridge.imgmsg_to_cv2(image_msg)
        # Restoring the color format
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        
        # Making different alterations on the image
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(cv_image, 125,175)
        texted = cv2.putText(cv_image.copy(), "Wake up Neo", (225,255), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (0,255,0), 2)
        
        # Initializing publishers to 3 different topics
        gray_pub = rospy.Publisher("grayscale_image", Image, queue_size=10)
        canny_pub = rospy.Publisher("canny_edge_detection", Image, queue_size=10)
        text_pub = rospy.Publisher("message_from_morpheus", Image, queue_size=10)
        
        try:
       
            # Before we can publish the images, we need to convert them to a ROS message img_msg using the function cv2_to_imgmsg (from CvBridge).
            grayimg = bridge.cv2_to_imgmsg(gray)
            gray_pub.publish(grayimg)
            
            cannyimg = bridge.cv2_to_imgmsg(canny)
            canny_pub.publish(cannyimg)
            
            # With the color encoding "bgr8" , future subscribers will know the color order, in this case, it is blue-green-red and 8-bits. We did not need to specify this in the grayscale and canny.
            textedimg = bridge.cv2_to_imgmsg(texted, "bgr8")
            text_pub.publish(textedimg)
          
        except CvBridgeError as error:
            print(error)
            
        # Delaying for 10 milliseconds or until any key is pressed before switching to the next frame
        cv2.waitKey(10)
        
    except CvBridgeError as error:
        print(error)


if __name__ == '__main__':
    bridge = CvBridge()
    
    # Initializing a node to subscribe the image_raw topic published by usb_cam, receive camera images, make various alterations on them and publish later
    rospy.init_node("image_transmitter_node", anonymous=True)
    print("Subscribe images from topic /image_raw")
    
    image_subscriber = rospy.Subscriber("usb_cam/image_raw", Image, callback)

    try:
        # spin() keeps python from exiting until this node is stopped.
        rospy.spin()
    except KeyboardInterrupt:
    	print("Shutting down!")
      
