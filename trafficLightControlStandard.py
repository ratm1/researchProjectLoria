import sys

import traci
import random
import os
from sumolib import checkBinary

"""
Traffic simulation without reinforcement learning
"""
NORTH_SOUTH_RIGHT_GREEN_PHASE = 0
NORTH_SOUTH_RIGHT_YELLOW_PHASE = 1

EAST_WEST_RIGHT_GREEN_PHASE = 2
EAST_WEST_RIGHT_YELLOW_PHASE = 3


class TrafficLightControlSimulation:
    def __init__(self, Configuration, TrafficGenerator):
        self.Configuration = Configuration
        self.TrafficGenerator = TrafficGenerator
        self.traci = traci
        self.startTraci = False
        self.step_ = 0
        self.maximumSteps = Configuration.getMaximumSteps()
        self.greenLightDuration = Configuration.getGreenLightDuration()
        self.yellowLightDuration = Configuration.getYellowLightDuration()

        self.actionsOutput = Configuration.getActionsOutput()
        self.cumulativeWaitingTime = []
        self.stepActionInformation = []
    """
    Returns configuration for the TrafficLightControlSimulation
    """
    def getConfiguration(self):
        return self.Configuration
    """
    Returns traffic generator for the TrafficLightControlSimulation
    """
    def getTrafficGenerator(self):
        return self.TrafficGenerator

    """
    Returns the sumo configuration for the TrafficLightControlSimulation
    """
    def getSumoConfiguration(self, pathSumoConfiguration, sumoGui, maximumNumberSteps):
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit(" It is necessary to be declared the variable 'SUMO_HOME'")

        if not sumoGui:
            binarySumo = checkBinary('sumo')
        else:
            binarySumo = checkBinary('sumo-gui')

        sumoConfiguration = [binarySumo, "-c", os.path.join('environment', pathSumoConfiguration), "--no-step-log",
                             "true", "--waiting-time-memory", str(maximumNumberSteps)]

        return sumoConfiguration

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

            self.saveInfoPerState(episode,self.getStep(), currentAction)

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

    # DONE HERE
    def setCloseTraci(self):
        self.getTraci().close()
        self.startTraci = False

    # DONE HERE
    def setInitialParametersEpisode(self):
        self.step_ = 0
        self.waitingTimes = {}
        self.sumWaitingTime = 0
        self.previousAction = -1
        self.informationStateEpisode = []

    # DONE HERE
    def getPreviousAction(self):
        return self.previousAction

    # DONE HERE
    def getTraci(self):
        return self.traci

    # DONE HERE
    def setTraciStart(self, sumoConfiguration):
        self.getTraci().start(sumoConfiguration)
        self.startTraci = True

    # TO DO HERE
    def setRouteFileSimulation(self, episode):
        self.TrafficGenerator.setRouteFileSimulation(episode)

    def saveInfoPerState(self,  episode,  step, currentAction):
        self.informationPerStateStep = []
        self.informationPerStateStep.append(episode)
        self.informationPerStateStep.append(step)
        self.informationPerStateStep.append(currentAction)
        self.informationStateEpisode.append(self.informationPerStateStep)

    # DONE  HERE #
    def setStepsSimulation(self, stepsLightDuration):
        totalStepsSimulation = self.getTotalStepsSimulationGivenMaximumSteps(self.getStep(), stepsLightDuration,
                                                                             self.getMaximumSteps())
        while totalStepsSimulation > 0:
            self.setTraciSimulationStep()
            self.setStepPerEpisode(1)
            totalStepsSimulation -= 1
            self.setSumWaitingTime(self.getLengthQueue())

    # DONE HERE
    def setSumWaitingTime(self, lengthQueue):
        self.sumWaitingTime += lengthQueue

    # DONE HERE
    def setTraciSimulationStep(self):
        self.getTraci().simulationStep()

    # DONE HERE
    def setStepPerEpisode(self, value):
        self.step_ += value

    # DONE HERE
    def getTotalStepsSimulationGivenMaximumSteps(self, steps, stepsLightDuration, maximumSteps):
        totalStepsSimulation = steps + stepsLightDuration

        if totalStepsSimulation >= maximumSteps:
            totalStepsSimulation = self.getTotalStepsSimulationWhenHigherThanMaximumSteps(maximumSteps, steps)
        else:
            totalStepsSimulation = stepsLightDuration

        return totalStepsSimulation

    #  DONE HERE
    def getTotalStepsSimulationWhenHigherThanMaximumSteps(self, maximumSteps, step):
        totalStepsSimulation = maximumSteps - step
        return totalStepsSimulation

    # DONE HERE
    def getLengthQueue(self):
        """
        Returns the total number of halting vehicles for the last time step on the given edge.
        A speed of less than 0.1 m/s is considered a halt. Number of vehicles without movement in a respective edge.
        """

        """
        Waiting time (number of vehicles) in the queue north
        """
        queueNorth = self.getNumberOfVehiclesWithoutMovement("north_edge_one")

        """
        Waiting time (number of vehicles) in the queue south
        """
        queueSouth = self.getNumberOfVehiclesWithoutMovement("east_edge_one")

        """
        Waiting time (number of vehicles) in the queue east
        """
        queueEast = self.getNumberOfVehiclesWithoutMovement("south_edge_one")

        """
        Waiting time (number of vehicles) in the queue west
        """
        queueWest = self.getNumberOfVehiclesWithoutMovement("west_edge_one")
        print("****** Queues ******* ")
        print(queueNorth)
        print(queueSouth)
        print(queueEast)
        print(queueWest)
        totalQueue = self.getTotalNumberOfVehiclesWithoutMovement(queueNorth, queueSouth, queueEast, queueWest)

        return totalQueue

    # DONE HERE
    def getTotalNumberOfVehiclesWithoutMovement(self, queueNorth, queueSouth, queueEast, queueWest):
        totalQueue = queueNorth + queueSouth + queueEast + queueWest
        return totalQueue

    # DONE HERE
    def getNumberOfVehiclesWithoutMovement(self, edge):
        queue = self.getTraci().edge.getLastStepHaltingNumber(edge)
        return queue

    # DONE HERE #
    def getAction(self, episode):
        """
        Returns a random integer N such that a <= N <= b.
        """
        return random.randint(0, self.getActionsOutput() - 1)

    # DONE HERE #
    """
    Set up the yellow color in the traffic light according to the .net.xml file
    """
    def setYellowPhase(self, previousAction):
        yellowPhasePositionTrafficLightId = previousAction + 1
        self.setPhaseLightId(yellowPhasePositionTrafficLightId)

    # DONE HERE #
    """
    Set up the green color in the traffic light according to the .net.xml file
    """

    def setGreenPhase(self, action):
        """
        Switches to the phase with the given index in the list of all phases for the current program.
        """
        if action == 0:
            self.setPhaseLightId(NORTH_SOUTH_RIGHT_GREEN_PHASE)
        elif action == 1:
            self.setPhaseLightId(EAST_WEST_RIGHT_GREEN_PHASE)

    """
    Set up movement traffic light ID phase
    """
    # TBD HERE
    def setPhaseLightId(self, directionTrafficLightHeaderId):
        """
        setPhase(self, tlsID, index)
        """
        self.getTraci().trafficlight.setPhase("junction_center", directionTrafficLightHeaderId)

    # DONE HERE #
    def getActionsOutput(self):
        return self.actionsOutput

    # DONE HERE #
    def getStep(self):
        return self.step_

    # DONE HERE #
    def getMaximumSteps(self):
        return self.maximumSteps

    # DONE
    def getTotalWaitingTime(self, values):
        return sum(values)

    # DONE
    def saveInformationPerEpisode(self):
        self.cumulativeWaitingTime.append(self.sumWaitingTime)
        self.stepActionInformation.append(self.informationStateEpisode)

    def getStepActionInformation(self):
        return self.stepActionInformation

    # DONE
    def getCumulativeWaitingTimeTotalEpisodes(self):
        return self.cumulativeWaitingTime
