### mta-routes
Parse the GTFS data provided by MTA for the NYC subway system and find routes between stations using Djikstra's algorithm.

### TODO
1. Web frontend
1. Add support for walking transfers between stations (MTA data sometimes lists stops as separate stations even when they are directly connected by stairs)
1. Proper edge weights between stations to prioritize faster routes
1. Support for different times of day (currently assumes weekday noon)

### Resources
[MTA Developer Data Downloads](http://www.mta.info/developers/download.html)  
[MTA New York City Transit Subway GTFS Schedule Data](http://www.mta.info/developers/data/nyct/subway/google_transit.zip)  
[Priority dict: a priority queue with updatable priorities](http://code.activestate.com/recipes/522995/)  
