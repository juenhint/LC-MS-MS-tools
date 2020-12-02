#helpers
import pandas as pd
import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

def getExcel(import_file_path):
    try:
        df = pd.DataFrame()
        df = pd.read_excel (import_file_path, header = 6, usecols = "A:DI")
        df.rename(columns=lambda x: x.replace(".", "_"), inplace = True)
        df = df.loc[df['MS_MS_spectrum'].notnull()]
        #df = df.loc[df['Flag'].isnull()]
        return df
    except:
        raise
    else:
        print(df.columns)
        print(df.shape)
        
def createmsts(df, workingfolder):
    export_path = os.path.join(workingfolder, "MAT")
    if (not os.path.isdir(export_path)): 
        os.mkdir(export_path)
    try:
        for row in df.itertuples(index=False, name="metabo"):
            name = getattr(row, 'Feature_ID')
            f = open(f"{export_path}\\{name}.mat", "w")
            f.write(f"NAME: {name}\n")
            f.write(f"PRECURSORMZ: {getattr(row, 'Average_Mz')}\n")
            f.write(f"PRECURSORTYPE: {getattr(row, 'Adduct_type')}\n")
            f.write(f"IONMODE: {getattr(row, 'Ion_type')}\n")
            f.write("MSTYPE: MS1\n")
            ms1 = str(getattr(row, 'MS1_isotopic_spectrum'))
            ms = ms1.replace(":", "\t")
            m = ms.split(" ")
            f.write(f"Num Peaks: {len(m)}\n")
            for peak in m:
                f.write(f"{peak}\n")
            msms = str(getattr(row, 'MS_MS_spectrum'))
            if (msms != "nan"):
                msm = msms.replace(":", "\t")
                mm = msm.split(" ")
                f.write("MSTYPE: MS2\n")
                f.write(f"Num Peaks: {len(mm)}\n")
                for peak in mm:
                    f.write(f"{peak}\n")
            f.close()
    except:
        raise
    else:
        print("Files created")

def mergeSheets(metadata, cnumber, merged):
    header = openpyxl.Workbook()    
    for r in range(1, metadata.active.max_row+1):
        for c in range(1, metadata.active.max_column+1):
            header.active.cell(row = r, column = c, value = metadata.active.cell(r,c).value)
    header.active.insert_cols(1, cnumber)
    
    for r in dataframe_to_rows(merged, index=False, header=True):
        header.active.append(r)
    return header

def getDataExcel(path, sheet):
    try:
        #import_file_path = os.path.join(workingfolder, filename)
        crn = getCorners(sheet)
        df = pd.read_excel (path, header = crn[0], usecols = range(crn[1],crn[3]))
        df.rename(columns=lambda x: x.replace(".", "_"), inplace = True)
        df.index = df.iloc[:, 0]
    except:
        raise
    return df

def getExcel(path, sheet):
    try:
        #import_file_path = os.path.join(workingfolder, filename)
        crn = getCorners(sheet)
        df = pd.read_excel (path, header = crn[0], usecols = range(0, crn[1]))
        df.rename(columns=lambda x: x.replace(".", "_"), inplace = True)
        df.index = df["Feature_ID"]
    except:
        raise
    return df

def getrExcel(path):
    try:
        #import_file_path = os.path.join(workingfolder, filename)
        df = pd.read_csv(path, delimiter='\t')
        df.rename(columns=lambda x: x.replace(".", "_"), inplace = True)
        df.index = df["File name"]
        df = df.iloc[:, range(7,28)]
    except:
        raise
    return df

def getCorners(sheet):
    corner = [0,0,0,0]
    corner[2] = sheet.max_row
    corner[3] = sheet.max_column
    for i in range(1, sheet.max_row):
        corner[0] = i-1;
        if (sheet.cell(i,1).value != None):
            break
    for i in range(1, sheet.max_column):
        corner[1] = i-1;
        if (sheet.cell(1,i).value != None):
            break
    return corner

def makeMetadata(sheet):
    metadata = openpyxl.Workbook()
    crnr = getCorners(sheet)
    md = metadata.active
    rr = 1
    for r in range(1, crnr[0]+1):
        cc = 1
        for c in range(crnr[1]+1, crnr[3]+1):
            value = sheet.cell(r, c).value
            md.cell(rr, cc,).value = value
            cc += 1
        rr += 1
    return metadata
