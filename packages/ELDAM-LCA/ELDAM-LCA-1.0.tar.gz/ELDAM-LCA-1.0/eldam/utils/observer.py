""" For more information on the observer design pattern: https://refactoring.guru/design-patterns/observer"""

from abc import ABC


class Suscriber(ABC):
    """ Abstract class for suscriber """

    def update(self, *args, **kwargs):
        pass


class Notifier(ABC):
    """ Abstract class for notifier """

    def __init__(self):
        self._suscribers = list()

    def add_suscriber(self, suscriber: Suscriber):
        self._suscribers.append(suscriber)

    def remove_suscriber(self, suscriber: Suscriber):
        if suscriber in self._suscribers:
            self._suscribers.remove(suscriber)

    def notify(self, *args, **kwargs):
        for suscriber in self._suscribers:
            suscriber.update(*args, **kwargs)
