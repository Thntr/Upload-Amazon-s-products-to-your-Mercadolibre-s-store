def howToSplit():
    bigNumber = 8250
    currentNumberOfProducts = bigNumber
    startingNumber = 0
    listOfExtremes = []
    listOfExtremes.append(startingNumber)

    while currentNumberOfProducts != 0 or currentNumberOfProducts > 0:
        thedividedNumber = bigNumber / 10
        currentNumberOfProducts = currentNumberOfProducts - thedividedNumber
        startingNumber = startingNumber + thedividedNumber
        listOfExtremes.append(startingNumber)

    return listOfExtremes