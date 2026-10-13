# MP1 Data Pipeline

This pipeline cleans a CSV file using settings from a YAML config file. `pipeline.py` runs the steps in order: check the
files, load the data, validate it, clean it, and save it. Each step exists in its own module in `src/`. 
`data_loaders.py` reads the files, `data_validator.py` checks the columns and numbers, and `data_processor.py` removes 
duplicates, missing values and outliers. `data_output.py` saves the cleaned CSV, and `utils.py` handles logging and file
checks. All column names and cleaning choices are in `config/config.yaml`, so the code does not change for new data.


## Example

```
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

21:51:19 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
21:51:19 INFO     src.utils — Input file validated: fixtures/sample_data.csv
21:51:19 INFO     src.utils — Input file validated: config/config.yaml
21:51:19 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
21:51:19 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
21:51:19 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
21:51:19 DEBUG    src.data_validator — Validation: 100 -> 98 rows
21:51:19 INFO     __main__ — Validation complete: 100 -> 98 rows
21:51:19 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows
21:51:19 DEBUG    src.data_processor — handle_missing: 96 → 94 rows
21:51:19 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
21:51:19 INFO     __main__ — Processing complete: 98 -> 92 rows
21:51:19 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
21:51:19 INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}