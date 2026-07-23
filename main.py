from managers.car_manager import CarManager

manager = CarManager()

manager.create_demo_project()

print("\n===== DISPLAY TEST =====\n")

manager.display_all_cars()

car = manager.cars[0]

car.ecu.profile.dyno.generate_performance_report(car,car.ecu)