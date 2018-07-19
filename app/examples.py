from .main import CoffeeMaker, Pot


if __name__ == '__main__':
    pot = Pot()
    coffeemaker = CoffeeMaker()
    coffeemaker.put_pot(pot)
    coffeemaker.pour_water_into_the_boiler(400)
    # coffeemaker.drop_coffee(400)
    coffeemaker.brew_coffee()
    pot = coffeemaker.take_pot(pot)
    print("Приготовлиось кофе:", pot.get_current_weight() - pot.initial_weight)