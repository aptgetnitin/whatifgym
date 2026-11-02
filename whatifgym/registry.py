"""Registry of base models. Add a model by importing its class here."""
from __future__ import annotations

from .base import BaseModel


def _registry() -> dict[str, type[BaseModel]]:
    # Imported lazily so that `import whatifgym` stays cheap and solver-free.
    from .models.battery_scheduling.model import BatteryScheduling
    from .models.bin_packing.model import BinPacking
    from .models.car_rental.model import CarRental
    from .models.car_rental_2.model import CarRental2
    from .models.assignment_with_constraints.model import AssignmentWithConstraints
    from .models.covid19_facility_location.model import Covid19FacilityLocation
    from .models.economic_planning.model import EconomicPlanning
    from .models.fantasy_basketball.model import FantasyBasketball
    from .models.farm_planning.model import FarmPlanning
    from .models.factory_planning.model import FactoryPlanning
    from .models.factory_planning_2.model import FactoryPlanning2
    from .models.food_manufacture.model import FoodManufacture
    from .models.food_supply.model import FoodSupply
    from .models.manpower_planning.model import ManpowerPlanning
    from .models.mining.model import Mining
    from .models.multiple_knapsack.model import MultipleKnapsack
    from .models.optimize_power_schedule.model import OptimizePowerSchedule
    from .models.power_generation_hydro.model import PowerGenerationHydro
    from .models.railway_dispatching.model import RailwayDispatching
    from .models.wedding_seating.model import WeddingSeating
    from .models.technician_routing_scheduling.model import TechnicianRoutingScheduling
    from .models.drone_network.model import DroneNetwork
    from .models.airline_planning.model import AirlinePlanning
    from .models.jobshop_ft06.model import JobshopFt06
    from .models.single_machine_scheduling.model import SingleMachineScheduling

    classes = [FactoryPlanning, FactoryPlanning2, FoodManufacture, Mining, ManpowerPlanning, PowerGenerationHydro,
               MultipleKnapsack, BinPacking, WeddingSeating, CarRental,
               FarmPlanning, BatteryScheduling, CarRental2, FoodSupply, EconomicPlanning, FantasyBasketball,
               AssignmentWithConstraints, Covid19FacilityLocation, RailwayDispatching, OptimizePowerSchedule,
               TechnicianRoutingScheduling, DroneNetwork, AirlinePlanning, JobshopFt06, SingleMachineScheduling]
    return {cls.name: cls for cls in classes}


def list_models() -> list[str]:
    return sorted(_registry())


def get_model(name: str) -> BaseModel:
    reg = _registry()
    if name not in reg:
        raise KeyError(f"unknown model {name!r}; available: {sorted(reg)}")
    return reg[name]()
