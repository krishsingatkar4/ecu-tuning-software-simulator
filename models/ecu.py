#ECU 
from models.ecu_firware import ECUFirmware
from models.ecu_profile import ECUProfile
import time

class ECU:
    def __init__(self,ecu_id,ecu_brand,ecu_model,protocol,connection_status,supported_features,firmware,profile):
        self.connection_status = "Disconnected"
        self.ecu_id = ecu_id
        self.ecu_brand = ecu_brand
        self.ecu_model = ecu_model
        self.protocol = protocol
        self.connection_status = connection_status
        self.supported_features = supported_features
        self.firmware = firmware
        self.profile = profile

    def display_ecu(self):
        print("============ ECU INFORMATION ============")
        print(f"ECU ID : {self.ecu_id}")
        print(f"ECU Brand : {self.ecu_brand}")
        print(f"ECU Model ; {self.ecu_model}")
        print(f"Protocol : {self.protocol}")
        print(f"Connection Status : {self.connection_status}")
        print(f"Supported Features : {self.supported_features}")
        print()
        print("========== FIRMwARE ===========")
        self.firmware.display_firmware()
        print("=========== PROFILE ==========")
        self.profile.display_profile()

    def connect_ecu(self):
        if self.connection_status.lower().strip() == "Connected".lower().strip():
            print("Your ECU is Already connected....")
        else:
            print("Preapring for connecting....")
            time.sleep(2)
            self.connection_status = "Connected"
            print("ECU connected successfully....")

    def disconnect_ecu(self):
        if self.connection_status.lower().strip() == "Disconnected".lower().strip():
            print("ECU is Already Disconnected....")
        else:
            print("Preparing ECU for disconnecting....")
            time.sleep(2)
            self.connection_status = "Disconnected"
            print("ECU disconnected successfully....")

    def update_ecu(self):
        print("========== UPDATE ECU ==========")
        print("1. Update ECU Brand")
        print("2. Update ECU Model")
        print("3. Update Protocol")
        print("4. Update Connection Status")
        print("5. Update Supported Features")
        print("6. Update Firmware")
        print("7. Update Profile")
        print()
        choice = input("Enter your choice:- ")
        if choice == "1":
            new_brand = input("Enter new ECU brand:- ")
            self.ecu_brand = new_brand
            print(f"ECU brand updated successfully to {self.ecu_brand}")
        elif choice == "2":
            new_ecu_model = input("Enter new ECU Model:- ")
            self.ecu_model = new_ecu_model
            print(f"ECU Model update successfully to {self.ecu_model}")
        elif choice == "3":
            new_protocol = input("Enter new Protocol:- ")
            self.protocol = new_protocol
            print(f"Protocol Updated successfully to {self.protocol}")
        elif choice == "4":
            new_connection_status = input("Enter new Connetion Status:- ")
            self.connection_status = new_connection_status
            print(f"Connection Status update successfully to {self.connection_status}")
        elif choice == "5":
            new_support_feature = input("Enter features separated by commas:- ").split(",")
            self.supported_features = new_support_feature
            print(f"Support feature update successfully to {self.supported_features}")
        elif choice == "6":
            self.firmware.update_firmware()
        elif choice == "7":
            self.profile.update_profile()
        else:
            print("Invalid choice!!!!")

    def to_dict(self):
        return {"ecu_id":self.ecu_id,
                "ecu_brand":self.ecu_brand,
                "ecu_model":self.ecu_model,
                "protocol":self.protocol,
                "connection_status":self.connection_status,
                "supported_features":self.supported_features,
                "firmware":self.firmware.to_dict(),
                "profile":self.profile.to_dict()}
