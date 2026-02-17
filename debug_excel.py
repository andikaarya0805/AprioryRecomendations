import sys
import os
print(f"Python Executable: {sys.executable}")
print(f"CWD: {os.getcwd()}")
try:
    import pandas as pd
    print("Pandas imported successfully")
    try:
        df = pd.read_excel('d:/dika/tugas/Apriori_Recommendations/packages (1).xlsx')
        print(df.head(10).to_string())
        print('\nColumns:', df.columns.tolist())
    except Exception as e:
        print(f"Error reading excel: {e}")
except ImportError as e:
    print(f"Import Error: {e}")
