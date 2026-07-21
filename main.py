from managers.ecu_manager import ECUManager

manager = ECUManager()

manager.create_test_ecu()

manager.ecus[0].profile.live_data.update_live_data()

manager.ecus[0].profile.live_data.display_live_data()

manager.ecus[0].profile.live_data.start_live_monitor()