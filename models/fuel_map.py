# Fuel Map
class FuelMap:
    def __init__(self,fuel_map_name,afr,injector_size,fuel_pressure,mode,fuel_type):
        self.fuel_map_name  = fuel_map_name
        self.afr = afr
        self.injector_size = injector_size
        self.fuel_pressure = fuel_pressure
        self.mode = mode
        self.fuel_type = fuel_type
        
    def display_fuel_map(self):
        print("========== FUEL MAP ==========")
        print(f"Fuel Map Name : {self.fuel_map_name}")
        print(f"afr : {self.afr}")
        print(f"Injector_size : {self.injector_size}")
        print(f"Fuel Pressure : {self.fuel_pressure}")
        print(f"Mode : {self.mode}")
        print(f"Fuel Type : {self.fuel_type}")
        print()

    def update_fuel_map(self):
        print("1. Update Fuel Map Name")
        print("2. Update afr")
        print("3. Update Injector Size")
        print("4. Update Fuel Pressure")
        print("5. Update Mode")
        print("6. Update Fuel Type")
        print()
        choice = input("Enter your choice:- ")
        if choice == "1":
            new_fuel_map_name = input("Enter new Fuel Map Name:- ")
            self.fuel_map_name = new_fuel_map_name
            print(f"Fuel Map Name update succesfully to {self.fuel_map_name}")
        elif choice == "2":
            new_afr = input("Enter new afr:- ")
            self.afr = new_afr
            print(f"Afr update successfully to {self.afr}")
        elif choice == "3":
            new_injector_size = input("Enter new Injectore Size:- ")
            self.injector_size = new_injector_size
            print(f"Injector Size update successfully to {self.injector_size}")
        elif choice == "4":
            new_fuel_pressure = input("Enter new Fuel pressure:- ")
            self.fuel_pressure = new_fuel_pressure
            print(f"Fuel Pressure update successfully to {self.fuel_pressure}")
        elif choice == "5":
            print("1. ECO")
            print("2. Street")
            print("3. Sport")
            print("4. Stage 1")
            print("5. Stage 2")
            print("6. Race")
            new_mode = input("Enter New mode:- ")
            self.mode = new_mode
            print(f"Mode update successfully to {self.mode}")
        elif choice == "6":
            new_fuel_type = input("Enter new Fuel Type:- ")
            self.fuel_type = new_fuel_type
            print(f"Fuel Type update successfully to {self.fuel_type}")
        else:
            print("Invalid Choice.....")
            
    def to_dict(self):
        return{"fuel_map_name": self.fuel_map_name,
               "afr": self.afr,
               "injector_size": self.injector_size,
               "fuel_pressure":self.fuel_pressure,
               "mode": self.mode,
               "fuel_type":self.fuel_type}
