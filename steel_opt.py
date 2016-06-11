"""Steel_opt.py
An optimisation program to determine the number of steel stock
lengths to use for a steel structure cut from stock
"""

def getStockLength():
    stockLength = raw_input("Please enter your stock length in mm: ")
    stockLength = int(stockLength)
    quantity = raw_input("How many do you have? ")
    quantity = int(quantity)

    return stockLength,quantity;

stockLength,quantity = getStockLength()
totalStock = stockLength*quantity
print "Stock Length is: "+str(stockLength)
print "Total Stock Length is: "+str(totalStock)
cutList = []

def addToCutList():

    partSize = raw_input("Please enter your cut length in mm: ")
    partSize = int(partSize)
    partQuant = raw_input("How many do you have? ")
    partQuant = int(partQuant)
    print "Total Stock Length available is: "+str(totalStock)
    i=0
    while (i<partQuant):
        cutList.append(partSize)
        i+=1
    return cutList;
answer="y"
while (answer =="y"):
    cutList = addToCutList()
    print "Current Length is: "+ str(sum(cutList))+" mm"

    answer = raw_input("do you have more to add? y/n?: ")



if (sum(cutList)>totalStock):
    print "Not enough stock."
    quit()
else: print "There is potentially enough stock, optimisation possible"

cutList.sort()
print cutList


""" Partition a list into sublists whose sums don't exceed a maximum
    using a First Fit Decreasing algorithm. See
    http://www.ams.org/new-in-math/cover/bins1.html
    for a simple description of the method.
"""


class Bin(object):
    """ Container for items that keeps a running sum """
    def __init__(self):
        self.items = []
        self.sum = 0

    def append(self, item):
        self.items.append(item)
        self.sum += item

    def __str__(self):
        """ Printable representation """
        return 'Bin(sum=%d, items=%s)' % (self.sum, str(self.items))


def pack(values, maxValue):
    values = sorted(values, reverse=True)
    bins = []

    for item in values:
        # Try to fit item into a bin
        for bin in bins:
            if bin.sum + item <= maxValue:
                #print 'Adding', item, 'to', bin
                bin.append(item)
                break
        else:
            # item didn't fit into any bin, start a new bin
            #print 'Making new bin for', item
            bin = Bin()
            bin.append(item)
            bins.append(bin)

    return bins


if __name__ == '__main__':
    import random

    def packAndShow(aList, maxValue):
        """ Pack a list into bins and show the result """
        print 'List with sum', sum(aList), 'requires at least', (sum(aList)+maxValue-1)/maxValue, 'bins'

        bins = pack(aList, maxValue)

        print 'Solution using', len(bins), 'bins:'
        for bin in bins:
            print bin

        print


    packAndShow(cutList, stockLength)
