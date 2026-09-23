"""
================================================================================
EXPERIMENT 06: AGRICULTURAL AI - PLANT LEAF DISEASE DETECTION & CLASSIFICATION
================================================================================
Author: AI Lab Student
Topic: Computer Vision in Agriculture, HSV Feature Extraction, Real Dataset 
       Classification (PlantVillage), and Multi-Panel Visual Analytics.

WHAT THIS SYSTEM DOES:
-----------------------
1. Loads real agricultural plant leaf images from the PlantVillage dataset
   (Healthy vs. Early Blight/Diseased).
2. Converts images to HSV (Hue-Saturation-Value) color space to isolate chlorophyll
   green from necrotic brown/yellow disease lesions independent of lighting.
3. Extracts visual feature vectors:
   - Green Tissue Ratio (H: 35-85)
   - Lesion Area Percentage (H: 8-32)
   - Mean Color Moments (Hue, Saturation)
   - Distinct Lesion Spot Count
4. Trains a Random Forest Classifier on the training split and evaluates performance.
5. Tests directly on a real holdout test leaf image from the dataset itself.
6. Renders and displays an interactive 3-Panel Visual GUI Dashboard:
   - [Panel 1] Original Input Leaf from Dataset
   - [Panel 2] HSV Segmented Lesion Mask
   - [Panel 3] AI Diagnostic Overlay with status badge & infection metrics
================================================================================
"""

import os
import glob
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# ==============================================================================
# 1. COMPUTER VISION FEATURE EXTRACTION PIPELINE
# ==============================================================================
# WHY HSV COLOR SPACE (FOR PROFESSOR / VIVA EXPLANATION):
# - Standard RGB mixes color and intensity, making it vulnerable to sunlight/shadows.
# - HSV decouples 'Hue' (color tint: 35-85 = Green, 8-32 = Yellow/Brown) from
#   'Value' (brightness). This allows robust disease lesion segmentation.
# ==============================================================================

def extract_leaf_features(img_bgr):
    """
    Extracts a 5-dimensional feature vector from a plant leaf image:
    [Green_Ratio, Disease_Ratio, Mean_Hue, Mean_Saturation, Spot_Count]
    """
    img_resized = cv2.resize(img_bgr, (256, 256))
    hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)
    
    # 1. Segment Entire Leaf Area (Ignore background)
    leaf_mask = cv2.inRange(hsv, np.array([5, 30, 20]), np.array([120, 255, 255]))
    total_leaf_pixels = np.count_nonzero(leaf_mask) + 1e-6
    
    # 2. Segment Healthy Green Tissue (Hue between 35 and 85)
    green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
    green_pixels = np.count_nonzero(green_mask)
    
    # 3. Segment Diseased Brown/Yellow Lesions (Hue between 8 and 32)
    disease_mask = cv2.inRange(hsv, np.array([8, 50, 40]), np.array([32, 255, 255]))
    disease_pixels = np.count_nonzero(disease_mask)
    
    # Compute Ratios relative to total leaf area
    green_ratio = green_pixels / total_leaf_pixels
    disease_ratio = disease_pixels / total_leaf_pixels
    
    # Extract mean color in leaf area
    mean_hue = np.mean(hsv[:, :, 0][leaf_mask > 0]) if np.any(leaf_mask) else 0
    mean_sat = np.mean(hsv[:, :, 1][leaf_mask > 0]) if np.any(leaf_mask) else 0
    
    # Count distinct disease spot contours
    contours, _ = cv2.findContours(disease_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    spot_count = len([c for c in contours if cv2.contourArea(c) > 15])
    
    features = np.array([green_ratio, disease_ratio, mean_hue, mean_sat, spot_count])
    return features, leaf_mask, disease_mask


# ==============================================================================
# 2. REAL DATASET LOADER & PREPARATION
# ==============================================================================

def load_real_dataset():
    """Loads healthy and diseased leaf image paths from the local dataset."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(script_dir, 'dataset_leaves')
    
    healthy_paths = glob.glob(os.path.join(dataset_dir, 'healthy', '*.*'))
    diseased_paths = glob.glob(os.path.join(dataset_dir, 'diseased', '*.*'))
    
    image_paths = []
    labels = []
    
    for p in healthy_paths:
        image_paths.append(p)
        labels.append(0)  # 0 = Healthy
        
    for p in diseased_paths:
        image_paths.append(p)
        labels.append(1)  # 1 = Diseased
        
    return image_paths, labels


# ==============================================================================
# 3. VISUAL 3-PANEL DASHBOARD GENERATION
# ==============================================================================

def build_visual_dashboard(original_img, disease_mask, label, confidence, lesion_pct, is_diseased):
    """
    Creates a side-by-side 3-panel visual dashboard:
    [Panel 1: Original Image] | [Panel 2: HSV Lesion Mask] | [Panel 3: AI Diagnosis Overlay]
    """
    H, W = 320, 320
    p1 = cv2.resize(original_img, (W, H))
    
    # Panel 2: Isolated disease mask (Bright Amber Orange on black)
    resized_mask = cv2.resize(disease_mask, (W, H))
    p2 = np.zeros((H, W, 3), dtype=np.uint8)
    p2[resized_mask > 0] = [0, 140, 255]
    
    # Panel 3: Annotated Overlay with contours
    p3 = p1.copy()
    contours, _ = cv2.findContours(resized_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(p3, contours, -1, (0, 0, 255), 2)
    p3[resized_mask > 0] = cv2.addWeighted(p3[resized_mask > 0], 0.4, np.full_like(p3[resized_mask > 0], (0, 0, 255)), 0.6, 0)
    
    # Headers & Banners
    def add_title(panel, title_text, bg_color=(30, 30, 30)):
        cv2.rectangle(panel, (0, 0), (W, 35), bg_color, -1)
        cv2.putText(panel, title_text, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.rectangle(panel, (0, 0), (W, H), (60, 60, 60), 1)

    add_title(p1, "[1] Input Leaf Image")
    add_title(p2, "[2] HSV Lesion Mask")
    
    status_bg = (0, 0, 160) if is_diseased else (0, 140, 0)
    add_title(p3, f"[3] AI: {label.split()[0]} ({confidence:.1f}%)", bg_color=status_bg)
    
    # Telemetry badge on Panel 3 bottom
    telemetry = f"Infection: {lesion_pct:.1f}% | Spots: {len(contours)}"
    cv2.rectangle(p3, (0, H - 30), (W, H), (20, 20, 20), -1)
    badge_color = (0, 100, 255) if is_diseased else (0, 255, 120)
    cv2.putText(p3, telemetry, (10, H - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.48, badge_color, 1, cv2.LINE_AA)

    # Stitch all 3 panels horizontally
    dashboard = np.hstack([p1, p2, p3])
    return dashboard


# ==============================================================================
# MAIN EXECUTION PIPELINE
# ==============================================================================
if __name__ == '__main__':
    print("=" * 65)
    print("   EXPERIMENT 06: AGRICULTURAL PLANT LEAF HEALTH DIAGNOSIS      ")
    print("=" * 65)
    
    # 1. Load dataset paths
    image_paths, labels = load_real_dataset()
    print(f"[*] Loaded Real PlantVillage Dataset: {len(image_paths)} images ({labels.count(0)} Healthy, {labels.count(1)} Diseased)")
    
    # 2. Train-Test Split (80% Train, 20% Test)
    train_paths, test_paths, y_train, y_test = train_test_split(
        image_paths, labels, test_size=0.20, random_state=42, stratify=labels
    )
    
    # 3. Extract Features from Training Set
    print(f"[*] Extracting visual features from {len(train_paths)} training images...")
    X_train = []
    for path in train_paths:
        img = cv2.imread(path)
        feats, _, _ = extract_leaf_features(img)
        X_train.append(feats)
        
    X_test = []
    for path in test_paths:
        img = cv2.imread(path)
        feats, _, _ = extract_leaf_features(img)
        X_test.append(feats)
        
    # 4. Train and Evaluate Random Forest Classifier
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    test_preds = model.predict(X_test)
    acc = accuracy_score(y_test, test_preds)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, test_preds, average='binary', zero_division=0)
    
    print("\n" + "=" * 65)
    print("             MODEL EVALUATION (HOLDOUT TEST SET)             ")
    print("=" * 65)
    print(f" Holdout Test Accuracy : {acc * 100:.2f}%")
    print(f" Precision (Diseased)  : {prec * 100:.2f}%")
    print(f" Recall (Diseased)     : {rec * 100:.2f}%")
    print(f" F1-Score              : {f1 * 100:.2f}%")
    print("=" * 65)
    
    # 5. Automatically Test on a Real Holdout Image from Dataset
    # Pick a real diseased test leaf from the test split
    test_sample_idx = 0
    # Find first diseased sample in test set for vivid demonstration
    for idx, label_val in enumerate(y_test):
        if label_val == 1:
            test_sample_idx = idx
            break
            
    sample_test_path = test_paths[test_sample_idx]
    actual_label = "DISEASED" if y_test[test_sample_idx] == 1 else "HEALTHY"
    
    print(f"\n[*] Running Visual AI Diagnosis on Test Sample: {os.path.basename(sample_test_path)}")
    print(f"    Ground Truth Label : {actual_label}")
    
    test_img = cv2.imread(sample_test_path)
    features, leaf_mask, disease_mask = extract_leaf_features(test_img)
    
    probs = model.predict_proba([features])[0]
    prediction = model.predict([features])[0]
    
    is_diseased = (prediction == 1)
    pred_label = "DISEASED (Early Blight / Leaf Spot)" if is_diseased else "HEALTHY CROP LEAF"
    confidence = probs[prediction] * 100
    lesion_pct = features[1] * 100
    
    # 6. Render 3-Panel Visual Dashboard
    dashboard = build_visual_dashboard(test_img, disease_mask, pred_label, confidence, lesion_pct, is_diseased)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, 'output_leaf_diagnosis.png')
    cv2.imwrite(out_path, dashboard)
    
    print("-" * 65)
    print(f" Predicted Class       : {pred_label}")
    print(f" AI Confidence Score   : {confidence:.2f}%")
    print(f" Lesion Surface Area   : {lesion_pct:.2f}%")
    print(f" Distinct Spot Clusters: {int(features[4])}")
    print(f"[+] 3-Panel Visual Dashboard saved to: {out_path}")
    print("=" * 65)
    
    # 7. Display GUI Window
    print("\n[+] Displaying GUI diagnosis window. Press ANY key on the window to close it...")
    cv2.imshow("Agricultural AI - Plant Leaf Diagnosis (Press Any Key to Close)", dashboard)
    cv2.waitKey(0)
    cv2.destroyAllWindows()