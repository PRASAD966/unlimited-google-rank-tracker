Keyword Rank Checker:

Overview:
This Streamlit web app automates Google keyword rank tracking using Brave Browser with Undetected ChromeDriver (UC).
It finds the ranking position of a target domain for a list of keywords and exports the results to Excel.

Features:
Streamlit-based UI with Sign In / Sign Up (local JSON authentication)
Uses Brave browser automation for Google SERP ranking
Accepts keywords from uploaded .txt file or manual entry
Detects and waits for CAPTCHA pages
Saves partial results if interrupted
Displays and allows Excel download (rank_results.xlsx)
Persistent user data in users.json
Supports up to 20 pages per keyword

Requirements
1. Python Packages
Install dependencies:
pip install streamlit undetected-chromedriver selenium pandas streamlit-tags openpyxl

2. Software:
Brave Browser installed (default Windows path used)
Windows environment recommended for correct path handling

File Structure:
project/
│
├── Main.py                	# Main Streamlit app
├── users.json               	# Stores registered users (auto-created)
├── NiceInteractive.png     	# Logo
├── rank_results.xlsx         	# Final results file
├── rank_results_partial.xlsx 	# Partial results (on failure)
└── requirements.txt          	# dependency list

Usage:
Step 1: Launch App
Run in terminal:
streamlit run brave6.py

Step 2: Sign In or Register
Enter email/password to log in or create a new account.
Accounts are stored in users.json.

Step 3: Provide Inputs
Upload a .txt file with keywords or type them manually.
Enter your target domain (e.g., https://example.com).
Set Max pages (default 10).

Step 4: Run and Download
Click Submit.
The app opens Brave, performs searches, and displays rankings.
Download the result file from the download button.

Configuration:
Default paths (Windows):
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
BRAVE_USER_DATA_DIR = os.path.join(os.getcwd(), "Brave_Automation_Profile")
PROFILE_DIRECTORY = "Default"
If Brave is installed elsewhere, modify BRAVE_PATH accordingly.

Output Format:
Each result is saved as an Excel sheet:

Url		Keyword		Rank		Page           
example.com	digital camera	3		1
example.com	best laptop	Not found	-

Error Handling:
If a CAPTCHA appears, the app waits until cleared.
If unsolved within timeout, it saves partial results.
Brave browser closes automatically on completion or error.

Notes:
Recommended to use a dedicated Brave user profile for automation.
Avoid excessive queries to reduce CAPTCHA risk.
App stores credentials locally in plaintext (users.json); for production, replace with a secure auth method.

License:
This project is provided as-is for educational and internal automation use.
