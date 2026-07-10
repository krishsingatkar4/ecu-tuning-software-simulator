from managers.car_manager import CarManager
manager = CarManager()

while True:
    print("\n========== ECU TUNING SOFTWARE ==========")
    print("1. Add Car")
    print("2. Search Car")
    print("3. Display All Cars")
    print("4. Update Car")
    print("5. Delete Car")
    print("6. Exit")
    print()
    choice = input("Enter your choice:- ")
    if choice == "1":
        manager.add_cars()
    elif choice == "2":
        manager.search_car()
    elif choice == "3":
        manager.display_all_cars()
    elif choice == "4":
        manager.update_car()
    elif choice == "5":
        manager.delete_car()
    elif choice == "6":
        print("Thank you for using our ECU Tuning Software!")
        break
    else:
        print("Invalid choice!")