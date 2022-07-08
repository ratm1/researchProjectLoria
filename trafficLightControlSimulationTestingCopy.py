import sys
import traci
import numpy as np
import os
from sumolib import checkBinary

NORTH_SOUTH_REVERSE_GREEN_PHASE = 0
EAST_WEST_REVERSE_GREEN_PHASE = 2

"""
Traffic simulation with reinforcement learning while training with Q-learning
"""


class TrafficLightControlSimulation:
    def __init__(self, Configuration, ModelTest, TrafficGenerator):
        self.ModelTest = ModelTest
        self.Configuration = Configuration
        self.TrafficGenerator = TrafficGenerator
        self.traci = traci

        self.startTraci = False
        self.step_ = 0
        self.maximumSteps = Configuration.getMaximumSteps()
        self.greenLightDuration = Configuration.getGreenLightDuration()
        self.yellowLightDuration = Configuration.getYellowLightDuration()

        self.statesInput = Configuration.getStatesInput()
        self.actionsOutput = Configuration.getActionsOutput()

        self.rewards = []
        self.cumulativeWaitingTime = []
        self.stepActionStateInformation = []

    def getModel(self):
        return self.ModelTest

    def getConfiguration(self):
        return self.Configuration

    def getTrafficGenerator(self):
        return self.TrafficGenerator

    # DONE #
    def getSumoConfiguration(self, pathSumoConfiguration, sumoGui, maximumSteps):
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
                             "true", "--waiting-time-memory", str(maximumSteps)]

        return sumoConfiguration

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
            # DONE #
            currentState = self.getStateInformation(self.Configuration.getStatesInput())

            print("The current state now  is: .....")
            print(currentState)

            currentTotalWaitingTime = self.getCollectiveWaitingTime()
            print("******* Current total waiting time *************")
            print(currentTotalWaitingTime)

            # TO DO
            currentAction = self.getAction(currentState)

            self.saveInfoPerState(episode, self.getStep(), currentAction, currentState)

            # DONE
            if self.getStep() != 0 and self.getPreviousAction() != currentAction:
                # DONE
                self.setYellowPhase(self.getPreviousAction())
                # DONE
                self.setStepsSimulation(self.yellowLightDuration)

            # DONE
            self.setGreenPhase(currentAction)
            self.setStepsSimulation(self.greenLightDuration)

            self.previousAction = currentAction
            self.previousTotalWaitingTime = currentTotalWaitingTime

            print("End while")
        # DONE
        self.saveInformationPerEpisode()

        """
        Ending Traci Simulation
        """

        print("Closing traci simulation ")
        # DONE
        self.setCloseTraci()

    def getStateInformation(self, stateInput):
        if stateInput == 4:
            return self.getStateLengthQueue()
        elif stateInput == 80:
            return self.getState()

    def saveInfoPerState(self, episode, step, currentAction, currentState):
        self.informationPerEpisodeStepActionReward = []
        self.informationPerEpisodeStepActionReward.append(episode)
        self.informationPerEpisodeStepActionReward.append(step)
        self.informationPerEpisodeStepActionReward.append(currentAction)
        self.informationStateEpisode.append(
            self.addCurrentState(self.informationPerEpisodeStepActionReward, currentState))

    def addCurrentState(self, informationPerEpisodeStepActionReward, currentState):
        self.informationWithElementsState = []
        self.informationWithElementsState.append(informationPerEpisodeStepActionReward[0])
        self.informationWithElementsState.append(informationPerEpisodeStepActionReward[1])
        self.informationWithElementsState.append(informationPerEpisodeStepActionReward[2])

        for stateElements in currentState:
            self.informationWithElementsState.append(stateElements)

        return self.informationWithElementsState

    #  DONE
    def setSumNegativeRewards(self, reward):
        if reward < 0:
            self.sumNegativeRewards += reward

    # DONE
    def setSumWaitingTime(self, lengthQueue):
        self.sumWaitingTime += lengthQueue

    # DONE
    def setCloseTraci(self):
        self.getTraci().close()
        self.startTraci = False

    # DONE
    def setInitialParametersEpisode(self):
        self.step_ = 0
        self.waitingTimes = {}
        self.sumNegativeRewards = 0
        self.sumWaitingTime = 0

        self.informationStateEpisode = []
        self.previousTotalWaitingTime = 0
        self.previousState = -1
        self.previousAction = -1

    # DONE
    def getPreviousTotalWaitingTime(self):
        return self.previousTotalWaitingTime

    # DONE
    def getPreviousState(self):
        return self.previousState

    # DONE
    def getPreviousAction(self):
        return self.previousAction

    # DONE
    def getWaitingTimes(self):
        return self.waitingTimes

    # DONE
    def getSumNegativeRewards(self):
        return self.sumNegativeRewards

    # DONE
    def getSumWaitingTime(self):
        return self.sumWaitingTime

    # DONE

    def getTraci(self):
        return self.traci

    # DONE
    def setTraciStart(self, sumoConfiguration):
        self.getTraci().start(sumoConfiguration)
        self.startTraci = True

    # DONE
    def getTraciStart(self):
        return self.startTraci

    # TO DO
    def setRouteFileSimulation(self, episode):
        self.TrafficGenerator.setRouteFileSimulation(episode)

    # DONE  #
    def setStepsSimulation(self, stepsLightDuration):
        totalStepsSimulation = self.getTotalStepsSimulationGivenMaximumSteps(self.getStep(), stepsLightDuration,
                                                                             self.getMaximumSteps())
        # DONE
        while totalStepsSimulation > 0:
            self.setTraciSimulationStep()
            self.setStepPerEpisode(1)
            totalStepsSimulation -= 1
            self.setSumWaitingTime(self.getLengthQueue())

    # DONE
    def setTraciSimulationStep(self):
        self.getTraci().simulationStep()

    # DONE
    def setStepPerEpisode(self, value):
        self.step_ += value

    # DONE
    def getTotalStepsSimulationGivenMaximumSteps(self, steps, stepsLightDuration, maximumSteps):
        totalStepsSimulation = steps + stepsLightDuration

        if totalStepsSimulation >= maximumSteps:
            totalStepsSimulation = self.getTotalStepsSimulationWhenHigherThanMaximumSteps(maximumSteps, steps)
        else:
            totalStepsSimulation = stepsLightDuration

        return totalStepsSimulation

    #  DONE
    def getTotalStepsSimulationWhenHigherThanMaximumSteps(self, maximumSteps, step):
        totalStepsSimulation = maximumSteps - step
        return totalStepsSimulation

    # DONE
    def getLengthQueue(self):
        """
        Returns the total number of halting vehicles for the last time step on the given edge.
        A speed of less than 0.1 m/s is considered a halt. Number of vehicles without movement in a respective edge.
        """

        queueNorth = self.getNumberOfVehiclesWithoutMovement("north_edge_one")

        queueSouth = self.getNumberOfVehiclesWithoutMovement("east_edge_one")

        queueEast = self.getNumberOfVehiclesWithoutMovement("south_edge_one")

        queueWest = self.getNumberOfVehiclesWithoutMovement("west_edge_one")

        totalQueue = self.getTotalNumberOfVehiclesWithoutMovement(queueNorth, queueSouth, queueEast, queueWest)

        return totalQueue

    # DONE
    def getTotalNumberOfVehiclesWithoutMovement(self, queueNorth, queueSouth, queueEast, queueWest):
        totalQueue = queueNorth + queueSouth + queueEast + queueWest
        return totalQueue

    # DONE
    def getNumberOfVehiclesWithoutMovement(self, edge):
        queue = self.getTraci().edge.getLastStepHaltingNumber(edge)
        return queue

    # TO DO # CHECK THIS ****
    def getAction(self, state):
        return self.ModelTest.getMaximumActions(self.ModelTest.getPredictionOneState(state))

    # DONE #
    """
    Set up the yellow color in the traffic light according to the .net.xml file
    """

    def setYellowPhase(self, previousAction):
        yellowPhasePositionTrafficLightId = previousAction + 1
        self.setPhaseLightId(yellowPhasePositionTrafficLightId)

    # DONE #
    """
    Set up the green color in the traffic light according to the .net.xml file
    """

    def setGreenPhase(self, action):
        """
        Switches to the phase with the given index in the list of all phases for the current program.
        """
        if action == 0:
            self.setPhaseLightId(NORTH_SOUTH_REVERSE_GREEN_PHASE)
        elif action == 1:
            self.setPhaseLightId(EAST_WEST_REVERSE_GREEN_PHASE)

    """
    Set up movement traffic light ID phase
    """

    def setPhaseLightId(self, directionTrafficLightHeaderId):
        """
        setPhase(self, tlsID, index)
        """
        self.getTraci().trafficlight.setPhase("junction_center", directionTrafficLightHeaderId)

    def getStateLengthQueue(self):
        state = np.zeros(self.statesInput)
        state[0] = self.getNumberOfVehiclesWithoutMovement("north_edge_one")
        state[1] = self.getNumberOfVehiclesWithoutMovement("east_edge_one")
        state[2] = self.getNumberOfVehiclesWithoutMovement("south_edge_one")
        state[3] = self.getNumberOfVehiclesWithoutMovement("west_edge_one")

        return state

    # TBD
    """
    Returns the current phase in the current program
    """

    def getCurrentPhase(self):
        print("The current phase is .....")
        print(self.getTraci().trafficlight.getPhase("junction_center"))
        return self.getTraci().trafficlight.getPhase("junction_center")

    # DONE #
    def getActionsOutput(self):
        return self.actionsOutput

    # DONE #
    def getStep(self):
        return self.step_

    # DONE #
    def getMaximumSteps(self):
        return self.maximumSteps

    # DONE #
    def getState(self):
        state = np.zeros(self.statesInput)
        """
        Returns a list of all objects in the network. e.g. ('E_W_11', 'N_S_12', 'W_E_10')
        """
        vehicleList = self.getVehiclesIdList()

        for vehicleIdentification in vehicleList:
            print("The vehicle identification ....")
            print(vehicleIdentification)
            """
            The position of the vehicle along the lane measured in m. e.g. 70.71
            """
            print("The position of the lane ....")
            positionLane = self.getLanePosition(vehicleIdentification)
            print(positionLane)
            """
            Returns the id if the lane the named vehicle was at within the last step. e.g. west_edge_one_1
            """
            identificationLane = self.getLaneId(vehicleIdentification)

            positionLane = 100 - positionLane
            """
            Returns the cell from the lane from 0 to 9
            """
            cellLane = self.getCellLane(positionLane)
            """
            Returns the lane identification in a clockwise manner from west to south
            """
            groupLane = self.getGroupLane(identificationLane)
            """
            Returns an array with the car's position and validity
            """
            positionValidCar = self.getPositionAndValidityCar(groupLane, cellLane)
            "Returns state with valid cars"
            state = self.getStateWithValidCars(state, positionValidCar)

        return state

    # DONE
    def getStateWithValidCars(self, state, positionValidCar):
        if positionValidCar[1]:
            state[positionValidCar[0]] = 1
        return state

    # DONE
    def getPositionAndValidityCar(self, groupLane, cellLane):
        positionValidCar = [0, False]
        if 1 <= groupLane <= 7:
            positionValidCar[0] = int(str(groupLane) + str(cellLane))
            positionValidCar[1] = True
        elif groupLane == 0:
            positionValidCar[0] = cellLane
            positionValidCar[1] = True
        else:
            positionValidCar[1] = False

        return positionValidCar

    # DONE
    def getGroupLane(self, identificationLane):
        if identificationLane == "west_edge_one_0":
            groupLane = 0
        elif identificationLane == "west_edge_one_1":
            groupLane = 1
        elif identificationLane == "north_edge_one_0":
            groupLane = 2
        elif identificationLane == "north_edge_one_1":
            groupLane = 3
        elif identificationLane == "east_edge_one_0":
            groupLane = 4
        elif identificationLane == "east_edge_one_1":
            groupLane = 5
        elif identificationLane == "south_edge_one_0":
            groupLane = 6
        elif identificationLane == "south_edge_one_1":
            groupLane = 7
        else:
            groupLane = -1

        return groupLane

    # DONE
    def getCellLane(self, positionLane):
        if positionLane < 10:
            cellLane = 0
        elif positionLane < 20:
            cellLane = 1
        elif positionLane < 30:
            cellLane = 2
        elif positionLane < 40:
            cellLane = 3
        elif positionLane < 50:
            cellLane = 4
        elif positionLane < 60:
            cellLane = 5
        elif positionLane < 70:
            cellLane = 6
        elif positionLane < 80:
            cellLane = 7
        elif positionLane < 90:
            cellLane = 8
        elif positionLane <= 100:
            cellLane = 9
        return cellLane

    # DONE
    def getLaneId(self, vehicleIdentification):
        identificationLane = self.getTraci().vehicle.getLaneID(vehicleIdentification)
        return identificationLane

    # DONE
    def getLanePosition(self, vehicleIdentification):
        positionLane = self.getTraci().vehicle.getLanePosition(vehicleIdentification)
        return positionLane

    # DONE
    def getVehiclesIdList(self):
        vehicleList = self.getTraci().vehicle.getIDList()
        return vehicleList

    # TO DO #
    def getCollectiveWaitingTime(self):
        waitingTimesDictionary = {}
        roadsWithTrafficLights = ["west_edge_one", "north_edge_one", "east_edge_one", "south_edge_one"]
        """
        Returns a list of all objects in the network. e.g. ('E_W_11', 'N_S_12', 'W_E_10')
        """
        vehicleList = self.getVehiclesIdList()
        # print("********* Vehicle list *****************")
        # print(vehicleList)
        for vehicleIdentification in vehicleList:
            # print("************** Vehicle identification ****************")
            # print(vehicleIdentification)
            """
            Returns the accumulated waiting time of a vehicle collects the vehicle's waiting time
            over a certain time interval (interval length is set per option '--waiting-time-memory')
            e.g. 35.0, 0.0, 51.0, waitingTimes: {'N_S_3': 0.0, 'E_W_11': 28.0, 'W_E_13': 11.0}
            """
            waitingTime = self.getAccumulatedTimePerVehicleIdentification(vehicleIdentification)
            # print("************* Waiting time ****************************")
            # print(waitingTime)
            """
            Returns the id of the edge the named vehicle was at within the last step.
            e.g. west_edge_two, east_edge_two
            """
            #   print("**************** Road identification ************************")
            roadIdentification = self.getRoadIdPerVehicleIdentification(vehicleIdentification)
            #  print(roadIdentification)
            """
            e.g. waitingTimes: {'E_W_1': 0.0, 'E_W_10': 0.0, 'E_W_15': 0.0, 'E_W_4': 0.0}
            """
            #  print("***************** Waiting times dictionary ******************")
            waitingTimesDictionary = self.getWaitingTimesDictionary(self.waitingTimes, roadsWithTrafficLights,
                                                                    vehicleIdentification, waitingTime,
                                                                    roadIdentification)

        totalWaitingTime = self.getTotalWaitingTime(waitingTimesDictionary.values())

        return totalWaitingTime

    # DONE
    def getTotalWaitingTime(self, values):
        return sum(values)

    # TO DO
    def getWaitingTimesDictionary(self, waitingTimes, roadsWithTrafficLights, vehicleIdentification, waitingTime,
                                  roadIdentification):
        """
        Recognize the road and delete repeated vehicles with identification
        """
        if roadIdentification in roadsWithTrafficLights:
            waitingTimes[vehicleIdentification] = waitingTime

        return waitingTimes

    # DONE
    def getRoadIdPerVehicleIdentification(self, vehicleIdentification):
        roadIdentification = self.getTraci().vehicle.getRoadID(vehicleIdentification)
        return roadIdentification

    # DONE
    def getAccumulatedTimePerVehicleIdentification(self, vehicleIdentication):
        waitingTime = self.getTraci().vehicle.getAccumulatedWaitingTime(vehicleIdentication)
        return waitingTime

    # DONE
    def saveInformationPerEpisode(self):
        print("Total cumulative reward ...... ")
        print(self.sumNegativeRewards)
        self.rewards.append(self.sumNegativeRewards)
        self.cumulativeWaitingTime.append(self.sumWaitingTime)
        self.stepActionStateInformation.append(self.informationStateEpisode)

    # DONE
    def getStepActionStateInformation(self):
        return self.stepActionStateInformation

    # DONE
    def getRewardsListTotalEpisodes(self):
        return self.rewards

    # DONE
    def getCumulativeWaitingTimeTotalEpisodes(self):
        return self.cumulativeWaitingTime
