class User():
    def __init__(self, role, id, route):
        self.id = id
        self.role = role
        self.route = route


class Queue():
    def __init__(self, used, orders_passengers, orders_drivers, already_find, stack_of_messages):
        self.used = used
        self.orders_passengers = orders_passengers
        self.orders_drivers = orders_drivers
        self.already_find = already_find
        self.stack_of_messages = stack_of_messages


    def add_driver(self, us):
        self.used[us.id] = us

        if us.route in self.orders_drivers:
            self.orders_drivers[us.route].append(us)
        else:
            self.orders_drivers[us.route] = [us]

        while q.may_build_trip(us.id):
            q.build_trip(us.id)


    def add_passenger(self, us):
        self.used[us.id] = us

        if us.route in self.orders_passengers:
            self.orders_passengers[us.route].append(us)
        else:
            self.orders_passengers[us.route] = [us]

        while q.may_build_trip(us.id):
            q.build_trip(us.id)


    def get_inform(self, id):
        if self.used[id].role == 0:
            self.stack_of_messages.append((1, id, "Все пассажиры нашлись, ниже приложены их номера\n" + '\n'.join(list(map(str, already_find[id])))))
        else:
            self.stack_of_messages.append((1, id, "Водитель нашелся, ниже приложен его номер\n" + '\n'.join(list(map(str, already_find[id])))))


    def is_order(self, id):
        if id not in self.used:
            return 0
        else:
            return 1


    def is_there(self, id):
        if not self.is_order(id):
            self.stack_of_messages.append((0, id, "Насколько нам известно у вас отсутсвуют активные заказы!"))
            return

        if id in self.already_find:
            self.get_inform(id);
            return

        route = self.used[id].route
        if route not in self.orders_drivers or len(self.orders_drivers[route]) == 0:
            self.stack_of_messages.append((0, id, "К сожалению водитель пока не нашелся : ("))
        elif route not in self.orders_passengers:
            self.stack_of_messages.append((0, id, "Недостаточно пассажиров, осталось найти 4"))
        elif len(self.orders_passengers[route]) != 4:
            self.stack_of_messages.append((0, id, "Недостаточно пассажиров, осталось найти " + str(4 - len(self.orders_passengers[route]))))


    def inform_about_delete_of_driver(self, whom):
        for v in whom:
            self.stack_of_messages.append((0, v, "Водитель отказался от поездки, ищем нового"))


    def inform_about_delete_of_passenger(self, whom):
        for v in whom:
            self.stack_of_messages.append((0, v, "Один из пассажиров отказался от поездки, ищем нового"))


    def delete_order(self, id):
        route = self.used[id].route

        if self.used[id].role == 0:
            if id in self.already_find:
                self.inform_about_delete_of_driver(self.already_find[id])

                for id_pas in self.already_find[id]:
                    self.orders_passengers[route].append(self.used[id_pas])
                    self.already_find.pop(id_pas, None)

                self.already_find.pop(id, None)
                self.used.pop(id, None)
            else:
                self.orders_drivers[route].pop(self.orders_drivers[route].index(self.used[id]))
                self.used.pop(id, None)
        else:
            if id in self.already_find:
                fl = self.already_find[self.already_find[id][0]][::]
                fl.pop(fl.index(id))
                fl.append(self.already_find[id][0])
                self.inform_about_delete_of_passenger(fl)

                id_dr = self.already_find[id][0]
                for id_pas in self.already_find[id_dr]:
                    if id_pas != id:
                        self.orders_passengers[route].append(self.used[id_pas])

                    self.already_find.pop(id_pas, None)

                self.already_find.pop(id_dr, None)
                self.orders_drivers[route].append(self.used[id_dr])
                self.used.pop(id, None)
            else:
                self.orders_passengers[route].pop(self.orders_passengers[route].index(self.used[id]))
                self.used.pop(id, None)

        while q.may_build_trip(id):
            q.build_trip(id)


    def may_build_trip(self, id):
        if not self.is_order(id):
            return 0

        route = self.used[id].route
        if route not in self.orders_drivers or route not in self.orders_passengers:
            return 0

        return len(self.orders_drivers[route]) >= 1 and len(self.orders_passengers[route]) >= 4


    def build_trip(self, id):
        route = self.used[id].route
        dr = self.orders_drivers[route][0].id
        self.orders_drivers[route].pop(0)
        ps1 = self.orders_passengers[route][0].id
        self.orders_passengers[route].pop(0)
        ps2 = self.orders_passengers[route][0].id
        self.orders_passengers[route].pop(0)
        ps3 = self.orders_passengers[route][0].id
        self.orders_passengers[route].pop(0)
        ps4 = self.orders_passengers[route][0].id
        self.orders_passengers[route].pop(0)

        self.already_find[dr] = [ps1, ps2, ps3, ps4]
        self.already_find[ps1] = self.already_find[ps2] = self.already_find[ps3] = self.already_find[ps4] = [dr]

        if not self.used[dr].label_test:
            self.stack_of_messages.append((1, dr, "Все пассажиры нашлись, ниже приложены их номера\n" + '\n'.join(
                list(map(str, self.already_find[dr])))))

        for v in self.already_find[dr]:
            if not self.used[v].label_test:
                self.stack_of_messages.append((1, v, "Водитель нашелся, ниже приложен его номер\n" + '\n'.join(
                                     list(map(str, self.already_find[v])))))


    def is_there_message(self):
        return len(self.stack_of_messages) >= 1


    def get_first_message(self):
        return self.stack_of_messages[0]


    def pop_first_message(self):
        self.stack_of_messages.pop(0)


q = Queue({}, {}, {}, {}, [])


def convert_to_route(text):
    # add exception about len(text) != 2
    text = text.lower().split()
    route = (text[0], text[1])
    return route