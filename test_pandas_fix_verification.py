
import pandas as pd
import os

# Mock the logic from server.py (Lines 1321-1335)
def test_pandas_fix(combined_data_rows):
    print(f"Testing with {len(combined_data_rows)} rows...")
    
    # Implementing the same logic as server.py
    if not combined_data_rows:
        # If no data collected, create empty DF with expected columns to avoid KeyError
        df = pd.DataFrame(columns=["Keyword", "Page", "Rank", "Landing Page"])
    else:
        df = pd.DataFrame(combined_data_rows)
    
    print("DataFrame columns:", df.columns.tolist())
    print("DataFrame row count:", len(df))
    
    # Test if we can access expected columns (this would fail without the fix if df was empty)
    try:
        # This is a common operation in the app later on (e.g., sorting or calculating stats)
        _ = df["Keyword"]
        print("✅ SUCCESS: Accessed 'Keyword' column without error.")
    except KeyError:
        print("❌ FAILED: 'Keyword' column not found.")

if __name__ == "__main__":
    # Test case 1: Empty results (The crash case)
    print("--- Test Case 1: Empty Results ---")
    test_pandas_fix([])
    
    # Test case 2: Normal results
    print("\n--- Test Case 2: Normal Results ---")
    test_pandas_fix([{"Keyword": "test", "Page": "1", "Rank": "5", "Landing Page": "http://test.com"}])
