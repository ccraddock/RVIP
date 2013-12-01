import numpy as np

# --- define the task parameters
duration = 4.0;  # minutes
rateMin = 100.0; # stim per minute
minSep = 5;      # minimum number of stim between targets
maxSep = 30;     # maximum number of stim between targets
nTargets = 32;   # total number of targets for test

# length of target sequences
targetLen = 3;

# these are the different targets
targets=[[2,4,6],
         [3,5,7],
         [4,6,8]]

# these are psuedo targets, that we want to remove
sm_targets=[[2,4],
            [3,5],
            [4,6]]

# these are the diffs
sm_diffs=[[6],
          [7],
          [8]]

kills = [[2,4,6,8]]

allVals = range(1,10)

# we want to ensure that we have 32 stims, which is kind of hard to do
# randomly (i tried for a loooong time), so what constructed a spacing
# list, which indicates the number of stims between consecutive targets,
# that allows 32 stims, and we will permute this to obtain the stim vector.
# Also, we will randomly assign targets and other stims, to allow another
# level of randomization
seps = np.random.shuffle([30, 7, 8, 10, 10, 14, 8, 6, 10, 6, 7, 7, 11, 8,\
    13, 9, 11, 14, 11, 11, 7, 12, 19, 12, 7, 13, 6, 13, 7, 9, 11, 7])

# utility functions to add in constructing the stimuli
#
# compute the difference between two lists
diff = lambda l1,l2: [x for x in l1 if x not in l2]
#
# randomly choose an element from a list
choice = lambda(a): a[np.random.randint(len(a))]

# count the number of stims
nStim = int(np.ceil((duration*rateMin)/float(targetLen))*float(targetLen))

# print to validate our calculations
print "showing %3.1f stims per min for %3.1f min results in %d stims"%(\
    rateMin,duration,nStim)

cnt30 = 0
stim_created = 0
while stim_created != 32 or cnt30 < 1:
    # create a list of zeros that will be populated with the stimuli
    stims=np.zeros(nStim).tolist()

    # create a binary list that will indicate when we expect a keypress
    response = np.zeros(nStim,dtype=np.int)

    # calculate a list of the seperation (in number of stimuli) between 
    # successive targets, this helps us identify where the targets will occur
    seps=[int(s) for s in np.round(np.random.normal(meanSep,stdSep,nTargets))]
    seps[0]=30
    #seps=np.random.random_integers(low=minSep,high=maxSep,size=(nTargets)).tolist()

    cnt30=0
    for i in range(len(seps)):
        if seps[i]<minSep:
            seps[i]=minSep
        if seps[i]>maxSep:
            seps[i]=maxSep
        if seps[i] > 20:
            cnt30+=1

    print "min %d, max %d"%(min(seps),max(seps))

    # --- now lets generate targets using rubrick
    #start at begining of sequence
    ndx = 0
    t = 0

    # repeat until we have created all of the targets
    while t < nTargets:
        # calculate the index of the next target
        targetNdx=ndx+seps[t]

        # make sure that there is room in the list for a new target
        if (targetNdx+targetLen) < nStim:
            # populate stimuli with a randomly chosen target
            stims[targetNdx:targetNdx+targetLen]=targets[\
                np.random.random_integers(0,np.shape(targets)[0]-1,size=1)]
            # update the response binary vector to indicate that we 
            # expect a response to this sequence
            response[targetNdx+targetLen-1]=1
            # update our counters
            t=t+1
            ndx=targetNdx+targetLen-1
        else:
            # if there isn't enough room at the end of the list, we are done
            break

    print "created %d stimuli"%(t)
    stim_created = t
    cnt30 = seps.count(30)

print seps
