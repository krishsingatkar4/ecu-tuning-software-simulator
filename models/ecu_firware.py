# ECU FIRMWARE 
class ECUFirmware:
    def __init__(self,firmware_version,manufacturer,release_year,checksum,flash_status,file_size_mb):
        self.firmware_version = firmware_version
        self.manufacturer = manufacturer
        self.release_year = release_year
        self.checksum = checksum
        self.flash_status = flash_status
        self.file_size_mb = file_size_mb
        
    def display_firmware(self):
        print("========== ECU FIRMWARE ==========")
        print(f"Firmware Version : {self.firmware_version}")
        print(f"Manufacturer : {self.manufacturer}")
        print(f"Release Year : {self.release_year}") 
        print(f"Flash Status : {self.flash_status}")
        print(f"File Size : {self.file_size_mb} MB")
        print(f"Checksum : {self.checksum}")

    def update_firmware(self):
        print("========== UPDATE FIRMWARE ==========")
        print("1. Update Firmware Version")
        print("2. Update Manufacturer")
        print("3. Update Release Year")
        print("4. Update Checksum")
        print("5. Update Flash Status")
        print("6. update File Size")
        print()
        choice = input("Enter your choice:- ")
        if choice == "1":
            new_firmware_version = input("Enter new Firmware Version:- ")
            self.firmware_version = new_firmware_version
            print(f"Firmware Version update successfully to {self.firmware_version}")
        elif choice == "2":
            new_manufaturer = input("Enter new Manufaturer:- ")
            self.manufacturer = new_manufaturer
            print(f"Manufaturer update successfully to {self.manufacturer}")
        elif choice == "3":
            new_release_year = input("Enter new Release year:- ")
            self.release_year = new_release_year
            print(f"Release Year update successfully to {self.release_year}")
        elif choice == "4":
            new_checksum = input("Enter new Checksum:- ")
            self.checksum = new_checksum
            print(f"Checksum update to successfully to {self.checksum}")
        elif choice == "5":
            new_file_status = input("Enter new File Status:- ")
            self.flash_status = new_file_status
            print(f"File status update successfully to {self.flash_status}")
        elif choice == "6":
            new_flash_size = input("Enter new Flash Size in MB:- ")
            self.file_size_mb = new_flash_size
            print(f"Flash Size update successfully in {self.file_size_mb}")
        else:
            print("Invalid choice!!!!")
    
    def to_dict(self):
        return {"firmware_version": self.firmware_version,
                 "manufacturer": self.manufacturer,
                "release_year": self.release_year,
                "checksum": self.checksum,
                "flash_status": self.flash_status,
                "file_size_mb": self.file_size_mb}