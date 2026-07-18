from managers import ecu_manager

manager = ecu_manager.ECUManager()
manager.add_ecus()

#manager.create_test_ecu()

manager.display_all_ecus()

diagnostic = manager.ecus[-1].profile.diagnostic

diagnostic.update_diagnostic()
diagnostic.scan_fault()
diagnostic.clear_fault()
manager.display_all_ecus()