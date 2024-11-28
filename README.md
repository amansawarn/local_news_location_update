## Cache entities

This repo contains code for creating in memory cache of entities in redis.

A module extracts records from specified mongo collections and dumps to redis in the format entity: entity_id.
For locations, districts and states are ingested as is. Cities which are marked as important are only ingested. 
A list of blocked names is maintained, which is used to prune locations.

Another module extracts source_location: nearby_locations (districts and important cities) within 100 km of all locations from mongo collection.
Creates a reverse index of nearby_location: source_locations and dumps to redis.

## Run: 
```
---src
    |--- python3 dump_entities_to_redis.py
    |--- python3 reverse_nearby_index.py
```