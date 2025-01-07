import random



def Calculate_Cost(plan, goal):
    cost = 0

    for task in plan:
        cost += task[2 + goal[2]]

    return cost


def Planner(tasks,goal,worldstate):
    plans = []
    unfinished = 1

    condition = goal[0]
    objectives = []

    for task in tasks:
        if task[4] == condition:
            objectives.append(task)


    for i in range(len(objectives)):
        if i > len(plans)-1:
            plans.append([objectives[i]])



    while unfinished > 0:
        unfinished = len(plans)
        for plan in plans:
            objectives = []
            condition = plan[len(plan)-1][1]



           
            for task in tasks:
                if task[4] == condition:
                    objectives.append(task)

       

            for i in range(len(objectives)):
                if i > len(plans)-1:
                    plans.append(plans[i-1].copy())
                    plans[len(objectives)-1].append(objectives[i])

            if len(objectives) > 0:
                plan.append(objectives[0])
                
            else:
                if worldstate[condition] == False:
                    plans.remove(plan);
                unfinished -= 1

            
                

                


    lowestcost = 999
    lowestplan = []

    
    print('\nNumber of Possible Plans: ' + str(len(plans)))
            
    
        
    for plan in plans:
        print('\nSteps Towards Goal: ')

        for i in range(len(plan)):
            print(" - " + str(plan[len(plan)-i-1][0]))

    
        plancost = Calculate_Cost(plan,goal)
        print('Cost:' + str(plancost))

        if plancost < lowestcost:
            lowestcost = plancost
            lowestplan = plan

    print('\nDiscarding other plans, using:')
    print('Steps Towards Goal: ')

    for i in range(len(lowestplan)):
            print(" - " + str(lowestplan[len(lowestplan)-i-1][0]))


    print('Cost:' + str(lowestcost))
            





#worldstate = {'nothungry': False, 'hasPhoneNumber': True, 'hasFood': False, 'pizzaOnRoute': False, 'foodCooked': False, 'hasMaterial': True}

worldstate = {'nothungry': False, 'hasPhoneNumber': True, 'hasMaterial': True}

goal = ('nothungry',True,0)


tasks = [

    ['Eat', 'hasFood', 30, 0, 'nothungry'],
    ['Wait for Delivery', 'pizzaOnRoute', 15, 0, 'hasFood'],
    ['Phone for Pizza', 'hasPhoneNumber', 1, 20, 'pizzaOnRoute'],

    ['Serve Food', 'foodCooked', 5, 0, 'hasFood'],
    ['Cook Food', 'hasIngredients', 60, 0, 'foodCooked'],
    ['Get Ingredients', 'hasMaterial', 10, 5, 'hasIngredients']


]

print('Goal: ' + str(goal[0]) + ' should be ' + str(goal[1]))
print('Do this in the lowest amount of: ')
if goal[2] == 0:
    print('Time')
else:
    print('Money')

print("\nWorld State: " + str(worldstate))

print('\nPossible Tasks: ')
for task in tasks:
    
    print(task)





Planner(tasks,goal,worldstate)
