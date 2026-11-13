import sys, math, os
import numpy as np
from PIL import Image
import rig, pipeline, anim
import rig_96 as R96
_orig = rig.build
def _b(who, pose, D):
    if who in R96.CFG96: return R96.build96(who, pose, D)
    return _orig(who, pose, D)
rig.build = _b; pipeline.build = _b
_pf = anim.pose_for
def pf(who, a, k, yaw):
    if who in R96.CFG96: return R96.pose96(who, a, k, yaw)
    return _pf(who, a, k, yaw)
def fr(who, a, k, yaw_deg):
    return pipeline.frame(who, pf(who, a, k, math.radians(yaw_deg)), 0)
if __name__ == '__main__':
    who, a, k, yaw = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
    im = fr(who, a, k, yaw); im.save(f'/home/claude/out96/{who}_{a}_{k}_{int(yaw)}.png'); print(im.size)
