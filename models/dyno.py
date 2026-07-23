# Phase 6 Dyno Simulator
import time

class Dyno:
    def __init__(self,dyno_name,vehicle_weight,drivetrain_loss,zero_to_hundred,quarter_mile,top_speed,):
        self.dyno_name = dyno_name
        self.vehicle_weight = vehicle_weight
        self.drivetrain_loss = drivetrain_loss
        self.zero_to_hundred = zero_to_hundred
        self.quarter_mile = quarter_mile
        self.top_speed = top_speed
        self.wheel_horsepower = 0
        self.wheel_torque = 0

    def display_dyno(self):
        print("============ DYNO INFO ============")
        print(f"Dyno Name : {self.dyno_name}")
        print(f"Vehicle Weight : {self.vehicle_weight} kg")
        print(f"drivetrain Loss : {self.drivetrain_loss} ")
        print(f"Wheel Horsepower : {self.wheel_horsepower} hp")
        print(f"Wheel Torque : {self.wheel_torque} Nm")
        print(f"0-100 km/h : {self.zero_to_hundred} sec")
        print(f"Quarter Mile : {self.quarter_mile} sec")
        print(f"Top Speed : {self.top_speed} km/h")
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
    
    def calculate_wheel_horsepower(self,stock_horsepower,horsepower_gain):
        wheel_horsepower = (stock_horsepower + horsepower_gain) * (1 - self.drivetrain_loss / 100)
        self.wheel_horsepower = round(wheel_horsepower,2)
        return self.wheel_horsepower
    
    def calculate_wheel_torque(self,stock_torque,torque_gain):
        wheel_torque = (stock_torque + torque_gain) * (1 - self.drivetrain_loss / 100)
        self.wheel_torque = round(wheel_torque, 2)
        return self.wheel_torque
    
    def calculate_zero_to_hundred(self, wheel_horsepower):
        zero_to_hundred = round(2.8 + (400 / wheel_horsepower),2)
        self.zero_to_hundred = zero_to_hundred
        return self.zero_to_hundred

    def calculate_quarter_mile(self,wheel_horsepower):
        quarter_mile = round(16 - (wheel_horsepower / 150),2)
        self.quarter_mile = quarter_mile
        return self.quarter_mile

    def calculate_top_speed(self,wheel_horsepower, vehicle_weight):
        top_speed = round(180 + (wheel_horsepower / 4) - (vehicle_weight / 100),2)
        self.top_speed = top_speed
        return self.top_speed

    def generate_performance_report(self,car,ecu):
        tuned_hp = car.engine.stock_horsepower + ecu.profile.horsepower_gain
        tuned_torque = car.engine.stock_torque + ecu.profile.torque_gain
        print("\n========== PERFORMANCE REPORT ==========\n")
        print("Vehicle Information")
        print("--------------------")
        print(f"Company : {car.company}")
        print(f"Model :   {car.model}")
        print(f"Year :    {car.year}")
        print(f"VIN :     {car.vin}\n")
        print("Engine Information")
        print("--------------------")
        print(f"Engine :      {car.engine.engine_code}")
        print(f"Fuel Type :   {car.engine.fuel_type}")
        print(f"Aspiration :  {car.engine.aspiration}\n")
        print("ECU Information")
        print("-----------------")
        print(f"ECU Brand : {ecu.ecu_brand}")
        print(f"ECU Model : {ecu.ecu_model}")
        print(f"Profile :   {ecu.profile.profile_name}\n")
        print("Power")
        print("--------")
        print(f"Stock Horsepower :   {car.engine.stock_horsepower} HP")
        print(f"Horsepower Gain :   +{ecu.profile.horsepower_gain} HP")
        print(f"Tuned Horsepower :   {tuned_hp} HP")
        print(f"Wheel Horsepower :   {self.wheel_horsepower} HP\n")
        print(f"Stock Torque :       {car.engine.stock_torque} Nm")
        print(f"Torque Gain :       +{ecu.profile.torque_gain} Nm")
        print(f"Tuned Torque :       {tuned_torque} Nm")
        print(f"Wheel Torque :       {self.wheel_torque} Nm\n")
        print("Performance")
        print("------------")
        print(f"0-100 km/h :   {self.zero_to_hundred} sec")
        print(f"Quarter Mile : {self.quarter_mile} sec")
        print(f"Top Speed :    {self.top_speed} km/h\n")
        print("=========================================")