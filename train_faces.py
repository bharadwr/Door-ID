import glob, os, sys, time, requests
from uuid import uuid4
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
import cv2

KEY = "c6926d31df9046bc9ac85c54705361ef"
ENDPOINT = "https://doorid.cognitiveservices.azure.com/"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
PERSON_GROUP_ID = 'house-residents'
TARGET_PERSON_GROUP_ID = "4248"

def trainPersonGroup():
    face_client.person_group.train(PERSON_GROUP_ID)
    while (True):
        training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(5)

def addImageToPerson(person, personImages, PERSON_GROUP_ID):
    for image in personImages:
        w = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person.person_id, w)

def CreatePersonGroup():
    face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

    #Create new person group
    rtvik = face_client.person_group_person.create(PERSON_GROUP_ID, "rtvik")
    ishaan = face_client.person_group_person.create(PERSON_GROUP_ID, "ishaan")
    sreyas = face_client.person_group_person.create(PERSON_GROUP_ID, "sreyas")
    dhruv = face_client.person_group_person.create(PERSON_GROUP_ID, "dhruv")

    #Assign images to each person
    rtvikImages = [file for file in glob.glob('users/*.jpg') if file.startswith("rtvik")]
    ishaanImages = [file for file in glob.glob('users/*.jpg') if file.startswith("ishaan")]
    sreyasImages = [file for file in glob.glob('users/*.jpg') if file.startswith("sreyas")]
    dhruvImages = [file for file in glob.glob('users/*.jpg') if file.startswith("dhruv")]

    addImageToPerson(rtvik, rtvikImages, PERSON_GROUP_ID)
    addImageToPerson(ishaan, ishaanImages, PERSON_GROUP_ID)
    addImageToPerson(sreyas, sreyasImages, PERSON_GROUP_ID)
    addImageToPerson(dhruv, dhruvImages, PERSON_GROUP_ID)
    trainPersonGroup()

def AddPersonToPersonGroup(personName="default", imgFile="default.jpg"):

    #Create new person group
    person = face_client.person_group_person.create(PERSON_GROUP_ID, personName)

    #Assign images to each person
    personImages = [imgFile]
    addImageToPerson(person, personImages, PERSON_GROUP_ID)

    #Retrain PersonGroup with personName
    trainPersonGroup()

def IdentifyPersonInImage(personImage="default.jpg"):
    try:
        # Get test image
        image = open(personImage, 'r+b')

        # Detect faces
        face_ids = []
        faces = face_client.face.detect_with_stream(image)
        for face in faces:
            face_ids.append(face.face_id)

        # Identify faces
        results = face_client.face.identify(face_ids, PERSON_GROUP_ID)

        print('Identifying faces in {}')
        if not results:
            print('No person identified in the person group for faces from the {}.'.format(os.path.basename(image.name)))
        for person in results:
            return person.candidates[0].confidence # Get topmost confidence score

    except (Warning, Exception) as e:
        return 0.0

def identify_person_at_door():
    cam = cv2.VideoCapture(0)
    time.sleep(1)
    s, img = cam.read()
    cam.release()
    cv2.imwrite("user.jpg", img)
    confidence = IdentifyPersonInImage(personImage="user.jpg")
    if confidence <= 0.7:
        print("Unidentified", confidence)
        url = "http://40.117.34.205:40862/"
        files = {'file': open('user.jpg', 'rb')}
        response = requests.post(url, files=files)
        decoded = response.content.decode()
        if "Unauthorized" in decoded:
            print("calling law enforcement on you")

        elif "Authorized" in decoded:
            print("adding user to the network")
            AddPersonToPersonGroup(personName=str(uuid4()), imgFile="user.jpg")
        else:
            print("Bruh what this response", decoded)
    else:
        print("Identified", confidence)

if __name__ == "__main__":
    identify_person_at_door()
