from .constants import SPACE, EMPTY
from .utils import ConvertTo


def nonDigitToSpace(char):
    if char.isdigit():
        return char
    
    return SPACE

def stringify(items):
    return ''.join(items)

def toIntegers(string):
    integersAndSpaceChars = map(nonDigitToSpace, string)
    string = stringify(integersAndSpaceChars)
    stringIntegers = string.split()
    integers = list(map(int, stringIntegers))
    return integers

@ConvertTo(list)
def stringRangesToIntegers(ranges):
    for stringRange in ranges:
        yield toIntegers(stringRange)



def validate(integerRanges, columnsAmount):
    for range in integerRanges:
        numbersAmount = len(range) 

        if numbersAmount > 2:
            raise ValueError('Label range should consist of maximally 2 numbers!'
                            f'{numbersAmount} were given: {range}!')

    lastInteger = columnsAmount

    for range in integerRanges[::-1]:
        for integer in range[::-1]:
            if not integer <= lastInteger:
                raise ValueError('Invalid range!')
            
            lastInteger = integer
        
        lastInteger -= 1

@ConvertTo(list)
def makeDoubleSides(integerRanges):
    for range in integerRanges:
        if len(range) == 1:
            yield [range[0], range[0]]
        else:
            yield range

@ConvertTo(list)
def withNolabelRanges(integerRanges, labels, columnsAmount):
    yield labels[0], integerRanges[0]

    for i in range(1, len(integerRanges)):
        currentRange = integerRanges[i]
        previousRange = integerRanges[i - 1]

        nolabelAmount = currentRange[0] - previousRange[1] - 1

        if nolabelAmount > 0:
            yield EMPTY, (previousRange[1] + 1,  previousRange[1] + nolabelAmount)
        
        yield labels[i], currentRange

    # lastRange = integerRanges[-1]

    # nolabelAmount = columnsAmount - lastRange[1]

    # if nolabelAmount > 0:
    #     yield NOLABEL, [lastRange[1] + 1,  lastRange[1] + nolabelAmount]  

@ConvertTo(list)
def generateAllLabels(labelsAndRanges):
    for label, labelRange in labelsAndRanges:
        for _ in range(labelRange[1] - labelRange[0] + 1):
            yield label

@ConvertTo(list)
def subtractOneFromRanges(ranges):
    for range in ranges:
        yield range[0] - 1, range[1] - 1

def dictLabelsToList(dictLabels, columnsAmount):
    integerRanges = stringRangesToIntegers(dictLabels.keys())
    labels = list(dictLabels.values())

    validate(integerRanges, columnsAmount)

    integerRanges = makeDoubleSides(integerRanges)
    integerRanges = subtractOneFromRanges(integerRanges)

    labelsAndRanges = withNolabelRanges(integerRanges, labels, columnsAmount)

    return labelsAndRanges


def normalize(rangesAndLabels: dict[str, str], columnsAmount: int):
    return dictLabelsToList(rangesAndLabels, columnsAmount)