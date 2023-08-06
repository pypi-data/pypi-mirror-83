import datetime as dt
from scam.CommManager import CommManager


class CLI:
    def __init__(self):
        try:
            self.cm = CommManager()
        except BaseException as e:
            print('Error: {0}'.format(str(e)))

    def command_1(self):
        try:
            print('Commands: type 1 to get a reservation from a name, 2 to get a reservation from an ID')
            command = str(input())
            if command == '1':
                name = str(input('Insert name:'))
                result = self.cm.get_reservations(name=name)
                for res in result:
                    print_result(res)
            elif command == '2':
                res_id = int(input('Insert ID:'))
                result = self.cm.get_reservations(reservation_id=res_id)
                print_result(result)
            else:
                print('Invalid command')
        except BaseException as e:
            print('Error: {0}'.format(str(e)))

    def command_2(self):
        try:
            res = self.input_reservation()

            check = self.cm.make_reservation(location=res['destination'],
                                             persons=res['n_people'],
                                             name=res['res_name'],
                                             phone_number=res['phone'],
                                             reservation=res['timestamp'])

            if check:
                print('Success')
            else:
                raise BaseException('Failed')
        except BaseException as e:
            print('Error: {0}'.format(str(e)))

    def command_3(self):
        try:
            res_id = int(input('Type the ID of the reservation you want to delete'))
            res = self.cm.delete_reservation(reservation_id=res_id)
            if res:
                print('Reservation {} canceled'.format(res_id))
            else:
                print('Reservation {} not found'.format(res_id))
        except BaseException as e:
            print('Error: {0}'.format(str(e)))

    def command_4(self):
        try:
            res_id = int(input('Type the ID of the reservation you want to modify:'))
            reservation = self.cm.get_reservations(reservation_id=res_id)
            print_result(reservation)
            print("Modified reservation:")
            new_reservation = self.input_reservation()
            check = self.cm.modify_reservation(
                reservation_id=res_id,
                location=new_reservation['destination'],
                name=new_reservation['res_name'],
                phone_number=new_reservation['phone'],
                persons=new_reservation['n_people'],
                reservation=new_reservation['timestamp']
            )
            if check:
                print('Success')
            else:
                raise BaseException('Failed')
        except BaseException as e:
            print('Error: {0}'.format(str(e)))

    def run(self):
        try:
            cmd = str(input('Commands: type 1 to look up, 2 to book, 3 to cancel, '
                            '4 to modify a reservation, 5 to exit'))
            while cmd != '5':
                if cmd == '1':
                    self.command_1()
                elif cmd == '2':
                    self.command_2()
                elif cmd == '3':
                    self.command_3()
                elif cmd == '4':
                    self.command_4()
                else:
                    print('Invalid command')
                cmd = str(input('Commands: type 1 to look up, 2 to book, 3 to delete, '
                                '4 to modify a reservation, 5 to exit'))
            print('Exit')
        except BaseException as e:
            print('Error: {0}'.format(str(e)))

    def input_reservation(self):
        destinations = self.cm.get_destinations()
        print('Type a destination number:')
        print_destinations(destinations)
        destination = int(input())

        if not check_destination(destination, destinations):
            raise ValueError('Invalid destination. Type a valid destination number')

        date_str = input('Type datetime as d-m-Y H:M \n')
        date_dt = dt.datetime.strptime(date_str, '%d-%m-%Y %H:%M')
        timestamp = int(dt.datetime.timestamp(date_dt))

        if not check_date(date_dt):
            raise ValueError('Datetime must come after current datetime')

        n_people = int(input('Number of people \n'))
        res_name = input('Under the name of \n')
        phone = input('Phone number \n')
        return {
            'destination': destination,
            'timestamp': timestamp,
            'n_people': n_people,
            'res_name': res_name,
            'phone': phone
        }


def check_date(date):
    return isinstance(date, dt.datetime) and date > dt.datetime.now()


def check_destination(destination, destinations):
    keys = [d['id'] for d in destinations]
    return destination in keys


def print_destinations(destinations):
    for d in destinations:
        print(str(d['id']) + '. ' + d['name'])


def print_result(res):
    for key in res:
        if key != 'reservation':
            print("{0}: {1}".format(str(key), str(res[key])))
        else:
            print("{0}: {1}".format(str(key), str(dt.datetime.fromtimestamp(int(res[key])))))
