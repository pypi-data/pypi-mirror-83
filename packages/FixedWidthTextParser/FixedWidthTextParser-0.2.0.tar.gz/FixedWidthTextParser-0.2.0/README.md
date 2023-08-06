# Fixed width text parser to array

Parsing different defined text formats to array data

**Parser** - parse anything according to the format definition

For use cases check **_tests_** folder

Format definition:
 
```python

definition = {
    'FIELD_1': [0, 1, 'string'],
    'FIELD_2': [1, 10, 'float'],
    'FIELD_3': [11, 10, 'float'],
    'FIELD_4': [23, 1, 'integer'],
    'FIELD_5': [24, 2, 'string'],
    'FIELD_6': [26, 4, 'integer', 0],
    'FIELD_7': [30, 4, 'integer', None],
    'FIELD_8': [34, 4, 'float', None],
    'FIELD_9': [38, 4, 'float', 0.0],
}
```

Field definition ```'FIELD_6': [26, 4, 'integer', 0]``` 
* 'FIELD_6' - field name
* 26 - index of text line where the field starts (count starts from 0)
* 4 - field length in characters 
* string - field value type (allowed types: string, integer, float)
* 0 - default value if empty in text line record

For every data type default value is always None if field results as empty string.
For every data type it is possible to set default value in format definition.

### Specific format parsers
* **Seismic.SpsParser.Sps21Parser** - SPS format version num.     SPS 2.1, JAN2006
* **Seismic.VibratorParser.ApsParser** 
* **Seismic.VibratorParser.CogParser** 
* **Seismic.VibratorParser.VapsParser** 

### File formats

* [SPS](doc/SPS.md)
* [Vibrator](doc/Vibrator.md)

### References
* [SPS - Shell Processing Support](https://en.wikipedia.org/wiki/Shell_Processing_Support)
