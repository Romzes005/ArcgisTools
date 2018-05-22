import arcpy

arcpy.env.workspace = r"C:\Rwork\s_10\Lesson2"
inputFC = r"C:\Rwork\s_10\Lesson2\CountyLines.shp"

# get spatial reference for the input feature class
inputDescribe = arcpy.Describe(inputFC)
inputSR = inputDescribe.SpatialReference
inputSRName = inputSR.Name

# create a list of FC
listFC = arcpy.ListFeatureClasses()
