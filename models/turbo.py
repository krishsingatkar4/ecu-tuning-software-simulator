class Turbo:
    def __init__(self,turbo_name,turbo_brand,turbo_type,boost_pressure,wastegate_pressure,spool_rpm,anti_lag,intercooler_type,horsepower_support):
        self.turbo_name = turbo_name
        self.turbo_brand = turbo_brand
        self.turbo_type = turbo_type
        self.boost_pressure = boost_pressure
        self.wastegate_pressure = wastegate_pressure
        self.spool_rpm = spool_rpm
        self.anti_lag = anti_lag
        self.intercooler_type = intercooler_type
        self.horsepower_support = horsepower_support

    def display_turbo(self):
        print("============ TURBO INFORMATION ===========")
        print(f"Turbo Name : {self.turbo_name}")
        print(f"Turbo Brand : {self.turbo_brand}")
        print(f"Turbo Type : {self.turbo_type}")
        print(f"Boost Pressure : {self.boost_pressure}")
        print(f"Wastegate Pressure : {self.wastegate_pressure}")
        print(f"Spool RPM : {self.spool_rpm}")
        print(f"Anti lag : {self.anti_lag}")
        print(f"Intercooler Type : {self.intercooler_type}")
        print(f"Horsepower Support : {self.horsepower_support}")
        print()
    
    def update_turbo(self):
        print("1. Update Turbo Name")
        print("2. Update Turbo Brand")
        print("3. Update Turbo Type")
        print("4. Update Boost pressure")
        print("5. Update Wastegate Pressure")
        print("6. Update Spool RPM")
        print("7. Update Anti Lag")
        print("8. Update Intercooler Type")
        print("9. Update Horsepower Support")
        print()
        choice = input("Enter your choice:- ")
        if choice ==  "1":
            new_turbo_name = input("Enter new Turbo Name:- ")
            self.turbo_name = new_turbo_name
            print(f"Turbo name update succesfully to {self.turbo_name}")
        elif choice == "2":
            new_turbo_brand = input("Enter new Turbo Brand:- ")
            self.turbo_brand = new_turbo_brand
            print(f"Tubro brand update successfully to {self.turbo_brand}")
        elif choice == "3":
            new_turbo_type = input("Enter new Turbo Type:- ")
            self.turbo_type = new_turbo_type
            print(f"Turbo Type update successfully to {self.turbo_type}")
        elif choice == "4":
            new_boost_pressure = input("Enter new Boost pressure:- ")
            self.boost_pressure = new_boost_pressure
            print(f"Boost pressure update successfully to {self.boost_pressure}")
        elif choice == "5":
            new_wastegate_pressure = input("Enter new Wastegate pressure:- ")
            self.wastegate_pressure = new_wastegate_pressure
            print(f"Wastegate pressure update successfully to {self.wastegate_pressure}")
        elif choice == "6":
            new_spool_rpm = input("Enter new Spool RPM:- ")
            self.spool_rpm = new_spool_rpm
            print(f"Spool RPM update successfully to {self.spool_rpm}")
        elif choice == "7":
            new_anti_lag = input("Enter new Anti Lag:- ")
            self.anti_lag = new_anti_lag
            print(f"Anti lag update successfully to {self.anti_lag}")
        elif choice == "8":
            new_intercooler_type = input("Enter new Intercooler Type:- ")
            self.intercooler_type = new_intercooler_type
            print(f"Intercooler type update successfully to {self.intercooler_type}")
        elif choice == "9":
            new_horsepower_support = input("Enter new Horsepower Support:- ")
            self.horsepower_support = new_horsepower_support
            print(f"Horsepower Support update successfully to {self.horsepower_support}")
        else:
            print("Invalid Choice!!!!")

    def to_dict(self):
        return{"turbo_name":self.turbo_name,
               "turbo_brand":self.turbo_brand,
               "turbo_type":self.turbo_type,
               "boost_pressure":self.boost_pressure,
               "wastegate_pressure":self.wastegate_pressure,
               "spool_rpm":self.spool_rpm,
               "anti_lag":self.anti_lag,
               "intercooler_type":self.intercooler_type,
               "horsepower_support":self.horsepower_support}