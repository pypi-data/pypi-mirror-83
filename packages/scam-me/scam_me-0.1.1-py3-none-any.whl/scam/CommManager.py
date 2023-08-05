import requests
import json


class CommManager:

    def __init__(self):
        self.url = 'http://40.66.46.195:8000/'

    def get_destinations(self):
        res = requests.get(url=self.url + 'destinations')
        if res.status_code != 200:
            raise BaseException('An error occurred')
        return res.json()

    def make_reservation(self, location: int, name: str, phone_number: str, persons: int, reservation: int):
        data = {'location': location,
                'name': name,
                'phone_number': phone_number,
                'persons': persons,
                'reservation': reservation}

        res = requests.post(url=self.url + 'reservation', data=json.dumps(data))

        if res.status_code != 200:
            raise BaseException('An error occurred')
        return True

    def get_reservations(self, reservation_id=-1, name=''):
        if reservation_id == -1:
            res = requests.get(url=self.url + 'reservations/{}'.format(name))
        else:
            res = requests.get(url=self.url + 'reservation/{}'.format(reservation_id))

        if res.status_code == 400:
            raise BaseException('Reservation not found')

        if res.status_code != 200:
            raise BaseException('An error occurred')

        return res.json()

    def delete_reservation(self, reservation_id: int):
        try:
            self.get_reservations(self, reservation_id)
        except BaseException:
            raise BaseException('Reservation not found')

        res = requests.delete(url=self.url + 'reservation/{}'.format(reservation_id))

        if res.status_code != 200:
            raise BaseException('An error occurred')

        return True

    def modify_reservation(self,
                           reservation_id: int,
                           location: int,
                           name: str,
                           phone_number: str,
                           persons: int,
                           reservation: int):

        data = {'location': location,
                'name': name,
                'phone_number': phone_number,
                'persons': persons,
                'reservation': reservation}

        res = requests.put(url=self.url + 'reservation/{}'.format(reservation_id), data=json.dumps(data))

        if res.status_code != 200:
            raise BaseException('An error occurred')

        return True
