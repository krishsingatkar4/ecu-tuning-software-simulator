from models.owner import Owner
from models.engine import Engine

class Car:
    def __init__(self,vin,company,model,year,transmission,drive_type,mileage,color,license_plate,owner,engine,ecu=None):
        self.vin = vin
        self.company = company
        self.model = model
        self.year = year
        self.transmission = transmission
        self.drive_type = drive_type
        self.mileage = mileage
        self.color = color
        self.license_plate = license_plate
        self.owner = owner
        self.engine = engine
        self.ecu = ecu

    def display_car(self):
        print("========== CAR INFORMATION ==========")
        print(f"VIN : {self.vin}")
        print(f"Company : {self.company}")
        print(f"Model : {self.model}")
        print(f"Year : {self.year}")
        print(f"Transmission : {self.transmission}")
        print(f"Driver Type : {self.drive_type}")
        print(f"Mileage : {self.mileage}")
        print(f"Color : {self.color}")
        print(f"License Plate : {self.license_plate}\n")
        print("------------ OWNER ------------")
        self.owner.display_owner()
        print()
        print("------------ ENGINE -----------")
        self.engine.display_engine()
        print()
        if self.ecu:
            self.ecu.display_ecu()

    def update_car(self):
        print("1. Update VIN:- ")
        print("2. Update Company:- ")
        print("3. Update Model:- ")
        print("4. Update Year:- ")
        print("5. Update Transmission:- ")
        print("6. Update Drive Type:- ")
        print("7. Update Mileage:- ")
        print("8. Update Color:- ")
        print("9. Update License Plate:- ")
        print("10. Update Owner:- ")
        print("11. Upadte Engine:- ")
        print()
        choice = input("Enter your choice:- ")
        if choice == "1":
            new_vin = input("Enter New VIN:- ")
            self.vin = new_vin
            print(f"VIN Update succefully to {self.vin}!!!!")
        elif choice == "2":
            new_company = input("Enter new Company:- ")
            self.company = new_company
            print(f"Company succefully to {self.company}!!!!")
        elif choice == "3":
            new_model = input("Enter new Model:- ")
            self.model = new_model
            print(f"Model Update succefully to {self.model}!!!!")
        elif choice == "4":
            new_year = input("Enter new Year:- ")
            self.year = new_year
            print(f"Year Update succefully to {self.year}!!!!")
        elif choice == "5":
            new_transmission = input("Enter new Transmission:- ")
            self.transmission = new_transmission
            print(f"Transmission Update succefully to {self.transmission}!!!!")
        elif choice == "6":
            new_drive_type = input("Enter new Drive Type:- ")
            self.driver_type = new_drive_type
            print(f"Drive Type Update succefully to {self.driver_type}!!!!")
        elif choice == "7":
            new_mileage = input("Enter new Mileage:- ")
            self.mileage = new_mileage
            print(f"Mileage Update succefully to {self.mileage}!!!!")
        elif choice == "8":
            new_color = input("Enter new Color:- ")
            self.color = new_color
            print(f"Color Update succefully to {self.color}!!!!")
        elif choice == "9":
            new_license = input("Enter new License Plate:- ")
            self.license_plate = new_license
            print(f"license Plate Update succefully to {self.license_plate}!!!!")
        elif choice == "10":
            self.owner.update_owner()
        elif choice == "11":
            self.engine.update_engine()
        else:
            print("Invalid Choice....")

    def to_dict(self):
        return {"vin":self.vin,
                "company":self.company,
                "model": self.model,
                "year": self.year,
                "transmission":self.transmission,
                "drive_type": self.drive_type,
                "mileage":self.mileage,
                "color":self.color,
                "license_plate":self.license_plate,
                "owner": self.owner.to_dict(),
                "engine": self.engine.to_dict(),
                "ecu":self.ecu.to_dict() if self.ecu else None}