# Lease Process Simulation Playground

A comprehensive Python simulation for **Quantitative Process Analysis** of leasing operations, focusing on bottleneck identification, ROI calculation, and "What-If" scenario modeling.

## 🎯 Simulation Objectives

1. **Predict System Behavior** under varying workloads
2. **Identify Bottlenecks** in the leasing process workflow
3. **Calculate What-If ROI** for process improvements (e.g., Undo/Edit protocol)

## 📊 Monitored Metrics

### Time Dimensions
- **Inter-Arrival Time**: Time between new applications
- **Service Time**: Actual processing time per task
- **Waiting Time**: Queue time when resources are busy
- **Cycle Time**: Total time from application to disbursement

### Quality Dimensions
- **Rework Probability**: Percentage requiring corrections
- **Defect Rate**: Frequency of "Ghost Applications"

### Cost Dimensions
- **Resource Utilization**: Staff busy vs. idle time
- **Activity-Based Costing**: Time × hourly rate

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## 📁 Project Structure

```
├── main.py                  # Main simulation runner
├── models/
│   ├── lease_application.py # Application data class
│   ├── resources.py         # Staff/resource definitions
│   └── process_simulation.py# Core simulation engine
├── scenarios/
│   ├── as_is_scenario.py    # Current "Lock-and-Cancel" process
│   └── to_be_scenario.py    # Proposed "Undo/Edit" process
├── analytics/
│   ├── kpi_calculator.py    # KPI computation logic
│   └── visualizer.py        # Charts and dashboards
└── config/
    └── parameters.py        # Simulation parameters
```

## 🔬 Usage Examples

### Run Basic Simulation
```python
from scenarios.as_is_scenario import AsIsScenario
from analytics.kpi_calculator import KPICalculator

scenario = AsIsScenario()
results = scenario.run()
kpis = KPICalculator(results, scenario.config).calculate_all()
print(kpis)
```

### Compare Scenarios
```python
from main import compare_scenarios

compare_scenarios(
    visualize=True,
    export_results=True
)
```

## 📈 Key Performance Indicators (KPIs)

| KPI | Formula | Business Insight |
|-----|---------|------------------|
| **Cycle Time Efficiency** | TCT/CT | Work time vs. total time ratio |
| **WIP** | λ × CT | Average active applications (Little's Law) |
| **Resource Utilization** | λ/(μ×c) | Staffing efficiency |
| **Cost of Waste** | Rework Hours × Hourly Rate | Financial loss from errors |

## 🎓 Professor's Tips

> **Sweet Spot**: Resource utilization near 100% = unstable queues. Find the balance between efficiency and reliability!

## 📝 License

MIT License