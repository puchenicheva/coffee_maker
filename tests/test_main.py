from .context import main, exceptions
from unittest.mock import patch
import unittest
import random


class TestReservoir(unittest.TestCase):
    initial_weight = 0

    def setUp(self):
        self.reservoir = main.Reservoir()
        self.weight = random.randint(100, 999)

    def test_increase_the_weight_in_reservoir(self):
        self.reservoir.increase_weight(self.weight)
        assert self.reservoir.current_weight == self.weight

    def test_reduce_weight_in_reservoir(self):
        self.reservoir.increase_weight(self.weight)
        assert self.reservoir.reduce_weight(self.weight) >= 0

    def test_get_current_weight(self):
        self.reservoir.increase_weight(self.weight)
        assert self.reservoir.get_current_weight() == self.weight

        self.reservoir.reduce_weight(self.weight)
        assert self.reservoir.get_current_weight() == 0


class TestWaterLevelSensor(unittest.TestCase):
    def setUp(self):
        self.reservoir = main.Reservoir()
        self.water_level_sensor = main.WaterLevelSensor(self.reservoir)
        self.weight = random.randint(100, 999)

    def test_check_the_water_level(self):
        self.reservoir.increase_weight(self.weight)
        assert self.water_level_sensor.check_the_water_level()


class TestWaterHeater(unittest.TestCase):
    def setUp(self):
        self.waterheater = main.WaterHeater()
        self.room_temperature = 20
        self.water_temperature = self.room_temperature

    def test_get_current_water_heating(self):
        self.waterheater.water_heating()
        self.waterheater.get_current_water_heating()
        assert self.waterheater.water_temperature == 100


class TestWaterHeatingSensor(unittest.TestCase):
    def setUp(self):
        self.waterheater = main.WaterHeater()
        self.waterheatingsensor = main.WaterHeatingSensor()

    def check_temperature_water(self):
        self.waterheater.water_heating()
        assert self.waterheatingsensor.check_temperature_water()


class TestAmountCoffee(unittest.TestCase):
    def setUp(self):
        self.amountcoffee = main.AmountCoffee()
        self.amount = random.randint(100, 999)

    def test_get_current_amount_coffee(self):
        self.amountcoffee.change_amount(self.amount)
        assert self.amountcoffee.get_current_amount_coffee() == self.amount


class TestCoffeeLevelSensor(unittest.TestCase):
    def setUp(self):
        self.amount = random.randint(100, 999)
        self.amountcoffee = main.AmountCoffee()
        self.coffeelevelsensor = main.CoffeeLevelSensor(self.amountcoffee)

    def test_check_the_coffee_level(self):
        self.amountcoffee.change_amount(self.amount)
        assert self.coffeelevelsensor.check_the_coffee_level()


class TestPot(unittest.TestCase):
    def setUp(self):
        self.pot = main.Pot()
        self.weight = random.randint(100, 999)

    def test_reduce_weight(self):
        self.pot.increase_weight(self.weight)
        self.pot.reduce_weight(self.weight)
        assert self.pot.current_weight == 0

    def test_get_current_weight(self):
        self.pot.increase_weight(self.weight)
        assert self.pot.get_current_weight() == self.weight

        self.pot.reduce_weight(self.weight)
        assert self.pot.get_current_weight() == 0


class TestPump(unittest.TestCase):
    def setUp(self):
        self.pot = main.Pot()
        self.coffeemaker = main.CoffeeMaker()
        self.coffeemaker.put_pot(self.pot)
        self.step = 10
        self.weight = random.randint(100, 999)

    def test_pour_water(self):
        self.coffeemaker.reservoir.increase_weight(self.weight)
        self.coffeemaker.pump.pour_water(self.step, self.pot)
        assert self.coffeemaker.reservoir.current_weight == self.weight - self.step
        assert self.coffeemaker.pot.current_weight == self.step

    def test_push_water(self):
        self.coffeemaker.reservoir.increase_weight(self.weight)
        self.coffeemaker.pump.push_water(self.pot)
        assert self.coffeemaker.reservoir.current_weight == 0
        assert self.coffeemaker.pot.current_weight == self.weight


class TestDrinkLevelSensor(unittest.TestCase):
    def setUp(self):
        self.reservoir = main.Reservoir()
        self.drinklevelsensor = main.DrinkLevelSensor(self.reservoir)
        self.weight = random.randint(100, 999)
        self.pot = main.Pot()
        self.pump = main.Pump(self.reservoir)

    def test_check_the_drink_level(self):
        self.reservoir.increase_weight(self.weight)
        self.pump.push_water(self.pot)
        assert self.drinklevelsensor.check_the_drink_level()


class TestPlate(unittest.TestCase):
    def setUp(self):
        self.pot = main.Pot()
        self.weight = random.randint(100, 999)
        self.coffeemaker = main.CoffeeMaker()

    def test_start_warming(self):
        self.pot.increase_weight(self.weight)
        self.coffeemaker.plate.plate_level_sensor.check_the_plate_empty(self.pot)
        self.coffeemaker.plate.plate_level_sensor.check_the_plate_empty_pot_level(self.pot)
        self.coffeemaker.plate.start_warming(self.pot)
        assert self.coffeemaker.plate.warming_state

    def test_stop_warming(self):
        self.coffeemaker.put_pot(self.pot)
        self.pot.increase_weight(self.weight)
        self.pot.reduce_weight(self.weight)
        self.coffeemaker.take_pot(self.pot)
        self.coffeemaker.plate.plate_level_sensor.check_the_plate_empty(self.pot)
        self.coffeemaker.plate.plate_level_sensor.check_the_plate_empty_pot_level(self.pot)
        self.coffeemaker.plate.stop_warming(self.pot)
        assert self.coffeemaker.plate.warming_state is False

    def test_is_warming(self):
        self.pot.increase_weight(self.weight)
        self.coffeemaker.plate.plate_level_sensor.check_the_plate_empty(self.pot)
        self.coffeemaker.plate.plate_level_sensor.check_the_plate_empty_pot_level(self.pot)
        self.coffeemaker.plate.stop_warming(self.pot)
        assert not self.coffeemaker.plate.is_warming()


class TestPlateLevelSensor(unittest.TestCase):
    def setUp(self):
        self.platelvelsensor = main.PlateLevelSensor()
        self.pot = main.Pot()
        self.weight = random.randint(100, 999)

    def test_check_the_plate_empty(self):
        self.pot.increase_weight(self.weight)
        assert not self.platelvelsensor.check_the_plate_empty(self.pot)

    def test_check_the_plate_empty_pot_level(self):
        self.pot.increase_weight(self.weight)
        assert not self.platelvelsensor.check_the_plate_empty_pot_level(self.pot)


class TestCoffeeMaker(unittest.TestCase):
    def setUp(self):
        self.coffeemaker = main.CoffeeMaker()
        self.pot = main.Pot()
        self.weight = random.randint(100, 999)
        self.amount = random.randint(100, 999)
        self.pot = main.Pot()

    def test_state_coffee_brew_stop(self):
        self.coffeemaker.state_coffee_brew_stop()
        assert not self.coffeemaker.state_coffee_brew_in_progress

    def test_check_state_heating_water(self):
        self.coffeemaker.waterheater.water_heating()
        self.coffeemaker.water_heating_sensor.check_temperature_water()
        self.coffeemaker.check_state_heating_water()
        assert self.coffeemaker.state_heating_water

    def test_check_state_drink_is_ready(self):
        self.coffeemaker.reservoir.increase_weight(self.weight)
        self.coffeemaker.reservoir.reduce_weight(self.weight)
        assert self.coffeemaker.drink_level_sensor.check_the_drink_level()

    def test_coffee_making_is_started(self):
        self.coffeemaker.reservoir.increase_weight(self.weight)
        self.coffeemaker.put_pot(self.pot)
        self.coffeemaker.amount_coffee.change_amount(self.amount)
        assert self.coffeemaker.state_coffee_brew_in_progress is False
        with patch('app.main.CoffeeMaker.check_state_drink_is_ready') as mocked_method:
            mocked_method.return_value = False
            self.coffeemaker.brew_coffee()
            with self.assertRaises(exceptions.CoffeeBrewInProgressException):
                self.coffeemaker.reservoir.increase_weight(self.weight)
                self.coffeemaker.brew_coffee()

    def test_water_level_check(self):
        self.coffeemaker.put_pot(self.pot)
        self.coffeemaker.amount_coffee.change_amount(self.amount)
        with self.assertRaises(exceptions.CheckTheWaterException):
            self.coffeemaker.brew_coffee()

    def test_check_the_plate_empty(self):
        self.coffeemaker.reservoir.increase_weight(self.weight)
        self.coffeemaker.amount_coffee.change_amount(self.amount)
        with self.assertRaises(exceptions.CheckThePlateEmptyException):
            self.coffeemaker.brew_coffee()

    def test_check_the_coffee(self):
        self.coffeemaker.reservoir.increase_weight(self.weight)
        self.coffeemaker.put_pot(self.pot)
        with self.assertRaises(exceptions.CheckTheCoffeeException):
            self.coffeemaker.brew_coffee()
            with patch('app.main.CoffeeMaker.check_state_drink_is_ready') as mocked_method:
                mocked_method.return_value = False
                assert not self.coffeemaker.state_pressure_valve

    def test_drink_is_ready(self):
        self.coffeemaker.reservoir.increase_weight(self.weight)
        self.coffeemaker.put_pot(self.pot)
        self.coffeemaker.amount_coffee.change_amount(self.amount)
        self.coffeemaker.brew_coffee()
        assert self.coffeemaker.indicator_ready_is_drink
        assert not self.coffeemaker.state_coffee_brew_in_progress
        assert self.coffeemaker.state_pressure_valve

    def test_pour_water_into_the_boiler(self):
        self.coffeemaker.pour_water_into_the_boiler(self.weight)
        assert self.coffeemaker.reservoir.get_current_weight() == self.weight

    def test_drop_coffee(self):
        self.coffeemaker.drop_coffee(self.amount)
        assert self.coffeemaker.amount_coffee.get_current_amount_coffee() == self.amount

    def test_take_pot(self):
        with self.assertRaises(exceptions.TakePotException):
            self.coffeemaker.take_pot(self.pot)

        self.coffeemaker.put_pot(self.pot)
        self.pot.increase_weight(self.weight)
        self.coffeemaker.plate.start_warming(self.pot)
        self.coffeemaker.take_pot(self.pot)
        assert self.coffeemaker.plate.warming_state

    def test_put_pot(self):
        self.coffeemaker.put_pot(self.pot)
        with self.assertRaises(exceptions.PutPotException):
            self.coffeemaker.put_pot(self.pot)

        self.coffeemaker.take_pot(self.pot)
        self.pot.increase_weight(self.weight)
        self.coffeemaker.put_pot(self.pot)
        assert self.coffeemaker.plate.warming_state


if __name__ == '__main__':
    unittest.main()
