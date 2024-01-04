
import os
from datetime import datetime

def get_file_ctime(filePath: str) -> str:
    if os.path.exists(filePath) == True:
        file_c_time = os.path.getctime(filePath)
        date_at = datetime.fromtimestamp(file_c_time).strftime('%Y/%m/%d %H:%M')
        return date_at
    else:
        return None