import uuid
import os
import pandas as pd
from tempfile import mkstemp


def qe(df, applyTable = True, name=None):
    fh, abs_path = mkstemp(suffix='.xlsx')

    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    if applyTable:
        writer = pd.ExcelWriter(abs_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']

        index_name = df.index.name
        if index_name is None: index_name = ''
        c = [{'header': str(index_name)}] + [{'header': str(x)} for x in df.columns]

        worksheet.add_table(0, 0, len(df), len(df.columns), {'columns': c})

        writer.save()

    else:
        df.to_excel(abs_path)

    os.close(fh)
    os.system(abs_path)


if __name__ == '__main__':
    pass