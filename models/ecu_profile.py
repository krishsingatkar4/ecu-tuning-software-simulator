from models.fuel_map import FuelMap
from models.ignition_timing import IgnitionTiming

class ECUProfile:
    def __init__(self,profile_name,fuel_map,ignition_timing,rev_limit,launch_control,pops_and_bangs,horsepower_gain,torque_gain,turbo):
        self.profile_name = profile_name
        self.fuel_map = fuel_map
        self.ignition_timing = ignition_timing
        self.rev_limit = rev_limit
        self.launch_control = launch_control
        self.pops_and_bangs = pops_and_bangs
        self.horsepower_gain = horsepower_gain
        self.torque_gain = torque_gain
        self.turbo = turbo

    def display_profile(self):
        print("========== ECU PROFILE ==========")
        print(f"Profile Name : {self.profile_name}")
        print(f"Ignition Timing : {self.ignition_timing}")
        print(f"Rev Limit : {self.rev_limit}")
        print(f"Launch Control : {self.launch_control}")
        print(f"Pops And Bangs : {self.pops_and_bangs}")
        print(f"Horsepower Gain : {self.horsepower_gain}")
        print(f"Torque Gain : {self.torque_gain}")
        self.fuel_map.display_fuel_map()
        self.ignition_timing.display_ignition_timing()
        self.turbo.display_turbo()

    def update_profile(self):
        print("========== Update Profile ===========")
        print("1. Update Profile Name")
        print("2. Update Fuel Map")
        print("3. Update Ingition Timing")
        print("4. Update Rev Limit")
        print("5. Update Launch Control")
        print("6. Update Pops and Bangs")
        print("7. Update Horsepower Gain")
        print("8. Update Torque Gain")
        print("9. Update Fuel Map")
        print("10 Update Ignition Timing")
        print("11. Update Tubro")
        print()
        choice = input("Enter your choice:- ")
        if choice == "1":
            new_profileName = input("Enter new Profile Name:- ")
            self.profile_name = new_profileName
            print(f"Profile Name update successfully to {self.profile_name}")
        elif choice == "2":
            new_fuelMap = input("Enter new Fuel Map:- ")
            self.fuel_map = new_fuelMap
            print(f"Fuel map update successfully to {self.fuel_map}")
        elif choice == "3":
            new_ignitionTiming = input("Enter new Ignition Timing:- ")
            self.ignition_timing = new_ignitionTiming
            print(f"Ignition Timing update successfully to {self.ignition_timing}")
        elif choice == "4":
            new_revLimit = input("Enter new Rev Limit:- ")
            self.rev_limit = new_revLimit
            print(f"Rev Limit update successfully to {self.rev_limit}")
        elif choice == "5":
            new_launchControl = input("Enter new Lauch Control:- ")
            self.launch_control = new_launchControl
            print(f"Launch Control update successfully to {self.launch_control}")
        elif choice == "6":
            new_popBangs = input("Enter new Pops and Bangs:- ")
            self.pops_and_bangs = new_popBangs
            print(f"Pops and Bangs update successfully to {self.pops_and_bangs}")
        elif choice == "7":
            new_horsepowerGain = input("Enter new Horsepower Gain:- ")
            self.horsepower_gain = new_horsepowerGain
            print(f"Horsepower Gain update successfully to {self.horsepower_gain}")
        elif choice == "8":
            new_torqueGain = input("Enter new Torque Gain:- ")
            self.torque_gain = new_torqueGain
            print(f"Torque Gain update successfully to {self.torque_gain}")
        elif choice == "9":
            self.fuel_map.update_fuel_map()
        elif choice == "10":
            self.ignition_timing.update_ignition_timing()
        elif choice == "10":
            self.turbo.update_turbo()
        else:
            print("Invalid choice!!!!")

    def to_dict(self):
        return {"profile_name": self.profile_name,
                "fuel_map": self.fuel_map.to_dict(),
                "ignition_timing": self.ignition_timing,
                "rev_limit": self.rev_limit,
                "launch_control": self.launch_control,
                "pops_and_bangs": self.pops_and_bangs,
                "horsepower_gain": self.horsepower_gain,
                "torque_gain": self.torque_gain,
                "ignition_timing": self.ignition_timing.to_dict(),
                "turbo": self.turbo.to_dict()}