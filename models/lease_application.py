"""
Data model for a lease application flowing through the system
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class LeaseApplication:
    """Represents a single lease application in the simulation"""
    
    app_id: int
    arrival_time: float
    
    # Timestamps for each stage
    sales_input_start: Optional[float] = None
    sales_input_end: Optional[float] = None
    
    credit_risk_start: Optional[float] = None
    credit_risk_end: Optional[float] = None
    
    disbursement_start: Optional[float] = None
    disbursement_end: Optional[float] = None
    
    # Quality flags
    has_typo: bool = False
    is_ghost_application: bool = False
    was_edited: bool = False
    was_cancelled: bool = False
    
    # Calculated metrics
    total_cycle_time: Optional[float] = None
    total_value_add_time: Optional[float] = None
    total_wait_time: Optional[float] = None
    
    # Cost tracking
    total_cost: float = 0.0
    
    def calculate_metrics(self):
        """Calculate derived metrics after completion"""
        if self.disbursement_end is None:
            return
        
        # Cycle Time (total time in system)
        self.total_cycle_time = self.disbursement_end - self.arrival_time
        
        # Value-Add Time (actual processing time)
        sales_time = (self.sales_input_end or 0) - (self.sales_input_start or 0)
        risk_time = (self.credit_risk_end or 0) - (self.credit_risk_start or 0)
        disb_time = (self.disbursement_end or 0) - (self.disbursement_start or 0)
        
        self.total_value_add_time = sales_time + risk_time + disb_time
        
        # Wait Time (queuing time)
        self.total_wait_time = self.total_cycle_time - self.total_value_add_time
    
    def get_cycle_time_efficiency(self) -> float:
        """Calculate CTE = Value-Add Time / Cycle Time"""
        if self.total_cycle_time and self.total_cycle_time > 0:
            return self.total_value_add_time / self.total_cycle_time
        return 0.0
    
    def __repr__(self):
        status = "Ghost" if self.is_ghost_application else "Normal"
        typo = "✗Typo" if self.has_typo else "✓Clean"
        return f"App#{{self.app_id}} [{{status}}, {{typo}}] CT={{self.total_cycle_time:.1f}}min"


@dataclass
class SimulationMetrics:
    """Container for aggregate simulation results"""
    
    completed_applications: list[LeaseApplication] = field(default_factory=list)
    simulation_time: float = 0.0
    
    # Resource utilization tracking
    sales_busy_time: float = 0.0
    risk_busy_time: float = 0.0
    
    def add_application(self, app: LeaseApplication):
        """Add completed application to results"""
        app.calculate_metrics()
        self.completed_applications.append(app)
    
    def get_summary(self) -> dict:
        """Generate summary statistics"""
        if not self.completed_applications:
            return {}
        
        cycle_times = [app.total_cycle_time for app in self.completed_applications 
                       if app.total_cycle_time]
        
        wait_times = [app.total_wait_time for app in self.completed_applications 
                      if app.total_wait_time]
        
        cte_values = [app.get_cycle_time_efficiency() 
                      for app in self.completed_applications]
        
        ghost_count = sum(1 for app in self.completed_applications 
                         if app.is_ghost_application)
        
        typo_count = sum(1 for app in self.completed_applications 
                        if app.has_typo)
        
        total_cost = sum(app.total_cost for app in self.completed_applications)
        
        return {
            'total_applications': len(self.completed_applications),
            'avg_cycle_time': sum(cycle_times) / len(cycle_times) if cycle_times else 0,
            'max_cycle_time': max(cycle_times) if cycle_times else 0,
            'avg_wait_time': sum(wait_times) / len(wait_times) if wait_times else 0,
            'avg_cte': sum(cte_values) / len(cte_values) if cte_values else 0,
            'ghost_applications': ghost_count,
            'applications_with_typos': typo_count,
            'total_cost': total_cost,
            'cost_per_application': total_cost / len(self.completed_applications),
        }