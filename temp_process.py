from os import listdir



def distance(T1,T2):
    return ( (T1[0]-T2[0])**2 + (T1[1] - T2[1])**2 ) ** 0.5


def DTW(T1,T2):
    numRows, numCols = len(T1), len(T2)
    cost = [[0 for _ in range(numCols)] for _ in range(numRows)]
    cost[0][0] = distance(T1[0],T2[0])
    
    for i in range(1,len(T1)):
        cost[i][0] = cost[i-1][0] + distance(T1[i],T2[0])
    for j in range(1,len(T2)):
        cost[0][j] = cost[0][j-1] + distance(T1[0],T2[j]) 

    
    for t1 in range(1,len(T1)):
        for t2 in range(1,len(T2)):
            d = distance(T1[t1],T2[t2])
            cost[t1][t2] = d + min(cost[t1-1][t2],cost[t1][t2-1],cost[t1-1][t2-1])
    
    if( cost[-1][-1] < 0.00000000000001):
        return 0.00000000000001
    else:
        return cost[-1][-1]


## Load data from pkl file
import cPickle
df = open('Open_Window_data.pkl','rb')
lf = open('labels.pkl','rb')
data = cPickle.load(df)
labels = cPickle.load(lf)


##


## Calculate the distance map between each pair of data

distance_map = [[0 for _ in xrange(len(data))] for _ in data]



for i in range(len(data)):
    print i
    for j in range(i+1,len(data)):
        d = DTW(data[i],data[j])
        distance_map[i][j] = d
        distance_map[j][i] = d


dist_f = open('Distance Matrix','wb')
cPickle.dump(distance_map,dist_f)
dist_f.close()
        
        
