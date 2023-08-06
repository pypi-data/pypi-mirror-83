import matplotlib.pyplot as plt

from weldx.transformations import CoordinateSystemManager

csm_global = CoordinateSystemManager("root", "global coordinate systems")
csm_global.create_cs("specimen", "root", coordinates=[1, 2, 3])
csm_global.create_cs("robot head", "root", coordinates=[4, 5, 6])

csm_specimen = CoordinateSystemManager("specimen", "specimen coordinate systems")
csm_specimen.create_cs("thermo couple 1", "specimen", coordinates=[1, 1, 0])
csm_specimen.create_cs("thermo couple 2", "specimen", coordinates=[1, 4, 0])

csm_robot = CoordinateSystemManager("robot head", "robot coordinate systems")
csm_robot.create_cs("torch", "robot head", coordinates=[0, 0, -2])
csm_robot.create_cs("mount point 1", "robot head", coordinates=[0, 1, -1])
csm_robot.create_cs("mount point 2", "robot head", coordinates=[0, -1, -1])

csm_scanner = CoordinateSystemManager("scanner", "scanner coordinate systems")
csm_scanner.create_cs("mount point 1", "scanner", coordinates=[0, 0, 2])

csm_robot.merge(csm_scanner)
csm_global.merge(csm_robot)
csm_global.merge(csm_specimen)
csm_global.plot()
plt.show()
