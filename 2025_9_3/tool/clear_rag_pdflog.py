import os
import shutil

logs_folder = os.path.join(os.getcwd(), "Rag/pdf_log")

if os.path.exists(logs_folder):
    for filename in os.listdir(logs_folder):
        file_path = os.path.join(logs_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  
        except Exception as e:
            print(f"刪除 {file_path} 失敗: {e}")
    print("logs 資料夾已清空")
else:
    print("logs 資料夾不存在")