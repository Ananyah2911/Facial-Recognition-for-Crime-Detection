# facerec.py
import cv2
import numpy
import os

size = 2
haar_cascade = cv2.CascadeClassifier(
    r'C:\Users\Microsoft\Desktop\major project\Facial-Recognition-for-Crime-Detection-master\haar_cascade.xml'
)

def train_model():
    model = cv2.face.LBPHFaceRecognizer_create()
    fn_dir = 'face_samples'

    print('Training...')

    images = []
    labels = []
    names = {}
    current_id = 0

    # Loop through each subdirectory
    for root, dirs, files in os.walk(fn_dir):
        for subdir in dirs:
            person_dir = os.path.join(fn_dir, subdir)
            names[current_id] = subdir  # store name for recognition

            # Loop through image files inside each person's folder
            for filename in os.listdir(person_dir):
                filepath = os.path.join(person_dir, filename)

                # Allow only image files
                ext = os.path.splitext(filename)[1].lower()
                if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.pgm']:
                    print("Skipping", filename, "invalid image type")
                    continue

                img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

                if img is None:
                    print("Failed to load image:", filepath)
                    continue

                # Append image and corresponding label
                images.append(img)
                labels.append(current_id)

            current_id += 1

    if len(images) < 2:
        raise Exception("Training failed: Not enough images. Need at least 2 images.")

    # Convert to numpy arrays
    images = numpy.array(images)
    labels = numpy.array(labels)

    print("Total images loaded:", len(images))
    print("Total labels:", len(labels))

    # Train the LBPH model
    model.train(images, labels)

    print("Training completed successfully.")
    return model, names


# Face detection function
def detect_faces(gray_frame):
    global size, haar_cascade
    mini_frame = cv2.resize(gray_frame, (gray_frame.shape[1] // size, gray_frame.shape[0] // size))
    faces = haar_cascade.detectMultiScale(mini_frame, 1.3, 5)
    return faces


# Recognition function
def recognize_face(model, frame, gray_frame, face_coords, names):
    (img_width, img_height) = (112, 92)
    recognized = []
    recog_names = []

    for face in face_coords:
        (x, y, w, h) = [v * size for v in face]
        face_img = gray_frame[y:y + h, x:x + w]
        face_resize = cv2.resize(face_img, (img_width, img_height))

        (prediction, confidence) = model.predict(face_resize)

        if confidence < 95 and names[prediction] not in recog_names:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            recog_names.append(names[prediction])
            recognized.append((names[prediction].capitalize(), confidence))
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame, recognized
