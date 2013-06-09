import csv
import pickle
from itertools import groupby
from djikstra import djikstra_path


class TransitSystem(object):
    def __init__(self):
        self.stations = {}
        self.routes = {}
        self.graph = {}

    def parse_stops(self, stops):
        """Parse data from stops.txt"""
        stop_defs = (st for st in stops if st['location_type'] == '1')
        stations = ((s['stop_id'], self.build_station(s)) for s in stop_defs)
        self.stations = dict(stations)

    def parse_stop_times(self, stop_times):
        """Parse data from stop_times.txt"""
        # split trip_id field into subfields and add to dict
        stop_times = self.parse_trip_id(stop_times)

        # weekday service, between 10 am and 2 pm
        stop_times = (s for s in stop_times if s['service_day'] == 'WKD')
        stop_times = (s for s in stop_times if
                      60000 <= int(s['trip_start_time']) <= 84000)

        self.add_route_stations(stop_times)
        self.add_station_routes()

    def add_route_stations(self, stop_times):
        """Add stations to self.routes"""
        for ((trip_id, trip_route), group_it) in groupby(
                stop_times, lambda s: (s['trip_id'], s['trip_route'])):
            route = self.build_route(trip_route)

            group_stops = list(group_it)
            # note: may include some special stops but not others
            if len(route.stations) < len(group_stops):
                route.stations = self.get_stations_for_stops(group_stops)

    def get_stations_for_stops(self, stops):
        """Get Station objects corresponding to stops, by stop_id"""
        stations = []
        for stop in stops:
            stop_id = stop['stop_id']
            if (len(stop_id) != 4):
                raise IndexError("invalid length: stop_id=%s" % stop_id)
            try:
                station = self.stations[stop_id[0:3]]
            except KeyError:
                raise KeyError("No Station found for stop_id=%s" % stop_id)
            stations.append(station)
        return stations

    def add_station_routes(self):
        """Add routes to self.stations."""
        for r in self.routes.values():
            for st in r.stations:
                self.stations[st.id].routes.append(r)

    def parse_trip_id(self, stop_time_defs):
        """Parse a stop_id fields with form: A20121216WKD_000800_1..S03R"""
        for s in stop_time_defs:
            try:
                trip_id = s['trip_id']
            except KeyError:
                raise AttributeError("No trip_id for %s" % s)
            if (len(trip_id) != 27):
                raise IndexError("invalid length: trip_id=%s" % trip_id)
            s.update(dict(zip(
                    ("service_id", "service_day", "trip_start_time",
                        "trip_route", "shape_id"),
                    (trip_id[0:12], trip_id[9:12], trip_id[13:19],
                        trip_id[20], trip_id[23:27]))))
            yield s

    def build_station(self, st_def):
        """Create a Station object from a station_def dict"""
        st = Station(st_def['stop_id'], st_def['stop_name'],
                     st_def['stop_lat'], st_def['stop_lon'])
        return st

    def build_route(self, route_name):
        """Find or create route with route_name"""
        if route_name not in self.routes:
            self.routes[route_name] = Route(route_name)
        return self.routes[route_name]

    def build_transit_graph(self):
        """Build transit graph for path search.

        Graph is represented as adjacency dict where graph[v][k] is edge weight
        from Station v to k."""
        # TODO: currently O(V*E), make it O(V+E)
        for s in self.stations.values():
            self.graph[s] = dict.fromkeys(s.find_adjacent(), 1.0)

    def get_path(self, start, end):
        """Find shortest path between stations."""
        return djikstra_path(self.graph, start, end)


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

    def find_adjacent(self):
        """Find stations one stop away"""
        adjacent = set()
        for r in self.routes:
            home_index = r.stations.index(self)
            try:
                adjacent.add(r.stations[home_index-1])
            except IndexError:
                pass
            try:
                adjacent.add(r.stations[home_index+1])
            except IndexError:
                pass
        return adjacent


class Route(object):
    def __init__(self, name, stations=None):
        self.name = name
        self.stations = stations if stations is not None else []

    def __str__(self):
        return self.name

    def str_full(self):
        return ("Route(%s, stations=%s)" %
                (self.name, ",\n".join((str(st) for st in self.stations))))


def parse_csv(csvfile):
    """Read csv file and yield rows as dict, using header row as keys"""
    csvreader = csv.reader(csvfile)
    header = csvreader.next()
    return (dict(zip(header, st)) for st in csvreader)


def load_transit():
    try:
        with open("transit.pickle", "r") as f:
            transit = pickle.load(f)
    except IOError:
        transit = TransitSystem()
        with open("google_transit/stops.txt") as csvfile:
            transit.parse_stops(parse_csv(csvfile))
        with open("google_transit/stop_times.txt") as csvfile:
            transit.parse_stop_times(parse_csv(csvfile))
        transit.build_transit_graph()
        with open("transit.pickle", "w") as f:
            pickle.dump(transit, f)
    return transit


def main():
    transit = load_transit()

    #print transit.routes['F'].str_full()
    #print "\n===\n".join(r.str_full() for r in transit.routes.values())

    fourth_ave = transit.stations['F23']
    jay_street = transit.stations['A41']
    spring_street = transit.stations['A33']

    print fourth_ave.find_adjacent()
    print jay_street.find_adjacent()
    print spring_street.find_adjacent()

    path = transit.get_path(fourth_ave, spring_street)
    for p in path:
        print p

    return transit


if __name__ == "__main__":
    ret = main()
