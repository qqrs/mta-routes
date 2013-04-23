import csv


#class Route(object):
    #all_routes = {}

#class Route(object):
    #all_routes = {}
    #def __new__(cls, name, *args, **kwargs):
        #if not name in self.all_routes:
            #r = super(Route, cls).__new__(cls, name, *args, **kwargs)
            #r.name = name
            #r.stations = list()
            #self.all_routes[name] = r
        #return self.all_routes[name]

    #def __init__(self, name, *stations):
        #self.name = name
        #self.stations = stations

class TransitSystem(object):
    def __init__(self):
        self.stations = []
        self.routes = {}

    def parse_csv(self, csvfile):
        csvreader = csv.reader(csvfile)
        header = csvreader.next()
        station_entrances = (dict(zip(header,st)) for st in csvreader)
        station_defs = uniq(station_entrances, 
                            lambda x: (x['Line'], x['Station_Name']))
        stations = (self.build_station(d) for d in station_defs)
        self.stations = list(stations)

    def build_station(self, station_def):
        route_list = list()
        st = Station(
                station_def['Line'], 
                station_def['Station_Name'], 
                station_def['Latitude'], 
                station_def['Longitude'], 
                route_list)
        routes = [self.build_route(r) 
                    for r in self.get_station_routes(station_def)]
        route_list.extend(routes)
        for r in route_list:
            r.stations.append(st)
        return st

    def build_route(self, route_name):
        if route_name not in self.routes:
            self.routes[route_name] = Route(route_name)
        return self.routes[route_name]

    def get_station_routes(self, station_dict):
        """Get non-empty route names for a station in range Route_1 to Route_11.
        >>> TransitSystem().get_station_routes({'Route_1': '1',  'Route_2': '',  'Line': None})
        ['1']
        """
        return filter(None, [station_dict.get('Route_%d' % i) for i in range(1,12)])


class Station(object):
    def __init__(self, line, name, latitude, longitude, routes=None):
        self.line = line
        self.name = name
        self.latitude = int(latitude)
        self.longitude = int(longitude)
        self.routes = routes if routes is not None else []

    def __repr__(self):
        return "Station(%s, %s, %s, %s, %s)" % (self.line, self.name, 
                                        self.latitude, self.longitude,
                                        "".join(str(r) for r in self.routes))
    def __str__(self):
        return "%s @ %s" % (self.line, self.name)

class Route(object):
    def __init__(self, name, stations=None):
        self.name = name
        self.stations = stations if stations is not None else []

    def __str__(self):
        return self.name

    def str_full(self):
        return "Route(%s, stations=%s)" % (self.name, 
                                ",\n".join((str(st) for st in self.stations)))


def uniq(iterable, keyfn=None):
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

def main():
    transit = TransitSystem()
    with open('StationEntrances.csv', 'rb') as csvfile:
        transit.parse_csv(csvfile)

    #it = iter(transit.stations)
    #for s in [it.next() for _ in range(10)]:
        #print s

    for s in transit.stations[:10]:
        print repr(s)

    #for r in transit.routes:
        #print r

    #print transit.routes['F'].str_full()

    return transit


if __name__ == "__main__":
    ret=main()
