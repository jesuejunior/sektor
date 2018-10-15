# sektor


### Preparing environment

Install pipenv

```shell
    pip3 install pipenv
```

Install dependencies

```shell
    pipenv --python `which python3` install
```


To start the gpsd module run:

```
    stty -F /dev/ttyS0 9600 && sudo gpsd /dev/ttyS0 -F /var/run/gpsd.socket
```


### Datastructure

```sql
time INTEGER // Time in seconds in the moment of took position i.e: 100
lat DOUBLE PRECISION // latitude position i.e: 40.741895 
lon DOUBLE PRECISION // longitude position i.e: -73.989308
speed INT // speed in KM/h i.e: 100
distance INT // distance ahead of latest
oil BOOLEAN // If it has grease the chain
created_at DATETIME // datetime of save
```


### Rules




