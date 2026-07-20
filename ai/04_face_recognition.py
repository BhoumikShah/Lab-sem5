import cv2
import os

def detect_faces(image_path='sample_face.png'):
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    if not os.path.exists(image_path):
        print(f"Error: Image '{image_path}' not found.")
        return

    img = cv2.imread(image_path)
    if img is None:
        print("Could not read the image.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    print(f"Found {len(faces)} face(s) in the image!")

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Face Detection', img)
    print("Press any key on the image window to close it.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    user_img = input("Enter the path to an image with faces (default: sample_face.png): ").strip()
    if not user_img:
        user_img = 'sample_face.png'
    detect_faces(user_img)
