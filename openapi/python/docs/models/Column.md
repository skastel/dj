# djopenapi.model.column.Column

A column.  Columns can be physical (associated with ``Table`` objects) or abstract (associated with ``Node`` objects).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A column.  Columns can be physical (associated with &#x60;&#x60;Table&#x60;&#x60; objects) or abstract (associated with &#x60;&#x60;Node&#x60;&#x60; objects). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**name** | str,  | str,  |  | 
**[type](#type)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Base type for all Column Types | 
**id** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] 
**dimension_id** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] 
**dimension_column** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# type

Base type for all Column Types

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Base type for all Column Types | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)
