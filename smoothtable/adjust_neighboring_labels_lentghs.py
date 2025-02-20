from constants import *

def adjustNeighboringLabelsLentghs(higherLayerLengths, higherLayerRanges, lowerLayerLengths):
    newHigherLayerLengths = []
    newLowerLayerLengths = lowerLayerLengths.copy()

    # columnLengthsGroups = [columnLengths[leftRangeLimit:rightRangeLimit + 1] for leftRangeLimit, rightRangeLimit in columnLabelRanges]

    for higherLayerLength, (leftRangeLimit, rightRangeLimit) in zip(higherLayerLengths, higherLayerRanges):
        columnsInRangeAmount = rightRangeLimit - leftRangeLimit + 1

        collectiveLowerLayerLength = sum(lowerLayerLengths[leftRangeLimit:rightRangeLimit + 1])
        separatorsLength = len(CENTER_VERTICAL_LINE) * (columnsInRangeAmount - 1)

        realLowerLayerLength = collectiveLowerLayerLength + separatorsLength

        if realLowerLayerLength > higherLayerLength:
            newHigherLayerLengths.append(realLowerLayerLength)
        elif realLowerLayerLength < higherLayerLength:
            # we could distribute length for different labels in the lower layer
            # but for now we assume that only first element with leftRangeLimit index 
            # is changing
            newHigherLayerLengths.append(higherLayerLength)
            newLowerLayerLengths[leftRangeLimit] += higherLayerLength - realLowerLayerLength
        else:
            newHigherLayerLengths.append(higherLayerLength)

    return newHigherLayerLengths, newLowerLayerLengths

def main():
    result = adjustNeighboringLabelsLentghs([10], [(0,2)], [1,2,3])
    print(result)
    
if __name__ == '__main__':
    main()