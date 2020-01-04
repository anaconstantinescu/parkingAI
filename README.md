# ParkingAI

This is a tehnical demo made to show what could be done when useing tehnology to eficently enfore parking rules and detect parking violations useing AI.
The tehnical demo uses a the Bucharest streets as refeance for AI training because parking violations are more frequent so it takes less sample data to train.

## Numberplate format

Full Numer
```
Non Trim
r"[a-z]{1,2}\s[0-9]{2,3}\s[a-z]{3}"gmi

Trim
r"[a-z]{1,2}[0-9]{2,3}[a-z]{3}"gmi
```

Red Numbers
```
Non Trim
r"[a-z]{1,2}[0-9]{3,6}"gmi

Trim

r"[a-z]{1,2}[0-9]{3,6}"gmi
```

## Database Specs
The data for the test will be found [CSV](plate_dictionary.csv)

## Database structure

| Number Plate  | Infraction    | Image Name [array]    | timestap  | GPS-Position [lat long]   | Test Flag Moving  |
| ---           | ---           | ---                   | ---       | ---                       | ---               |
| B 97 YBH      | A1            | G0597882              |           | 44.4459156,26.0754033     |                   |

## Test Flags

### Moving 
If GPS position is long this would indicate the car is moving so it is not parked
Expected: Boolean Numeric 1 0

## GPS-Position [lat long] 
I need the position of the image with the larges number.

## timestap [lat long] 
I need the timestap of the image with the larges number.

## Image Name
I need all the images separated by space

G0597882 G0597883 G0597884 G0597885

## Infraction
Leave empty for now, we will run the AI separatly
