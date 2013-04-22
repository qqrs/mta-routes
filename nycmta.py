import csv

class Route(object):
    pass

class Station(object):
    def __init__(self, line, name, routes):
        self.line = line
        self.name = name
        self.routes = routes

    def __repr__(self):
        return "<Station %s, %s, %s>" % (self.line, self.name, "".join(self.routes))

def main():
    pass


def get_station_routes(station_dict):
    """Get non-empty routes.
    >>> get_station_routes({'Route_1': '1',  'Route_2': '',  'Line': None})
    ['1']
    """
    return filter(None, [station_dict.get('Route_%d' % i) for i in range(1,12)])

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

if __name__ == "__main__":
    main()

    with open('StationEntrances.csv', 'rb') as csvfile:
        mtareader = csv.reader(csvfile)
        header = mtareader.next()
        station_dicts = uniq((dict(zip(header,st)) for st in mtareader),
                             lambda x: (x['Line'], x['Station_Name']))
        stations = (Station(d['Line'],
                            d['Station_Name'], 
                            get_station_routes(d))
                    for d in station_dicts)

        it = iter(stations)
        for s in [it.next() for _ in range(10)]:
            print s

        routes = {}
        for station in stations:
            for route_name in station.routes:
                if route_name in routes:
                    print 'we should add route objects here'


