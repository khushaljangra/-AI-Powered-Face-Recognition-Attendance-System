import face_recognition
import pickle
import os
import cv2

def encode_faces():
    known_encodings = []
    known_names = []
    known_faces_dir = "known_faces"

    if not os.path.exists(known_faces_dir):
        os.makedirs(known_faces_dir)

    for image_name in os.listdir(known_faces_dir):
        image_path = os.path.join(known_faces_dir, image_name)
        if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        name = os.path.splitext(image_name)[0]
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(name)
            print(f"Encoded: {name}")
        else:
            print(f"Warning: No face found in {image_name}")

    data = {"encodings": known_encodings, "names": known_names}
    with open("encodings.pickle", "wb") as f:
        pickle.dump(data, f)
    print("Encodings saved to encodings.pickle")

if __name__ == "__main__":
    encode_faces()
