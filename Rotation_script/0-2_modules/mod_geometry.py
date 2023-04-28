import numpy as np
from numpy.linalg import    norm        as norm
from numpy import           subtract    as sub
from scipy.spatial.transform import Rotation as R


def rad_to_grad(rad):
    return 360*rad/(2*np.pi)

def revolve(vec,angle,ax):
    rotation = R.from_rotvec(-1*ax*angle)
    return rotation.apply(vec)

def get_dihedral(vec1, vec2, axis):
    n1=np.cross(vec1,axis)
    n2=np.cross(vec2,axis)
    ang = np.arccos(  np.dot(n1,n2) / (norm(n1)*norm(n2))  )

    sign_help=np.cross(n1,-1*axis)
    sign_num=np.dot(n2,sign_help)
    if sign_num>0:
        ang = 2*np.pi - ang
    return -ang     # we obtained the angle mathematical (counter-clockwise) Gaussian is opposite

# https://byjus.com/maths/dihedral-angle/
def rotate(points,frame):
    v=frame[0]
    ax      = sub( v[2],v[1] )
    vec1    = sub( v[0],v[1] )
    vec2    = sub( v[3],v[2] )
    ang=-float(frame[1])/360*np.pi*2  # mathematical angle (opposite)
    ang_cur = -get_dihedral( vec1, vec2, ax ) #mathematical angle
    ang=ang - ang_cur
    if ang<0:
        ang     = 2*np.pi + ang
    zeropt       =v[1]
    ax          /=norm(ax)
    tmp_ar=[]
    for pt in points:
        pt_tra       = sub(pt,zeropt)
        pt_tra_rot   = revolve(pt_tra,ang,ax)
        pt_rot       = np.add(pt_tra_rot,zeropt)
        tmp_ar.append(pt_rot)
    return tmp_ar

def mirror(points,frame):
    print("!!!!mirror not yet implemented")
    return(points)

def coor_ass(coor,labels):
    tmp_ar=[]
    for i in labels:
        tmp_ar.append(coor[i])
    return tmp_ar

def run_operation(coor,operation,excluded):
    if operation[0]=='exclude':
        return coor, excluded+operation[1]
    else:
        tmp_ar  =coor_ass(coor,operation[1])
        if operation[0]=='mirror':
            frame   =coor_ass(coor,operation[2])
        elif operation[0]=='rotate':
            frame    =[coor_ass(coor,operation[2][0]), operation[2][1]]
        else:
            quit("Something wrong about the input of the operation-frame")
        tmp_ar  =globals()[operation[0]](tmp_ar,frame)
        i=0
        for point in tmp_ar:
            coor[operation[1][i]]=point
            i+=1
        return coor,excluded


