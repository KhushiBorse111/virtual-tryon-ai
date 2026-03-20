import numpy as np

# Function to calculate alignment transformation based on given keypoints

def calculate_transformation(src_keypoints, dst_keypoints):
    assert len(src_keypoints) == len(dst_keypoints), "Keypoints count mismatch"

    # Convert keypoints to numpy arrays for matrix operations
    src_points = np.array(src_keypoints)
    dst_points = np.array(dst_keypoints)

    # Calculate centroids of the keypoints
    src_centroid = np.mean(src_points, axis=0)
    dst_centroid = np.mean(dst_points, axis=0)

    # Center the points around the centroids
    src_centered = src_points - src_centroid
    dst_centered = dst_points - dst_centroid

    # Compute the covariance matrix
    cov_matrix = np.dot(src_centered.T, dst_centered)

    # Singular Value Decomposition
    U, S, Vt = np.linalg.svd(cov_matrix)
    R = np.dot(Vt.T, U.T)  # Rotation matrix

    # Ensure a right-handed coordinate system
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = np.dot(Vt.T, U.T)

    # Calculate translation
    translation = dst_centroid - np.dot(R, src_centroid)

    return R, translation

# Function to apply transformation to a set of points
def apply_transformation(points, R, translation):
    return np.dot(points, R.T) + translation
