class Engine:
    def __init__(self,engine_code,displacement_cc,cylinders,fuel_type,aspiration,stock_horsepower,stock_torque,compression_ratio,redline_rpm,engine_status):
        self.engine_code = engine_code
        self.displacement_cc = displacement_cc
        self.cylinder = cylinders
        self.fuel_type = fuel_type
        self.aspiration = aspiration
        self.stock_horsepower = stock_horsepower
        self.stock_torque = stock_torque
        self.compression_ratio = compression_ratio
        self.redline_rpm = redline_rpm
        self.engine_status = engine_status

    def display_engine(self):
        print("============== ENGINE INFORMATION ==============")
        print(f"Engine code : {self.engine_code}")
        print(f"Displacement in cc : {self.displacement_cc} cc")
        print(f"Cylinder : {self.cylinder}")
        print(f"Fuel type : {self.fuel_type}")
        print(f"Aspiration : {self.aspiration}")
        print(f"Stock Horsepower : {self.stock_horsepower} HP")
        print(f"Stock Troque : {self.stock_torque} Nm")
        print(f"Compression Ratio : {self.compression_ratio}")
        print(f"Redline RPM : {self.redline_rpm} RPM")
        print(f"Engine_status: {self.engine_status}")
        print()

    def update_engine(self):
        print("1. Update Engine code:- ")
        print("2. Update Engine Displacement:- ")
        print("3. Update Cylinder:- ")
        print("4. Update Fuel Type:- ")
        print("5. Update Aspiration:- ")
        print("6. Update Stock Horsepower:- ")
        print("7. Update Stock Troque:- ")
        print("8. Update Compression Ratio:- ")
        print("9. Update Redline RPM:- ")
        print("10. Update Engine status:- ")
        print()
        choice = input("Enter your choice:- ")
        if choice == "1":
            new_engine_code = input("Enter New Engine Code:- ")
            self.engine_code = new_engine_code
            print(f"Engine Code Update succefully to {self.engine_code}!!!!")
        elif choice == "2":
            new_displacement = input("Enter new Displacement in CC:- ")
            self.displacement_cc = new_displacement
            print(f"Displacement Update succefully to {self.displacement_cc}!!!!")
        elif choice == "3":
            new_cylinder = input("Enter new Cylinder:- ")
            self.cylinder = new_cylinder
            print(f"Cylinder Update succefully to {self.cylinder}!!!!")
        elif choice == "4":
            new_fuel_type = input("Enter new Fuel type:- ")
            self.fuel_type = new_fuel_type
            print(f"Fuel Type Update succefully to {self.fuel_type}!!!!")
        elif choice == "5":
            new_aspiration = input("Enter new Aspiration:- ")
            self.aspiration = new_aspiration
            print(f"Aspiration Update succefully to {self.aspiration}!!!!")
        elif choice == "6":
            new_stock_horsepower = input("Enter new Stock Horsepower:- ")
            self.stock_horsepower = new_stock_horsepower
            print(f"Stock Horsepower Update succefully to {self.stock_horsepower}!!!!")
        elif choice == "7":
            new_stock_torque = input("Enter new Stock Torque:- ")
            self.stock_torque = new_stock_torque
            print(f"Stock torque Update succefully to {self.stock_torque}!!!!")
        elif choice == "8":
            new_compression_ratio = input("Enter new Compression Ratio:- ")
            self.compression_ratio = new_compression_ratio
            print(f"Compression Ratio Update succefully to {self.compression_ratio}!!!!")
        elif choice == "9":
            new_redline_rpm = input("Enter new Redline RPM:- ")
            self.redline_rpm = new_redline_rpm
            print(f"Redline RPM Update succefully to {self.redline_rpm}0!!!!")
        elif choice == "10":
            new_engine_status = input("Enter new Engine Status:- ")
            self.engine_status = new_engine_status
            print(f"Engine status Update succefully to {self.engine_status}!!!!")
        else:
            print("Invalid Choice....")

    def to_dict(self):
        return {"engine_code": self.engine_code,
                "displacement_cc": self.displacement_cc,
                "cylinders": self.cylinder,
                "fuel_type": self.fuel_type,
                "aspiration": self.aspiration,
                "stock_horsepower": self.stock_horsepower,
                "stock_torque": self.stock_torque,
                "compression_ratio": self.compression_ratio,
                "redline_rpm": self.redline_rpm,
                "engine_status": self.engine_status}