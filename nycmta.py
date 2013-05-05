import csv


class TransitSystem(object):
    def __init__(self):
        self.stations = []
        self.routes = {}

    def parse_stops(self, stops):
        """Parse data from stops.txt"""
        stop_defs = filter(lambda st: st['location_type'] == '1', stops)
        stop_defs = uniq(stop_defs, lambda sd: sd['stop_name'])
        stations = (self.build_station(sd) for sd in stop_defs)
        self.stations = list(stations)

    def parse_stop_times(self, stop_times):
        """Parse data from stop_times.txt"""
        for s in stop_times:
            #(h,m,sec) = map(int, s['departure_time'].split(":"))
            assert(len(s['departure_time']) == 8)
            assert(len(s['trip_id']) == 27)
            assert(len(s['stop_id']) == 4)
            print self.parse_trip_id(s['trip_id'])
            break
        #print (h,m,sec)

    def parse_trip_id(self, trip_id):
        """Parse a stop_id with form: A20121216WKD_000800_1..S03R"""
        if (len(trip_id) != 27):     # TODO: more specific exception type
            raise Exception("trip_id with invalid length: %s" % trip_id)
        return dict(zip(("service_id", "service_day", "trip_start_time",
                         "trip_route", "shape_id"),
                       (trip_id[0:12], trip_id[9:12], trip_id[13:19],
                           trip_id[20], trip_id[23:27])))

    #def parse_station_entrances(self, station_entrances):
        #station_defs = uniq(station_entrances,
                            #lambda x: (x['Line'], x['Station_Name']))
        #print len(list(station_defs))
        ##stations = (self.build_station(d) for d in station_defs)
        ##self.stations = list(stations)

    def build_station(self, st_def):
        st = Station(st_def['stop_id'], st_def['stop_name'],
                     st_def['stop_lat'], st_def['stop_lon'])
        return st

    #def build_station(self, station_def):
        #route_list = list()
        #st = Station(
                #station_def['Line'],
                #station_def['Station_Name'],
                #station_def['Latitude'],
                #station_def['Longitude'],
                #route_list)
        #routes = [self.build_route(r)
                    #for r in self.get_station_routes(station_def)]
        #route_list.extend(routes)
        #for r in route_list:
            #r.stations.append(st)
        #return st

    def build_route(self, route_name):
        if route_name not in self.routes:
            self.routes[route_name] = Route(route_name)
        return self.routes[route_name]

    def get_station_routes(self, station_dict):
        """Get non-empty route names for station in range Route_1 to Route_11.
        >>> TransitSystem().get_station_routes(
                        >>> {'Route_1': '1',  'Route_2': '',  'Line': None})
        ['1']
        """
        return filter(None,
                      [station_dict.get('Route_%d' % i) for i in range(1, 12)])


class Station(object):
    def __init__(self, id, name, latitude, longitude, routes=None):
        self.id = id
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.routes = routes if routes is not None else []

    def __repr__(self):
        return ("Station(%s, %s, %s, %s, %s)" %
                (self.id, self.name, self.latitude, self.longitude,
                "".join(str(r) for r in self.routes)))

    def __str__(self):
        return self.name


class Route(object):
    def __init__(self, name, stations=None):
        self.name = name
        self.stations = stations if stations is not None else []

    def __str__(self):
        return self.name

    def str_full(self):
        return ("Route(%s, stations=%s)" %
                (self.name, ",\n".join((str(st) for st in self.stations))))


def uniq(iterable, keyfn=None):
    pass
    """Yields unique items in iterable using keyfn to determine uniqueness.
    >>> list(uniq([1,2,2]))
    [1, 2]
    >>> list(uniq([1,2,3], keyfn=lambda x: x % 2))
    [1, 2]
    """
    seen = set()
    for value in iterable:
        key = keyfn(value) if keyfn is not None else value
        if key in seen:
            continue
        seen.add(key)
        yield value


def parse_csv(csvfile):
    """Read csv file and yield rows as dict, using header row as keys"""
    csvreader = csv.reader(csvfile)
    header = csvreader.next()
    return (dict(zip(header, st)) for st in csvreader)


def main():
    transit = TransitSystem()
    with open('google_transit/stops.txt') as csvfile:
        transit.parse_stops(parse_csv(csvfile))
    #with open('google_transit/stop_times.txt') as csvfile:
        #transit.parse_stop_times(parse_csv(csvfile))

    #with open('StationEntrances.csv', 'rb') as csvfile:
        #transit.parse_station_entrances(parse_csv(csvfile))

    #it = iter(transit.stations)
    #for s in [it.next() for _ in range(10)]:
        #print s

    for s in transit.stations:
        print repr(s)

    #print transit.routes['G'].str_full()
    #print transit.routes['F'].str_full()
    #print "\n===\n".join(r.str_full() for r in transit.routes.values())

    return transit


if __name__ == "__main__":
    ret = main()
