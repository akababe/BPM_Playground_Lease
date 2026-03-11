"""
Simulation Configuration Parameters
Adjust these values to model different scenarios
"""

class SimulationConfig:
    """Base configuration for all simulations"""
    
    # Simulation Control
    RANDOM_SEED = 42
    SIM_TIME = 8 * 60  # 8 hours in minutes
    NUM_REPLICATIONS = 30  # For statistical significance
    
    # Arrival Process
    MEAN_INTER_ARRIVAL_TIME = 15  # minutes (λ = 4 applications/hour)
    ARRIVAL_DISTRIBUTION = "exponential"  # or "constant", "normal"
    
    # Resources (Staff)
    NUM_SALES_STAFF = 3
    NUM_RISK_STAFF = 2
    
    # Service Times (minutes)
    SALES_INPUT_TIME_MEAN = 10
    SALES_INPUT_TIME_STD = 2
    
    CREDIT_RISK_TIME_MEAN = 20
    CREDIT_RISK_TIME_STD = 5
    
    DISBURSEMENT_TIME_MEAN = 8
    DISBURSEMENT_TIME_STD = 1.5
    
    # Quality Parameters
    TYPO_PROBABILITY = 0.15  # 15% of applications have typos
    
    # Cost Parameters ($ per hour)
    SALES_HOURLY_RATE = 25
    RISK_HOURLY_RATE = 35
    
    # Process-Specific Settings
    GHOST_APP_OVERHEAD = 1.5  # Multiplier for rework effort


class AsIsConfig(SimulationConfig):
    """Configuration for current 'Lock-and-Cancel' process"""
    
    ALLOW_EDIT = False
    CANCEL_TIME_MEAN = 5  # Time to cancel and create new app
    CANCEL_TIME_STD = 1


class ToBeConfig(SimulationConfig):
    """Configuration for proposed 'Undo/Edit' process"""
    
    ALLOW_EDIT = True
    EDIT_TIME_MEAN = 3  # Time to undo and fix typo
    EDIT_TIME_STD = 0.5
    
    # Reduced typo impact
    GHOST_APP_OVERHEAD = 1.0  # No ghost applications
