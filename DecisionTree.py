
# splits allowed
# [has, item, <item name>]
# [has, ability, <ability name>]
# [has, type, <type name>]
# [has, moves, <move name>]        # actually only tests for one move, the condition is called "has moves" just for ease of programming
# [stat, <index>, <integer value>] # this condition means (stat[index] < value)

# save processing time by remembering which examples were grouped together after each split examined, then
# pass that information down to the child nodes' calculations

# actually, the below approach won't work: the tree won't always be complete
# since splits are always binary, the tree will be stored as a list: [0,1,2,3,4,5...]
#              0
#            /   \
#           1     2
#          / \   /
#         3  4  5

# tree will be stored with each node looking like this: [<split condition>, yesChild, noChild]
# where leaf nodes are simply sets containing some samples: {charizard, abomasnow, venomoth}

import pickle
from math import log2
from pprint import pprint

import sys


def nodeEntropy(node):
    group = [e for mem in node for e in mem["labels"]]
    counter = dict()

    for elem in group:
        if elem in counter:
            counter[elem] = counter[elem] + 1
        else:
            counter[elem] = 1

    counts = [counter[key] for key in counter]

    return -sum(log2(c/len(group)) * c/len(group) for c in counts)


# expects a list of items as group
def entropy(group):
    counter = dict()

    for elem in group:
        if elem in counter:
            counter[elem] = counter[elem] + 1
        else:
            counter[elem] = 1

    counts = [counter[key] for key in counter]

    return -sum(log2(c/len(group)) * c/len(group) for c in counts)


# expects a group of examples
def informationGain(node1, node2):
    labels1 = [e for mem in node1 for e in mem["labels"]]
    labels2 = [e for mem in node2 for e in mem["labels"]]
    labelsOriginal = labels1 + labels2

    entropy1 = entropy(labels1)
    entropy2 = entropy(labels2)
    entropyOriginal = entropy(labelsOriginal)

    return entropyOriginal - (entropy1 + entropy2)


def test(condition, example):
    assert(len(condition) > 0)
    assert(condition[0] == "has" or condition[0] == "stat")

    if condition[0] == "has":
        assert(condition[1] == "item" or
               condition[1] == "ability" or
               condition[1] == "type" or
               condition[1] == "moves"
               )

        return condition[2] in example["features"][condition[1]]
    if condition[0] == "stat":
        assert(type(condition[2]) is int)

        stat = example["features"]["stats"][condition[1]]
        return stat < condition[2]


def gain(condition, dataset, weightBySplitProportion=False):
    tChild = [e for e in dataset if test(condition, e)]
    fChild = [e for e in dataset if not test(condition, e)]

    # I REALLY don't want it to keep picking the same option over and over again, just because it doesn't
    # cause information loss due to not actually splitting the data at all
    if len(tChild) == 0 or len(fChild) == 0:
        return -999999

    infogain = informationGain(tChild, fChild)

    if weightBySplitProportion:
        splitProportion = 1 + (min(len(tChild), len(fChild)) / len(dataset))
        return infogain * splitProportion

    return infogain


def treeEntropy(tree):
    try:
        if type(tree[0]) == tuple:
            labels = []
            for e in tree:
                try:
                    labels += e[1]
                except:
                    print(e)
                    pprint(tree, indent=4)
                    return 0
            return entropy(labels)
        else:
            return treeEntropy(tree[1]) + treeEntropy(tree[2])
    except:
        print(tree, file=sys.error)
        return 0.5


#
# best split condition search
#

def findBestSplitValue(values, valuesType, dataset):
    bestCondition = []
    bestGain = -1000

    for value in values:
        condition = ["has", valuesType, value]
        tgain = gain(condition, dataset)

        if(tgain > bestGain):
            bestCondition = condition
            bestGain = tgain

    return (bestCondition, bestGain)


def findBestSplitValue_Stat(statIndex, dataset, weightBySplitProportion=False):
    statValues = [data["features"]["stats"][statIndex] for data in dataset]

    bestCondition = 0
    bestGain = -10000
    for i in range(min(statValues), max(statValues)):
        condition = ["stat", statIndex, i]
        tgain = gain(condition, dataset, weightBySplitProportion=weightBySplitProportion)

        if tgain > bestGain:
            bestGain = tgain
            bestCondition = condition

    return (bestCondition, bestGain)


def clean(dataset):
    return [(e["name"], e["labels"]) for e in dataset]


# depth is not meant to be a variable used by whoever calls this function
def buildTree(dataset, maxDepth=10, _depth=0, minNodeCount=1):
    assert(type(maxDepth) is int)
    assert(type(_depth) is int)
    assert(type(minNodeCount) is int)
    assert(type(dataset) is list)

    #
    # immediate stopping conditions
    #

    if nodeEntropy(dataset) == 0:
        return clean(dataset)
    if len(dataset) <= minNodeCount:
        return clean(dataset)
    if _depth >= maxDepth:
        return clean(dataset)

    #
    # finding the best condition
    #
    bestCondition = []
    bestGain = -1000

    moves = {e for mem in dataset for e in mem["features"]["moves"]}
    items = {e for mem in dataset for e in mem["features"]["item"]}
    types = {e for mem in dataset for e in mem["features"]["type"]}
    abilities = {e for mem in dataset for e in mem["features"]["ability"]}

    conditions = (findBestSplitValue(moves, "moves", dataset),
                  findBestSplitValue(items, "item",  dataset),
                  findBestSplitValue(types, "type",  dataset),
                  findBestSplitValue(abilities, "ability", dataset),
                  findBestSplitValue_Stat(0, dataset),
                  findBestSplitValue_Stat(1, dataset),
                  findBestSplitValue_Stat(2, dataset),
                  findBestSplitValue_Stat(3, dataset),
                  findBestSplitValue_Stat(4, dataset),
                  findBestSplitValue_Stat(5, dataset)
                  )

    pprint(conditions)

    for e in conditions:
        if e[1] > bestGain:
            bestCondition, bestGain = e

    #
    # splitting on that condition
    #
    tChild = buildTree([e for e in dataset if test(bestCondition, e)],
                       maxDepth=maxDepth,
                       _depth=_depth+1,
                       minNodeCount=minNodeCount
                       )
    fChild = buildTree([e for e in dataset if not test(bestCondition, e)],
                       maxDepth=maxDepth,
                       _depth=_depth+1,
                       minNodeCount=minNodeCount
                       )

    return [bestCondition, tChild, fChild]

classes = ["wall", "wallbreaker", "sweeper", "pivot", "support",
           "tank", "utility", "glasscannon", "trapper", "revengekiller", "stallbreaker", "spinblocker"]

replacements = {"utility": "support", "glasscannon": "sweeper", "tank": "wall"}

# load dataset
dataset = pickle.load(open("dataset_pickle", "rb"))

# simplify labels
for e in dataset:
    for c in classes:
        if c in e["labels"]:
            e["labels"] = [c]
            break
    if type(e["labels"]) is set:
        e["labels"] = [e["labels"].pop()]

    if e["labels"][0] in replacements:
        e["labels"][0] = replacements[e["labels"][0]]

startEntropy = nodeEntropy(dataset)

tree = buildTree(dataset, maxDepth=100, minNodeCount=10)
pprint(tree, indent=4)

endEntropy = treeEntropy(tree)

print("Initial Entropy: ", startEntropy)
print("Final   Entropy: ", endEntropy)
print("Improvement:    %", (startEntropy-endEntropy)/endEntropy)