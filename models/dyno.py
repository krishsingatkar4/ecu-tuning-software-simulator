# Phase 6 Dyno Simulator
import time
class Dyno:
    def __init__(self,dyno_name,vehicle_weight,drivetrain_loss,wheel_horsepower,wheel_torque,zero_to_hundred,quarter_mile,top_speed):
        self.dyno_name = dyno_name
        self.vehicle_weight = vehicle_weight
        self.drivetrain_loss = drivetrain_loss
        self.wheel_horsepower = wheel_horsepower
        self.wheel_torque = wheel_torque
        self.zero_to_hundred = zero_to_hundred
        self.quarter_mile = quarter_mile
        self.top_speed = top_speed

    def display_dyno(self):
        print("============ DYNO INFO ============")
        print(f"Dyno Name : {self.dyno_name}")
        print(f"Vehicle Weight : {self.vehicle_weight}")
        print(f"drivetrain Loss : {self.drivetrain_loss}")
        print(f"Wheel Horsepower : {self.wheel_horsepower}")
        print(f"Wheel Torque : {self.wheel_torque}")
        print(f"0-100 km/h : {self.zero_to_hundred}")
        print(f"Quarter Mile : {self.quarter_mile}")
        print(f"Top Speed : {self.top_speed}")
        print()

    def calculation_performance(self):
        power_to_weight = self.wheel_horsepower / self.vehicle_weight
        print("1. Power to Weight Ratio")
        print("2. Zero to Hundred")
        print("3. Top Speed")
        print("4. Quarter Mile")
        print()
        choice = input("Enter your Choice:- ")
        if choice == "1":
            print("Calculating Power to Weight Ratio....")
            time.sleep(2)
            power_to_weight = self.wheel_horsepower / self.vehicle_weight
            print(f"Power to Weight Ratio is {power_to_weight}....")
        elif choice == "2":
            print("Calculating 0-100....")
            time.sleep(2)
            zero_to_hundred = round(8 / power_to_weight,2)
            print(f"0-100 is {zero_to_hundred}....")
        elif choice == "3":
            print("Calculating Top Speed....")
            time.sleep(2)
            top_speed = round(self.wheel_horsepower * 0.55) + 120
            print(f"Top Speed is {top_speed} km/h")
        elif choice == "4":
            print("Calculating Quarter Mile....")
            time.sleep(2)
            quarter_mile = round(15 - (power_to_weight * 10),2)
            print(f"Quarter Mile is {quarter_mile}....")
        else:
            print("Invalid Choice")

    def update_dyno(self):
        print("1. Update Dyno Name")
        print("2. Update Vehicle Weight")
        print("3. Update Drivetrain Loss")
        print("4. Update Wheel Horsepower")
        print("5. Update Wheel Torque")
        print()
        choice = input("Enter Your Choice:- ")
        if choice == "1":
            new_dyno_name = input("Enter new Dyno Name:- ")
            self.dyno_name = new_dyno_name
            print(f"Dyno Name update successfully to {self.dyno_name}")
        elif choice == "2":
            new_vehicle_weight = input("Enter new Vehicel Weight:- ")
            self.vehicle_weight = new_vehicle_weight
            print(f"Vehicle Weight update successfully to {self.vehicle_weight}")
        elif choice == "3":
            new_drivetrain_loss = input("Enter new drivetrain Loss:- ")
            self.drivetrain_loss = new_drivetrain_loss
            print(f"drivetrain Loss update successfully to {self.drivetrain_loss}")
        elif choice == "4":
            new_wheel_horsepower = input("Enter new Wheel Horsepower:- ")
            self.wheel_horsepower = new_wheel_horsepower
            print(f"Wheel Horsepower update successfully to {self.wheel_horsepower}")
        elif choice == "5":
            new_wheel_torque = input("Enter new Wheel Torque:- ")
            self.wheel_torque = new_wheel_torque
            print(f"Wheel Torque Update successfully to {self.wheel_torque}")
        else:
            print("Invalid Choice....")

    def to_dict(self):
        return {"dyno_name": self.dyno_name,
                "vehicle_weight": self.vehicle_weight,
                "drivetrain_loss": self.drivetrain_loss,
                "wheel_horsepower": self.wheel_horsepower,
                "wheel_torque": self.wheel_torque,
                "zero_to_hundred": self.zero_to_hundred,
                "quarter_mile": self.quarter_mile,
                "top_speed": self.top_speed}