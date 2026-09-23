import cv2
import os
import time

# Load pre-trained Haar Cascades for Face and Eye detection
CASCADE_DIR = cv2.data.haarcascades
face_cascade = cv2.CascadeClassifier(os.path.join(CASCADE_DIR, 'haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(CASCADE_DIR, 'haarcascade_eye.xml'))


def preprocess_frame(img_bgr):
    # Grayscale conversion and histogram equalization for contrast normalization
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    equalized_gray = cv2.equalizeHist(gray)
    return gray, equalized_gray


def process_face_detection(frame):
    annotated = frame.copy()
    _, equalized = preprocess_frame(frame)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        equalized,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40)
    )
    
    face_details = []
    
    for i, (fx, fy, fw, fh) in enumerate(faces, start=1):
        # Draw face bounding box (Green)
        cv2.rectangle(annotated, (fx, fy), (fx + fw, fy + fh), (0, 230, 115), 2)
        
        # Region of interest (ROI) for eyes (restricted to upper 60% of face)
        upper_face_roi = equalized[fy:fy + int(fh * 0.6), fx:fx + fw]
        eyes = eye_cascade.detectMultiScale(
            upper_face_roi,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(15, 15),
            maxSize=(int(fw * 0.4), int(fh * 0.4))
        )
        
        for (ex, ey, ew, eh) in eyes:
            center = (fx + ex + ew // 2, fy + ey + eh // 2)
            radius = int(round((ew + eh) * 0.25))
            cv2.circle(annotated, center, radius, (255, 191, 0), 2)
        
        # Badge overlay
        label = f"Face #{i} | Eyes: {len(eyes)}"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.rectangle(annotated, (fx, fy - th - 10), (fx + tw + 6, fy), (0, 0, 0), -1)
        cv2.putText(annotated, label, (fx + 3, fy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        
        face_details.append({"id": i, "box": (fx, fy, fw, fh), "eyes_count": len(eyes)})
    
    # Header summary badge
    cv2.rectangle(annotated, (10, 10), (140, 45), (30, 30, 30), -1)
    cv2.putText(annotated, f"Faces: {len(faces)}", (20, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 200), 2)
    
    return annotated, {"faces_detected": len(faces), "details": face_details}


def run_image_mode(image_path='sample_face.png', output_path='output_detected_face.png'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, image_path) if not os.path.isabs(image_path) else image_path
    
    if not os.path.exists(full_path):
        full_path = image_path if os.path.exists(image_path) else None
    
    if not full_path or not os.path.exists(full_path):
        print(f"[!] Error: Image '{image_path}' not found.")
        return

    img = cv2.imread(full_path)
    if img is None:
        print("[!] Error: Could not read image.")
        return

    start_t = time.time()
    annotated_img, analytics = process_face_detection(img)
    latency_ms = (time.time() - start_t) * 1000

    print(f"Image: {os.path.basename(full_path)} | Size: {img.shape[1]}x{img.shape[0]} | Latency: {latency_ms:.1f}ms")
    print(f"Faces Detected: {analytics['faces_detected']}")
    for face in analytics['details']:
        fx, fy, fw, fh = face['box']
        print(f" -> Face #{face['id']}: ({fw}x{fh}) at ({fx},{fy}) | Eyes: {face['eyes_count']}")

    full_output = os.path.join(script_dir, output_path)
    cv2.imwrite(full_output, annotated_img)
    print(f"[+] Output saved: {full_output}")

    cv2.imshow("Face & Eye Detection", annotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam_mode():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Error: Camera not accessible.")
        return

    print("[+] Webcam stream started. Press 'q' to quit, 's' to snapshot.")
    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()
        fps = 1.0 / (now - prev_time) if prev_time != 0 else 0
        prev_time = now

        annotated_frame, _ = process_face_detection(frame)
        cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (20, annotated_frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Live Face Detection", annotated_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite(f"snapshot_{int(time.time())}.png", annotated_frame)
            print("[+] Snapshot saved.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("EXPERIMENT 04: FACE & EYE DETECTION")
    print("[1] Static Image (sample_face.png)\n[2] Live Webcam Stream")
    choice = input("Select (1/2, default 1): ").strip()
    
    if choice == '2':
        run_webcam_mode()
    else:
        path = input("Image path (Press Enter for default): ").strip() or 'sample_face.png'
        run_image_mode(path)
