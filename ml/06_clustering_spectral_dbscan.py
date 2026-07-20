# 6. Implementation and comparison of various clustering techniques such as Spectral and DBSCAN.

from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import SpectralClustering, DBSCAN
import matplotlib.pyplot as plt

# Generate non-linear dummy data (make_moons is great for testing these algorithms)
# Replace this with your Kaggle dataset for real applications
X, y = make_moons(n_samples=300, noise=0.05, random_state=42)

# Scale data (Crucial for DBSCAN and Spectral)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 1. Spectral Clustering
spectral = SpectralClustering(n_clusters=2, affinity='nearest_neighbors', random_state=42)
spectral_labels = spectral.fit_predict(X_scaled)

# 2. DBSCAN
# eps: max distance between samples, min_samples: core point threshold
dbscan = DBSCAN(eps=0.3, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_scaled)

# Plotting the comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Spectral Plot
axes[0].scatter(X[:, 0], X[:, 1], c=spectral_labels, cmap='viridis', s=50)
axes[0].set_title('Spectral Clustering')

# DBSCAN Plot
axes[1].scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap='plasma', s=50)
axes[1].set_title('DBSCAN Clustering')

plt.suptitle("Clustering Comparison (Non-linear Data)")
plt.show()

print("Comparison:")
print("- Spectral Clustering requires the number of clusters to be specified in advance.")
print("- DBSCAN automatically finds the number of clusters based on density and can identify outliers (labeled as -1).")
