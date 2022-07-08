import sys

import traci
import random
import os
from sumolib import checkBinary
from trafficLightControl import TrafficLightControl

"""
Traffic simulation without reinforcement learning
"""
NORTH_SOUTH_REVERSE_GREEN_PHASE = 0
EAST_WEST_REVERSE_GREEN_PHASE = 2


class TrafficLightControlSimulation(TrafficLightControl):
    def __init__(self, Configuration, TrafficGenerator):
        super().__init__(Configuration, TrafficGenerator)

    """
    Run the traffic light simulation
    """

    def run(self, episode):
        # DONE
        sumoConfiguration = self.getSumoConfiguration(self.Configuration.getPathSumoConfiguration(),
                                                      self.Configuration.getSumoGui(),
                                                      self.Configuration.getMaximumSteps())
        # TO DO
        self.setRouteFileSimulation(episode)
        """
        Starting Traci simulation
        """
        print("Starting traci simulation ")
        # DONE
        self.setTraciStart(sumoConfiguration)

        # DONE
        self.setInitialParametersEpisode()

        # DONE
        while self.getStep() < self.getMaximumSteps():
            print("Beginning while ")

            # TO DO
            currentAction = self.getAction(self.getStep())

            self.saveInfoPerState(episode, self.getStep(), currentAction)

            # DONE
            if self.getStep() != 0 and self.getPreviousAction() != currentAction:
                # DONE
                self.setYellowPhase(self.getPreviousAction())
                # DONE
                self.setStepsSimulation(self.yellowLightDuration)

            # DONE
            self.setGreenPhase(currentAction)
            # TO DO PARTIALLY
            self.setStepsSimulation(self.greenLightDuration)

            self.previousAction = currentAction

            print("End while")
        # DONE
        self.saveInformationPerEpisode()

        """
        Ending Traci Simulation
        """
        print("Closing traci simulation ")
        # DONE
        self.setCloseTraci()
