# sqlcomp: An SQL Converter

`sqlcomp` is a converter library for the rare case where you might need to store some simple SQL in a very small amount of space, so you can retrieve it and execute it later.

Currently, the library only supports very basic conditionals (x=y, x<y, x like y, things like that) and INSERT/UPDATE/DELETE.

We have two classes - `SQLCompressor` and `SQLExpander`.
You can use these classes to generate configured objects that will compress down a long SQL string to a much shorter string.

## Config Grammar
`sqlcomp` config files are written as JSON files that map individual words to shorthand abbreviations.
For example, one of the test files for the package contains:

```
{
    'Test': 'T',
    'table': 't',
    'value': 'v'
}
```

This will be used as a lookup table when compressing and expanding SQL.

## Example
```
from sqlcomp import SQLCompressor, SQLExpander

sql = "INSERT INTO `Test` (`table`) VALUES (`value`);"
config = './config.json'

>>> SQLCompressor(config).compress(sql)
'I T t v'

>>> SQLExpander(config).compress('I T t v')
'INSERT INTO `Test` (`table`) VALUES (`value`);'
```