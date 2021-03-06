import arcpy

facilitshp = arcpy.GetParameterAsText(0)
zipshp = arcpy.GetParameterAsText(1)
resultsWorkspace = arcpy.GetParameterAsText(2)
distance = arcpy.GetParameterAsText(3) #3000
fieldName = arcpy.GetParameterAsText(4) #FACILITY
fieldvalue = arcpy.GetParameterAsText(5) #COLLEGE
arcpy.env.workspace = resultsWorkspace
arcpy.env.overwriteOutput = True

# make feature layers, select within a distance and certain attributes
arcpy.MakeFeatureLayer_management(facilitshp, 'facilit')
arcpy.MakeFeatureLayer_management(zipshp, 'zip')
arcpy.AddMessage('Making feature layers')
arcpy.SelectLayerByLocation_management('facilit', 'WITHIN_A_DISTANCE', 'zip', distance+' meters', 'NEW_SELECTION')
arcpy.SelectLayerByAttribute_management("facilit", "SUBSET_SELECTION", "{} = '{}'".format(fieldName, fieldvalue))
arcpy.AddMessage('Selecting objects within ' + distance + " meters with '{}' values in the field '{}'".format(fieldvalue, fieldName))


# create a new feature class similar to facilities.shp in Results directory
res_shp = "facilities_Distance_"+distance+'.shp'
arcpy.CreateFeatureclass_management(arcpy.env.workspace, res_shp, "POINT", spatial_reference="facilit")

#create new fields
insertfields = ['ADDRESS', 'NAME', 'FACILITY']
for f in insertfields:
    arcpy.AddField_management(res_shp, f, "TEXT")

searchFields = ('SHAPE@XY', 'ADDRESS', 'NAME', 'FACILITY')
with arcpy.da.InsertCursor(res_shp, searchFields) as cursorInsert, arcpy.da.SearchCursor("facilit", searchFields) as cursorSearch:
    for row in cursorSearch:
        cursorInsert.insertRow(row)
arcpy.AddMessage("Updated fields: ".format(str(searchFields)))


# facilities_Distance_3000.shp COLLEGE_NAME
newfield = fieldvalue[:5] + '_NAME'
arcpy.AddField_management(res_shp, newfield, "DOUBLE")

searchvalues = []
with arcpy.da.SearchCursor("facilit", ('FAC_ID',)) as cursor:
    for row in cursor:
        searchvalues.append(row)
arcpy.AddMessage(str(len(searchvalues)))
with arcpy.da.UpdateCursor(res_shp, (newfield)) as cursor:
    i = 0
    for row in cursor:
        row = searchvalues[i]
        cursor.updateRow(row)
        i += 1


# add the result to display
mxd = arcpy.mapping.MapDocument("CURRENT")
dataframe = arcpy.mapping.ListDataFrames(mxd, "*")[0]
addLayer = arcpy.mapping.Layer(res_shp)
arcpy.mapping.AddLayer(dataframe, addLayer, "AUTO_ARRANGE")
arcpy.AddMessage("Added '{}' to display".format(res_shp))
del addLayer, mxd, dataframe

