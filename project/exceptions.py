class CoffeeBrewInProgressException(Exception):
    def __init__(self,*args, **kwargs):
        super().__init__('Процесс уже запущен', *args, **kwargs)


class CheckTheWaterException(Exception):
    def __init__(self,*args, **kwargs):
        super().__init__('Налейте воду', *args, **kwargs)


class CheckThePlateEmptyException(Exception):
     def __init__(self,*args, **kwargs):
         super().__init__('Поставьте кофейник', *args, **kwargs)


class CheckTheCoffeeException(Exception):
    def __init__(self,*args, **kwargs):
        super().__init__('Добавьте кофе', *args, **kwargs)


class TakePotException(Exception):
    def __init__(self,*args, **kwargs):
        super().__init__('Вы уже взяли кофейник', *args, **kwargs)


class PutPotException(Exception):
    def __init__(self,*args, **kwargs):
        super().__init__('Кофейник уже поставлен', *args, **kwargs)

