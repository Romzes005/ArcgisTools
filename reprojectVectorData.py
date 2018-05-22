import arcpy

arcpy.env.workspace = r"E:\_Sheva\course_3_geoinf\Python_2\GIT\p_6\Lesson2"
inputFC = r"E:\_Sheva\course_3_geoinf\Python_2\GIT\p_6\Lesson2\CountyLines.shp"

# get spatial reference for the input feature class
inputDescribe = arcpy.Describe(inputFC)
inputSR = inputDescribe.SpatialReference
inputSRName = inputSR.Name

# create a list of FC
listFC = arcpy.ListFeatureClasses()

for fc in listFC:
    fcDescribe = arcpy.Describe(fc)
    fcSR = fcDescribe.SpatialReference
    fcSRName = fcSR.Name

    if fcSRName != inputSRName:
        print "The coordinate system has been changed to " + str(inputSRName)
    else:
        print "The coordinate system has not been changed"

    if fcSRName == inputSRName:
        continue
    else:
        # create output feature class path and it's name
        outFS = fc[:-4] + "_projected.shp"
        arcpy.Project_management(fc, outFS, inputSR)
        print outFS