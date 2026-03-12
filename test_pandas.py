import sys
print(sys.executable)
try:
    import pandas
    print("Pandas imported successfully")
except ImportError as e:
    print(f"Error importing pandas: {e}")
