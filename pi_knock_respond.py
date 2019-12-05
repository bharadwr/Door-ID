import os, sys, time, requests
import cv2

def take_photo(camID=0, extension=".jpg"):
    image_name = "user" + extension
    try:
        cam = cv2.VideoCapture(camID)
        time.sleep(1)
        s, img = cam.read()
        cam.release()
        cv2.imwrite(image_name, img)
        return image_name
    except (Warning, Exception) as e:
        print(e)
        if os.isfile(image_name):
            os.remove(image_name)
        return ""
    finally:
        pass

if __name__ == "__main__":
    flask_url = "http://40.117.34.205:40862/"
    image_name = take_photo()
    if image_name == "":
        print("OpenCV error, please check settings")
        sys.exit(1)
    try:
        files = {'file': open(image_name, 'rb')}
        response = requests.post(flask_url, files=files, timeout=120)
        print(response.content.decode())
    except (requests.exceptions.Timeout) as e:
        print("Request timed out: ", e)
    except (Warning, Exception) as e:
        print(e)
    finally:
        os.remove(image_name)
