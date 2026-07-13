from models.ecu import ECU
from models.ecu_firware import ECUFirmware
from models.ecu_profile import ECUProfile
from models.fuel_map import FuelMap
import time
import json

class ECUManager:
    def __init__(self):
        self.ecus = []
        self.load_ecus()

    def add_ecus(self):
        #ECU Information
        ecu_id = input("Enter ECU ID:- ")
        ecu_brand = input("Enter ECU Brand:- ")
        ecu_model = input("Enter ECU Model:- ")
        protocol = input("Enter Protocol:- ")
        connection_status = input("Enter Connection Status:- ")
        supported_features = input("Enter Supported Feature separated by commas:- ").split(",")
        #ECU Firmware
        firmware_version = input("Enter Firmware Version:- ")
        manufacturer = input("Enter Manufacturer:- ")
        release_year = input("Enter Release Year:- ")
        checksum = input("Enter Checksum:- ")
        flash_status = input("Enter Flash Status:- ")
        file_size_mb = input("Enter File size in MB:- ")
        firmware = ECUFirmware(firmware_version,manufacturer,release_year, checksum,flash_status,file_size_mb)
        #Fuel Map
        fuel_map_name = input("Enter Fuel Map Name:- ")
        afr = input("Enter afr:- ")
        injector_size = input("Enter Injector Size:- ")
        fuel_pressure = input("Enter Fuel Pressure:- ")
        mod = input("Enter Mode:- ")
        fuel_type = input("Enter Fuel Type:- ")
        fuel_map = FuelMap(fuel_map_name,afr,injector_size,fuel_pressure,mod,fuel_type)
        #ECU Profile
        profile_name = input("Enter Profile Name:- ")
        ingnition_timing = input("Enter Inginition Timing:- ")
        rev_limit = input("Enter Rev Limit:- ")
        launch_control = input("Enter Launch Control:- ")
        pop_bangs = input("Enter Pops and Bangs:- ")
        horsepower_gain = input("Enter Horsepower Gain:- ")
        torque_gain = input("Enter Torque Gain:- ")
        profile = ECUProfile(profile_name,fuel_map,ingnition_timing,rev_limit,launch_control,pop_bangs,horsepower_gain,torque_gain)
        ecu = ECU(ecu_id,ecu_brand,ecu_model,protocol,connection_status,supported_features,firmware,profile)
        self.ecus.append(ecu)
        self.save_ecus()
        print("ECU added successfully.....")

    def search_ecu(self):
        ecu_id = input("Enter ECU ID of which you want to search:- ")
        print("Searching ECU ID....")
        time.sleep(2)
        if not self.ecus:
            print("No ECUs!!!!")
        for ecu in self.ecus:
            if ecu.ecu_id.lower().strip() == ecu_id.lower().strip():
                print(f"ECU found successfully....")
                ecu.display_ecu()
                return
            print("ECU not found!!!!")

    def display_all_ecus(self):
        if not self.ecus:
            print("Searching for the ECUs....")
            time.sleep(2)
            print("No ECUs found!!!!")
        else:
            for ecu in self.ecus:
                ecu.display_ecu()
                print()

    def update_ecu(self):
        ecu_id = input("Enter ECU ID of which you want to update information:- ")
        print("Searching ECU ID")
        time.sleep(2)
        if not self.ecus:
            print("No ECUs found!!!!")
        else: 
            for ecu in self.ecus:
                if ecu.ecu_id.lower().strip() == ecu_id.lower().strip():
                    ecu.update_ecu()
                    print("ECU update successfully....")
                    return
        print("ECU not found....")

    def delete_ecu(self):
        ecu_id = input("Enter ECU ID of ECU which you want to delete:- ")
        print("Searching ECU ID....")
        time.sleep(2)
        if not self.ecus:
            print("NO ECUs found!!!!")
        else:
            for ecu in self.ecus:
                if ecu.ecu_id.lower().strip() == ecu_id.lower().strip():
                    ecu.display_ecu()
                    self.ecus.remove(ecu)
                    print("ECU removed successfully....")
                    return
            else:
                print("ECU not found!!!!")

    def update_fuel_map(self):
        fuel_map_name = input("Enter Fuel Map name of which you want to update information:- ")
        print("Searching....")
        time.sleep(2)
        if not self.ecus:
            print("No Fuel Maps found!!!!")
        else:
            for ecu in self.ecus:
                if ecu.profile.fuel_map.fuel_map_name.lower().strip() == fuel_map_name.lower().strip():
                    ecu.profile.fuel_map.update_fuel_map()
                    print("Update done succesfully....")
                    return
            else:
                print("NO Fuel Map found....")

    def search_fuel_map(self):
        fuel_map_name = input("Enter Fuel Map Name of which you want to search:- ")
        print("Searching....")
        time.sleep(2)
        if not self.ecus:
            print("No Fuel Map found!!!!")
        else:
            for ecu in self.ecus:
                if ecu.profile.fuel_map.fuel_map_name.lower().strip() == fuel_map_name.lower().strip():
                    print("Fuel Map found successfully....")
                    ecu.profile.fuel_map.display_fuel_map()
                    return
            else:
                print("No Fuel Map Found....")

    def save_ecus(self):
        ecus_data = []
        for ecu in self.ecus:
            ecus_data.append(ecu.to_dict())
        with open("database/ecus.json","w") as file:
            json.dump(ecus_data, file, indent=4)
        print("ECUs saved successfully....")

    def load_ecus(self):
        try:
            with open("database/ecus.json","r") as file:
                ecus_data = json.load(file)
        except FileNotFoundError:
            print("Database not found....")
            return
        for ecu_data in ecus_data:
            firmware_info = ecu_data["firmware"]
            profile_info = ecu_data["profile"]
            fuel_map_info = profile_info["fuel_map"]
            firmware = ECUFirmware(
            firmware_info["firmware_version"],
            firmware_info["manufacturer"],
            firmware_info["release_year"],
            firmware_info["checksum"],
            firmware_info["flash_status"],
            firmware_info["file_size_mb"] )
            fuel_map = FuelMap(
            fuel_map_info["fuel_map_name"],
            fuel_map_info["afr"],
            fuel_map_info["injector_size"],
            fuel_map_info["fuel_pressure"],
            fuel_map_info["mode"],
            fuel_map_info["fuel_type"])
            profile = ECUProfile(
            profile_info["profile_name"],
            fuel_map,
            profile_info["ignition_timing"],
            profile_info["rev_limit"],
            profile_info["launch_control"],
            profile_info["pops_and_bangs"],
            profile_info["horsepower_gain"],
            profile_info["torque_gain"])
            ecu = ECU(
            ecu_data["ecu_id"],
            ecu_data["ecu_brand"],
            ecu_data["ecu_model"],
            ecu_data["protocol"],
            ecu_data["connection_status"],
            ecu_data["supported_features"],
            firmware,
            profile)
            self.ecus.append(ecu)