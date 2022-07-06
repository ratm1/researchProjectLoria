import math

import numpy as np


class TrafficGenerator:
    def __init__(self, maximumSteps, carsGenerated):
        self.maximumSteps_ = maximumSteps
        self.carsGenerated_ = carsGenerated

    def setRouteFileSimulation(self, seed):
        np.random.seed(seed)
        """
        Set a weibull distribution according to the number of vehicles generated
        """
        carSteps = self.carsGenerated_
        with open("environment/episode_current_small_environment.rou.xml", "w") as movement:
            print("""<routes>
            <vType accel="1.0" decel="4.5" id="standard_car" length="5.0" minGap="2.5" maxSpeed="25" sigma="0.5" />

            <route id="W_E" edges= "west_edge_one east_edge_two"/>
            <route id="W_S" edges= "west_edge_one south_edge_two"/>

            <route id="N_W" edges= "north_edge_one west_edge_two"/>
            <route id="N_S" edges= "north_edge_one south_edge_two"/>

            <route id="E_N" edges= "east_edge_one north_edge_two"/>
            <route id="E_W" edges= "east_edge_one  west_edge_two"/>

            <route id="S_E" edges= "south_edge_one  east_edge_two "/>
            <route id="S_N" edges= "south_edge_one north_edge_two"/> """, file=movement)

            for counter in range(carSteps):
                """
                Samples are uniformly distributed over the half-open interval [low, high) (includes low, but excludes high)
                """
                carMovementDirectionStraight = np.random.uniform()

                if carMovementDirectionStraight < 0.20:
                    print(
                        '<vehicle id="W_E_%i" type="standard_car" route="W_E" depart="0" departLane="random" '
                        'departSpeed="10" />' % (
                            counter), file=movement)

                elif carMovementDirectionStraight < 0.45:
                    print(
                            '<vehicle id="E_W_%i" type="standard_car" route="E_W" depart="0" departLane="random" '
                            'departSpeed="10" />' % (
                                counter), file=movement)

                elif carMovementDirectionStraight < 0.70:
                    print(
                            '<vehicle id="N_S_%i" type="standard_car" route="N_S" depart="0" departLane="random" '
                            'departSpeed="10" />' % (
                                counter), file=movement)

                else:
                    print(
                            '<vehicle id="S_N_%i" type="standard_car" route="S_N" depart="0" departLane="random" '
                            'departSpeed="10" />' % (
                                counter), file=movement)

            print("</routes>", file=movement)
