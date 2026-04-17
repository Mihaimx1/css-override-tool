
import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QMessageBox, QTextEdit, QDialog, QDialogButtonBox
)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PyQt6.QtGui import QGuiApplication

class SettingsValidatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.csv_file_path = None

    def initUI(self):
        self.setWindowTitle("Settings Validator")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        # URL input
        self.url_label = QLabel("Study Settings URL:")
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        # Element input
        self.elm_label = QLabel("Study settings element#:")
        self.elm_input = QLineEdit()
        layout.addWidget(self.elm_label)
        layout.addWidget(self.elm_input)
        # Username input
        self.user_label = QLabel("Username:")
        self.user_input = QLineEdit()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        # Password input
        self.pass_label = QLabel("Password:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        # File upload button
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        layout.addWidget(self.upload_btn)
        # Run button
        self.run_btn = QPushButton("Run Automation")
        self.run_btn.clicked.connect(self.run_automation)
        layout.addWidget(self.run_btn)
        self.setLayout(layout)

    def upload_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.csv_file_path = file_path
            QMessageBox.information(self, "File Selected", f"CSV File: {os.path.basename(file_path)}")

    def run_automation(self):
        if not self.csv_file_path or not os.path.exists(self.csv_file_path):
            QMessageBox.warning(self, "Missing Info", "Please upload a valid CSV file.")
            return
        if not self.url_input.text() or not self.user_input.text() or not self.pass_input.text():
            QMessageBox.warning(self, "Missing Info", "Please fill all fields.")
            return
        # Run Selenium automation
        try:
            self.automate_settings_check()
            QMessageBox.information(self, "Completed", "Automation completed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def load_expected_data(self, file_path):
        """Load expected settings from a CSV or Excel file."""
        if not isinstance(file_path, str):
            file_path = str(file_path)
        print(f"DEBUG: Checking file path - {file_path}")
        if not os.path.exists(file_path):
            print(f"ERROR: File not found at {file_path}")
            return {}
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, engine='openpyxl')
            else:
                print("ERROR: Unsupported file type.")
                return {}
            print("DEBUG: File loaded successfully.")
            print("Headers:", df.columns.tolist())
            # Clean up the expected values
            df.iloc[:, 1] = df.iloc[:, 1].astype(str).str.strip().str.lower()
            # Remove [default] from values and strip any extra spaces
            df.iloc[:, 1] = df.iloc[:, 1].str.replace(r"\[default\]", "", regex=True).str.strip()
            # Replace "environment-specific" with empty string
            df.iloc[:, 1] = df.iloc[:, 1].replace("environment-specific", "")
            # Replace "nan" with empty string
            df.iloc[:, 1] = df.iloc[:, 1].replace("nan", "").fillna("")

            expected_data = dict(zip(df.iloc[:, 0].str.strip().str.lower(), df.iloc[:, 1]))
            return expected_data
        except Exception as e:
            print(f"ERROR: {e}")
            return {}

    def automate_settings_check(self):
        """Perform Selenium automation."""
        expected_data = self.load_expected_data(self.csv_file_path)
        # Configure ChromeDriver
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        service = Service(ChromeDriverManager().install())  # Automatically install and use ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(self.url_input.text())
        # Login
        driver.find_element(By.ID, "username").send_keys(self.user_input.text())
        driver.find_element(By.ID, "password").send_keys(self.pass_input.text(), Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2'))
        )

        select = driver.find_element(By.CSS_SELECTOR, '.k-select:nth-child(3)')
        select.click()
        time.sleep(1)
        idx = int(self.elm_input.text())
        option = driver.find_element(By.XPATH, f"//ul[@id='EntityType_listbox']/li[{idx}]")
        option.click()

        # Wait for settings table
        time.sleep(30)
        rows = driver.find_elements(By.CSS_SELECTOR, "tr")
        mismatches = []
        for row in rows:
            column1 = row.find_elements(By.CSS_SELECTOR, "td:nth-child(2)")
            column2 = row.find_elements(By.CSS_SELECTOR, "td:nth-child(5)")
            if column1 and column2:
                # Get the text from the first element in the list for both columns
                setting_name = column1[0].text.strip().lower()
                setting_value = column2[0].text.strip().lower()

                setting_value = setting_value.replace("(default)", "").strip()
                if setting_name in expected_data:
                    expected_value = (expected_data[setting_name] or "").strip().lower()
                    setting_value  = setting_value.strip().lower()

                    if expected_value == "":
                        if setting_value != "":
                            mismatches.append(
                                f"<b>Mismatch</b>: {setting_name.title()} <br>"
                                f"<b>Expected</b>: (empty) <br>"
                                f"<b>Actual</b>: {setting_value or '(empty)'} <br>"
                            )
                    else:
                        expected_set = {v.strip() for v in expected_value.split(",") if v.strip()}
                        actual_set   = {v.strip() for v in setting_value.split(",") if v.strip()}

                        missing_values = expected_set - actual_set
                        extra_values   = actual_set - expected_set

                        if missing_values or extra_values:
                            mismatch_message = f"<b>Mismatch</b>: {setting_name.title()} <br>"
                            if missing_values:
                                mismatch_message += f"<b>Expected</b>: {', '.join(sorted(missing_values))} <br>"
                            if extra_values:
                                mismatch_message += f"<b>Actual</b>: {', '.join(sorted(extra_values))} <br>"
                            mismatches.append(mismatch_message)


        driver.quit()
        # Show results
        if mismatches:
            dialog = MismatchDialog(mismatches, self)
            dialog.exec()
        else:
            QMessageBox.information(self, "Success", "All settings match.")


class MismatchDialog(QDialog):
    def __init__(self, mismatches, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mismatches Found")
        # Get screen size
        screen = QGuiApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.75)   # 75% of screen width
        height = int(screen.height() * 0.75) # 75% of screen height
        self.resize(width, height)  # Set dialog size
        layout = QVBoxLayout()
        # Scrollable text area for mismatches
        self.text_edit = QTextEdit()
        self.text_edit.setHtml("<br>".join(mismatches))  # Display mismatches
        self.text_edit.setReadOnly(True)  # Make text read-only
        self.text_edit.setFontPointSize(12)  # Increase font size
        layout.addWidget(self.text_edit)
        # OK button
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsValidatorApp()
    window.show()
    sys.exit(app.exec())