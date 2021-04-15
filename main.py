import csv

if __name__ == "__main__":

    symbolsDict = {}

    input_file = open("input.csv")
    csv_reader = csv.reader(input_file, delimiter=",")
    for line in csv_reader:

        ################################
        # Split line into variables and
        # ensure right types
        timeStamp, symbol, quantity, price = line
        timeStamp = int(timeStamp)
        quantity = int(quantity)
        price = int(price)

        #######################################
        # check if symbol exists in dictionary,
        #  if not then add an empty record
        if symbol not in symbolsDict:
            symbolsDict[symbol] = {
                "MaxTimeGap": 0,
                "Volume": 0,
                "WeightedAveragePrice": 0.0,
                "MaxPrice": 0,
                "lastTimestamp": timeStamp
            }

        #######################
        # compute stats and
        # update the dictionary
        musSinceLastTimestamp = timeStamp - symbolsDict[symbol]["lastTimestamp"]

        if musSinceLastTimestamp > symbolsDict[symbol]["MaxTimeGap"]:
            symbolsDict[symbol]["MaxTimeGap"] = musSinceLastTimestamp

        symbolsDict[symbol]["lastTimestamp"] = timeStamp

        if price > symbolsDict[symbol]["MaxPrice"]:
            symbolsDict[symbol]["MaxPrice"] = price

        newAveragePrice = (symbolsDict[symbol]["WeightedAveragePrice"] * symbolsDict[symbol]["Volume"] + price*quantity) / (symbolsDict[symbol]["Volume"] + quantity)
        symbolsDict[symbol]["WeightedAveragePrice"] = newAveragePrice

        symbolsDict[symbol]["Volume"] += quantity

    input_file.close()

    ########################################
    # Order the symbols and dump the output
    # to a CSV file
    sortedSymbols = sorted(symbolsDict.keys())

    output_file = open('output.csv', mode='w')
    csv_writer = csv.writer(output_file, delimiter=",", lineterminator='\n')

    for symbol in sortedSymbols:

        output_line = [
            symbol,
            symbolsDict[symbol]["MaxTimeGap"],
            symbolsDict[symbol]["Volume"],
            int(symbolsDict[symbol]["WeightedAveragePrice"]),
            symbolsDict[symbol]["MaxPrice"]
        ]

        csv_writer.writerow(output_line)

    output_file.close()
