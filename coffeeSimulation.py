import pandas as pd
import os
from datetime import date

def coffee():

    '''
    Mariel Reyes Salazar coffeeshop simulation script 

    This mini script will run a simulation of a coffeeshop with 3 tables. 
    Each table can accommodate groups of 1, 2 and 3 customers respectively. 

    If a group cannot find the most suitable table for them 
    (i.e. group of 2 will prefer to pick the table for 2), it will sit in the next larger table.

    For a group of 3, if the table of 3 is not available, then it will take the tables for 2 and 1 
    (if they are available) and will join them.

    The profit is updated as soon as the group is able to sit down, regardless of the time they take
     in the coffeeshop.

    The termination time is 60 minutes; however, it can be updated up to any value. 
    There are no further interarrival events past 67

    The simulation will use past data coming from the coffee.csv file. 
    This file contains the group size, potential profit, interarrival times and occupancy times.

    inputs:
    None

    outputs:
    simResults_date.csv file: This file contains the results and performance indicators for the simulation
    '''

    #initializations
    tNow = 0 
    currSize = 0
    numLeft = 0
    B1 = 0
    B2 = 0
    B3 = 0
    
    totalAreaQ = 0
    totalBusy1 = 0
    totalBusy2 = 0
    totalBusy3 = 0
    totalProfit = 0

    termination = 60

    avgCustomers = 0
    utilization1 = 0
    utilization2 = 0
    utilization3 = 0
    throughput = 0

    # import past data
    currDir = os.getcwd()
    pastData = pd.read_csv(os.path.join(currDir, "coffee.csv"))

    eventCalendar = [0, 0, 0, 0, 0, 0]

    tableIdx = 0

    # 6 events in the calendar
    # event0: arrival, event1: service on T1, event2: service on T2, event3: service on T3, event4: service  on T1 and T2, event5: termination 

    eventCalendar[0] = pastData.interarrival_t[0]
    eventCalendar[1] = termination + 1
    eventCalendar[2] = termination + 1
    eventCalendar[3] = termination + 1
    eventCalendar[4] = termination + 1
    eventCalendar[5] = termination

    # output lists
    l_time = []
    l_group = []
    l_type = []
    l_b1 =[]
    l_b2 = []
    l_b3 = []
    l_profit = []

    while(tNow < termination):

        tNext = min(eventCalendar)
        typeNext = eventCalendar.index(min(eventCalendar))

        # update the performance indicators

        totalAreaQ += (tNext - tNow)*currSize
        totalBusy1 += (tNext - tNow)*B1
        totalBusy2 += (tNext - tNow)*B2
        totalBusy3 += (tNext - tNow)*B3

        tNow = tNext

        # process the arrivals/services/terminations

        if(typeNext == 0):

            # arrival case
            groupSize = pastData.group_size[tableIdx]
            
            # check the group size and see where they can sit down. If they can sit down, calculate profit and update events
            if groupSize == 1:
                if (B1 == 0):

                    B1 = 1
                    currSize += groupSize
                    totalProfit += pastData.potential_profit[tableIdx]
                    eventCalendar[1] = tNow + pastData.occupancy_t[tableIdx]
        
                elif(B2 == 0):

                    B2 = 1
                    currSize += groupSize
                    totalProfit += pastData.potential_profit[tableIdx]
                    eventCalendar[2] = tNow + pastData.occupancy_t[tableIdx]
            
                elif(B3 == 0):

                    B3 = 1
                    currSize += groupSize
                    totalProfit += pastData.potential_profit[tableIdx]
                    eventCalendar[3] = tNow + pastData.occupancy_t[tableIdx]
            
            elif groupSize == 2:
                if(B2 == 0):

                    B2 = 1
                    currSize += groupSize
                    totalProfit += pastData.potential_profit[tableIdx]
                    eventCalendar[2] = tNow + pastData.occupancy_t[tableIdx]
            
                elif(B3 == 0):

                    B3 = 1
                    currSize += groupSize
                    totalProfit += pastData.potential_profit[tableIdx]
                    eventCalendar[3] = tNow + pastData.occupancy_t[tableIdx]
            
            elif groupSize == 3:
                if (B3 == 0):

                    B3 = 1
                    currSize += groupSize
                    totalProfit += pastData.potential_profit[tableIdx]
                    eventCalendar[3] = tNow + pastData.occupancy_t[tableIdx]
        
                elif(B1 == 0 and B2 == 0):

                    B1 = 1
                    B2 = 1
                    currSize += groupSize
                    totalProfit += pastData.potential_profit[tableIdx]
                    eventCalendar[4] = tNow + pastData.occupancy_t[tableIdx]

            eventCalendar[0] = tNow + pastData.interarrival_t[tableIdx+1]
            tableIdx += 1
        
        elif(typeNext == 1):

            # service case at table 1
            currSize -= 1
            numLeft += 1

            # no more people in the queue
            B1 = 0
            eventCalendar[1] = termination + 1

        elif(typeNext == 2):

            # service case at table 2
            currSize -= 2
            numLeft += 2

            # no more people in the queue
            B2 = 0
            eventCalendar[2] = termination + 1

        elif(typeNext == 3):

            # service case at table 3
            currSize -= 3
            numLeft += 3

            # no more people in the queue
            B3 = 0
            eventCalendar[3] = termination + 1

        elif(typeNext == 4):

            # service case at table 2 and 1, for a group of 3
            currSize -= 3
            numLeft += 3

            # no more people in the queue
            B1 = 0
            B2 = 0
            eventCalendar[4] = termination + 1

        elif(typeNext == 5):

            # termination case
            avgCustomers = totalAreaQ / termination
            utilization1 = totalBusy1 / termination
            utilization2 = totalBusy2  / termination
            utilization3 = totalBusy3  / termination
            throughput = numLeft / termination
          
        l_time.append(tNow)
        l_group.append(groupSize)
        l_type.append(typeNext)
        l_b1.append(B1)
        l_b2.append(B2)
        l_b3.append(B3)
        l_profit.append(totalProfit)
    
    # create a dataframe for exporting the simulation values
    outResults = pd.DataFrame(data=zip(l_time, l_group, l_type, l_b1, l_b2, l_b3, l_profit), 
    columns=["tNow", "groupSize", "eventType", "B1", "B2", "B3", "profit"])

    # date object containing current date and time
    today = date.today()
    dt_string = today.strftime("%d-%m-%Y")

    # output a csv file with the results and append the performance indicators
    outFile = os.path.join(currDir, f"simResults_{dt_string}.csv")
    outResults.to_csv(outFile, sep= "\t", index=False)

    with open(outFile, "a") as f:
         f.write("\nSimulation results for " + str(termination) + " mins\n\n")
         f.write("Average customers: " + str(avgCustomers) + "\n") 
         f.write("Utilization of table 1: " + str(utilization1) + "\n")
         f.write("Utilization of table 2: " + str(utilization2) + "\n")
         f.write("Utilization of table 3: " + str(utilization3) + "\n")
         f.write("Throughput: " + str(throughput) + "\n")
         f.write("Total profit: " + str(totalProfit))

    print(f"Created {outFile}")

    return

coffee()