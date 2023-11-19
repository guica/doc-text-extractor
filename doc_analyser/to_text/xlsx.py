import pandas as pd

def convert_xlsx_to_txt(path):
    xls = pd.ExcelFile(path)
    result = {}
    result['full'] = ''

    for i, sheet in enumerate(xls.sheet_names):
        try:
            df = pd.read_excel(xls, sheet, header=None)
        except:
            print('Could not sheet {} on excel {}'.format(sheet, path))
            continue
        if not df.empty:
            sheet_content = df.to_string(index=False, header=False, na_rep='')
            result[str(i+1)] = sheet_content
            result['full'] += sheet_content

    return result