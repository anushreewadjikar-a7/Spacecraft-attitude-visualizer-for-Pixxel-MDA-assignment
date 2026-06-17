#Construction of LVLH
import numpy as np
 # Unit vectors
LVLH_X = np.array([1.0, 0.0, 0.0])
LVLH_Y = np.array([0.0, 1.0, 0.0])
LVLH_Z = np.array([0.0, 0.0, 1.0])
def build_lvlh(r, v):
    
    r = np.array(r)          #r= satellite positon vector
    v = np.array(v)          #v=satellite velocity vector
    # np.linalg.norm(r) -|r|=squareroot of (x^2+y^2+z^2) , magnitude of the position vector
    z_lvlh = -r / np.linalg.norm(r)     # z points towards earth center (normalize)

    y_lvlh = -np.cross(r, v)        # r x v ( cross product) angular momentum direction (-ve sign because points opposite)
    y_lvlh = y_lvlh / np.linalg.norm(y_lvlh)

    x_lvlh = np.cross(y_lvlh, z_lvlh)       # vector perpendicular to both y and z
    x_lvlh = x_lvlh / np.linalg.norm(x_lvlh)

    return x_lvlh, y_lvlh, z_lvlh