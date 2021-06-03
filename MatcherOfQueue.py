from QueueOfDrivers import QueueOfDriver
from QueueOfPassengers import QueueOfPassenger
from MessageClass import BotMessage

class MatcherOfQueue():
    def __init__(self, QueDriver, QuePassenger, FindedOrdersForUsers, StackOfMessages):
        self.__QueDriver = QueDriver
        self.__QuePassenger = QuePassenger
        self.__FindedOrdersForUsers = FindedOrdersForUsers
        self.__StackOfMessages = StackOfMessages
        self.__ConstNumberPlaces = 4

    def GetInformationAboutOrder(self, Id):
        if not self.IsDriver(Id) and not self.IsPassenger(Id):
            self.__StackOfMessages.append(BotMessage(Id, "Насколько нам известно у вас отсутсвуют активные заказы!"))
            return

        if self.IsDriver(Id):
            Route = self.__QueDriver.GetDriverById(Id).GetRoute()
        else:
            Route = self.__QuePassenger.GetPassengerById(Id).GetRoute()

        while self.MayBuildTrip(Route):
            self.BuildTrip(Route)

        if self.AlredyFinded(Id):
            if self.IsDriver(Id):
                Driver = self.__QueDriver.GetDriverById(Id)
                self.__StackOfMessages.append(BotMessage(Id, "Все пассажиры нашлись, ниже приложена их информация\n" + '\n'.join(TransPassengerToInformation(self.__FindedOrdersForUsers[Driver]))))
            else:
                Passenger = self.__QuePassenger.GetPassengerById(Id)
                self.__StackOfMessages.append(BotMessage(Id, "Водитель нашелся, ниже приложена его информация\n" + '\n'.join(TransDriverToInformation(self.__FindedOrdersForUsers[Passenger]))))
        else:
            if self.__QueDriver.CountDriverByRoute(Route) == 0:
                self.__StackOfMessages.append(BotMessage(Id, "К сожалению водитель не нашелся :("))
            else:
                self.__StackOfMessages.append(BotMessage(Id, "Осталось найти " + str(self.__ConstNumberPlaces - self.__QuePassenger.CountPassengerByRoute(Route)) + " пассажиров"))

    def IsThereOrder(self, Id):
        return self.IsDriver(Id) or self.IsPassenger(Id)

    def IsDriver(self, Id):
        return self.__QueDriver.IsOrder(Id)

    def IsPassenger(self, Id):
        return self.__QuePassenger.IsOrder(Id)

    def AlredyFinded(self, Id):
        return Id in self.__FindedOrdersForUsers

    def AddPassenger(self, NewPassenger):
        self.__QuePassenger.AddPassenger(NewPassenger)
        Route = NewPassenger.GetRoute()

        while self.MayBuildTrip(Route):
            self.BuildTrip(Route)

    def AddDriver(self, NewDriver):
        self.__QueDriver.AddDriver(NewDriver)
        Route = NewDriver.GetRoute()

        while self.MayBuildTrip(Route):
            self.BuildTrip(Route)

    def InformAboutDeleteOfDriver(self, Users):
        for User in Users:
            self.__StackOfMessages.append(BotMessage(User.GetId(), "Водитель отказался от поездки, ищем нового"))

    def InformAboutDeleteOfPassenger(self, Users):
        for User in Users:
            self.__stack_of_messages.append(BotMessage(User.GetId(), "Один из пассажиров отказался от поездки, ищем нового"))

    def DeleteOrder(self, Id):
        if self.IsDriver(Id):
            Driver = self.__QueDriver.GetDriverById(Id)
            Route = Driver.GetRoute()

            if self.AlredyFinded(Id):
                self.InformAboutDeleteOfPassenger(self.__FindedOrdersForUsers[Driver])

                for IdPas in self.__FindedOrdersForUsers[Driver]:
                    Passenger = self.__QuePassenger.GetPassengerById(IdPas)
                    self.__FindedOrdersForUsers.pop(Passenger, None)
                    self.AddPassenger(Passenger)

                self.__FindedOrdersForUsers.pop(Driver, None)
                self.__QueDriver.PopDriverByRoute(Driver.GetRoute(), Driver)
            else:
                self.__QueDriver.PopDriverByRoute(Driver.GetRoute(), Driver)
        else:
            Passenger = self.__QuePassenger.GetPassengerById(Id)
            Route = Passenger.GetRoute()

            if self.AlredyFinded(Id):
                Driver = self.__FindedOrdersForUsers[Passenger][0]
                self.__FindedOrdersForUsers.pop(Passenger, None)
                self.__QuePassenger.PopPassengerByRoute(Driver.GetRoute(), Passenger)

                Passengers = self.__FindedOrdersForUsers[Driver]
                Passengers.pop(Passengers.index(Passenger))

                self.InformAboutDeleteOfPassenger(Passengers + [Driver])

                self.AddDriver(Driver)
                for Ps in Passengers:
                    self.AddPassenger(Ps)
            else:
                self.__QuePassenger.PopPassengerByRoute(Passenger.GetRoute(), Passenger)

        while self.MayBuildTrip(Route):
            self.BuildTrip(Route)

    def MayBuildTrip(self, Route):
        return self.__QuePassenger.CountPassengerByRoute(Route) >= self.__ConstNumberPlaces and self.__QueDriver.CountDriverByRoute(Route)

    def BuildTrip(self, Route):
        Driver = self.__QueDriver.GetDriverByRoute(Route)
        self.__QueDriver.PopDriverByRoute(Route, Driver)

        ListOfPassengers = []
        for i in range(self.__ConstNumberPlaces):
            ListOfPassengers.append(self.__QuePassenger.GetPassengerByRoute(Route))
            self.__QuePassenger.PopPassengerByRoute(ListOfPassengers[-1])

        self.__FindedOrdersForUsers[Driver] = ListOfPassengers
        for Ps in ListOfPassengers:
            self.__FindedOrdersForUsers[Ps] = [Driver]

        self.__StackOfMessages.append(BotMessage(Driver, "Все пассажиры нашлись, ниже приложена их информация\n" + '\n'.join(TransPassengerToInformation(ListOfPassengers))))
        for Ps in ListOfPassengers:
            self.__StackOfMessages.append(BotMessage(Id, "Водитель нашелся, ниже приложена его информация\n" + '\n'.join(TransDriverToInformation([Driver]))))

    def IsThereMessage(self):
        return len(self.__StackOfMessages) >= 1

    def GetFirstMessage(self):
        return self.__StackOfMessages[0]

    def PopFirstMessage(self):
        self.__StackOfMessages.pop(0)


def TransPassengerToInformation(Passengers):
    Information = []
    for User in Passengers:
        Information.append(User.GetId())

    return list(map(str, Information))


def TransDriverToInformation(Drivers):
    Information = []
    for User in Drivers:
        Information.append(User.GetId())

    return list(map(str, Information))