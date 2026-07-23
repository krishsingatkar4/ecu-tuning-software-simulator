from managers.car_manager import CarManager

manager = CarManager()

manager.create_demo_project()

car = manager.cars[0]

car.ecu.profile.dyno.generate_performance_report(car,car.ecu)
car.ecu.profile.dyno.performance_analysis(car, car.ecu)