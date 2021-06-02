class User():
    def __init__(self, role, id, route):
        self.__id = id
        self.__role = role
        self.__route = route

    def get_id(self):
        return self.__id

    def get_route(self):
        return self.__route

    def get_role(self):
        return self.__role



class Queue_of_orders():
    def __init__(self, used, orders_passengers, orders_drivers, already_find, stack_of_messages):
        self.__used = used
        self.__orders_passengers = orders_passengers
        self.__orders_drivers = orders_drivers
        self.__already_find = already_find
        self.__stack_of_messages = stack_of_messages
        self.__CONST_NUMBER_PLACES = 4


    def add_driver(self, us):
        self.__used[us.get_id()] = us

        if us.get_route() in self.__orders_drivers:
            self.__orders_drivers[us.get_route()].append(us)
        else:
            self.__orders_drivers[us.get_route()] = [us]

        while self.may_build_trip(us.get_route()):
            self.build_trip(us.get_route())


    def add_passenger(self, us):
        self.__used[us.get_id()] = us

        if us.get_route() in self.__orders_passengers:
            self.__orders_passengers[us.get_route()].append(us)
        else:
            self.__orders_passengers[us.get_route()] = [us]

        while self.may_build_trip(us.get_route()):
            self.build_trip(us.get_route())


    def get_inform(self, id):
        if self.__used[id].get_role() == 0:
            self.__stack_of_messages.append((1, id, "Все пассажиры нашлись, ниже приложены их номера\n" + '\n'.join(list(map(str, already_find[id])))))
        else:
            self.__stack_of_messages.append((1, id, "Водитель нашелся, ниже приложен его номер\n" + '\n'.join(list(map(str, already_find[id])))))


    def is_order(self, id):
        if id not in self.__used:
            return 0
        else:
            return 1


    def is_there(self, id):
        if not self.is_order(id):
            self.__stack_of_messages.append((0, id, "Насколько нам известно у вас отсутсвуют активные заказы!"))
            return

        if id in self.__already_find:
            self.get_inform(id);
            return

        route = self.__used[id].get_route()
        if route not in self.__orders_drivers or len(self.__orders_drivers[route]) == 0:
            self.__stack_of_messages.append((0, id, "К сожалению водитель пока не нашелся : ("))
        elif route not in self.__orders_passengers:
            self.__stack_of_messages.append((0, id, "Недостаточно пассажиров, осталось найти " + str(self.__CONST_NUMBER_PLACES)))
        elif len(self.__orders_passengers[route]) != self.__CONST_NUMBER_PLACES:
            self.__stack_of_messages.append((0, id, "Недостаточно пассажиров, осталось найти " + str(self.__CONST_NUMBER_PLACES - len(self.__orders_passengers[route]))))


    def inform_about_delete_of_driver(self, whom):
        for v in whom:
            self.__stack_of_messages.append((0, v, "Водитель отказался от поездки, ищем нового"))


    def inform_about_delete_of_passenger(self, whom):
        for v in whom:
            self.__stack_of_messages.append((0, v, "Один из пассажиров отказался от поездки, ищем нового"))


    def delete_order(self, id):
        route = self.__used[id].get_route()

        if self.__used[id].get_role() == 0:
            if id in self.__already_find:
                self.inform_about_delete_of_driver(self.__already_find[id])

                for id_pas in self.__already_find[id]:
                    self.__orders_passengers[route].append(self.__used[id_pas])
                    self.__already_find.pop(id_pas, None)

                self.__already_find.pop(id, None)
                self.__used.pop(id, None)
            else:
                self.__orders_drivers[route].pop(self.__orders_drivers[route].index(self.__used[id]))
                self.__used.pop(id, None)
        else:
            if id in self.__already_find:
                fl = self.__already_find[self.__already_find[id][0]][::]
                fl.pop(fl.index(id))
                fl.append(self.__already_find[id][0])
                self.inform_about_delete_of_passenger(fl)

                id_dr = self.__already_find[id][0]
                for id_pas in self.__already_find[id_dr]:
                    if id_pas != id:
                        self.__orders_passengers[route].append(self.__used[id_pas])

                    self.__already_find.pop(id_pas, None)

                self.__already_find.pop(id_dr, None)
                self.__orders_drivers[route].append(self.__used[id_dr])
                self.__used.pop(id, None)
            else:
                self.__orders_passengers[route].pop(self.__orders_passengers[route].index(self.__used[id]))
                self.__used.pop(id, None)

        while self.may_build_trip(route):
            self.build_trip(route)


    def may_build_trip(self, route):
        if route not in self.__orders_drivers or route not in self.__orders_passengers:
            return 0

        return len(self.__orders_drivers[route]) and len(self.__orders_passengers[route]) >= self.__CONST_NUMBER_PLACES


    def build_trip(self, route):
        driver = self.__orders_drivers[route][0].id
        self.__orders_drivers[route].pop(0)

        list_of_pasengers = []
        for i in range(self.__CONST_NUMBER_PLACES):
            list_of_pasengers.append(self.__orders_passengers[route][0].id)
            self.__orders_passengers[route].pop(0)

        self.__already_find[driver] = list_of_pasengers
        for v in list_of_pasengers:
            self.__already_find[v] = [driver]


        self.__stack_of_messages.append((1, driver, "Все пассажиры нашлись, ниже приложены их номера\n" + '\n'.join(
            list(map(str, list_of_pasengers)))))

        for v in list_of_pasengers:
            self.__stack_of_messages.append((1, v, "Водитель нашелся, ниже приложен его номер\n" + str(driver)))


    def is_there_message(self):
        return len(self.__stack_of_messages) >= 1


    def get_first_message(self):
        return self.__stack_of_messages[0]


    def pop_first_message(self):
        self.__stack_of_messages.pop(0)


def convert_to_route(text):
    # add exception about len(text) != 2
    text = text.lower().split()
    route = (text[0], text[1])
    return route