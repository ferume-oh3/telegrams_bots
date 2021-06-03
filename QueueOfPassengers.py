from DriverPassengerClass import Passenger

class QueueOfPassenger():
    def __init__(self, PassengerById, PassengersByRoute):
        self.__PassengerById = PassengerById
        self.__PassengersByRoute = PassengersByRoute

    def AddPassenger(self, NewPassenger):
        self.__PassengerById[NewPassenger.GetId()] = NewPassenger

        if NewPassenger.GetRoute() in self.__PassengersByRoute:
            self.__PassengersByRoute[NewPassenger.GetRoute()].append(NewPassenger)
        else:
            self.__PassengersByRoute[NewPassenger.GetRoute()] = [NewPassenger]

    def IsOrder(self, Id):
        return Id in self.__PassengerById

    def GetPassengerById(self, Id):
        return self.__PassengerById[Id]

    def IsAlredyMatched(self, Id):
        return self.IsOrder(Id) and self.__PassengersByRoute[self.__PassengerById[Id].GetRoute()].count(Id) == 0

    def DeleteOrder(self, Id):
        Route = self.__PassengerById[Id].GetRoute()
        self.PopPassengerByRoute(Route, self.__PassengerById[Id])

    def GetPassengerByRoute(self, Route):
        return self.__PassengersByRoute[Route][0]

    def PopPassengerByRoute(self, Route, Passenger):
        if Route in self.__PassengersByRoute and Passenger in self.__PassengersByRoute[Route]:
            self.__PassengersByRoute[Route].pop(self.__PassengersByRoute[Route].index(Passenger))

        self.__PassengerById.pop(Passenger.GetId(), None)

    def CountPassengerByRoute(self, Route):
        if Route not in self.__PassengersByRoute:
            return 0
        else:
            return len(self.__PassengersByRoute[Route])