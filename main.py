from managers.ecu_manager import ECUManager

manager = ECUManager()

manager.create_test_ecu()

manager.display_all_ecus()

flash = manager.ecus[0].profile.flash

flash.creat_backup()
flash.start_flash()
flash.update_flash()