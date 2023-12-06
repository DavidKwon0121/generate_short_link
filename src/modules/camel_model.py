from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        coerce_numbers_to_str=True,
        strict=False,  # attempts to coerce values to the correct type, when possible.
    )