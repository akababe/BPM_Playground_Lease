"""
As-Is Scenario: Lock-and-Cancel Process

When a typo is discovered, the application is locked/cancelled
and a new 'ghost' application is created, wasting resources.
"""
import random
from models.process_simulation import LeaseProcessSimulation
from models.lease_application import LeaseApplication
from config.parameters import AsIsConfig


class AsIsScenario(LeaseProcessSimulation):
    """Current process with Lock-and-Cancel for typos"""
    
    def __init__(self):
        super().__init__(AsIsConfig(), scenario_name="As-Is (Lock-and-Cancel)")
    
    def process_application(self, app: LeaseApplication):
        """Process flow with cancel-and-recreate logic"""
        # Stage 1: Sales Input
        yield self.env.process(self.sales_input_stage(app))
        
        # Check for typo after sales input
        if app.has_typo:
            # Lock and cancel - this app becomes a ghost
            app.is_ghost_application = True
            app.was_cancelled = True
            
            # Cancel overhead time
            cancel_time = max(0.1, random.normalvariate(
                self.config.CANCEL_TIME_MEAN,
                self.config.CANCEL_TIME_STD
            ))
            yield self.env.timeout(cancel_time)
            
            # Add cancel cost
            app.total_cost += (cancel_time / 60) * self.config.SALES_HOURLY_RATE
            
            # Complete this ghost app (goes nowhere)
            app.disbursement_end = self.env.now
            self.metrics.add_application(app)
            
            # Create NEW application (rework)
            self.app_counter += 1
            new_app = LeaseApplication(
                app_id=self.app_counter,
                arrival_time=self.env.now,
                has_typo=False  # Corrected version
            )
            
            # Process the corrected version from the beginning
            yield self.env.process(self.sales_input_stage(new_app))
            yield self.env.process(self.credit_risk_stage(new_app))
            yield self.env.process(self.disbursement_stage(new_app))
        else:
            # No typo - normal flow
            yield self.env.process(self.credit_risk_stage(app))
            yield self.env.process(self.disbursement_stage(app))
