from .context import main, exceptions
import unittest


class TestReservoir(unittest):
    initial_weight = 0

    def setUp(self):
        self.reservoir = main.Reservoir()

    def test_increase_the_weight_in_reservoir(self):
        weight = 400
        self.reservoir.increase_weight(weight)
        assert self.reservoir.current_weight == 400, ''

    def test_reduce_weight_in_reservoir(self):
        weight = 400
        assert self.reservoir.reduce_weight(weight) == 0

    def test_get_current_weight(self):
        weight = 400
        self.reservoir.increase_weight(weight)
        assert self.reservoir.get_current_weight() == 400

        self.reservoir.reduce_weight(weight)
        assert self.reservoir.get_current_weight() == 0


class TestWaterLevelSensor(unittest):
    def  setUp(self, reservoir):
        self.reservoir = main.Reservoir()
        self.water_level_sensor = main.WaterLevelSensor()

    def test_check_the_water_level(self):
        assert self.water_level_sensor.check_the_water_level()


class TestWaterHeater(unittest):
    def  setUp(self):
        self.waterheater = main.WaterHeater()
        self.room_temperature = 20
        self.water_temperature = self.room_temperature

    def test_water_heating(self):
        self.waterheater.water_heating()
        assert self.waterheater.water_temperature >=100.02

    def test_get_current_water_heating(self):
        self.waterheater.water_heating()
        assert self.waterheater.get_current_water_heating()


class TestWaterHeatingSensor(unittest):
    def setUp(self):
        self.waterheater = main.WaterHeater()
        self.waterheatingsensor = main.WaterHeatingSensor()

    def check_temperature_water(self):
        self.waterheater.water_heating()
        assert self.waterheatingsensor.check_temperature_water


class TestAmountCoffee(unittest):
    def setUp(self):
        self.amountcoffee = main.AmountCoffee()
        self.amount = 400

    def test_change_amount(self):
        self.amountcoffee.change_amount(self.amount)
        assert self.amountcoffee.current_amount == 400

    def test_get_current_amount_coffee(self):
        self.amountcoffee.change_amount(self.amount)
        assert self.amountcoffee.get_current_amount_coffee() == 400


class TestCoffeeLevelSensor(unittest):
    def setUp(self):
        self.coffeelevelsensor = main.CoffeeLevelSensor()
        self.amountcoffee = main.AmountCoffee()
        self.amount = 400

    def test_check_the_coffee_level(self):
        self.amountcoffee.change_amount(self.amount)
        assert self.coffeelevelsensor.check_the_coffee_level()

class TestPot(unittest):
    def setUp(self):
        self.pot = main.Pot()
        self.weight = 400

    def test_increase_weight(self):
        self.pot.increase_weight(self.weight)
        assert self.pot.current_weight == 400

    def test_reduce_weight(self):
        self.pot.increase_weight(self.weight)
        self.pot.reduce_weight(self.weight)
        assert self.pot.current_weight == 0

    def test_get_current_weight(self):
        self.pot.increase_weight(self.weight)
        assert self.pot.get_current_weight() == 400

        self.pot.reduce_weight(self.weight)
        assert self.pot.get_current_weight() == 0


class TestPump(unittest):
    def setUp(self):
        self.pump = main.Pump()
        self.pot = main.Pot()
        self.reservoir = main.Reservoir()
        self.step =10
        self.weight = 400

    def test_pour_water(self):
        self.reservoir.increase_weight(self.weight)
        self.pump.pour_water(self.step, self.pot)
        assert self.reservoir.current_weight == 0
        assert self.pot.current_weight == 400

    def test_push_water(self):
        self.reservoir.increase_weight(self.weight)
        self.pump.push_water()
        assert self.reservoir.current_weight == 0
        assert self.pot.current_weight == 400


class TestDrinkLevelSensor(unittest):
    def setUp(self):
        self.drinklevelsensor = main.DrinkLevelSensor()

    def test_check_the_drink_level(self):
        self.reservoir.increase_weight(self.weight)
        self.pump.push_water()
        assert self.drinklevelsensor.check_the_drink_level()


class TestPlate(unittest):
    def setUp(self):
        self.palte = main.Plate()
        self.platelvelsensor = main.PlateLevelSensor()
        self.pot = main.Pot()
        self.weight = 400

    def test_start_warming(self):
        self.pot.increase_weight(self.weight)
        self.platelvelsensor.check_the_plate_empty(self.pot)
        self.platelvelsensor.check_the_plate_empty_pot_level()
        assert self.plate.start_warming(self.pot)

    def test_stop_warming(self):
        self.pot.increase_weight(self.weight)
        self.platelvelsensor.check_the_plate_empty(self.pot)
        self.platelvelsensor.check_the_plate_empty_pot_level()
        assert not self.palte.stop_warming(self.pot)

    def test_is_warming(self):
        self.pot.increase_weight(self.weight)
        self.platelvelsensor.check_the_plate_empty(self.pot)
        self.platelvelsensor.check_the_plate_empty_pot_level()
        self.palte.stop_warming(self.pot)
        assert self.plate.is_warming()


class TestPlateLevelSensor(unittest):
    def setUp(self):
        self.platelvelsensor = main.PlateLevelSensor()
        self.pot = main.Pot()
        self.weight = 400

    def test_check_the_plate_empty(self):
        self.pot.increase_weight(self.weight)
        assert not self.platelvelsensor.check_the_plate_empty()

    def test_check_the_plate_empty_pot_level(self):
        self.pot.increase_weight(self.weight)
        assert not self.platelvelsensor.check_the_plate_empty_pot_level()


class TestCoffeeMaker(unittest):
    def setUp(self):
       self.coffemaker = main.CoffeeMaker

    def test_state_coffee_brew_stop(self):
        self.coffemaker.state_coffee_brew_stop()
        assert not self.coffemaker.state_coffee_brew_in_progress

    def test_check_state_heating_water(self):
        self.waterheater = main.WaterHeater()
        self.waterheater.water_heating()
        self.waterheatingsensor = main.WaterHeatingSensor()
        self.waterheatingsensor.check_temperature_water()
        self.coffemaker.check_state_heating_water()
        assert self.coffemaker.state_heating_water

    def test_check_state_drink_is_ready(self):
        self.reservoir = main.Reservoir()
        self.drinklevelsensor = main.DrinkLevelSensor()
        assert self.drinklevelsensor.check_the_drink_level()

    def test_coffee_making_is_started(self):
        assert self.coffee_maker.state_coffee_brew_in_progress is False
        self.coffee_maker.brew_coffee()
        with self.assertRaises(exceptions.CoffeeBrewInProgressException):
            self.coffee_maker.brew_coffee()


































