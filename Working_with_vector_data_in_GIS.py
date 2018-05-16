import arcpy


facilitshp = r'C:\Rwork\s_10\Progr_GIS_s11\facilities.shp'
zipshp = r'C:\Rwork\s_10\Progr_GIS_s11\zip.shp'
resultsWorkspace = r'C:\Rwork\s_10\Progr_GIS_s11\Results'
distance = 3000
fieldName = 'FACILITY'
fieldvalue = 'COLLEGE'


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



