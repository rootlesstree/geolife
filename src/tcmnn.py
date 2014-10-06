import cPickle
import time
f = open("Open_Window_data.pkl","rb")
fl= open("labels.pkl","rb")
fd = open("Distance_Matrix.pkl","rb")
data = cPickle.load(f)
labels = cPickle.load(fl)
Dist_Matrix = cPickle.load(fd)
for i in range(len(Dist_Matrix[0])):
    Dist_Matrix[i][i] = 0.000000000001

#Dist_Matrix = []


#for i in range(len(data)):
#    if(Dist_Matrix[i][5922] < 0.01):
#        print i,Dist_Matrix[i][5922]

start = time.time()
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


def findKShortestDistanceWithinGroup(sample,groupData,K):
    distVector = []
    for data in groupData:
        dist = Dist_Matrix[sample[1]][data[1]]
        distVector.append(dist)
    
    distVector.sort()
    if(len(groupData)==1 and sample in groupData):
        return [0]*K
    else:       
        return distVector[0:K]

import load_index as li

train_index = li.train_index
test_index = li.test_index



class_data = []
alpha_values = range(len(data))
distSameGroupValues = range(len(data))
distDifferentGroupValues = range(len(data))

for i in range(len(set(labels))):
    class_data.append([])


for i in train_index:
    cls = labels[i]
    sample = data[i]
    class_data[cls].append([sample,i])


#print findKShortestDistanceWithinGroup(class_data[0][0],class_data[0],5)



for r,cls in enumerate(class_data):
    groups = [c for c in class_data if c!=cls]
    for c in cls:
        DistSameGroup = findKShortestDistanceWithinGroup(c,cls,2)
        distDifferentGroups = []
        for group in groups:
            distDifferent = findKShortestDistanceWithinGroup(c,group,1)
            distDifferentGroups.append(distDifferent[0])

        distDifferentGroups.sort()
        distSameGroupValues[c[1]] = float(DistSameGroup[1])
        distDifferentGroupValues[c[1]]= float(distDifferentGroups[0])


        alpha_values[c[1]] = float(DistSameGroup[1])/distDifferentGroups[0]







test_sample = []
for i in range(10):
    test_sample.append(data[test_index[i]])
test_sample_index = test_index[0:10]



statistics = [0 for p in range(20)]

for test_r,test in enumerate(test_sample):

    pValues = []
    for j in range(182):

        final_alphas = []
        for r,cls in enumerate(class_data):
            DistDifferentGroupTest = []

            if (r==j):
                DistSameGroupTest = findKShortestDistanceWithinGroup([test,test_sample_index[test_r]],cls,1)
            else:
                distDifferentTest = findKShortestDistanceWithinGroup([test,test_sample_index[test_r]],cls,1)
                if(j==181):
                    print distDifferentTest[0]
                DistDifferentGroupTest.append(distDifferentTest[0])

            for c in cls:
                   
                if (r==j):                                                                           
                    if(distSameGroupValues[c[1]] > Dist_Matrix[c[1]][test_sample_index[test_r]]):
                        final_alpha = float(Dist_Matrix[c[1]][test_sample_index[test_r]])/distDifferentGroupValues[c[1]]
                    else:
                        final_alpha = alpha_values[c[1]]
        
                    final_alphas.append(final_alpha)
       
                else:
                    if(distDifferentGroupValues[c[1]] > Dist_Matrix[c[1]][test_sample_index[test_r]]):
                        final_alpha = distSameGroupValues[c[1]]/float(Dist_Matrix[c[1]][test_sample_index[test_r]])
                    else:
                        final_alpha = alpha_values[c[1]]
                    final_alphas.append(final_alpha)

    #calculate p value of specfic class j
        DistDifferentGroupTest.sort()


        try:
            if(j==181):
                #print DistSameGroupTest[0]
                print len(DistDifferentGroupTest)
            alpha_test = float(DistSameGroupTest[0])/DistDifferentGroupTest[0]
        except:
            pass
        
        total_greater_alphas = [a for a in final_alphas if a >= alpha_test]
        pValues.append(len(total_greater_alphas)/float(len(final_alphas)+1))


#print pValues                                                                    
    for i in range(0,20,1):
        th = i/float(20)
        ps = [p for p in pValues if p > th and p <= th+0.05]
        statistics[i] += len(ps)



for s in statistics:
    print s
#    print pValues.index(max(pValues)),":",max(pValues)," ",pValues[labels[test_sample_index[test_r]]]," ", labels[test_sample_index[test_r]]
    

