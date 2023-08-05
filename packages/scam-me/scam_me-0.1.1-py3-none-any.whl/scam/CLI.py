import datetime as dt
from scam.CommManager import CommManager


class CLI:
    def __init__(self):
        try:
            self.cm = CommManager()
        except Exception as e:
            print('Error: {0}'.format(str(e)))

    def run(self):
        try:
            cmd = str(input('Commands: type 1 to look up, 2 to book, 3 to delete,'
                            '4 to update a reservation, 5 to exit'))
            while cmd != '5':
                if cmd == '1':
                    print('Commands: type 1 to get a reservation from a name, 2 to get a reservation from an ID')
                    command = str(input())
                    if command == '1':
                        print('Insert input:')
                        name = str(input())
                        result = self.cm.get_reservations(-1, name)
                        print()
                        for res in result:
                            print_result(res)
                            print()
                    elif command == '2':
                        print('Insert input:')
                        res_id = int(input())
                        result = self.cm.get_reservations(res_id)
                        print(result)
                        print_result(result)
                    else:
                        print('Invalid command')
                elif cmd == '2':
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

                    check = self.cm.make_reservation(location=destination, persons=n_people, name=res_name,
                                                     phone_number=phone, reservation=timestamp)

                    if check:
                        print('Success')
                    else:
                        raise Exception('Failed')
                elif cmd == '3':
                    print('3')
                elif cmd == '4':
                    print('4')
                else:
                    print('Invalid command')
                cmd = str(input('Commands: type 1 to look up, 2 to book, 3 to delete,'
                                '4 to update a reservation, 5 to exit'))
            print('Exit')
        except Exception as e:
            print("Error: {0}".format(str(e)))


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
            print("{0}: {1}".format(str(key), str(dt.datetime.fromtimestamp(res[key]))))
