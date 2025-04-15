import subprocess
import logging
import datetime
import os

def log_pycharm_packages(log_file_path="requirements1txt"):
    """
    Logs the installed packages in the PyCharm environment to a specified file, clearing previous entries.

    Args:
        log_file_path (str): The path to the log file. Defaults to "requirements.txt".
    """
    try:
        # Check if pip is installed
        subprocess.run(["pip", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("pip is not installed. Please install pip.")
        return
    except subprocess.CalledProcessError:
        print("pip is not working correctly. Please check your pip installation.")
        return

    try:
        # Get the list of installed packages
        result = subprocess.run(["pip", "list"], capture_output=True, text=True, check=True)
        packages = result.stdout.strip()

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Clear the log file before writing new entries
        with open(log_file_path, "w"):  # "w" mode truncates the file
            pass  # Do nothing, just open and close to clear

        # Configure the logger
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        # Log the timestamp and installed packages
        logging.info(f"PyCharm packages installed at {timestamp}:\n{packages}")

        print(f"Packages logged to {log_file_path} (previous entries cleared)")

    except subprocess.CalledProcessError as e:
        print(f"Error listing packages: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    log_pycharm_packages()
