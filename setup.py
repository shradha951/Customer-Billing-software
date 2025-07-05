from cx_Freeze import setup, Executable, sys
import os

# Create a dummy icon file if it doesn't exist
if not os.path.exists('icon.ico'):
    # Create a simple empty file
    with open('icon.ico', 'wb') as f:
        f.write(b'')  # Write empty bytes
    print("Created empty icon.ico file")

# Files to include
includefiles = [
    'icon.ico',
    'database.py',
    'billing_system.db'  # Include the database file
]

# Exclude unnecessary modules
excludes = []
packages = ['tkinter', 'sqlite3']

# Set the base depending on the platform
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Create desktop shortcut
shortcut_table = [
    ("DesktopShortcut",
     "DesktopFolder",
     "Retail Billing System",
     "TARGETDIR",
     "[TARGETDIR]\\retail_billing.exe",
     None,
     None,
     None,
     None,
     None,
     None,
     "TARGETDIR",
     )
]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

setup(
    version="1.0",
    description="Retail Billing System with Database",
    author="Retail Manager",
    name="Retail Billing System",
    options={
        'build_exe': {
            'include_files': includefiles,
            'packages': packages,
            'excludes': excludes,
        },
        'bdist_msi': bdist_msi_options,
    },
    executables=[
        Executable(
            script="main.py",
            base=base,
            icon='icon.ico',
            target_name="retail_billing.exe",
            shortcut_name="Retail Billing System",
            shortcut_dir="DesktopFolder",
        )
    ]
)