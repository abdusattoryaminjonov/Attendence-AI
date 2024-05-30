import cv2
import matplotlib.pyplot as plt

# Importing Models and set mean values
face1 = r"C:\Users\Pbl4\pbl4\images\models\opencv_face_detector.pbtxt"
face2 = r"C:\Users\Pbl4\pbl4\images\models\opencv_face_detector_uint8.pb"
age1 = r"C:\Users\Pbl4\pbl4\images\models\age_deploy.prototxt"
age2 = r"C:\Users\Pbl4\pbl4\images\models\age_net.caffemodel"
gen1 = r"C:\Users\Pbl4\pbl4\images\models\gender_deploy.prototxt"
gen2 = r"C:\Users\Pbl4\pbl4\images\models\gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
# Categories of distribution
la = ['(0-3)', '(4-7)', '(8-14)', '(15-24)', '(25-37)', '(38-47)', '(48-59)', '(60-100)']
lg = ['Erkak', 'Ayol']

# Using models
# Face
face_net = cv2.dnn.readNet(face2, face1)
# age
age_net = cv2.dnn.readNet(age2, age1)
# gender
gen_net = cv2.dnn.readNet(gen2, gen1)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if not ret:
        continue

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)  # Corrected line
    detections = face_net.forward()

    # Face bounding box creation
    faceBoxes = []
    for i in range(detections.shape[2]):
        # Bounding box creation if confidence > 0.6
        confidence = detections[0, 0, i, 2]
        if confidence > 0.6:
            x1 = int(detections[0, 0, i, 3] * w)
            y1 = int(detections[0, 0, i, 4] * h)
            x2 = int(detections[0, 0, i, 5] * w)
            y2 = int(detections[0, 0, i, 6] * h)

            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), int(round(h / 150)), 8)

    # Checking if face detected or not
    if not faceBoxes:
        print("No face detected")

    # Final results (otherwise)
    # Loop for all the faces detected
    for faceBox in faceBoxes:
        # Extracting face as per the faceBox
        face_roi = frame[max(0, faceBox[1] - 15): min(faceBox[3] + 15, h - 1),
                    max(0, faceBox[0] - 15):min(faceBox[2] + 15, w - 1)]

        # Extracting the main blob part
        blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        # Prediction of gender
        gen_net.setInput(blob)
        genderPreds = gen_net.forward()
        gender = lg[genderPreds[0].argmax()]

        # Prediction of age
        age_net.setInput(blob)
        agePreds = age_net.forward()
        agePerson = agePreds[0].argmax() + 1
        a = la[agePerson]

        # Putting text of age and gender at the top of box
        cv2.putText(frame, f'{gender}{a}', (faceBox[0] - 15, faceBox[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (255, 0, 255), 2)

    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
