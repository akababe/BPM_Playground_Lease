"""
Resource definitions for staff and equipment
"""
import simpy
from typing import Dict


class ProcessResources:
    """Container for all simulation resources"""
    
    def __init__(self, env: simpy.Environment, config):
        self.env = env
        self.config = config
        
        # Staff resources
        self.sales_staff = simpy.Resource(env, capacity=config.NUM_SALES_STAFF)
        self.risk_staff = simpy.Resource(env, capacity=config.NUM_RISK_STAFF)
        
        # Utilization tracking
        self.sales_busy_time = 0
        self.risk_busy_time = 0
        
        # Counters
        self.sales_requests = 0
        self.risk_requests = 0
    
    def get_utilization(self) -> Dict[str, float]:
        """Calculate resource utilization percentages"""
        current_time = self.env.now
        
        return {
            'sales_utilization': (self.sales_busy_time / 
                                 (current_time * self.config.NUM_SALES_STAFF)) if current_time > 0 else 0,
            'risk_utilization': (self.risk_busy_time / 
                                (current_time * self.config.NUM_RISK_STAFF)) if current_time > 0 else 0,
        }