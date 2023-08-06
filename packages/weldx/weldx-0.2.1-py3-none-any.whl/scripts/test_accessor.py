import pandas as pd

import weldx

lcs = weldx.transformations.LocalCoordinateSystem(
    coordinates=[[1, 0, 0], [1, 2, 3]], time=pd.TimedeltaIndex(["0s", "2s"])
)
c = lcs.coordinates
c.weldx.time_ref = pd.Timestamp("2020-01-01 00:00:00")
print(c.time)
c.weldx.time_ref = pd.Timestamp("2020-01-01 00:00:01")
print(c.time)

buffer = weldx.asdf.utils._write_buffer({"LCS": lcs})
weldx.asdf.utils.notebook_fileprinter(buffer)
