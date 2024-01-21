import great_expectations as gx

context = gx.get_context()

validator = context.sources.pandas_default.read_csv(
    "https://raw.githubusercontent.com/great-expectations/gx_tutorials/main/data/yellow_tripdata_sample_2019-01.csv"
)

print(type(validator))

context.add_or_update_expectation_suite("my_expectation_suite")
# Optional. Run assert "my_expectation_suite" in context.list_expectation_suite_names() to veriify the Expectation Suite was created.

expectation_validation_result = validator.expect_column_values_to_not_be_null(
    column="vendor_id"
)
print(expectation_validation_result)


print(expectation_validation_result)
