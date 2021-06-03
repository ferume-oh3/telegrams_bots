from DriverPassengerClass import Driver

class QueueOfDriver():
    def __init__(self, DriverById, DriversByRoute):
        self.__DriverById = DriverById
        self.__DriversByRoute = DriversByRoute

    def AddDriver(self, NewDriver):
        self.__DriverById[NewDriver.GetId()] = NewDriver

        if NewDriver.GetRoute() in self.__DriversByRoute:
            self.__DriversByRoute[NewDriver.GetRoute()].append(NewDriver)
        else:
            self.__DriversByRoute[NewDriver.GetRoute()] = [NewDriver]

    def IsOrder(self, Id):
        return Id in self.__DriverById

    def GetDriverById(self, Id):
        return self.__DriverById[Id]

    def IsAlredyMatched(self, Id):
        return self.IsOrder(Id) and self.__DriversByRoute[self.__DriverById[Id].GetRoute()].count(Id) == 0

    def DeleteOrder(self, Id):
        Route = self.__DriverById[Id].GetRoute()
        self.PopDriverByRoute(Route, self.__DriverById[Id])

    def GetDriverByRoute(self, Route):
        return self.__DriversByRoute[Route][0]

    def PopDriverByRoute(self, Route, Driver):
        if Route in self.__DriversByRoute and Driver in self.__DriversByRoute[Route]:
            self.__DriversByRoute[Route].pop(self.__DriversByRoute[Route].index(Driver))

        self.__DriverById.pop(Driver.GetId(), None)


    def CountDriverByRoute(self, Route):
        if Route not in self.__DriversByRoute:
            return 0
        else:
            return len(self.__DriversByRoute[Route])