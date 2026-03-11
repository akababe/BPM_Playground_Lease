"""
Core simulation engine using SimPy
"""
import simpy
import random
import numpy as np
from typing import List
from models.lease_application import LeaseApplication, SimulationMetrics
from models.resources import ProcessResources


class LeaseProcessSimulation:
    """Base class for lease process simulation"""
    
    def __init__(self, config, scenario_name="Base"):
        self.config = config
        self.scenario_name = scenario_name
        self.env = simpy.Environment()
        self.resources = ProcessResources(self.env, config)
        self.metrics = SimulationMetrics()
        
        # Application counter
        self.app_counter = 0
        
        # Set random seed for reproducibility
        random.seed(config.RANDOM_SEED)
        np.random.seed(config.RANDOM_SEED)
    
    def generate_arrivals(self):
        """Generate incoming lease applications"""
        while True:
            # Generate inter-arrival time
            inter_arrival = random.expovariate(1.0 / self.config.MEAN_INTER_ARRIVAL_TIME)
            yield self.env.timeout(inter_arrival)
            
            # Create new application
            self.app_counter += 1
            app = LeaseApplication(
                app_id=self.app_counter,
                arrival_time=self.env.now,
                has_typo=(random.random() < self.config.TYPO_PROBABILITY)
            )
            
            # Start processing
            self.env.process(self.process_application(app))
    
    def process_application(self, app: LeaseApplication):
        """
        Main process flow - to be overridden by scenario-specific logic
        """
        raise NotImplementedError("Subclasses must implement process_application")
    
    def sales_input_stage(self, app: LeaseApplication):
        """Stage 1: Sales Input (OI)"""
        app.sales_input_start = self.env.now
        
        with self.resources.sales_staff.request() as request:
            yield request
            
            # Service time
            service_time = max(0.1, random.normalvariate(
                self.config.SALES_INPUT_TIME_MEAN,
                self.config.SALES_INPUT_TIME_STD
            ))
            
            # Track utilization
            start_work = self.env.now
            yield self.env.timeout(service_time)
            self.resources.sales_busy_time += (self.env.now - start_work)
            
            # Calculate cost
            app.total_cost += (service_time / 60) * self.config.SALES_HOURLY_RATE
        
        app.sales_input_end = self.env.now
    
    def credit_risk_stage(self, app: LeaseApplication):
        """Stage 2: Credit Risk Assessment"""
        app.credit_risk_start = self.env.now
        
        with self.resources.risk_staff.request() as request:
            yield request
            
            # Service time
            service_time = max(0.1, random.normalvariate(
                self.config.CREDIT_RISK_TIME_MEAN,
                self.config.CREDIT_RISK_TIME_STD
            ))
            
            # Track utilization
            start_work = self.env.now
            yield self.env.timeout(service_time)
            self.resources.risk_busy_time += (self.env.now - start_work)
            
            # Calculate cost
            app.total_cost += (service_time / 60) * self.config.RISK_HOURLY_RATE
        
        app.credit_risk_end = self.env.now
    
    def disbursement_stage(self, app: LeaseApplication):
        """Stage 3: Disbursement (PPD)"""
        app.disbursement_start = self.env.now
        
        with self.resources.sales_staff.request() as request:
            yield request
            
            # Service time
            service_time = max(0.1, random.normalvariate(
                self.config.DISBURSEMENT_TIME_MEAN,
                self.config.DISBURSEMENT_TIME_STD
            ))
            
            # Track utilization
            start_work = self.env.now
            yield self.env.timeout(service_time)
            self.resources.sales_busy_time += (self.env.now - start_work)
            
            # Calculate cost
            app.total_cost += (service_time / 60) * self.config.SALES_HOURLY_RATE
        
        app.disbursement_end = self.env.now
        
        # Mark as complete
        self.metrics.add_application(app)
    
    def run(self, until=None):
        """Execute the simulation"""
        if until is None:
            until = self.config.SIM_TIME
        
        # Start the arrival process
        self.env.process(self.generate_arrivals())
        
        # Run simulation
        self.env.run(until=until)
        
        # Store final utilization
        self.metrics.sales_busy_time = self.resources.sales_busy_time
        self.metrics.risk_busy_time = self.resources.risk_busy_time
        self.metrics.simulation_time = self.env.now
        
        return self.metrics