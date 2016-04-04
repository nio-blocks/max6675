MAX6675
=======

Read temperature from a MAX6675 thermocouple over SPI.

Properties
--------------

-   **bus**: SPI bus number (generally 0 or 1)
-   **client**: SPI client number

Dependencies
------------
spidev

Commands
--------
None

Input
-------
Any Signal

Output
------
The attribute `temperature` (in degrees celsius) is appended onto the input signal.

```
{
  "temperature": 23.0
}
```
