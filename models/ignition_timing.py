# Ignition Timing
class IgnitionTiming:
    def __init__(self,timing_name,timing_advance,timing_retard,knock_detection,safe_limit,octane_requirement):
        self.timing_name = timing_name
        self.timing_advance = timing_advance
        self.timing_retard = timing_retard
        self.knock_detection = knock_detection
        self.safe_limit = safe_limit
        self.octane_requirement = octane_requirement
        
    def display_ignition_timing(self):
        print("========== IGNITION TIMING ===========")
        print(f"Timing Name : {self.timing_name}")
        print(f"Timing Advance : {self.timing_advance}°")
        print(f"Timing Retared : {self.timing_retard}°")
        print(f"Knock Detection : {self.knock_detection}")
        print(f"Safe Limit : {self.safe_limit}")
        print(f"Octane Requirement : {self.octane_requirement}")
        print()

    def update_ignition_timing(self):
        print("1. Update Timing Name")
        print("2. Update Timing Advance")
        print("3. Update Timing Retared")
        print("4. Update Knock Detection")
        print("5. Update Safe Limit")
        print("6. Update Octance Requrimenet")
        print()
        choice = input("Enter Your choice:- ")
        if choice == "1":
            new_timing_name = input("Enter new Timing Name:- ")
            self.timing_name = new_timing_name
            print(f"Timing Name update successfully to {self.timing_name}")
        elif choice == "2":
            new_timing_advance = input("Enter new Timing Advance:- ")
            self.timing_advance = new_timing_advance
            print(f"Timing Advance update successfully to {self.timing_advance}")
        elif choice == "3":
            new_timing_retard = input("Enter new Timing Retared:- ")
            self.timing_retard = new_timing_retard
            print(f"Timing Retared update successfully to {self.timing_retard}")
        elif choice == "4":
            new_knock_detection = input("Enter new Knock Detection:- ")
            self.knock_detection = new_knock_detection
            print(f"Knock Detection update successfully to {self.knock_detection}")
        elif choice == "5":
            new_safe_limit = input("Enter new Safe limit:- ")
            self.safe_limit = new_safe_limit
            print(f"Safe Limit Update successfully to {self.safe_limit}")
        elif choice == "6":
            new_octane_requirement = input("Enter new Octance Requrimenet:- ")
            self.octane_requirement = new_octane_requirement
            print(f"Octance Requirement update successfully to {self.octane_requirement}")
        else:
            print("Invalid Choice!!!!")

    def to_dict(self):
        return{"timing_name": self.timing_name,
               "timing_advance":self.timing_advance,
               "timing_retard":self.timing_retard,
               "knock_detection":self.knock_detection,
               "safe_limit":self.safe_limit,
               "octane_requirement":self.octane_requirement}