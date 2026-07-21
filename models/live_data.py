# Phase 9 Live Data
import random
import time

class LiveData:
    def __init__(self,rpm,speed,engine_temperature,throttle_position,boost_pressure,air_fuel_ratio,battery_voltage,gear):
        self.rpm = rpm
        self.speed = speed
        self.engine_temperature = engine_temperature
        self.throttle_position = throttle_position
        self.boost_pressure = boost_pressure
        self.air_fuel_ratio = air_fuel_ratio
        self.battery_voltage = battery_voltage
        self.gear = gear

    def display_live_data(self):
        print("========== LIVE DATA ==========")
        print(f"RPM : {self.rpm}")
        print(f"Speed : {self.speed} km/h")
        print(f"Engine Temp : {self.engine_temperature} °C")
        print(f"Throttle Position : {self.throttle_position} %")
        print(f"Boost Pressure : {round(self.boost_pressure, 2)} bar")
        print(f"Air Fuel Ratio : {round(self.air_fuel_ratio, 2)}")
        print(f"Battery Voltage : {round(self.battery_voltage, 2)} V")
        print(f"Gear : {self.gear}")
        
    def to_dict(self):
        return{"rpm":self.rpm,
               "speed":self.speed,
               "engine_temperature":self.engine_temperature,
               "throttle_position":self.throttle_position,
               "boost_pressure":self.boost_pressure,
               "air_fuel_ratio":self.air_fuel_ratio,
               "battery_voltage":self.battery_voltage,
               "gear":self.gear}
    
    def start_live_monitor(self):
        print("Connecting to ECU....")
        time.sleep(2)
        print("Live Data Started....\n")
        time.sleep(2)
        for _ in range(10):
            self.rpm += random.randint(-200,300)
            self.speed += random.randint(-5,10)
            self.engine_temperature += random.randint(-1,2)
            self.throttle_position += random.randint(-10,10)
            self.boost_pressure += round(random.uniform(-0.2,0.3),2)
            self.air_fuel_ratio += round(random.uniform(-0.3,0.3),2)
            self.battery_voltage += round(random.uniform(-0.2,0.2),2)
            print("========== LIVE DATA ==========")
            print(f"RPM : {self.rpm}")
            print(f"Speed : {self.speed} km/h")
            print(f"Engine Temp : {self.engine_temperature} °C")
            print(f"Throttle Position : {self.throttle_position} %")
            print(f"Boost Pressure : {self.boost_pressure} bar")
            print(f"Air Fuel Ratio : {self.air_fuel_ratio}")
            print(f"Battery Voltage : {self.battery_voltage} V")
            print(f"Gear : {self.gear}")
            print()
            time.sleep(1)
            self.speed = max(0, self.speed)
            self.rpm = max(800, self.rpm)
            self.engine_temperature = max(70, self.engine_temperature)
            self.throttle_position = max(0, min(100, self.throttle_position))
            self.boost_pressure = max(0, self.boost_pressure)
            self.battery_voltage = max(12.0, self.battery_voltage)
        
    def update_live_data(self):
        print("========== UPDATE LIVE DATA ==========")
        print("1. Update RPM")
        print("2. Update Speed")
        print("3. Update Engine Temperature")
        print("4. Update Throttle Position")
        print("5. Update Boost Pressure")
        print("6. Update Air Fuel Ratio")
        print("7. Update Battery Voltage")
        print("8. Update Gear")
        print()
        choice = input("Enter Your Choice:- ")
        if choice == "1":
            new_rpm = int(input("Enter new RPM:- "))
            self.rpm = new_rpm
            print(f"RPM update successfully to {self.rpm}")
        elif choice == "2":
            new_speed = int(input("Enter new Speed:- "))
            self.speed = new_speed
            print(f"Speed update successfully to {self.speed}")
        elif choice == "3":
            new_engine_temperature = int(input("Enter new Engine Temperature:- "))
            self.engine_temperature = new_engine_temperature
            print(f"Engine Temperature Update successfully to {self.engine_temperature}")
        elif choice == "4":
            new_throttle_position = int(input("Enter new Throttle Position:- "))
            self.throttle_position = new_throttle_position
            print(f"Throttle Position Update successfully to {self.throttle_position}")
        elif choice == "5":
            new_boost_pressure = float(input("Enter new Boost Pressure:- "))
            self.boost_pressure = new_boost_pressure
            print(f"Boost Pressure update successfully to {self.boost_pressure}")
        elif choice == "6":
            new_air_fuel_ratio = float(input("Enter new Air Fuel Ratio:- "))
            self.air_fuel_ratio = new_air_fuel_ratio
            print(f"Air Fuel Ratio update successfully to {self.air_fuel_ratio}")
        elif choice == "7":
            new_battery_voltage = float(input("Enter New Battery Voltage:- "))
            self.battery_voltage = new_battery_voltage
            print(f"Battery Voltage Update successfully to {self.battery_voltage}")
        elif choice == "8":
            new_gear = int(input("Enter New Gear:- "))
            self.gear = new_gear
            print(f"Geat Update successfully to {self.gear}")
        else:
            print("Invalid Choice....")