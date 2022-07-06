import os

"""
PLot the graph according to the finding results_data
"""
import csv
import os


class Plot:
    def __init__(self, path, fontSize):
        self.path = path
        self.fontSize = fontSize

    """
    Draw the graph according to certain parameters
    """

    def draw(self, plt, fileName, results, xLabelTag, yLabelTag, colorTag, labelTag, titleTag):

        xValues = []
        yValues = []

        with open(results, 'r') as file:
            data = csv.reader(file, delimiter=',')
            for row in data:
                xValues.append(float(row[0]))
                yValues.append(float(row[1]))

        print(xValues)
        print(yValues)
        print("Draw and save it")
        plt.rc('font', size=self.fontSize)
        plt.plot(xValues, yValues, color=colorTag, label=labelTag)
        plt.ylabel(yLabelTag)
        plt.xlabel(xLabelTag)
        plt.legend()
        plt.title(titleTag)
        plt.gcf().set_size_inches(20, 15)
        plt.gcf().savefig(os.path.join(self.path, fileName + '.png'))

    def setClosePlot(self, plt):
        plt.close("all")

    def printFile(self, fileName, information):
        with open(os.path.join(self.path, fileName), 'w') as f:
            w = csv.writer(f)
            # print(information)
            # w.writerow(['episode', 'step', 'action', 'reward', 'state'])
            for i, row in enumerate(information):
                # ['episode', 'step', 'action', 'reward', 'state']
                if isinstance(row, list):
                    w.writerows(row)
                # ['episode', 'cumulative time']
                # ['episode', 'reward']
                else:
                    w.writerow([i, row])
