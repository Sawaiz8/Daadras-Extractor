import zipfile
import io
import pandas as pd
import os

def load_file_as_dataframe(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1]
    if file_extension in ['xlsx', 'ods']:
        return pd.read_excel(uploaded_file, engine='openpyxl')
    elif file_extension == 'xls':
        return pd.read_excel(uploaded_file, engine='xlrd')
    elif file_extension == 'csv':
        return pd.read_csv(uploaded_file)
    else:
        return None
