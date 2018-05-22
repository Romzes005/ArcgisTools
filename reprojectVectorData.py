import arcpy

arcpy.env.workspace = arcpy.GetParameterAsText(0)
inputFC = arcpy.GetParameterAsText(1)

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
        arcpy.AddMessage("The coordinate system has been changed to " + str(inputSRName))
    else:
        print "The coordinate system has not been changed"
        arcpy.AddMessage("The coordinate system has not been changed")

    if fcSRName == inputSRName:
        continue
    else:
        # create output feature class path and it's name
        outFS = fc[:-4] + "_projected.shp"
        arcpy.Project_management(fc, outFS, inputSR)
        print outFS
        arcpy.AddMessage(str(outFS))
