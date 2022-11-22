#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from common.geogebra import Geogebra
from common.roadmap import RoadMap

from setups.setup_logger import *
from setups.setup_robot_name import *

def init_roadmap(robot_id, desired_id):
    if robot_id == BORNIBUS_ID:
        setup_logger(INFO ,"Bornibus")
    elif robot_id == R128_ID:
        setup_logger(INFO ,"R128")
    else:
        setup_logger(INFO ,"Not on a robot !")

    if robot_id == desired_id and not UNKNOWN:
        os.chdir("/home/pi/git/clubrobot/team-2020")

    roadmap_path = None
    for root, dirs, files in os.walk("."):
        for file in files:
            if desired_id == BORNIBUS_ID:
                if file == "bornibus.ggb":
                    roadmap_path = os.path.join(root, file)
            elif desired_id == R128_ID:
                if file == "128.ggb":
                    roadmap_path = os.path.join(root, file)

    geo  = Geogebra(roadmap_path)
    road = RoadMap.load(geo)

    return geo, road

