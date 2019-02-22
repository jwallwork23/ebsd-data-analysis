import numpy as np
from math import cos, sin, acos


def orientation_matrix(euler_angle):
    """
    Assemble orientation matrix associated with given Euler angle.
    """

    # Convert from degrees to radians
    phi1 = np.deg2rad(euler_angle[0])
    Phi  = np.deg2rad(euler_angle[1])
    phi2 = np.deg2rad(euler_angle[2])

    # Assemble orientation matrix
    M = np.zeros([3, 3])
    M[0,0] = cos(phi1)*cos(phi2) - sin(phi1)*sin(phi2)*cos(Phi)
    M[0,1] = sin(phi1)*cos(phi2) + cos(phi1)*sin(phi2)*cos(Phi)
    M[0,2] = sin(phi2)*sin(Phi)
    M[1,0] = -cos(phi1)*sin(phi2) - sin(phi1)*cos(phi2)*cos(Phi)
    M[1,1] = -sin(phi1)*sin(phi2) + cos(phi1)*cos(phi2)*cos(Phi)
    M[1,2] = cos(phi2)*sin(Phi)
    M[2,0] = sin(phi1)*sin(Phi)
    M[2,1] = -cos(phi1)*sin(Phi)
    M[2,2] = cos(Phi)
    return M


def compute_misorientation(euler_angle1, euler_angle2):
    """
    Compute misorientation between two given Euler angles.
    """

    # Assemble orientation matrices
    M1 = orientation_matrix(euler_angle1)
    M2 = orientation_matrix(euler_angle2)

    # Calculate misorientation
    M = np.dot(M1, np.linalg.inv(M2))

    # Get angle
    cosTheta = (M[0,0]+M[1,1]+M[2,2]-1.)/2
    eps = 1e-6
    if 1-eps < cosTheta < 1+eps:
        cosTheta = 1

    return np.rad2deg(acos(cosTheta))
