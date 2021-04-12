
"""This file has been used once to generate the SAOColoursList.json file.
It does NOT need to be run each time building the project"""

import json
import os

def loadJSON(filename):
    filename = os.path.normpath(filename)
    with open(filename) as f:
        loadedJSON = json.load(f)
    return loadedJSON

def saveJSON(filename, JSONToSave):
    filename = os.path.normpath(filename)
    with open(filename, "w") as f:
        f.write(json.dumps(JSONToSave, indent = 4))

def SAO_RGBToHex(colorRGB):
    return ("#%02x%02x%02x" % colorRGB).upper()

def convertMain():
    colours_old = loadJSON("./RebaneColoursList.json")
    colours_new = {}
    for colourSetNumber, colourSet in enumerate(colours_old):
        colours_new[str(colourSetNumber)] = {}
        colours_new[str(colourSetNumber)]["tonesRGB"] = {
            "dark": [colourSet[0][0][0],colourSet[0][0][1],colourSet[0][0][2]],
            "normal": [colourSet[0][1][0],colourSet[0][1][1],colourSet[0][1][2]],
            "light": [colourSet[0][2][0],colourSet[0][2][1],colourSet[0][2][2]],
            "unobtainable": [colourSet[0][3][0],colourSet[0][3][1],colourSet[0][3][2]]
            }
        colours_new[str(colourSetNumber)]["blocks"] = {}
        for blockNumber, block in enumerate(colourSet[1]):
            colours_new[str(colourSetNumber)]["blocks"][str(blockNumber)] = {
                "displayName": block[2],
                "validVersions": [
                    "1.12.2",
                    "1.13.2",
                    "1.14.4",
                    "1.15.2",
                    "1.16.5"
                ],
                "NBTWorkerName": block[0],
                "NBTWorkerArgs": {} if block[1] == "" else {key: value for (key, value) in [t.replace("'", "").split(":") for t in block[1].split(",")]},
                "supportBlockMandatory": block[3],
                "flammable": block[6]
            }
    patches = loadJSON("./RebanePatches.json")
    for patch in patches["1.13"]["patch"]:
        colourSetNumber = str(patch[0][0])
        blockNo = str(patch[0][1])
        # toAssert = colours_new[colourSetNumber]["blocks"][blockNo]
        # I manually changed colourSets 1 and 5 in ./RebanePatches for blockNos to align
        # assert toAssert["displayName"] == patch[1][2]
        # toAssert["validVersions"][-1]["to"] = "1.12.2"
        colours_new[colourSetNumber]["blocks"][blockNo]["validVersions"] = ["1.12.2"]
        blockNoNew = str(1 + max([int(t) for t in colours_new[colourSetNumber]["blocks"]]))
        block = patch[1]
        colours_new[colourSetNumber]["blocks"][blockNoNew] = {
            "displayName": block[2],
            "validVersions": [
                "1.13.2",
                "1.14.4",
                "1.15.2",
                "1.16.5"
            ],
            "NBTWorkerName": block[0],
            "NBTWorkerArgs": {} if block[1] == "" else {key: value for (key, value) in [t.replace("'", "").split(":") for t in block[1].split(",")]},
            "supportBlockMandatory": block[3],
            "flammable": block[6]
        }
    for remove in patches["1.13"]["remove"]:
        # just iron bars, again in ./RebanePatches changed so remove[0][1] is correct
        colourSetNumber = str(remove[0][0])
        blockNo = str(remove[0][1])
        colours_new[colourSetNumber]["blocks"][blockNo]["validVersions"] = ["1.12.2"]

    for addBlock in patches["1.16"]["add"]:
        colourSetNumber = str(addBlock[0][0])
        blockNo = str(addBlock[0][1])
        blockNoNew = str(1 + max([int(t) for t in colours_new[colourSetNumber]["blocks"]] + [-1]))
        theBlock = addBlock[1]
        colours_new[colourSetNumber]["blocks"][blockNoNew] = {
            "displayName": theBlock[2],
            "validVersions": [
                "1.16.5"
            ],
            "NBTWorkerName": theBlock[0],
            "NBTWorkerArgs": {} if theBlock[1] == "" else {key: value for (key, value) in [t.replace("'", "").split(":") for t in theBlock[1].split(",")]},
            "supportBlockMandatory": theBlock[3],
            "flammable": theBlock[6]
        }

    for addBlock in patches["1.16.2"]["add"]:
        colourSetNumber = str(addBlock[0][0])
        blockNo = str(addBlock[0][1])
        blockNoNew = str(1 + max([int(t) for t in colours_new[colourSetNumber]["blocks"]] + [-1]))
        theBlock = addBlock[1]
        colours_new[colourSetNumber]["blocks"][blockNoNew] = {
            "displayName": theBlock[2],
            "validVersions": [
                "1.16.5"
            ],
            "NBTWorkerName": theBlock[0],
            "NBTWorkerArgs": {} if theBlock[1] == "" else {key: value for (key, value) in [t.replace("'", "").split(":") for t in theBlock[1].split(",")]},
            "supportBlockMandatory": theBlock[3],
            "flammable": theBlock[6]
        }

    # Now reshuffle

    def reOrder(colourSetId, newOrder):
        colours_new[str(colourSetId)]["blocks"] = {str(index): colours_new[str(colourSetId)]["blocks"][str(key)] for (index, key) in enumerate(newOrder)}

    reOrder(0, [0,2, 1,3])
    reOrder(1, [0, 1, 2,12, 3,8, 4,9, 5,10, 6, 7,11])
    reOrder(6, [0,6, 1,7, 2,8, 3,9, 4,10, 5,11])
    reOrder(8, [0,7,1,8,2,9,3,4,10,5,6,11])
    reOrder(9, [0, 3,9, 1, 2,8, 4,10, 5, 6,11, 7])
    reOrder(11, [0,4, 1,5, 2,6, 3])
    reOrder(12, [0,5, 1,6, 2, 3,7, 4,8])
    reOrder(13, [0,8, 1,9, 2,10, 3,11, 4,12, 5, 6,13, 7,14])
    reOrder(14, [0,12, 1,13, 2,14, 3,15, 4,16, 5, 6,17, 7,18, 8,19, 9,20, 10,21, 11,22])
    reOrder(15, [0,8, 1,9, 2,10, 3,11, 4,12, 5, 6, 7,13])
    reOrder(16, [0,6, 1,7, 2,8, 3,9, 4,10, 5,11])
    reOrder(17, [0,8, 1,9, 2,10, 3,11, 4,12, 5, 6, 7,13])
    reOrder(18, [0,7, 1,8, 2,9, 3,10, 4,11, 5, 6,12])
    reOrder(19, [0,6, 1,7, 2,8, 3,9, 4,10, 5,11])
    reOrder(20, [0,6, 1,7, 2,8, 3,9, 4,10, 5,11])
    reOrder(21, [0,6, 1,7, 2,8, 3,9, 4,10, 5,11])
    reOrder(22, [0,7, 1,8, 2,9, 3,10, 4,11, 5, 6,12])
    reOrder(23, [0,7, 1,8, 2,9, 3,10, 4,11, 5, 6,12])
    reOrder(24, [0,6, 1,7, 2,8, 3,9, 4,10, 5,11])
    reOrder(25, [0,11, 1,12, 2,13, 3,14, 4,15, 5, 6,16, 7,17, 8,18, 9,19, 10,20])
    reOrder(26, [0,6, 1,7, 2,8, 3,9, 4,10, 5,11])
    reOrder(27, [0,8, 1,9, 2,10, 3,11, 4,12, 5, 6,13, 7,14])
    reOrder(28, [0,8, 1,9, 2,10, 3,11, 4,12, 5, 6, 7,13])

    reOrder(30, [0, 1,4, 2,5, 3,6])
    reOrder(33, [0,6, 1,7, 2,8, 3,9, 4,10, 5,11])
    reOrder(34, [0, 1,4, 2,5, 3,6])

    def prunebine(colourSetId, toCombine):
        colourSetId = str(colourSetId)
        toCombine = [str(t) for t in toCombine]
        combinedItem = colours_new[colourSetId]["blocks"][toCombine[0]]
        for version in colours_new[colourSetId]["blocks"][toCombine[1]]["validVersions"]:
            combinedItem["validVersions"].append(version)
        del colours_new[colourSetId]["blocks"][toCombine[1]]

    prunebine(1, [11,12])
    prunebine(3, [1,2])
    prunebine(4, [1,2])
    prunebine(7, [0,1])
    prunebine(10, [0,1])
    prunebine(12, [7,8])
    prunebine(16, [10,11])
    prunebine(17, [12,13])
    prunebine(19, [10,11])
    prunebine(20, [10,11])
    prunebine(21, [10,11])
    prunebine(22, [11,12])
    prunebine(23, [11,12])
    prunebine(24, [10,11])
    prunebine(25, [19,20])
    prunebine(26, [10,11])
    prunebine(27, [13,14])
    prunebine(28, [12,13])
    prunebine(30, [5,6])
    prunebine(31, [0,1])
    prunebine(32, [0,1])

    for colset in colours_new:
        for block in colours_new[colset]["blocks"].values():
            block["NBTWorkerName1.12"] = block["NBTWorkerName"]
            block["NBTWorkerArgs1.12"] = block["NBTWorkerArgs"]
            block["NBTWorkerNameFlattening"] = block["NBTWorkerName"]
            block["NBTWorkerArgsFlattening"] = block["NBTWorkerArgs"]
            del block["NBTWorkerName"]
            del block["NBTWorkerArgs"]

    def flattenBine(colourSetId, toCombine):
        mergeFrom = colours_new[str(colourSetId)]["blocks"][str(toCombine[1])]
        mergeTo = colours_new[str(colourSetId)]["blocks"][str(toCombine[0])]
        mergeTo["validVersions"] = mergeTo["validVersions"] + mergeFrom["validVersions"]
        mergeTo["NBTWorkerNameFlattening"] = mergeFrom["NBTWorkerName1.12"]
        mergeTo["NBTWorkerArgsFlattening"] = mergeFrom["NBTWorkerArgs1.12"]
        del colours_new[str(colourSetId)]["blocks"][str(toCombine[1])]

    flattenBine(0, [0,1])
    flattenBine(0, [2,3])
    flattenBine(1, [2,3])
    flattenBine(1, [4,5])
    flattenBine(1, [6,7])
    flattenBine(1, [8,9])
    flattenBine(2, [0,1])
    flattenBine(5, [3,4])

    flattenBine(6, [0,1])
    flattenBine(6, [2,3])
    flattenBine(6, [4,5])
    flattenBine(6, [6,7])
    flattenBine(6, [8,9])
    flattenBine(6, [10,11])

    flattenBine(8, [0,1])
    flattenBine(8, [2,3])
    flattenBine(8, [4,5])
    flattenBine(8, [7,8])
    flattenBine(8, [10,11])

    flattenBine(9, [1,2])
    flattenBine(9, [4,5])
    flattenBine(9, [6,7])
    flattenBine(9, [9,10])

    flattenBine(11, [0,1])
    flattenBine(11, [2,3])
    flattenBine(11, [4,5])

    flattenBine(12, [0,1])
    flattenBine(12, [2,3])
    flattenBine(12, [5,6])

    for i in range(16):
        flattenBine(13 + i, [0,1])
        flattenBine(13 + i, [2,3])
        flattenBine(13 + i, [4,5])
        flattenBine(13 + i, [6,7])
        flattenBine(13 + i, [8,9])

    flattenBine(13, [11,12])
    flattenBine(13, [13,14])

    flattenBine(14, [11,12])
    flattenBine(14, [13,14])
    flattenBine(14, [15,16])
    flattenBine(14, [17,18])
    flattenBine(14, [19,20])
    flattenBine(14, [21,22])

    flattenBine(15, [12,13])

    flattenBine(18, [11,12])

    flattenBine(25, [11,12])
    flattenBine(25, [13,14])
    flattenBine(25, [15,16])
    flattenBine(25, [17,18])

    flattenBine(27, [11,12])

    flattenBine(29, [1,2])

    flattenBine(30, [1,2])
    flattenBine(30, [3,4])

    flattenBine(33, [0,1])
    flattenBine(33, [2,3])
    flattenBine(33, [4,5])
    flattenBine(33, [6,7])
    flattenBine(33, [8,9])
    flattenBine(33, [10,11])

    flattenBine(34, [1,2])
    flattenBine(34, [3,4])
    flattenBine(34, [5,6])

    for i in range(16):
        flattenBine(35 + i, [0,1])

    #make blockIds 0-n
    for i in range(58):
        colours_new[str(i)]["blocks"] = {key: value for (key, value) in enumerate(colours_new[str(i)]["blocks"].values())}

    for colourSetId, colourSet in colours_new.items():
        for blockId, block in colourSet["blocks"].items():
            if block["validVersions"] != [
                "1.12.2",
                "1.13.2",
                "1.14.4",
                "1.15.2",
                "1.16.5"
            ]:
                # print(colourSetId, blockId)
                if block["validVersions"] == ["1.12.2"]:
                    del block["NBTWorkerNameFlattening"]
                    del block["NBTWorkerArgsFlattening"]
                if not "1.12.2" in block["validVersions"]:
                    del block["NBTWorkerName1.12"]
                    del block["NBTWorkerArgs1.12"]

    saveJSON("./SAOColoursList.json", colours_new)

if __name__ == "__main__":
    convertMain()
