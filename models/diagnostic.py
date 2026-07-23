# Phase 7 Diagnostic
import json

class Diagnostic:
    def __init__(self,fault_code,fault_name,severity,status,sensor,description):
        self.fault_code = fault_code
        self.fault_name = fault_name
        self.severity = severity
        self.status = status
        self.sensor = sensor
        self.description = description

    def display_diagnostic(self):
        print("========== DIAGNOSTIC ==========")
        print(f"Fault Code : {self.fault_code}")
        print(f"Fault Name : {self.fault_name}")
        print(f"Severity : {self.severity}")
        print(f"Status : {self.status}")
        print(f"Sensor : {self.sensor}")
        print(f"Description : {self.description}")
        print()

    def update_diagnostic(self):
        print("========== UPDATE FAULT CODES ===========")
        print("1. Update Fault code")
        print("2. Update Fault Name")
        print("3. Update Severity")
        print("4. Update Stauts")
        print("5. Update Sensor")
        print("6. Update Description")
        print()
        choice = input("Enter your choice:- ")
        if choice == "1":
            new_fault_code = input("Enter new Fault Code:- ")
            self.fault_code = new_fault_code
            print(f"Fault code update successfully to {self.fault_code}")
        elif choice == "2":
            new_fault_name = input("Enter new Fault Name:- ")
            self.fault_name = new_fault_name
            print(f"Fault Name update successfully to {self.fault_name}")
        elif choice == "3":
            new_severity = input("Enter new Severity:- ")
            self.severity = new_severity
            print(f"Severity update successfully to {self.severity}")
        elif choice == "4":
            new_status = input("Enter New Status:- ")
            self.status = new_status
            print(f"Status update successfully to {self.status}")
        elif choice == "5":
            new_sensor = input("Enter new Status:- ")
            self.sensor = new_sensor
            print(f"Sensor Update successfully to {self.sensor}")
        elif choice == "6":
            new_description = input("Enter New Description:- ")
            self.description = new_description
            print(f"Description update successfully to {self.description}")
        else:
            print("Invalid Choice")

    def to_dict(self):
        return{"fault_name":self.fault_name,
               "fault_code":self.fault_code,
               "severity":self.severity,
               "status":self.status,
               "sensor":self.sensor,
               "description":self.description}

    def scan_fault(self):
        with open("database/fault_codes.json","r") as file:
            fault_database = json.load(file)
        code = input("Enter Fault code:- ")
        found = False
        for fault in fault_database:
            if fault["fault_code"] == code:
                print("\n===== FAULT DETECTED =====")
                print(f"Fault Name : {fault['fault_name']}")
                print(f"Severity : {fault['severity']}")
                print(f"Status : {fault['status']}")
                print(f"Sensor : {fault['sensor']}")
                print(f"Description : {fault['description']}")
                found = True
                break
        if not found:
            print("Unknown Fault Code!!!!")

    def clear_fault(self):
        print("1. Want to clear all fault")
        print("2. Clear Specific Fault")
        choice = input("Enter your Choice:- ")
        if choice == "1":
            with open("database/fault_codes.json","r") as file:
                fault_database = json.load(file)
            for fault in fault_database:
                fault["status"] = "Cleared"
            with open("database/fault_codes.json","w") as file:
                json.dump(fault_database,file,indent=4)
            print("All faults cleared Successfully....")
        elif choice == "2":
            code = input("Enter code which you want to clear:- ")
            with open("database/fault_codes.json","r") as file:
                fault_database = json.load(file)
            found = False
            for fault in fault_database:
                if fault["fault_code"].lower().strip() == code.lower().strip():
                    found = True
                    if fault["status"] == "Active":
                        fault["status"] = "Cleared"
                        with open("database/fault_codes.json", "w") as file:
                            json.dump(fault_database, file, indent=4)
                        print("============ CLEARED FAULT CODE ===========")
                        print(f"Fault Code : {fault['fault_code']}")
                        print(f"Fault Name : {fault['fault_name']}")
                        print(f"Severity : {fault['severity']}")
                        print(f"Status : {fault['status']}")
                        print(f"Sensor : {fault['sensor']}")
                        print(f"Description : {fault['description']}")
                        print("=======================")   
                        break
                    elif fault["status"] == "Cleared":
                        print("Fault code Status is already Cleared....")
            if not found:
                    print("Code Not Found!!!!")
        else:
            print("Invalid Choice!!!!")             