# Source: https://pyimagesearch.com/2018/07/30/opencv-object-tracking/

from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

DEFAULT_TRACKER="kcf"

GOTURN_MODEL_BIN='data/goturn/goturn.caffemodel'
GOTURN_MODEL_TXT='data/goturn/goturn.prototxt'
DASIAMRPN_MODEL='data/dasiamrpn/dasiamrpn_model.onnx'
DASIAMRPN_KERNEL_R1='data/dasiamrpn/dasiamrpn_kernel_r1.onnx'
DASIAMRPN_KERNEL_CLS1='data/dasiamrpn/dasiamrpn_kernel_cls1.onnx'
FACE_CASCADE_FILE='data/haarcascades/haarcascade_frontalface_alt.xml'

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default=DEFAULT_TRACKER, help="OpenCV object tracker type (kcf or csrt)")
args = vars(ap.parse_args())

print(f'[INFO] cv2 version: {cv2.__version__}')
(major, minor) = cv2.__version__.split(".")[:2]
if int(major) < 3 or (int(major) == 3 and int(minor) < 3):
	raise f'cv2 version 3.3 or higher is required. Found {cv2.__version__}'

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"goturn": cv2.TrackerGOTURN_create,
	"dasiamrpn": cv2.TrackerDaSiamRPN_create,
}

TRACKER_PROPS = {
	"csrt": cv2.TrackerCSRT_Params(),
	"kcf": cv2.TrackerKCF_Params(),
	"goturn": cv2.TrackerGOTURN_Params(),
	"dasiamrpn": cv2.TrackerDaSiamRPN_Params(),
}
TRACKER_PROPS["goturn"].modelBin = GOTURN_MODEL_BIN
TRACKER_PROPS["goturn"].modelTxt = GOTURN_MODEL_TXT
TRACKER_PROPS["dasiamrpn"].model = DASIAMRPN_MODEL
TRACKER_PROPS["dasiamrpn"].kernel_cls1 = DASIAMRPN_KERNEL_CLS1
TRACKER_PROPS["dasiamrpn"].kernel_r1 = DASIAMRPN_KERNEL_R1


# grab the appropriate object tracker using our dictionary of
# OpenCV object tracker objects
tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]](TRACKER_PROPS[args["tracker"]])

faces = []
classifier = cv2.CascadeClassifier()
if not classifier.load(cv2.samples.findFile(FACE_CASCADE_FILE)):
 print('--(!)Error loading face cascade')
 exit(0)

# initialize the bounding box coordinates of the object we are going
# to track
initBB = None

# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# initialize the FPS throughput estimator
fps = None

# loop over frames from the video stream
while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame
	# check to see if we have reached the end of the stream
	if frame is None:
		break
	# resize the frame (so we can process it faster) and grab the
	# frame dimensions
	frame = imutils.resize(frame, width=500)
	(H, W) = frame.shape[:2]

	# check to see if we are currently tracking an object
	if initBB is None:
		# Peform face detection
		# Source: https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html

		# Convert to greyscale
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		frame_gray = cv2.equalizeHist(frame_gray)
		# Detect a face
		faces = classifier.detectMultiScale(frame_gray)
		if len(faces) > 0:
			initBB = faces[0]
			# start OpenCV object tracker using the supplied bounding box
			# coordinates, then start the FPS throughput estimator as well
			tracker.init(frame, initBB)
			fps = FPS().start()

	if initBB is not None:
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)
		# check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)

		# update the FPS counter
		fps.update()
		fps.stop()

		# initialize the set of information we'll be displaying on
		# the frame
		info = [
			("Tracker", args["tracker"]),
			("Success", "Yes" if success else "No"),
			("FPS", "{:.2f}".format(fps.fps())),
		]
		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		initBB = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
		tracker.init(frame, initBB)
		fps = FPS().start()
