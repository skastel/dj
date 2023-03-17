# coding: utf-8

"""
    DJ server

    A DataJunction metrics layer  # noqa: E501

    The version of the OpenAPI document: 0.0.post1.dev1+gee35d4f
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from djclient import schemas  # noqa: F401


class UpdateNode(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Update node object where all fields are optional
    """


    class MetaOapg:
        
        class properties:
            catalog = schemas.StrSchema
            schema_ = schemas.StrSchema
            table = schemas.StrSchema
            
            
            class columns(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def additional_properties() -> typing.Type['SourceNodeColumnType']:
                        return SourceNodeColumnType
                
                def __getitem__(self, name: typing.Union[str, ]) -> 'SourceNodeColumnType':
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> 'SourceNodeColumnType':
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: 'SourceNodeColumnType',
                ) -> 'columns':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            display_name = schemas.StrSchema
            description = schemas.StrSchema
        
            @staticmethod
            def mode() -> typing.Type['NodeMode']:
                return NodeMode
            query = schemas.StrSchema
            __annotations__ = {
                "catalog": catalog,
                "schema_": schema_,
                "table": table,
                "columns": columns,
                "display_name": display_name,
                "description": description,
                "mode": mode,
                "query": query,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["catalog"]) -> MetaOapg.properties.catalog: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["schema_"]) -> MetaOapg.properties.schema_: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["table"]) -> MetaOapg.properties.table: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["columns"]) -> MetaOapg.properties.columns: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["display_name"]) -> MetaOapg.properties.display_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["mode"]) -> 'NodeMode': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["query"]) -> MetaOapg.properties.query: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["catalog"], typing_extensions.Literal["schema_"], typing_extensions.Literal["table"], typing_extensions.Literal["columns"], typing_extensions.Literal["display_name"], typing_extensions.Literal["description"], typing_extensions.Literal["mode"], typing_extensions.Literal["query"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["catalog"]) -> typing.Union[MetaOapg.properties.catalog, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["schema_"]) -> typing.Union[MetaOapg.properties.schema_, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["table"]) -> typing.Union[MetaOapg.properties.table, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["columns"]) -> typing.Union[MetaOapg.properties.columns, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["display_name"]) -> typing.Union[MetaOapg.properties.display_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["mode"]) -> typing.Union['NodeMode', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["query"]) -> typing.Union[MetaOapg.properties.query, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["catalog"], typing_extensions.Literal["schema_"], typing_extensions.Literal["table"], typing_extensions.Literal["columns"], typing_extensions.Literal["display_name"], typing_extensions.Literal["description"], typing_extensions.Literal["mode"], typing_extensions.Literal["query"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        catalog: typing.Union[MetaOapg.properties.catalog, str, schemas.Unset] = schemas.unset,
        schema_: typing.Union[MetaOapg.properties.schema_, str, schemas.Unset] = schemas.unset,
        table: typing.Union[MetaOapg.properties.table, str, schemas.Unset] = schemas.unset,
        columns: typing.Union[MetaOapg.properties.columns, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        display_name: typing.Union[MetaOapg.properties.display_name, str, schemas.Unset] = schemas.unset,
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        mode: typing.Union['NodeMode', schemas.Unset] = schemas.unset,
        query: typing.Union[MetaOapg.properties.query, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'UpdateNode':
        return super().__new__(
            cls,
            *_args,
            catalog=catalog,
            schema_=schema_,
            table=table,
            columns=columns,
            display_name=display_name,
            description=description,
            mode=mode,
            query=query,
            _configuration=_configuration,
        )

from djclient.model.node_mode import NodeMode
from djclient.model.source_node_column_type import SourceNodeColumnType
