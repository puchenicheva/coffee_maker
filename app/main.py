from time import sleep
from . import exceptions


class Reservoir(object):
    initial_weight = 0

    def __init__(self):
        self.current_weight = self.initial_weight

    def increase_weight(self, weight):
        self.current_weight += weight

    def get_current_weight(self):
        return self.current_weight - self.initial_weight

    def reduce_weight(self, weight):
        if self.current_weight - weight >= 0:
            self.current_weight -= weight
            return weight
        else:
            self.current_weight = 0
            return self.current_weight - weight


class WaterLevelSensor(object):
    def __init__(self, reservoir):
        self.reservoir = reservoir

    def check_the_water_level(self):
        return self.reservoir.initial_weight < self.reservoir.current_weight


class WaterHeater(object):
    room_temperature = 20

    def __init__(self):
        self.water_temperature = self.room_temperature

    def water_heating(self):
        while self.water_temperature <= 100:
            sleep(0.1)
            self.water_temperature += 0.91

    def get_current_water_heating(self):
        return self.water_temperature


class WaterHeatingSensor(object):
    def __init__(self, water_heater):
        self.water_heater = water_heater

    def check_temperature_water(self):
        return self.water_heater.get_current_water_heating() >= 100


class AmountCoffee(object):
    initial_amount = 0

    def __init__(self):
        self.current_amount = self.initial_amount

    def change_amount(self, amount):
        self.current_amount += amount

    def get_current_amount_coffee(self):
        return self.current_amount


class CoffeeLevelSensor(object):
    def __init__(self, amount_coffee):
        self.amount_coffee = amount_coffee

    def check_the_coffee_level(self):
        return self.amount_coffee.initial_amount < self.amount_coffee.get_current_amount_coffee()


class Pot(object):
    """
    Емкость для готового кофе
    """

    initial_weight = 0

    def __init__(self):
        self.current_weight = self.initial_weight

    def increase_weight(self, weight):
        self.current_weight += weight

    def get_current_weight(self):
        return self.current_weight

    def reduce_weight(self, weight):
        self.current_weight -= weight


class Pump(object):
    """Насос"""
    water_step = 10

    def __init__(self, reservoir):
        self.reservoir = reservoir

    def pour_water(self, step, pot):
        pot.increase_weight(self.reservoir.reduce_weight(step))

    def push_water(self, pot):
        while self.reservoir.get_current_weight() > 0:
            self.pour_water(self.water_step, pot)


class DrinkLevelSensor(object):
    def __init__(self, reservoir):
        self.reservoir = reservoir

    def check_the_drink_level(self):
        return self.reservoir.get_current_weight() == self.reservoir.initial_weight


class Plate(object):

    def __init__(self):
        self.warming_state = False
        self.plate_level_sensor = PlateLevelSensor()

    def start_warming(self, pot):
        if (not self.plate_level_sensor.check_the_plate_empty_pot_level(pot) and
                not self.plate_level_sensor.check_the_plate_empty(pot)):
            self.warming_state = True

    def stop_warming(self, pot):
        if (self.plate_level_sensor.check_the_plate_empty_pot_level(pot) or
                self.plate_level_sensor.check_the_plate_empty(pot)):
            self.warming_state = False

    def is_warming(self):
        return self.warming_state


class PlateLevelSensor(object):
    def check_the_plate_empty(self, pot):
        return pot is None

    def check_the_plate_empty_pot_level(self, pot):
        return pot.get_current_weight() <= pot.initial_weight


class CoffeeMaker(object):

    def __init__(self):
        self.reservoir = Reservoir()
        self.plate = Plate()
        self.pot = None

        self.state_coffee_brew_in_progress = False
        self.water_level_sensor = WaterLevelSensor(self.reservoir)

        self.waterheater = WaterHeater()
        self.state_heating_water = False
        self.water_heating_sensor = WaterHeatingSensor(self.waterheater)

        self.amount_coffee = AmountCoffee()
        self.coffee_level_sensor = CoffeeLevelSensor(self.amount_coffee)

        self.state_pressure_valve = True

        self.pump = Pump(self.reservoir)
        self.drink_level_sensor = DrinkLevelSensor(self.reservoir)
        self.state_drink_is_ready = False

        self.indicator_ready_is_drink = False

        self.plate_level_sensor = PlateLevelSensor()

    def state_coffee_brew_stop(self):
        self.state_coffee_brew_in_progress = False

    def check_state_heating_water(self):
        if self.water_heating_sensor.check_temperature_water():
            self.state_heating_water = True

    def check_state_drink_is_ready(self):
        if self.drink_level_sensor.check_the_drink_level():
            self.state_drink_is_ready = True
            return self.state_drink_is_ready

    def brew_coffee(self):
        if self.state_coffee_brew_in_progress:
            raise exceptions.CoffeeBrewInProgressException()
        self.state_coffee_brew_in_progress = True

        if not self.water_level_sensor.check_the_water_level():
            self.state_coffee_brew_stop()
            raise exceptions.CheckTheWaterException()

        self.waterheater.water_heating()
        self.check_state_heating_water()
        if self.plate_level_sensor.check_the_plate_empty(self.pot):
            self.state_coffee_brew_stop()
            raise exceptions.CheckThePlateEmptyException()

        if self.state_heating_water:
            if not self.coffee_level_sensor.check_the_coffee_level():
                self.state_coffee_brew_stop()
                raise exceptions.CheckTheCoffeeException()
            self.state_pressure_valve = False
            self.pump.push_water(self.pot)

            if self.check_state_drink_is_ready():
                self.indicator_ready_is_drink = True
                self.state_coffee_brew_in_progress = False
                self.state_pressure_valve = True
                self.plate.start_warming(self.pot)

    def pour_water_into_the_boiler(self, reservoir):
        self.reservoir.increase_weight(reservoir)

    def drop_coffee(self, amount_coffee):
        self.amount_coffee.change_amount(amount_coffee)

    def take_pot(self,pot):
        if self.plate_level_sensor.check_the_plate_empty(self.pot):
            raise exceptions.TakePotException()

        if self.plate.is_warming():
            self.plate.stop_warming(pot)
        pot_returned = self.pot
        self.pot = None
        return pot_returned

    def put_pot(self, pot):
        if not self.plate_level_sensor.check_the_plate_empty(self.pot):
            raise exceptions.PutPotException()

        self.pot = pot
        if (self.state_coffee_brew_in_progress and
                not self.plate_level_sensor.check_the_plate_empty_pot_level(self.pot) and
                not self.plate.is_warming()):
            self.plate.start_warming(self.pot)
