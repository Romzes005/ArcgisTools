# -*- coding: utf-8 -*-
# Import arcpy module
import arcpy

Precip2008Readings = arcpy.GetParameterAsText(0)
Nebraska__2_= arcpy.GetParameterAsText(1)
clipout = arcpy.GetParameterAsText(2)

# Local variables:
IDWout = "C:\\Rwork\\p_6\\Lesson2\\Test.gdb\\IDWout2"
reclassout = "C:\\Rwork\\p_6\\Lesson2\\Test.gdb\\reclassou2"
rasterout = "C:\\Rwork\\p_6\\Lesson2\\Test.gdb\\rasterout2"


# Process: IDW
arcpy.gp.Idw_sa(Precip2008Readings, "RASTERVALU", IDWout, "1850,46466995651", "2", "VARIABLE 12", "")

# Process: Reclassify
arcpy.gp.Reclassify_sa(IDWout, "VALUE", "27715,960938 46615,086060 1;46615,086060 64536,670227 2;64536,670227 82132,407410 3;82132,407410 111132,789063 4", reclassout, "DATA")

# Process: Raster to Polygon
arcpy.RasterToPolygon_conversion(reclassout, rasterout, "SIMPLIFY", "VALUE")

# Process: Clip
arcpy.Clip_analysis(rasterout, Nebraska__2_, clipout, "")
arcpy.env.overwriteOutput = True
