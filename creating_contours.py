# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Import arcpy module

import arcpy
arcpy.env.overwriteOutput = True



try:
    # Local variables:
    inRaster = arcpy.GetParameterAsText(0)
    outContours = arcpy.GetParameterAsText(1)

    # Process: Contour
    arcpy.gp.Contour_sa(inRaster, outContours, "25", "0", "1")

    # Report a success message
    arcpy.AddMessage("All done!")
except:
    # Report an error messages
    arcpy.AddError("Could not complete the buffer")

    # Report any error messages that the Buffer tool might have generated
    arcpy.AddMessage(arcpy.GetMessages())




