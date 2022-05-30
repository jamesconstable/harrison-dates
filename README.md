# Date Calculator | harrison.ai
A simple utility for calculating the number of days between two dates,
according to harrison.ai's [tech task spec](
https://github.com/harrison-ai/hai-tech-tasks/blob/develop/dates.md).

Note that the proleptic Gregorian calendar is used for all calculations (i.e.
the modern system for calculating leap years is extrapolated indefinitely both
forwards and backwards), so calculations before and around the
Julian-to-Gregorian changeover may require region-specific corrections to match historical values.

All dates must have the format `YYYY-MM-DD`, so any years prior to 1000 AD
should have padding zeros added. 1 BC is the earliest representable year and
may be expressed as 0000, while 9999 AD is the latest.

Command line usage:
```bash
python3 -m dates <date1> <date2>
```

where both dates must have the format `YYYY-MM-DD`.

To run the unit tests, use the following command:
```bash
python3 -m unittest
```
