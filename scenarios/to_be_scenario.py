"""
To-Be Scenario: Undo/Edit Process

When a typo is discovered, the application can be edited in-place,
avoiding ghost applications and resource waste.
"""
import random
from models.process_simulation import LeaseProcessSimulation
from models.lease_application import LeaseApplication
from config.parameters import ToBeConfig


class ToBeScenario(LeaseProcessSimulation):
    """Proposed process with Undo/Edit capability"""
    
    def __init__(self):
        super().__init__(ToBeConfig(), scenario_name="To-Be (Undo/Edit)")
    
    def process_application(self, app: LeaseApplication):
        """Process flow with undo/edit logic"""
        # Stage 1: Sales Input
        yield self.env.process(self.sales_input_stage(app))
        
        # Check for typo after sales input
        if app.has_typo:
            # UNDO and EDIT in-place (no ghost application)
            app.was_edited = True
            
            # Edit overhead time (much faster than cancel+recreate)
            edit_time = max(0.1, random.normalvariate(
                self.config.EDIT_TIME_MEAN,
                self.config.EDIT_TIME_STD
            ))
            yield self.env.timeout(edit_time)
            
            # Add edit cost (minimal)
            app.total_cost += (edit_time / 60) * self.config.SALES_HOURLY_RATE
            
            # Continue with corrected application (same app object)
            app.has_typo = False  # Fixed!
        
        # Normal flow continues (no rework needed)
        yield self.env.process(self.credit_risk_stage(app))
        yield self.env.process(self.disbursement_stage(app))
