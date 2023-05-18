# playground

Run the following commands in the terminal (current working directory: `IMP-utils` folder). You can change the available parameter of the functions in `IMP_utils_py/config/playground.gin`. The path parameters in `playground.gin` have to be relative to the `IMP-utils` folder.

## table of content

- [grade-calculator](#grade-calculator): calculate grade from Leitsungsspiegel


<a name="grade-calculator"/>

## Grade-calculator

### path parameters

LEISTUNGSSPIEGEL_PATH: path to pdf file of agnes Leistungsspiegel
  - `string` e.g. "Leistungsspiegel.pdf"

### calculation example

| name                                                  |   grade |   credit |
|:------------------------------------------------------|--------:|---------:|
| Einführung in die formale Logik für IMP               |     1   |        5 |
| Lineare Algebra und Analytische Geometrie I           |     1   |        9 |
| Lineare Algebra und Analytische Geometrie II          |     2.3 |        9 |
| Einführung in die Theoretische Informatik             |     2.7 |        9 |
| Analysis I                                            |     1.3 |        9 |
| Analysis II                                           |     1.3 |        9 |
| Klassische Mechanik und spezielle Relativitätstheorie |     2.3 |        8 |

uses weighted average of grades:

<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;grade&space;=&space;\frac{1&space;\cdot&space;5&space;&plus;&space;1&space;\cdot&space;9&space;&plus;&space;2.3&space;\cdot&space;9&space;&plus;&space;2.7&space;\cdot&space;9&space;&plus;&space;1.3&space;\cdot&space;9&space;&plus;&space;1.3&space;\cdot&space;9&space;&plus;&space;2.3&space;\cdot&space;8}{5&plus;9&plus;9&plus;9&plus;9&plus;9&plus;8}" /> 

If you use the command for IMP only the better grade of 

- "Lineare Algebra und Analytische Geometrie I" and "Lineare Algebra und Analytische Geometrie II"

- "Analysis I" and "Analysis II"

will be used in the calculations

### command for IMP

```
python IMP_utils_py/cli.py --mode=grade-calculator-IMP --gin_file=IMP_utils_py/config/playground.gin
```

### command for not IMP

```
python IMP_utils_py/cli.py --mode=grade-calculator-general --gin_file=IMP_utils_py/config/playground.gin
```
