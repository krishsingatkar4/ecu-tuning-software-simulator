from managers.ecu_manager import ECUManager
from models.dyno import Dyno
manager = ECUManager()

manager.ecus[0].profile.dyno.calculation_performance()