import os, sys, time, requests
import cv2

def take_photo(camID=0, extension=".jpg"):
    image_name = "user" + extension
    try:
        video_capture = cv2.VideoCapture(camID)
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        start_time = time.time()
        while True:
            ret, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.5,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            if len(faces) > 0:
                cv2.imwrite(image_name, frame)
                break

            if time.time() - start_time > 10:
                raise TimeoutError("CV2 Timed out")

        return image_name

    except (Warning, Exception) as e:
        print(e)
        if os.path.isfile(image_name):
            os.remove(image_name)
        return ""
    finally:
        video_capture.release()

if __name__ == "__main__":
    flask_url = "http://40.117.34.205:40862/"
    image_name = ""
    try:
        image_name = take_photo(camID=-1)
        if image_name == "":
            print("OpenCV error, please check settings")
            raise EnvironmentError("OpenCV Error")
        files = {'file': open(image_name, 'rb')}
        response = requests.post(flask_url, files=files, timeout=120)
        print(response.content.decode())
    except (Warning, Exception) as e:
        exc_type, _, _ = sys.exc_info()
        params = {"error_message" : "%s %s" % (str(exc_type), str(e))}
        response = requests.put(flask_url, params=params, timeout=30)
        print(e)
    finally:
        if os.path.isfile(image_name):
            os.remove(image_name)
