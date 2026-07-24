# Phase 8 ECU Flash
import time

class ECUFlash:
    def __init__(self,flash_name,tune_file,tune_version,file_size,flash_status,backup_status,flash_time):
        self.flash_name = flash_name
        self.tune_file = tune_file
        self.tune_version = tune_version
        self.file_size = file_size
        self.flash_status = flash_status
        self.backup_status = backup_status
        self.flash_time = flash_time

    def display_flash(self):
        print("========== ECU FLASH ==========")
        print(f"Flash Name : {self.flash_name}")
        print(f"Tune File : {self.tune_file}")
        print(f"Tune Version : {self.tune_version}")
        print(f"File Size : {self.file_size}")
        print(f"Flash Status : {self.flash_status}")
        print(f"Backup Status : {self.backup_status}")
        print(f"Flash Time : {self.flash_time}")
        print()

    def update_flash(self):
        print("1. Update Tune File")
        print("2. Update Tune Version")
        print("3. Update File Size")
        print("4. Update Flash Status")
        print()
        choice = input("Enter your Choice:- ")
        if choice == "1": 
            new_tune_file = input("Enter new Tune File:- ")
            self.tune_file = new_tune_file
            print(f"Tune File Update successfully to {self.tune_file}")
        elif choice == "2":
            new_tune_version = input("Enter new Tune Version:- ")
            self.tune_version = new_tune_version
            print(f"Tune Version update successfully to {self.tune_version}")
        elif choice == "3":
            new_file_size = input("Enter New File Size:- ")
            self.file_size = new_file_size
            print(f"File Size Update successfully to {self.file_size}")
        elif choice == "4":
            new_flash_status = input("Enter new Flash Status:- ")
            self.flash_status = new_flash_status
            print(f"Flash status Update successfully to {self.flash_status}")
        else:
            print("Invalid Choice!!!!")
    
    def to_dict(self):
        return {
            "flash_name": self.flash_name,
            "tune_file": self.tune_file,
            "tune_version": self.tune_version,
            "file_size": self.file_size,
            "flash_status": self.flash_status,
            "backup_status": self.backup_status,
            "flash_time": self.flash_time}

    def creat_backup(self):
        print("Connecting to ECU....")
        time.sleep(2)
        print("Reading current tune....")
        time.sleep(2)
        print("Creating backup file....")
        time.sleep(2)
        self.backup_status = "Created"
        print("Backup created successfully....")
        if self.backup_status != "Created":
            print("Please create backup first.")
            return
        
    def start_flash(self):
        print("Connecting to ECU....")
        time.sleep(2)
        print("Checking ECU compatibility....")
        time.sleep(2)
        print("Creating Backup....")
        time.sleep(2)
        print("Uploading tune file....")
        time.sleep(2)
        print("Verifying Checksum....")
        time.sleep(2)
        print("Flashing ECU....")
        time.sleep(2)
        print("Flash completed successfully.")
       