class User():
    def __init__(self, Id, Route):
        self.__Id = Id
        self.__Route = Route

    def GetId(self):
        return self.__Id

    def GetRoute(self):
        return self.__Route


class Driver(User):
    def __init__(self, Id, Route):
        User.__init__(self, Id, Route)

    def IsDriver(self):
        return 1

    def IsPassenger(self):
        return 0


class Passenger(User):
    def __init__(self, Id, Route):
        User.__init__(self, Id, Route)

    def IsDriver(self):
        return 0

    def IsPassenger(self):
        return 1