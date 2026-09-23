import os
import glob
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def extract_leaf_features(img_bgr):
    # Resize and convert to HSV color space
    img_resized = cv2.resize(img_bgr, (256, 256))
    hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)
    
    # 1. Total leaf mask
    leaf_mask = cv2.inRange(hsv, np.array([5, 30, 20]), np.array([120, 255, 255]))
    total_pixels = np.count_nonzero(leaf_mask) + 1e-6
    
    # 2. Healthy green tissue (H: 35-85)
    green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
    green_ratio = np.count_nonzero(green_mask) / total_pixels
    
    # 3. Diseased lesion tissue (H: 8-32)
    disease_mask = cv2.inRange(hsv, np.array([8, 50, 40]), np.array([32, 255, 255]))
    disease_ratio = np.count_nonzero(disease_mask) / total_pixels
    
    mean_hue = np.mean(hsv[:, :, 0][leaf_mask > 0]) if np.any(leaf_mask) else 0
    mean_sat = np.mean(hsv[:, :, 1][leaf_mask > 0]) if np.any(leaf_mask) else 0
    
    # Count disease spot contours
    contours, _ = cv2.findContours(disease_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    spot_count = len([c for c in contours if cv2.contourArea(c) > 15])
    
    return np.array([green_ratio, disease_ratio, mean_hue, mean_sat, spot_count]), leaf_mask, disease_mask


def load_dataset():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(script_dir, 'dataset_leaves')
    
    healthy = glob.glob(os.path.join(dataset_dir, 'healthy', '*.*'))
    diseased = glob.glob(os.path.join(dataset_dir, 'diseased', '*.*'))
    
    paths = healthy + diseased
    labels = [0] * len(healthy) + [1] * len(diseased)
    return paths, labels


def build_dashboard(original_img, disease_mask, label, confidence, lesion_pct, is_diseased):
    H, W = 320, 320
    p1 = cv2.resize(original_img, (W, H))
    
    # Panel 2: Segmented Lesion Mask (Amber on black)
    resized_mask = cv2.resize(disease_mask, (W, H))
    p2 = np.zeros((H, W, 3), dtype=np.uint8)
    p2[resized_mask > 0] = [0, 140, 255]
    
    # Panel 3: Diagnosis Overlay with contours
    p3 = p1.copy()
    contours, _ = cv2.findContours(resized_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(p3, contours, -1, (0, 0, 255), 2)
    p3[resized_mask > 0] = cv2.addWeighted(p3[resized_mask > 0], 0.4, np.full_like(p3[resized_mask > 0], (0, 0, 255)), 0.6, 0)
    
    def add_title(panel, text, bg=(30, 30, 30)):
        cv2.rectangle(panel, (0, 0), (W, 35), bg, -1)
        cv2.putText(panel, text, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        cv2.rectangle(panel, (0, 0), (W, H), (60, 60, 60), 1)

    add_title(p1, "[1] Input Leaf Image")
    add_title(p2, "[2] HSV Lesion Mask")
    add_title(p3, f"[3] AI: {label.split()[0]} ({confidence:.1f}%)", bg=(0, 0, 160) if is_diseased else (0, 140, 0))
    
    # Bottom telemetry
    cv2.rectangle(p3, (0, H - 30), (W, H), (20, 20, 20), -1)
    badge_color = (0, 100, 255) if is_diseased else (0, 255, 120)
    cv2.putText(p3, f"Lesion: {lesion_pct:.1f}% | Spots: {len(contours)}", (10, H - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, badge_color, 1)

    return np.hstack([p1, p2, p3])


if __name__ == '__main__':
    print("EXPERIMENT 06: AGRICULTURAL PLANT LEAF HEALTH DIAGNOSIS")
    
    # 1. Load dataset
    paths, labels = load_dataset()
    print(f"[*] Dataset: {len(paths)} images ({labels.count(0)} Healthy, {labels.count(1)} Diseased)")
    
    train_paths, test_paths, y_train, y_test = train_test_split(
        paths, labels, test_size=0.20, random_state=42, stratify=labels
    )
    
    # 2. Extract features
    X_train = [extract_leaf_features(cv2.imread(p))[0] for p in train_paths]
    X_test = [extract_leaf_features(cv2.imread(p))[0] for p in test_paths]
    
    # 3. Train Classifier
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, preds, average='binary', zero_division=0)
    
    print(f"[*] Evaluation: Accuracy: {acc*100:.1f}% | Precision: {prec*100:.1f}% | Recall: {rec*100:.1f}% | F1: {f1*100:.1f}%")
    
    # 4. Test on real holdout image
    test_idx = next(i for i, label in enumerate(y_test) if label == 1)
    test_img_path = test_paths[test_idx]
    
    test_img = cv2.imread(test_img_path)
    feats, _, d_mask = extract_leaf_features(test_img)
    
    probs = model.predict_proba([feats])[0]
    pred = model.predict([feats])[0]
    
    is_diseased = (pred == 1)
    pred_label = "DISEASED (Early Blight / Spot)" if is_diseased else "HEALTHY CROP LEAF"
    confidence = probs[pred] * 100
    lesion_pct = feats[1] * 100
    
    print(f"\nTest Sample : {os.path.basename(test_img_path)}")
    print(f"Diagnosis   : {pred_label} ({confidence:.1f}% confidence)")
    print(f"Infected Area: {lesion_pct:.1f}% | Spot Clusters: {int(feats[4])}")
    
    # 5. Render & display dashboard
    dashboard = build_dashboard(test_img, d_mask, pred_label, confidence, lesion_pct, is_diseased)
    
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_leaf_diagnosis.png')
    cv2.imwrite(out_path, dashboard)
    print(f"[+] Output saved: {out_path}")
    
    cv2.imshow("Plant Leaf Diagnosis Dashboard", dashboard)
    cv2.waitKey(0)
    cv2.destroyAllWindows()