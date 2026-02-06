import time
from src.domain.models import CombatParams, Scenario
from src.domain.edge_cases import EdgeCaseGenerator
from src.domain.template_renderer import TemplateRenderer

def run_performance_test():
    """
    Measure time to generate and render 100+ test cases.
    Target: < 2.0 seconds
    """
    print("Starting Performance Test...")
    
    # Setup: Create params that will generate multiple cases
    # 4 base scenarios + 3 edge cases = 7 cases per generation call.
    # To get ~100 cases, we need about 15 iterations or just massive inputs.
    # The requirement is likely "generating a file with 100 cases" or "total throughput".
    # Let's simple measure the generation of a complex set 100 times.
    
    params = CombatParams(
        player_damage=50,
        enemy_hp=100,
        scenarios=[Scenario.NORMAL, Scenario.CRITICAL, Scenario.DODGE, Scenario.DEATH], # 4 scenarios
        language="csharp"
    )
    
    generator = EdgeCaseGenerator()
    renderer = TemplateRenderer()
    
    start_time = time.time()
    
    LAYER_1_COUNT = 20 # Generate 20 times (7 * 20 = 140 cases)
    
    total_cases = 0
    for _ in range(LAYER_1_COUNT):
        cases = generator.generate(params)
        _ = renderer.render(cases, "csharp")
        total_cases += len(cases)
        
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Generated {total_cases} cases in {duration:.4f} seconds.")
    
    if duration < 2.0:
        print("PASS: Performance requirement met (< 2.0s)")
        return True
    else:
        print(f"FAIL: Too slow ({duration:.4f}s >= 2.0s)")
        return False

if __name__ == "__main__":
    success = run_performance_test()
    if not success:
        exit(1)
