import os

for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename.lower() == "desktop.ini":
            file_path = os.path.join(root, filename)
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")