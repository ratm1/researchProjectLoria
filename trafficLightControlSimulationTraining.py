import numpy as np
from sample import Sample
import random
from trafficLightControl import TrafficLightControl


class TrafficLightControlSimulation(TrafficLightControl):
    def __init__(self, Configuration, ModelTrain, Memory, TrafficGenerator):
        super().__init__(Configuration, TrafficGenerator)
        self.ModelTrain = ModelTrain
        self.Memory = Memory

        self.gamma_ = self.Configuration.getGamma()

        self.statesInput = Configuration.getStatesInput()
        self.epochsTraining = Configuration.getEpochsTraining()
        self.rewards = []
        self.cumulativeWaitingTime = []
        self.stepActionStateInformation = []

    def getModel(self):
        return self.ModelTrain

    def getMemory(self):
        return self.Memory

    def run(self, episode, epsilon):
        # DONE
        sumoConfiguration = self.getSumoConfiguration(self.Configuration.getPathSumoConfiguration(),
                                                      self.Configuration.getSumoGui(),
                                                      self.Configuration.getMaximumSteps())
        # TO DO
        self.setRouteFileSimulation(episode)
        """
        # Starting Traci simulation
        # """
        print("Starting traci simulation ")
        # # DONE
        self.setTraciStart(sumoConfiguration)
        # # DONE
        self.setInitialParametersEpisode()

        # # DONE
        while self.getStep() < self.getMaximumSteps():
            print("Beginning while ")
            # DONE #
            currentState = self.getStateInformation(self.Configuration.getStatesInput())
            print("The current state now  is: .....")
            print(currentState)

            currentTotalWaitingTime = self.getCollectiveWaitingTime()

            # DONE
            reward = self.getPreviousTotalWaitingTime() - currentTotalWaitingTime
            # DONE
            # Conditional for correct actions #
            if self.getStep() != 0:
                Sample_ = Sample(self.getPreviousState(), self.getPreviousAction(), reward, currentState)
                self.Memory.setSample(Sample_)

            currentAction = self.getAction(currentState, epsilon)

            self.saveInfoPerStateTraining(episode, self.getStep(), currentAction, reward, currentState)

            # DONE
            if self.getStep() != 0 and self.getPreviousAction() != currentAction:
                # DONE
                self.setYellowPhase(self.getPreviousAction())
                # DONE
                self.setStepsSimulation(self.yellowLightDuration)

            # DONE
            self.setGreenPhase(currentAction)
            self.setStepsSimulation(self.greenLightDuration)

            self.previousState = currentState
            self.previousAction = currentAction
            self.previousTotalWaitingTime = currentTotalWaitingTime
            # DONE
            self.setSumNegativeRewards(reward)

            print("End while")
        self.saveInformationPerEpisode()
        """
        Ending Traci Simulation
        """
        print("Closing traci simulation ")
        self.setCloseTraci()
        """
        Training neural networks model
        """
        self.setTraining(self.epochsTraining)

    def getStateInformation(self, stateInput):
        if stateInput == 4:
            return self.getStateLengthQueue()
        elif stateInput == 80:
            return self.getState()


    def saveInfoPerStateTraining(self, episode, step, currentAction, reward, currentState):
        self.informationPerEpisodeStepActionReward = []
        self.informationPerEpisodeStepActionReward.append(episode)
        self.informationPerEpisodeStepActionReward.append(step)
        self.informationPerEpisodeStepActionReward.append(currentAction)
        self.informationPerEpisodeStepActionReward.append(reward)
        self.informationStateEpisode.append(
            self.addCurrentState(self.informationPerEpisodeStepActionReward, currentState))

    def addCurrentState(self, informationPerEpisodeStepActionReward, currentState):
        self.informationWithElementsState = []
        self.informationWithElementsState.append(informationPerEpisodeStepActionReward[0])
        self.informationWithElementsState.append(informationPerEpisodeStepActionReward[1])
        self.informationWithElementsState.append(informationPerEpisodeStepActionReward[2])
        self.informationWithElementsState.append(informationPerEpisodeStepActionReward[3])

        for stateElements in currentState:
            self.informationWithElementsState.append(stateElements)

        return self.informationWithElementsState

    def setTraining(self, epochs):
        print("Start training with " + str(epochs))
        for epoch in range(epochs):
            self.replayTraining()

        print("Finish training with " + str(epochs))

    #  DONE
    def setSumNegativeRewards(self, reward):
        if reward < 0:
            self.sumNegativeRewards += reward

    # DONE
    def setInitialParametersEpisode(self):
        self.step_ = 0
        self.sumNegativeRewards = 0
        self.sumWaitingTime = 0
        self.waitingTimes = {}

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
    def getWaitingTimes(self):
        return self.waitingTimes

    # DONE
    def getSumNegativeRewards(self):
        return self.sumNegativeRewards

    # DONE
    def getSumWaitingTime(self):
        return self.sumWaitingTime

    # DONE
    def getTraciStart(self):
        return self.startTraci

    # TO DO
    def getAction(self, state, epsilon):
        if random.random() < epsilon:
            return random.randint(0, self.getActionsOutput() - 1)
        else:
            return self.ModelTrain.getMaximumActions(self.ModelTrain.getPredictionOneState(state))

    def getStateLengthQueue(self):
        state = np.zeros(self.statesInput)
        state[0] = self.getNumberOfVehiclesWithoutMovement("north_edge_one")
        state[1] = self.getNumberOfVehiclesWithoutMovement("east_edge_one")
        state[2] = self.getNumberOfVehiclesWithoutMovement("south_edge_one")
        state[3] = self.getNumberOfVehiclesWithoutMovement("west_edge_one")

        return state

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
            e.g. 35.0, 0.0, 51.0, waitingTimes: {'N_S_3': 0.0, 'E_W_11': 28.0, 'W_E_13': 11.0, 'W_S_14': 0.0}
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
            e.g. waitingTimes: {'E_N_7': 0.0, 'E_W_1': 0.0, 'E_W_10': 0.0, 'E_W_15': 0.0, 'E_W_4': 0.0}
            """
            #  print("***************** Waiting times dictionary ******************")
            waitingTimesDictionary = self.getWaitingTimesDictionary(self.waitingTimes, roadsWithTrafficLights,
                                                                    vehicleIdentification, waitingTime,
                                                                    roadIdentification)

        totalWaitingTime = self.getTotalWaitingTime(waitingTimesDictionary.values())

        return totalWaitingTime

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
    def replayTraining(self):
        # Array of samples
        batch = self.Memory.getSamples(self.ModelTrain.getBatchSize())

        if len(batch) > 0:
            print(" Batch ....")
            print(batch)
            #   Find state from the samples
            states = self.getStatesFromSamplesInBatch(batch)
            print(" States ...")
            print(states)
            nextStates = self.getNewStatesFromSamplesInBatch(batch)
            print("Next states ...")
            print(nextStates)

            q = self.ModelTrain.getPredictionBatch(states)
            qPrime = self.ModelTrain.getPredictionBatch(nextStates)

            # Initialize
            states = np.zeros((len(batch), self.statesInput))
            qTarget = np.zeros((len(batch), self.getActionsOutput()))
            # In the batch, there are different samples
            for position, sample in enumerate(batch):
                state = sample.getPreviousState()
                action = sample.getPreviousAction()
                reward = sample.getReward()
                currentQ = q[position]  # array: [0.8 0.3]
                currentQ[action] = reward + self.gamma_ * np.amax(qPrime[position])
                states[position] = state
                qTarget[position] = currentQ

            self.ModelTrain.getTrainBatch(states, qTarget)

    def getStatesFromSamplesInBatch(self, batch):
        statesFromSamplesInBatch = []
        for sample in batch:
            statesFromSamplesInBatch.append(sample.getPreviousState())

        return np.array(statesFromSamplesInBatch)

    def getNewStatesFromSamplesInBatch(self, batch):
        newStatesFromSampleInBatch = []
        for sample in batch:
            newStatesFromSampleInBatch.append(sample.getCurrentState())

        return np.array(newStatesFromSampleInBatch)

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
