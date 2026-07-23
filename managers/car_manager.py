from models.owner import Owner
from models.engine import Engine
from models.car import Car
from managers.ecu_manager import ECUManager
from models.ecu import ECU
from models.ecu_firware import ECUFirmware
from models.fuel_map import FuelMap
from models.ecu_profile import ECUProfile
from models.live_data import LiveData
from models.ignition_timing import IgnitionTiming
from models.turbo import Turbo
from models.dyno import Dyno
from models.diagnostic import Diagnostic
from models.ecu_flash import ECUFlash
import time
import json

class CarManager:
    def __init__(self):
        self.cars = []
        self.load_cars()

    def add_cars(self):
        owner_id = input("Enter owner id:- ")
        name = input("Enter name:- ")
        phone = input("Enter phone:- ")
        email = input("Enter email:- ")
        city = input("Enter city:- ")
        owner = Owner(owner_id,name,phone,email,city)
        engine_code = input("Enter engine code:- ")
        displacement_cc = input("Enter diplacement in cc:- ")
        cylinders = input("Enter cylinders number:- ")
        aspiration = input("Enter aspiration:- ")
        fuel_type = input("Enter fuel Type:- ")
        stock_horsepower = input("Enter stock horsepower:- ")
        stock_torque = input("Enter stock torque:- ")
        compression_ratio = input("Enter compression ratio:- ")
        redline_rpm = input("Enter redline rpm:- ")
        engine_status = input("Enter engine status:- ")
        engine = Engine(engine_code,displacement_cc,cylinders,fuel_type,aspiration,stock_horsepower,stock_torque,compression_ratio,redline_rpm,engine_status)
        vin = input("Enter vin:- ")
        company = input("Enter company:- ")
        model = input("Enter model:- ")
        year = input("Enter year:- ")
        transmission = input("Enter transmission:- ")
        drive_type = input("Enter drive type:- ")
        mileage = input("Enter mileage:- ")
        color = input("Enter color:- ")
        license_plate = input("Enter license plate:- ")
        car = Car(vin,company,model,year,transmission,drive_type,mileage,color,license_plate,owner,engine)
        self.cars.append(car)
        self.save_cars()
        print("Car added successfully!")
        
    def search_car(self):
        car_vin = input("Enter the VIN of the car which you want to search:- ")
        for car in self.cars:
            if car.vin.lower().strip() == car_vin.lower().strip():
                print("Searching the VIN....")
                time.sleep(2)
                print("Car VIN found successfully....")
                car.display_car()
                return
            print("Car not found!!!!")        

    def display_all_cars(self):
        if not self.cars:
            print("Searching for the Cars....")
            time.sleep(2)
            print("No Cars Found!!!!")
        else:
            for car in self.cars:
                car.display_car()
                print()
                
    def delete_car(self):
        vin = input("Enter the VIN of the car to delete the car:- ")
        print("Searching for VIN of the car")
        time.sleep(2)
        if not self.cars:
            print("No Car Found!!!!")
        else:
            for car in self.cars:
                if car.vin.lower().strip() == vin.lower().strip():
                    car.display_car()
                    self.cars.remove(car) 
                    self.save_cars()
                    print("The Car with above Information deleted successfully....")
                    return
            else:
                print("Car not found!!!!")
       
    def update_car(self):
        vin = input("Enter VIN of the car of which you want to Update information:- ")
        print("Searching for VIN of the car")
        time.sleep(2)
        if not self.cars:
            print("No Cars found!!!!")
        else:
            for car in self.cars:
                if car.vin.lower().strip() == vin.lower().strip():
                    print("Updating your car information")
                    time.sleep(2)
                    car.update_car() 
                    self.save_cars()
                    print("Your car information updated successfully....")
                    return
            else:
                print("Car not found!!!!")
       
    def save_cars(self):
        cars_data = []
        for car in self.cars:
            cars_data.append(car.to_dict())
        with open("database/cars.json","w") as file:
            json.dump(cars_data, file, indent=4)

    def load_cars(self):
        try:
            with open("database/cars.json", "r") as file:
                cars_data = json.load(file)
            for car_data in cars_data:
                owner_info = car_data["owner"]
                engine_info = car_data["engine"]
                owner = Owner(owner_info["owner_id"],
                            owner_info["name"],
                            owner_info["phone"],
                            owner_info["email"],
                            owner_info["city"])
                engine = Engine(engine_info["engine_code"],
                                engine_info["displacement_cc"],
                                engine_info["cylinders"],
                                engine_info["fuel_type"],
                                engine_info["aspiration"],
                                engine_info["stock_horsepower"],
                                engine_info["stock_torque"],
                                engine_info["compression_ratio"],
                                engine_info["redline_rpm"],
                                engine_info["engine_status"])
                car = Car(car_data["vin"],
                            car_data["company"],
                            car_data["model"],
                            car_data["year"],
                            car_data["transmission"],
                            car_data["drive_type"],
                            car_data["mileage"],
                            car_data["color"],
                            car_data["license_plate"],
                            owner,
                            engine)
                self.cars.append(car)
        except FileNotFoundError:
            print("Database not found...")

    def attach_ecu(self):
        vin = input("Enter the VIN of car which you want to attach:- ")
        for attach in self.cars:
            if attach.vin.lower().strip() == vin.lower().strip():
                ecu_manager = ECUManager()
                ecu_manager.add_ecus()
                attach.ecu = ecu_manager.ecus[-1]
                attach.ecu.profile.dyno.calculate_wheel_power(
                attach.engine.stock_horsepower,
                attach.ecu.profile.horsepower_gain)
                attach.ecu.profile.dyno.calculate_wheel_torque(
                attach.engine.stock_torque,
                attach.ecu.profile.torque_gain)
                self.save_cars()
                print("ECU attached successfully....")
                break
        else:
            print("Car not found....")

    def create_demo_project(self):
        owner = Owner(
            owner_id="OWN001",
            name="Krish",
            phone="9876543210",
            email="krish@gmail.com",
            city="Pune")
        
        engine = Engine(
            engine_code="S58",
            displacement_cc=3000,
            cylinders=6,
            fuel_type="Petrol",
            aspiration="Twin Turbo",
            stock_horsepower=530,
            stock_torque=650,
            compression_ratio=9.3,
            redline_rpm=7500,
            engine_status="Healthy")

        fuel_map = FuelMap(
            "Street Tune",
            12.3,
            "850cc",
            "5.5 bar",
            "Sport",
            "Petrol")

        ignition = IgnitionTiming(
            "Race Timing",
            10,
            2,
            "Enable",
            9000,
            100)

        turbo = Turbo(
            "GTX3582R",
            "Garrett",
            "Twin Turbo",
            2.0,
            1.4,
            3500,
            "Enable",
            "Front Mount",
            800)

        dyno = Dyno(
            "Race Dyno",
            1500,
            15,
            0,
            0,
            0)
        
        diagnostic = Diagnostic(
            "P0300",
            "Random Misfire",
            "High",
            "Active",
            "Crankshaft Sensor",
            "Engine misfire detected")

        flash = ECUFlash(
            "Stage 5 Flash",
            "stage5.bin",
            "V2.0",
            72,
            "Ready",
            "Not Created",
            120)
        
        live_data = LiveData(
            900,
            0,
            85,
            0,
            0,
            14.7,
            12.6,
            1)

        profile = ECUProfile(
            "Stage 5",
            fuel_map,
            ignition,
            9000,
            "Enable",
            "Enable",
            220,
            300,
            turbo,
            dyno,
            diagnostic,
            flash,
            live_data)

        ecu = ECU(
            "ECU010",
            "Bosch",
            "MED17.5",
            "CAN Bus",
            "Connected",
            [
                "Fuel Map",
                "Launch Control",
                "Turbo",
                "Dyno",
                "Diagnostic",
                "Flash",
                "Live Data"
            ],
            ECUFirmware(
                "V10",
                "Bosch",
                2026,
                "XYZ999",
                "Ready",
                64
            ),
            profile)

        dyno.calculate_wheel_horsepower(engine.stock_horsepower,profile.horsepower_gain)
        dyno.calculate_wheel_torque(engine.stock_torque,profile.torque_gain)
        dyno.calculate_zero_to_hundred(dyno.wheel_horsepower)
        dyno.calculate_quarter_mile(dyno.wheel_horsepower)
        dyno.calculate_top_speed(dyno.wheel_horsepower, dyno.vehicle_weight)

        car = Car(
            vin="MP68",
            company="BMW",
            model="M4 Competition",
            year=2026,
            transmission="Automatic",
            drive_type="RWD",
            mileage=0,
            color="Black",
            license_plate="MH12AB1234",
            owner=owner,
            engine=engine,
            ecu=ecu)
        self.cars.append(car)
        print("Demo project created successfully...")