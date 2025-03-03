from .nodes import Node
from .utils import returnList, iterateNeighbors, convertMatrix
from .table_builder import TableBuilder
from .cell import Cell
from .empty_cell import EmptyCell
from .column import Column


class LengthAdjustManager:
    def __init__(self, labelLayers: list[list[Cell | EmptyCell]], columns: list[Column]):
        self.labelLayers = labelLayers
        self.columns = columns

    @returnList
    def _createColumnsLayer(self):
        for index, column in enumerate(self.columns):
            yield EmptyCell((index, index + 1), column.length)

    def _connectNodes(self):
        # I'm so desprate here... 
        for (higherNodes, lowerNodes), higherLayer in zip(iterateNeighbors(self.nodesMatrix, 2), self.allLayers):
            for node, cell in zip(higherNodes, higherLayer):
                node.connectManyLower(lowerNodes[index] for index in cell.lowerCellIndexes)        

    def _createNodesMatrix(self):
        return [[Node(cell.length) for cell in layer] for layer in self.allLayers]
    
    def _createHighestNode(self):
        return Node(0).connectManyLower(self.nodesMatrix[0])

    def _runAdjustAlgorithm(self):
        targetNodes = [self.highestNode]

        while targetNodes:
            topNode = targetNodes.pop()

            lowerNodesLength = sum(node.data for node in topNode.lowerNodes)
            separatorsLength = len(topNode.lowerNodes) - 1

            wholeUpperLength = topNode.data
            wholeLowerLength = lowerNodesLength + separatorsLength

            if wholeUpperLength > wholeLowerLength and topNode.lowerNodes:
                topNode.lowerNodes[0].data += wholeUpperLength - wholeLowerLength
            
            if wholeUpperLength < wholeLowerLength:
                topNode.data += wholeLowerLength - wholeUpperLength
                
                if topNode.higherNode:
                    targetNodes.append(topNode.higherNode)
        
            targetNodes.extend(topNode.lowerNodes)
    
    @returnList
    def _getAllLengthsMatrix(self):
        for nodesRow in self.nodesMatrix:
            yield [node.data for node in nodesRow]

    def _adjustLabels(self):
        for layer, lengthsRow in zip(self.labelLayers, self.labelsLengths):
            for cell, wantedLength in zip(layer, lengthsRow):
                cell.length = wantedLength
                

    def _adjustColumns(self):
        for column, length in zip(self.columns, self.columnsLengths):
            column.adjustRight(length)


    def execute(self):
        self.columnsLayer = self._createColumnsLayer()
        self.allLayers = self.labelLayers + [self.columnsLayer]
        self.nodesMatrix = self._createNodesMatrix()
        self.highestNode = self._createHighestNode()

        self._connectNodes()
        self._runAdjustAlgorithm()

        self.allLengths = self._getAllLengthsMatrix()

        self.labelsLengths = self.allLengths[:-1]
        self.columnsLengths = self.allLengths[-1]

        self._adjustLabels()
        self._adjustColumns()

if __name__ == '__main__':
    labelLayers = [
        [Cell((0, 3), 'Identification'), Cell((3, 5), 'Other')],
        [Cell((0, 1), 'Id'), Cell((1, 2), 'First Name'), Cell((2, 3), 'Last Name'), Cell((3, 4), 'Favourite Color'), Cell((4, 5), 'Car')]
    ]
    columns = [['asas', 'assa'], ['asas', 'assa'], ['asas', 'assa'], ['asas', 'assa'], ['asas', 'assa']]

    LengthAdjustManager(labelLayers, columns).execute()

    labelsMatrix = convertMatrix(lambda cell: cell.label, labelLayers)

    table = TableBuilder().appendRows(labelsMatrix).appendColumns(columns).build()
    print(str(table))