"""
================================================================================
EXPERIMENT 04: FACIAL & EYE FEATURE DETECTION SYSTEM
================================================================================
Author: AI Lab Student
Topic: Computer Vision (CV), Object Detection, Haar Cascades, & Biometrics

WHAT THIS SYSTEM DOES:
-----------------------
1. Loads Haar-Cascade XML classifiers for Face and Eye detection.
2. Applies Computer Vision Preprocessing:
   - Grayscale conversion (converts 3-channel RGB into 1-channel intensity).
   - Histogram Equalization (normalizes illumination, contrast & shadows).
3. Executes a Hierarchical Region-of-Interest (ROI) Detection Pipeline:
   - Primary: Detects the bounding coordinates (x, y, w, h) of full faces.
   - Secondary: Extracts the Face ROI to detect Eyes in the upper 60% area.
4. Renders an augmented analytics HUD:
   - Color-coded bounding markers, eye counts, and real-time telemetry.
5. Dual Mode Execution: Supports both Static Image processing and Live Webcam Stream.
================================================================================
"""

import cv2
import os
import time

# ==============================================================================
# 1. LOAD PRE-TRAINED HAAR CASCADE CLASSIFIERS
# ==============================================================================
# HOW HAAR CASCADES WORK (FOR PROFESSOR / VIVA EXPLANATION):
# - Haar Cascades use edge, line, and rectangle features to detect visual contrast.
# - 'Integral Images' compute pixel area sums in O(1) constant time.
# - 'AdaBoost' chains hundreds of weak classifiers into an attentional cascade.
#   If a background region fails stage 1, it is discarded immediately, making it
#   fast enough for real-time video processing.
# ==============================================================================

CASCADE_DIR = cv2.data.haarcascades
FACE_CASCADE_PATH = os.path.join(CASCADE_DIR, 'haarcascade_frontalface_default.xml')
EYE_CASCADE_PATH = os.path.join(CASCADE_DIR, 'haarcascade_eye.xml')

face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
eye_cascade = cv2.CascadeClassifier(EYE_CASCADE_PATH)

# Verify cascade models loaded properly
if face_cascade.empty() or eye_cascade.empty():
    raise RuntimeError("Error: Failed to load Haar Cascade XML models from OpenCV!")


def preprocess_frame(img_bgr):
    """
    PREPROCESSING PIPELINE:
    1. Grayscale: Intensity contrast is what Haar features evaluate.
    2. Histogram Equalization: Stretches pixel intensity distribution, improving
       contrast under uneven lighting or harsh shadows.
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    equalized_gray = cv2.equalizeHist(gray)
    return gray, equalized_gray


def process_face_detection(frame):
    """
    HIERARCHICAL DETECTION PIPELINE:
    Takes an input BGR frame, detects faces, and performs nested eye detection.
    
    Returns:
        annotated_frame: Frame with bounding boxes, markers, and HUD analytics.
        analytics: Dictionary containing counts and detection metadata.
    """
    annotated = frame.copy()
    gray, equalized = preprocess_frame(frame)
    
    # --------------------------------------------------------------------------
    # STEP 1: DETECT PRIMARY FACES
    # --------------------------------------------------------------------------
    # scaleFactor=1.1: Multi-scale image pyramid steps down by 10% each pass.
    # minNeighbors=5: Candidate rectangle must have >= 5 neighbor boxes (removes noise).
    # minSize=(40, 40): Filters out tiny false positive artifacts.
    # --------------------------------------------------------------------------
    faces = face_cascade.detectMultiScale(
        equalized,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    face_details = []
    
    for i, (fx, fy, fw, fh) in enumerate(faces, start=1):
        # Draw bounding box for Face (Vibrant Green)
        cv2.rectangle(annotated, (fx, fy), (fx + fw, fy + fh), (0, 230, 115), 2)
        
        # ----------------------------------------------------------------------
        # STEP 2: REGION OF INTEREST (ROI) EXTRACTION FOR EYES
        # ----------------------------------------------------------------------
        # Why ROI? Slicing the face boundary reduces computational search space
        # from O(W_img * H_img) to O(w_face * h_face) and eliminates false positives.
        # Restricting vertical height to the upper 60% prevents detecting nostrils/lips as eyes.
        # ----------------------------------------------------------------------
        face_roi_gray = equalized[fy:fy + fh, fx:fx + fw]
        upper_face_roi = face_roi_gray[0:int(fh * 0.6), :]
        
        eyes = eye_cascade.detectMultiScale(
            upper_face_roi,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(15, 15),
            maxSize=(int(fw * 0.4), int(fh * 0.4))
        )
        
        for (ex, ey, ew, eh) in eyes:
            # Draw eye bounding circle (Cyan/Sky Blue)
            center = (fx + ex + ew // 2, fy + ey + eh // 2)
            radius = int(round((ew + eh) * 0.25))
            cv2.circle(annotated, center, radius, (255, 191, 0), 2)
        
        # ----------------------------------------------------------------------
        # STEP 3: RENDER HUD BADGE OVER EACH FACE
        # ----------------------------------------------------------------------
        label = f"Face #{i} | Eyes: {len(eyes)}"
        (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.rectangle(annotated, (fx, fy - text_h - 10), (fx + text_w + 6, fy), (0, 0, 0), -1)
        cv2.putText(annotated, label, (fx + 3, fy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        
        face_details.append({
            "id": i,
            "box": (fx, fy, fw, fh),
            "eyes_count": len(eyes)
        })
    
    # Summary banner on top-left
    summary_text = f"Faces: {len(faces)}"
    cv2.rectangle(annotated, (10, 10), (140, 45), (30, 30, 30), -1)
    cv2.putText(annotated, summary_text, (20, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 200), 2, cv2.LINE_AA)
    
    return annotated, {
        "faces_detected": len(faces),
        "details": face_details
    }


def run_image_mode(image_path='sample_face.png', output_path='output_detected_face.png'):
    """Processes a static image from disk, prints diagnostics, and displays results."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_img_path = os.path.join(script_dir, image_path) if not os.path.isabs(image_path) else image_path
    
    if not os.path.exists(full_img_path):
        if os.path.exists(image_path):
            full_img_path = image_path
        else:
            print(f"[!] Error: Image file '{image_path}' could not be found.")
            return

    print(f"\n[*] Loading image from: {full_img_path}")
    img = cv2.imread(full_img_path)
    if img is None:
        print("[!] Error: OpenCV was unable to decode the image file.")
        return

    # Benchmark execution latency
    start_time = time.time()
    annotated_img, analytics = process_face_detection(img)
    latency_ms = (time.time() - start_time) * 1000

    print("\n" + "=" * 60)
    print("           FACE & EYE DETECTION ANALYTICS REPORT            ")
    print("=" * 60)
    print(f" Image Dimensions     : {img.shape[1]}x{img.shape[0]} px")
    print(f" Processing Latency   : {latency_ms:.2f} ms")
    print(f" Total Faces Detected : {analytics['faces_detected']}")
    print("-" * 60)
    
    for face in analytics['details']:
        fx, fy, fw, fh = face['box']
        print(f" -> Face #{face['id']}: Coords=(x:{fx}, y:{fy}), Size=({fw}x{fh}) px | Eyes Detected={face['eyes_count']}")
    print("=" * 60)

    # Save output image
    full_output_path = os.path.join(script_dir, output_path)
    cv2.imwrite(full_output_path, annotated_img)
    print(f"[+] Annotated result saved to: {full_output_path}")

    print("\n[+] Displaying GUI window. Press ANY key on the window to close it...")
    cv2.imshow("Face & Eye Detection (Press Any Key to Close)", annotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam_mode():
    """Starts real-time live webcam video detection stream with FPS counter."""
    print("\n[*] Initializing Camera Stream (Device Index 0)...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[!] Error: Could not access the webcam. Please verify camera permissions.")
        return

    print("[+] Webcam stream started!")
    print("    - Press 'q' on the video window to EXIT.")
    print("    - Press 's' to save a snapshot.")

    prev_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[!] Failed to capture frame from webcam.")
            break

        # Calculate Real-Time FPS
        current_time = time.time()
        fps = 1.0 / (current_time - prev_frame_time) if prev_frame_time != 0 else 0
        prev_frame_time = current_time

        annotated_frame, analytics = process_face_detection(frame)

        # FPS badge
        cv2.putText(
            annotated_frame, 
            f"FPS: {fps:.1f}", 
            (20, annotated_frame.shape[0] - 20), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.6, 
            (0, 255, 0), 
            2, 
            cv2.LINE_AA
        )

        cv2.imshow("Live Face Detection (Press 'q' to Quit, 's' to Save)", annotated_frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("[*] Exiting webcam stream...")
            break
        elif key == ord('s'):
            snapshot_name = f"snapshot_{int(time.time())}.png"
            cv2.imwrite(snapshot_name, annotated_frame)
            print(f"[+] Saved snapshot to '{snapshot_name}'")

    cap.release()
    cv2.destroyAllWindows()


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
if __name__ == '__main__':
    print("=" * 65)
    print("        EXPERIMENT 04: FACE & EYE DETECTION SYSTEM              ")
    print("=" * 65)
    print("Select Execution Mode:")
    print(" [1] Static Image Detection (Default: sample_face.png)")
    print(" [2] Real-Time Live Webcam Stream")
    
    choice = input("\nEnter your choice (1 or 2, default: 1): ").strip()
    
    if choice == '2':
        run_webcam_mode()
    else:
        user_path = input("Enter path to image (Press Enter for 'sample_face.png'): ").strip()
        if not user_path:
            user_path = 'sample_face.png'
        run_image_mode(user_path)
