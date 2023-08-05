from xlrd import open_workbook
from xlwt import *
from xlutils.copy import copy


#path = '/dbfs/mnt/stage/greenleaf/Test/Bhavsik/CSV/'

Experiment = dbutils.widgets.get("Experiment")
Model = dbutils.widgets.get("Model")
Dataset = dbutils.widgets.get("Dataset")
Corridor = dbutils.widgets.get("Corridor")
DeliveryDate = dbutils.widgets.get("Delivery Date")
Change = dbutils.widgets.get("Change")
BronzeDataConversionHoliday = dbutils.widgets.get("Bronze - Data Conversion Holiday")
BronzeDataConversionNonHoliday = dbutils.widgets.get("Bronze - Data Conversion Non-Holiday")
BronzeDataCleanup = dbutils.widgets.get("Bronze - Data Cleanup")
SilverUnscaleAllFeaturesHoliday = dbutils.widgets.get("Silver - Unscale All Features Holiday")
SilverUnscaleAllFeaturesNonHoliday = dbutils.widgets.get("Silver - Unscale All Features Non-Holiday")
GoldDataSplit = dbutils.widgets.get("Gold - Data Split")
FeaturesAdded = dbutils.widgets.get("Features Added")
InputFolderPath = dbutils.widgets.get("Input Folder Path")
DataIssues = dbutils.widgets.get("Data Issues")
ModelObservations = dbutils.widgets.get("Model Observations")
OutputModel  = dbutils.widgets.get("Output Model #")
Metrics = dbutils.widgets.get("Metrics")
Comments = dbutils.widgets.get("Comments")

list = [Experiment,Model,Dataset,Corridor,DeliveryDate,Change,BronzeDataConversionHoliday,BronzeDataConversionNonHoliday,BronzeDataCleanup,SilverUnscaleAllFeaturesHoliday,SilverUnscaleAllFeaturesNonHoliday,GoldDataSplit,FeaturesAdded,InputFolderPath,DataIssues,ModelObservations,OutputModel,Metrics,Comments]

  
rb = open_workbook("/dbfs/mnt/stage/greenleaf/Test/Bhavsik/CSV/Test7.xls",formatting_info=True)
wb = copy(rb)
sheet1 = rb.sheet_by_name('Sheet1')
#style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')

s = wb.get_sheet(0)
rows = sheet1.nrows
print(rows)
columns = sheet1.ncols 
i=0

if (sheet1.cell(0,columns-1).value) == Experiment:
  currentcolumn = columns-1
  for val in list:
    if len(sheet1.cell(i,currentcolumn).value) == 0:
      s.write(i,currentcolumn,val)
      #print(val)
      i+=1
    else :
      s.write(i,currentcolumn,sheet1.cell(i,currentcolumn).value)
      #print(val)
      i+=1
  print(currentcolumn)
else:
  currentcolumn = columns
  for val in list:
    s.write(i,currentcolumn,val)
    #print(val)
    i+=1
  print(currentcolumn)

wb.save('/dbfs/mnt/stage/greenleaf/Test/Bhavsik/CSV/Test7.xls')