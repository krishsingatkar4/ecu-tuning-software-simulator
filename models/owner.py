# ECU_Tuning_Simulator
class Owner:
    def __init__(self,owner_id,name,phone,email,city):
        self.owner_id = owner_id
        self.name = name
        self.phone = phone
        self.email = email
        self.city = city

    def display_owner(self):
        print("========== OWNER INFORMATION ==========")
        print(f"Owner ID : {self.owner_id}")
        print(f"Name : {self.name}")
        print(f"Phone : {self.phone}")
        print(f"Email : {self.email}")
        print(f"City : {self.city}")
        print()

    def update_owner(self):
        print("========== UPDATE OWNER ==========\n"
        "1. Change Owner ID:- " \
        "2. Change Name:- " \
        "3. Change Phone:- " \
        "4. Change Email:- " \
        "5. Change City:- \n")
        choice = input("Enter your choice:- ")
        if choice == "1":
            new_owner_id = input("Enter the new Owner ID:- ")       
            self.owner_id = new_owner_id
            print(f"Owner ID change successfully to {self.owner_id}")
        elif choice == "2":
            new_name = input("Enter the new name:- ")
            self.name = new_name
            print(f"Name changed successfully to {self.name}")
        elif choice == "3":
            new_phone = input("Enter new phone:- ")
            self.phone = new_phone
            print(f"Phone number changed successfully to {self.phone}")
        elif choice == "4":
            new_email = input("Enter the new email:- ")
            self.email = new_email
            print(f"Email changed successfully to {self.email}")
        elif choice == "5":
            new_city = input("Enter new city:- ")
            self.city = new_city
            print(f"City changed successfully to {self.city}")
        else:
            print("Invaild Choice....")

    def to_dict(self):
        return {"owner_id": self.owner_id,
                "name": self.name,
                "phone": self.phone,
                "email": self.email,
                "city": self.city}