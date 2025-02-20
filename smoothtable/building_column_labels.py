"""
╭─────────────────┬───────────────────╮
│ Favourite Color │ AHA               │
├─────────────────┴───────────────────┤    ╭─────────────────╮    ╭─────╮
│ Identification                      │    │ Favourite Color │    │ AHA │
├───┬───────────┬────────────┬────────┼────┼───────┬────┬────┼────┼─────┤
│ 1 │ Kamil     │ Lenczewski │ Blue   │ R1 │ R1    │ R1 │ R1 │ R1 │ R1  │
│ 2 │ Anastazja │ Kasprzyk   │ Red    │ R1 │ R1    │ R1 │ R1 │ R1 │ R1  │
│ 3 │ Karolina  │ Olawska    │ Yellow │ V1 │ V1    │ V1 │ V1 │ V1 │ V1  │
╰───┴───────────┴────────────┴────────┴────┴───────┴────┴────┴────┴─────╯

"""



from .constants import *
from .string_matrix_builder import StringMatrixBuilder

class LabelsBuilder:
    def __init__(self, columnLabelNames, columnLabelRanges, areRowLabels, columnLengths):
        self.labelNames = columnLabelNames
        self.labelRanges = columnLabelRanges
        self.labelsSize = len(self.labelNames)

        self.areRowLabels = areRowLabels
        self.columnLengths = columnLengths

    def createEmptyLabel(self, labelLength):
        top = labelLength * SPACE
        middle = labelLength * SPACE

        bottom = labelLength * HORIZONTAL_LINE

        return [top, middle, bottom]

    def doesNextLabelExist(self, labelIndex):
        return labelIndex + 1 < self.labelsSize

    def isNextLabelNonempty(self, labelIndex):
        return self.doesNextLabelExist(labelIndex) and not self.labelNames[labelIndex + 1].isspace()

    def isPreviousLabelNonempty(self, labelIndex):
        return labelIndex - 1 >= 0 and not self.labelNames[labelIndex - 1].isspace()
    

    def createBottomLine(self):
        pass

    def createLabel(self, labelName, range, labelIndex):
        labelLength = len(labelName)

        if labelName.isspace():
            return self.createEmptyLabel(labelLength)

        # delete range and columnNameLengths then subside it with pre-calculated columnNameLengths
        leftRangeLimit, rightRangeLimit = range
        columnNameLengths = self.columnLengths[leftRangeLimit:rightRangeLimit + 1]        

        topHorizontalLine = labelLength * HORIZONTAL_LINE
        bottomHorizontalLine = TOP_CENTER_CONDUIT.join(HORIZONTAL_LINE * length for length in columnNameLengths)

        builder = StringMatrixBuilder(width=3, height=3)

        builder.set(TOP_LEFT_CORNER).at(0,0).set(topHorizontalLine).at(0,1).set(TOP_RIGHT_CORNER).at(0,2)\
               .set(LEFT_VERTICAL_LINE).at(1,0).set(labelName).at(1,1).set(RIGHT_VERTICAL_LINE).at(1,2)\
               .set(CENTER_CONDUIT).at(2,0).set(bottomHorizontalLine).at(2,1).set(CENTER_CONDUIT).at(2,2)

        if labelIndex == 0 and not self.areRowLabels:
            builder.set(LEFT_CONDUIT).at(2,0)

        if self.isNextLabelNonempty(labelIndex):
            builder.set(TOP_CENTER_CONDUIT).at(0,2)
            builder.set(CENTER_CONDUIT).at(2,2)

        if self.isPreviousLabelNonempty(labelIndex):
            builder.set(EMPTY).at(0,0).at(1,0).at(2,0)

        if not self.doesNextLabelExist(labelIndex):
            builder.set(RIGHT_CONDUIT).at(2,2)

        List = builder.buildVerticalList()

        return List
    