from typing import List
from src.domain.models import CombatParams, Scenario, TestCase

import random

class EdgeCaseGenerator:
    """
    Generates a list of test cases based on combat parameters, including edge cases.
    """
    
    def generate(self, params: CombatParams) -> List[TestCase]:
        cases = []
        
        # 0. Random Variations
        if params.random_count > 0:
            for i in range(params.random_count):
                cases.append(self._create_random_case(params, i + 1))
        
        # 1. Base Scenarios (User selected)
        if Scenario.NORMAL in params.scenarios:
            cases.append(self._create_normal_case(params))
            
        if Scenario.CRITICAL in params.scenarios:
            cases.append(self._create_critical_case(params))
            
        if Scenario.DODGE in params.scenarios:
            cases.append(self._create_dodge_case(params))
            
        if Scenario.DEATH in params.scenarios:
             cases.append(self._create_death_case(params))

        # 2. Edge Case Variations (Auto-generated variations based on inputs)
        # Always add these or make them optional? 
        # For now, let's treat "Edge Cases" as implicit additions for robustness
        
        # Zero Damage Case
        cases.append(TestCase(
            name="Test_ZeroDamage",
            description="데미지 0일 때 HP 감소 없음",
            input_damage=0,
            input_hp=params.enemy_hp,
            expected_hp=params.enemy_hp,
            is_critical=False
        ))
        
        # 1 HP Case
        cases.append(TestCase(
            name="Test_OneHP_Survival",
            description="HP 1인 적이 데미지 0을 받아도 생존",
            input_damage=0,
            input_hp=1,
            expected_hp=1,
            is_critical=False
        ))
        
        # Overkill Case (if damage > hp)
        overkill_dmg = params.enemy_hp + 50
        cases.append(TestCase(
            name="Test_Overkill",
            description=f"데미지 {overkill_dmg}로 HP 0 및 사망 확인 (오버킬)",
            input_damage=overkill_dmg,
            input_hp=params.enemy_hp,
            expected_hp=0,
            is_death=True
        ))
        
        return cases

    def _create_normal_case(self, params: CombatParams) -> TestCase:
        final_hp = max(0, params.enemy_hp - params.player_damage)
        return TestCase(
            name=f"Test_Normal_{params.player_damage}dmg_{params.enemy_hp}hp",
            description="Normal attack calculation",
            input_damage=params.player_damage,
            input_hp=params.enemy_hp,
            expected_hp=final_hp,
            is_death=(final_hp == 0)
        )

    def _create_critical_case(self, params: CombatParams) -> TestCase:
        # Assuming Critical is 2.0x
        crit_dmg = params.player_damage * 2
        final_hp = max(0, params.enemy_hp - crit_dmg)
        return TestCase(
            name=f"Test_Critical_{crit_dmg}dmg_{params.enemy_hp}hp",
            description="Critical attack (2x damage)",
            input_damage=params.player_damage,
            input_hp=params.enemy_hp,
            expected_hp=final_hp,
            is_critical=True,
            is_death=(final_hp == 0)
        )

    def _create_dodge_case(self, params: CombatParams) -> TestCase:
        return TestCase(
            name=f"Test_Dodge_{params.player_damage}dmg",
            description="Dodge should result in 0 damage taken",
            input_damage=params.player_damage,
            input_hp=params.enemy_hp,
            expected_hp=params.enemy_hp,
            is_dodge=True
        )

    def _create_death_case(self, params: CombatParams) -> TestCase:
        # User wants to test death flow specifically
        # We ensure damage kills the enemy
        kill_dmg = params.enemy_hp
        return TestCase(
            name=f"Test_Death_{params.enemy_hp}hp",
            description="Exact damage to kill enemy",
            input_damage=kill_dmg,
            input_hp=params.enemy_hp,
            expected_hp=0,
            is_death=True
        )

    def _create_random_case(self, params: CombatParams, seq: int) -> TestCase:
        # Vary damage and HP by +/- 20%
        dmg_mult = random.uniform(0.8, 1.2)
        hp_mult = random.uniform(0.8, 1.2)
        
        # Avoid 0 damage if original wasn't 0, but keep integers
        input_damage = int(params.player_damage * dmg_mult)
        input_hp = int(params.enemy_hp * hp_mult)
        
        # Recalculate expected result
        final_hp = max(0, input_hp - input_damage)
        
        return TestCase(
            name=f"Test_Random_{seq}_{input_damage}dmg_{input_hp}hp",
            description=f"무작위 변형 케이스 #{seq} (입력값의 ±20%)",
            input_damage=input_damage,
            input_hp=input_hp,
            expected_hp=final_hp,
            is_death=(final_hp == 0)
        )
