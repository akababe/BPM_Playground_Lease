# Complete Simulation Runner

from scenarios import AsIsScenario, ToBeScenario
from analytics import KPICalculator, SimulationVisualizer


def run_single_scenario(scenario_class):
    scenario = scenario_class()
    # Run your scenario logic here
    return scenario.run()


def compare_scenarios(scenario1_class, scenario2_class):
    scenario1 = run_single_scenario(scenario1_class)
    scenario2 = run_single_scenario(scenario2_class)
    # Compare KPIs
    return KPICalculator.calculate(scenario1, scenario2)

# Full KPI Reporting and ROI Analysis logic here
