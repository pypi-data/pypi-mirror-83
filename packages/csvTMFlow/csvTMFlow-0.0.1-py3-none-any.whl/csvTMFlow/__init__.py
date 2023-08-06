import dbutils as dbutils


def get_dbutils_Bronze():
    dbutils.widgets.text("Experiment", "")
    dbutils.widgets.text("Model", "")
    dbutils.widgets.text("Corridor", "")
    dbutils.widgets.text("Dataset", "")
    dbutils.widgets.text("Bronze - Data Conversion", "")
    dbutils.widgets.text("Bronze - Data Cleanup", "")


def get_dbutils_Silver():
    dbutils.widgets.text("Experiment", "")
    dbutils.widgets.text("Silver - Unscale All Features", "")

def Bronze_Update():
  from xlrd import open_workbook
  from xlwt import Workbook
  from xlutils.copy import copy
  Experiment = dbutils.widgets.get("Experiment")
  Model = dbutils.widgets.get("Model")
  Corridor = dbutils.widgets.get("Corridor")
  Dataset = dbutils.widgets.get("Dataset")
  Bronze_Data_Conversion = dbutils.widgets.get("Bronze - Data Conversion")
  Bronze_Data_Cleanup = dbutils.widgets.get("Bronze - Data Cleanup")
  rb = open_workbook("/dbfs/mnt/transcommlpoc/Test/Riddhi/TranscomML.xls",formatting_info=True)
  wb = copy(rb)
  sheet1 = rb.sheet_by_name('TranscomML')
  s = wb.get_sheet(0)
  rows = sheet1.nrows
  print(rows)
  columns = sheet1.ncols
  i=0
  if (sheet1.cell(1,columns-1).value) == Experiment:
    currentcolumn = columns-1
    s.write(0,currentcolumn,Model)
    s.write(1,currentcolumn,Experiment)
    s.write(2,currentcolumn,Dataset)
    s.write(3,currentcolumn,Corridor)
    s.write(6,currentcolumn,Bronze_Data_Conversion)
    s.write(7,currentcolumn,Bronze_Data_Cleanup)
    print(currentcolumn)
  else:
    currentcolumn = columns-1
    s.write(0,currentcolumn,Model)
    s.write(1,currentcolumn,Experiment)
    s.write(2,currentcolumn,Dataset)
    s.write(3,currentcolumn,Corridor)
    s.write(6,currentcolumn,Bronze_Data_Conversion)
    s.write(7,currentcolumn,Bronze_Data_Cleanup)
    print(currentcolumn)


  wb.save('/dbfs/mnt/transcommlpoc/Test/Riddhi/TranscomML.xls')

def Silver_Update():
  from xlrd import open_workbook
  from xlwt import Workbook
  from xlutils.copy import copy
  Experiment = dbutils.widgets.get("Experiment")
  Silver_Unscale_All_Features = dbutils.widgets.get("Silver - Unscale All Features")
  rb = open_workbook("/dbfs/mnt/transcommlpoc/Test/Riddhi/TranscomML.xls",formatting_info=True)
  wb = copy(rb)
  sheet1 = rb.sheet_by_name('TranscomML')
  s = wb.get_sheet(0)
  rows = sheet1.nrows
  print(rows)
  columns = sheet1.ncols
  i=0
  if (sheet1.cell(1,columns-1).value) == Experiment:
    currentcolumn = columns-1
    s.write(8,currentcolumn,Silver_Unscale_All_Features)
    print(currentcolumn)
  else:
    currentcolumn = columns-1
    s.write(8,currentcolumn,Silver_Unscale_All_Features)
    print(currentcolumn)


  wb.save('/dbfs/mnt/transcommlpoc/Test/Riddhi/TranscomML.xls')