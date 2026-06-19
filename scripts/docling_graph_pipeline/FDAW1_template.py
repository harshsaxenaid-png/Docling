from pydantic import BaseModel, Field


class Company(BaseModel):
    model_config = {
        "is_entity": True,
        "graph_id_fields": ["name"]
    }

    name: str


class Facility(BaseModel):
    model_config = {
        "is_entity": True,
        "graph_id_fields": ["name"]
    }

    name: str
    address: str | None = None


class Person(BaseModel):
    model_config = {
        "is_entity": True,
        "graph_id_fields": ["name"]
    }

    name: str
    title: str | None = None


class Product(BaseModel):
    model_config = {
        "is_entity": True,
        "graph_id_fields": ["name"]
    }

    name: str
    category: str | None = None


class Observation(BaseModel):
    model_config = {
        "is_entity": True,
        "graph_id_fields": ["description"]
    }

    description: str
    regulation: str | None = None


class WarningLetter(BaseModel):
    model_config = {
        "is_entity": True,
        "graph_id_fields": ["letter_id"]
    }

    letter_id: str = "FDAW1"
    subject: str | None = None
    issue_date: str | None = None

    companies: list[Company] = Field(
        default_factory=list,
        json_schema_extra={"edge_label": "ISSUED_TO"},
    )
    facilities: list[Facility] = Field(
        default_factory=list,
        json_schema_extra={"edge_label": "INSPECTED_FACILITY"},
    )
    people: list[Person] = Field(
        default_factory=list,
        json_schema_extra={"edge_label": "ADDRESSED_TO"},
    )
    products: list[Product] = Field(
        default_factory=list,
        json_schema_extra={"edge_label": "INVOLVES_PRODUCT"},
    )
    observations: list[Observation] = Field(
        default_factory=list,
        json_schema_extra={"edge_label": "CONTAINS_OBSERVATION"},
    )
