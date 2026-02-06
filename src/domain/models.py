from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class Scenario(str, Enum):
    """
    Defines the types of combat scenarios to generate.
    """
    NORMAL = "normal"
    CRITICAL = "critical"
    DODGE = "dodge"
    DEATH = "death"

class CombatParams(BaseModel):
    """
    Input parameters for generating combat test cases.
    Includes validation rules for damage, HP, and output settings.
    """
    player_damage: int = Field(..., ge=0, le=9999, description="Damage dealt by the player (0-9999)")
    enemy_hp: int = Field(..., ge=1, le=999999, description="Target enemy HP (1-999999)")
    scenarios: List[Scenario] = Field(
        default_factory=lambda: [Scenario.NORMAL],
        description="List of scenarios to generate"
    )
    random_count: int = Field(
        default=0,
        ge=0,
        le=1000,
        description="Number of additional random test cases to generate"
    )
    output_path: str = Field(
        default="./CombatTests.xlsx",
        description="File path to save the generated tests"
    )
    language: str = Field(
        default="excel",
        pattern="^(csharp|python|json|excel)$",
        description="Target language: csharp, python, json, or excel",
        # The original request for a validation message was syntactically incorrect
        # for direct inclusion in Field. This is a common way to add a custom
        # regex error message in Pydantic v1.
        error_messages={"value_error.str.regex": "지원하지 않는 언어입니다. (csharp, python, json, excel 중 선택)"}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "player_damage": 50,
                "enemy_hp": 100,
                "scenarios": ["normal", "critical"],
                "output_path": "./CombatTests.cs",
                "language": "csharp"
            }
        }

class TestCase(BaseModel):
    """
    Represents a single generated test case.
    """
    name: str
    description: str
    input_damage: int
    input_hp: int
    expected_hp: int
    is_critical: bool = False
    is_dodge: bool = False
    is_death: bool = False

