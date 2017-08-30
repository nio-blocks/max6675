MAX6675
=======
Read temperature from a MAX6675 thermocouple over SPI.

Properties
----------
- **bus**: SPI bus number (generally 0 or 1).
- **client**: SPI client number.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: The attribute `temperature` (in degrees celsius) is appended onto the input signal.

Commands
--------
None

Dependencies
------------
spidev

Output Example
--------------
```
{
  "temperature": 23.0
}
```

