#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.77.02), Tue Aug  6 11:30:02 2013
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions


############################
# Configuration Parameters #
############################

# for debegguing set full_screen to false
FULL_SCREEN = False

# number of "respond now" target cues for practice
NUM_PRACTICE_RESPOND_NOW = 8
PRACTICE_OUTCOME_CUE_ONTIME = 1.2

# --- define the task parameters
duration = 4.0;  # minutes
rateMin = 100.0; # stim per minute
minSep = 5;      # minimum number of stim between targets
maxSep = 30;     # maximum number of stim between targets
nTargets = 32;   # total number of targets for test

RESPONSE_TIME = 1.500 # number of seconds to allow responses after a target

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

# instructions
instruction_text1=u'A string of numbers will be presented in a box'
instruction_text2=u'in the center of the screen. Press the space'
instruction_text3=u'bar if you see the seqeunces (2-4-6), (3-5-7),'
instruction_text4=u'or (4-6-8).'

#############################
# Build the list of stimuli #
#############################

# utility functions to add in constructing the stimuli
#
# compute the difference between two lists
diff = lambda l1,l2: [x for x in l1 if x not in l2]
#
# randomly choose an element from a list
choice = lambda(a): a[np.random.randint(len(a))]

# calculate the number of stims
nStim = int(np.ceil((duration*rateMin)/float(targetLen))*float(targetLen))

# create a list of zeros that will be populated with the stimuli
stims=np.zeros(nStim).tolist()

# create a binary list that will indicate when we expect a keypress
response = np.zeros(nStim,dtype=np.int)

# we want to ensure that we have 32 stims, which is kind of hard to do
# randomly (i tried for a loooong time), so what constructed a spacing
# list, which indicates the number of stims between consecutive targets,
# that allows 32 stims, and we will permute this to obtain the stim vector.
# Also, we will randomly assign targets and other stims, to allow another
# level of randomization
seps = [30, 7, 8, 10, 10, 14, 8, 6, 10, 6, 7, 7, 11, 8,\
    13, 9, 11, 14, 11, 11, 7, 12, 19, 12, 7, 13, 6, 13, 7, 9, 11, 7]
np.random.shuffle(seps)

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
logging.log(level=logging.EXP, msg='Created %d stimuli'%(t))

# now go through and add non-targets based on these rools
# 1. no two consecutive stims should be the same (no repeats)
# 2. we do not want the sequence 2-4-6-8
#
# iterate over all of the stims
for i in range(0,nStim):
    # if the current stim is zero, we replace it with a randomly selected 
    # stim. We accomplish this by first determining the set of values
    # that the stim could take, and then randomly selecting a value from 
    # this set
    if stims[i] == 0:
        if i == 0:
            # if we are at the first stim, then any of the acceptable values
            # can be used
            possibleVals = allVals
        elif i == 1:
            # if we are at the second stim, we remove the first stim from the
            # possible values
            possibleVals = diff(allVals,[stims[i-1]])
        else:
            # we want to make sure that we do not randomly generate a target
            # sequence, so we compare the two previous stims to a list
            # of stems for the target sequence, if there is a match, we make
            # sure that we remove the remaining value of the sequence, so that
            # we do not complete the target sequence
            #
            # look for a stem
            pmatch=[j for j in range(0,np.shape(sm_targets)[0])\
                if sm_targets[j] == stims[i-targetLen+1:i]]

            # if there is a stem, remove the 3rd val of the sequence from the
            # set of possible values, along with the previous stim (avoids 
            # duplicates)
            if len(pmatch) > 0:
                possibleVals = \
                    diff(allVals,[stims[i-1],sm_diffs[pmatch[0]][0]])
            else:
                # if no stem, then just add the previous stim to avoid dups
                possibleVals = diff(allVals,[stims[i-1]])

        # there are also target sequences following the current stim, and
        # we need we need to take this sequence into account to avoid creating
        # duplicates, or the kill sequence. 
        # so we avoid it
        if i < nStim-1:
            # exclude the stim after the current ndx, and two less than this
            # value to make sure we dont have a duplicate or induce a kill
            # sequence
            possibleVals=diff(possibleVals,[stims[i+1],stims[i+1]-2])

        # now that we have caluclated the set of possible values for this stim
        # randomly choose one
        stims[i]=choice(possibleVals)

# for a santity check we can look through the generated sequence for a
# dupliace or the kill sequence
dups=[i for i in range(1,nStim) if stims[i-1] == stims[i]]
if dups:
    print "found %d duplicates %s"%(len(dups),\
        ",".join([str(d) for d in dups]))

killSeqs=[i for i in range(0,nStim-(targetLen+1))\
    if stims[i:i+targetLen+1] in kills]
if killSeqs:
    print "found %d kill sequences %s"%(len(killSeqs),\
        ",".join([str(k) for k in killSeqs]))

# convert the stim and response lists in to a list of dictionaries, which is
# the format that PsychoPy seems to prefer
exp_trials=[]
for i in range(len(stims)):
    trial={}
    trial['stim']=stims[i]
    trial['response']=response[i]
    exp_trials.append(trial)

###########################################
# Get configuration information from user #
###########################################

# Store info about the experiment session
expName = 'RVIP'  # from the Builder filename that created this script
expInfo = {'Participant':'',\
           'Session':'001',\
           'Configuration':['Task', 'Practice']}

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel

expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Setup files for saving
if not os.path.isdir('../data'+os.path.sep+expName):
    # if this fails (e.g. permissions) we will get an error
    os.makedirs('../data'+os.path.sep+expName)

filename = '../data' + os.path.sep + expName + os.path.sep + \
    '%s_%s_%s' %(expInfo['Participant'], expInfo['date'], \
    expInfo['Configuration'])
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
# this outputs to the screen, not a file
logging.console.setLevel(logging.WARNING)

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# Setup the Window
win = visual.Window(size=(1024, 768), fullscr=FULL_SCREEN, \
    screen=0, allowGUI=False, allowStencil=False, \
    monitor='testMonitor', color='black', colorSpace='rgb')

######################################
# Create the various display methods #
######################################

# Initialize components for Routine "instruct"
instructClock = core.Clock()
instruct_text1 = visual.TextStim(win=win, ori=0, name='instruct_text1',
    text=instruction_text1,
    pos=[0, 0.08], height=0.08, wrapWidth=1.5,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

instruct_text2 = visual.TextStim(win=win, ori=0, name='instruct_text2',
    text=instruction_text2,
    pos=[0, 0], height=0.08, wrapWidth=1.5,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

instruct_text3 = visual.TextStim(win=win, ori=0, name='instruct_text3',
    text=instruction_text3,
    pos=[0, -0.08], height=0.08, wrapWidth=1.5,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

instruct_text4 = visual.TextStim(win=win, ori=0, name='instruct_text4',
    text=instruction_text4,
    pos=[0, -0.16], height=0.08, wrapWidth=1.5,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
stim_text = visual.TextStim(win=win, ori=0, name='stim_text',
    text='nonsense',    font=u'Arial',
    pos=[0, 0], height=0.3, wrapWidth=None,
    color='white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

# Setup the square for the stimulus presentation
sqrVertices = [ [0.2,-0.2], [-0.2,-0.2], [-0.2,0.2], [0.2,0.2] ]
square = visual.ShapeStim(win, 
    lineColor='white',
    lineWidth=2.0, #in pixels
    fillColor='black', #beware, with convex shapes this won't work
    fillColorSpace='rgb',
    vertices=sqrVertices,#choose something from the above or make your own
    closeShape=True,#do you want the final vertex to complete a loop with 1st?
    pos= [0,0], #the anchor (rotaion and vertices are position with respect to this)
    interpolate=True,
    opacity=0.9,
    autoLog=False)

if expInfo['Configuration'] == 'Practice':

    # clock for timing practice cues
    practiceClock = core.Clock()

    # setup text boxes for practice cues
    respond_now_text = visual.TextStim(win=win, ori=0,\
        name='respond_now_text',\
        text='Press Space Now',    font=u'Arial',\
        pos=[0, 0.35], height=0.1, wrapWidth=None,\
        color='white', colorSpace=u'rgb', opacity=1,\
        depth=0.0)

    outcome_text = visual.TextStim(win=win, ori=0, name='outcome_text',
        text='outcome',    font=u'Arial',
        pos=[0, -0.35], height=0.1, wrapWidth=None,
        color='white', colorSpace=u'rgb', opacity=1,
        depth=0.0)

# Initialize components for Routine "Thanks"
ThanksClock = core.Clock()
thanks = visual.TextStim(win=win, ori=0, name='thanks',
    text='Thanks!',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
# to track time remaining of each (non-slip) routine
routineTimer = core.CountdownTimer()  

############################
# Now start the experiment #
############################

#------Prepare to start Routine "instruct"-------
t = 0
instructClock.reset()  # clock 
frameN = -1

# update component parameters for each repeat
ready = event.BuilderKeyResponse()  # create an object of type KeyResponse
ready.status = NOT_STARTED

# keep track of which components have finished
instructComponents = []
instructComponents.append(instruct_text1)
instructComponents.append(instruct_text2)
instructComponents.append(instruct_text3)
instructComponents.append(instruct_text4)
instructComponents.append(ready)

for thisComponent in instructComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instruct"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instructClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *instruct_text* updates
    for thisComponent in instructComponents:
        if hasattr(thisComponent, 'status'):
            if t >= 0.0 and thisComponent.status == NOT_STARTED:
                if hasattr(thisComponent, 'tStart'):
                    thisComponent.tStart = t
                if hasattr(thisComponent, 'frameNStart'):
                    thisComponent.frameNStart = frameN  # exact frame index
                if hasattr(thisComponent, 'setAutoDraw'):
                    thisComponent.setAutoDraw(True)

    # *ready* updates
    if t >= 0.0 and ready.status == NOT_STARTED:
        # keep track of start time/frame for later
        ready.tStart = t  # underestimates by a little under one frame
        ready.frameNStart = frameN  # exact frame index
        ready.status = STARTED
        # keyboard checking is just starting
        event.clearEvents()
    if ready.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the [Esc] key)
    if event.getKeys(["escape"]):
        core.quit()

    # refresh the screen
    # don't flip if this routine is over or we'll get a blank screen
    if continueRoutine:
        win.flip()
    else:
        # this Routine was not non-slip safe so reset non-slip timer
        routineTimer.reset()

#-------Ending Routine "instruct"-------
for thisComponent in instructComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

#-------Stimulus trials-----------------

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method=u'sequential', extraInfo=expInfo,
    originPath=None, trialList=exp_trials, seed=None, name='trials')

thisExp.addLoop(trials)  # add the loop to the experiment

# turn on the square for all trials
square.setAutoDraw(True)

# turn on key logging for all trials
stim_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
stim_response.status = NOT_STARTED
# also clear any previous responses
event.clearEvents()

# initialize statistics
stim_stat_rt = []
stim_stat_hit = 0
stim_stat_miss = 0
stim_stat_false_alarm = 0
stim_stat_target_count = 0

if expInfo['Configuration'] == 'Practice':
    # initialize text boxes for practice cues
    respond_now_text.status=NOT_STARTED
    outcome_text.status=NOT_STARTED

# loop over the trials, presenting each one for .6 seconds and 
# hadnling responses to targets
for thisTrial in trials:

    # not sure why this is here, or if it helps
    currentLoop = trials

    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    routineTimer.add(0.600000)

    trialComponents = []
    trialComponents.append(stim_text)
    #trialComponents.append(stim_response)
    #square.setAutoDraw(val=True)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # set the new stimulus
    stim_text.setText(thisTrial['stim'], log=False)

    # if we this is a target stim, reset the stim_response
    # we are now waiting for keypressed
    if thisTrial['response'] == 1:
        logging.log(level=logging.EXP, msg='Target, waiting for response')
        stim_response.keys = []
        stim_response.tStart = t
        stim_response.frameNStart = frameN
        stim_response.status = STARTED
        stim_response.clock.reset()
        event.clearEvents()
        # count the target
        stim_stat_target_count += 1

        if expInfo['Configuration'] == 'Practice' and \
            stim_stat_target_count <= NUM_PRACTICE_RESPOND_NOW:

            # initialize text boxes for practice cues
            respond_now_text.status=STARTED
            respond_now_text.setAutoDraw(True)

    # if respond_now cue was on, turn it off
    if expInfo['Configuration'] == 'Practice':
        if respond_now_text.status == STARTED:
            if thisTrial['response'] == 0:
                respond_now_text.status=STOPPED
                respond_now_text.setAutoDraw(False)


    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *stim_text* updates
        if t >= 0.0 and stim_text.status == NOT_STARTED:
            # keep track of start time/frame for later
            stim_text.tStart = t  # underestimates by a little under one frame
            stim_text.frameNStart = frameN  # exact frame index
            stim_text.setAutoDraw(True)
        elif stim_text.status == STARTED and t >= (0.0 + .6):
            stim_text.setAutoDraw(False)
        #if stim_text.status == STARTED:  # only update if being drawn
            #stim_text.setText(thisTrial['stim'], log=False)

        # if the response timer is exceeded, turn off response
        # we wouldn't get here if there was a response, hence
        # this is a miss
        if stim_response.status == STARTED and \
            stim_response.clock.getTime() > RESPONSE_TIME:

            logging.log(level=logging.EXP, msg='Timed out before response, miss')
            # we assume that this is a miss, update statistics
            stim_stat_miss += 1
            #
            # we are no longing listening for responses
            stim_response.status = STOPPED
            stim_response.keys = []
            stim_response.clock.reset()
            event.clearEvents()

        # if we have any key presses deal with them
        theseKeys = event.getKeys( keyList=['space'] )
        if len(theseKeys) > 0:
            #
            # get the info corresponding to the keypress
            # we just take the last, to deal with any bounce
            stim_response.keys = theseKeys[-1]
            stim_response.rt = stim_response.clock.getTime()

            # Record the response
            trials.addData('stim_response.keys',stim_response.keys)

            if stim_response.status == STARTED:
                logging.log(level=logging.EXP, msg='Target detected, hit')
                # if we are started, then this is a hit, turn
                # off the response timer so that any further
                # responses will be counted as false alarms
                #
                # add the response time, as this is a legitimate hit
                trials.addData('stim_response.rt', stim_response.rt)
                #
                # update statistics
                stim_stat_rt.append(stim_response.rt)
                stim_stat_hit += 1
                #
                # reset status
                stim_response.status = STOPPED
                stim_response.keys = []
                stim_response.clock.reset()
                event.clearEvents()

                # if we are in practice mode, then tell the user that they
                # got it right
                if expInfo['Configuration'] == 'Practice':
                    practiceClock.reset()
                    outcome_text.setText('Hit')
                    outcome_text.setColor('green')
                    outcome_text.setAutoDraw(True)
                    outcome_text.status == STARTED
            else:
                logging.log(level=logging.EXP, msg='No target present, false alarm')
                # if we are not started, then this is a false alarm
                stim_stat_false_alarm += 1

                # if we are in practice mode, then tell the user that they
                # got it wrong
                if expInfo['Configuration'] == 'Practice':
                    practiceClock.reset()
                    outcome_text.setText('False Alarm')
                    outcome_text.setColor('red')
                    outcome_text.setAutoDraw(True)
                    outcome_text.status == STARTED

        if expInfo['Configuration'] == 'Practice':
            if outcome_text.status == STARTED:
                if practiceClock.getTime() > PRACTICE_OUTCOME_CUE_ONTIME:
                    # if the response is on for longer than the alloted
                    # time, turn it off
                    outcome_text.setAutoDraw(False)
                    outcome_text.status == STOPPED

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the [Esc] key)
        if event.getKeys(["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    thisExp.nextEntry()

# completed 1 repeats of 'trials'
# 
# calculate A' using the procedure in 
#   Snodgrass, J. G., Levy-Berger, G., & Haydon, M. (1985). Human
#    experimental psychology. New York: Oxford University Press
# as recounted in:
#   Stanislaw, H. and Todorov, N. (1999). Calculation of signal 
#     detection theory measures. Behavior Research Methods, 
#     Instruments, & Computes (1), 137-149.
stim_stat_hit_rate = float(stim_stat_hit)/float(stim_stat_target_count)
stim_stat_false_alarm_rate = float(stim_stat_false_alarm)/float(stim_stat_target_count)
stim_stat_miss_rate = float(stim_stat_miss)/float(stim_stat_target_count)

if stim_stat_hit_rate >= stim_stat_false_alarm_rate:
    stim_stat_Aprime = .5 + (stim_stat_hit_rate - stim_stat_false_alarm_rate)\
        *(1+stim_stat_hit_rate - stim_stat_false_alarm_rate)\
        /(4*stim_stat_hit_rate*(1-stim_stat_false_alarm_rate))
else:
    stim_stat_Aprime = .5 + (stim_stat_false_alarm_rate - stim_stat_hit_rate)\
        *(1+stim_stat_false_alarm_rate - stim_stat_hit_rate)\
        /(4*stim_stat_false_alarm_rate*(1-stim_stat_hit_rate))

# output the stats
print stim_stat_rt
print "total targets: ", stim_stat_target_count
print "hits: ",stim_stat_hit
print "misses: ",stim_stat_miss
print "false alarms: ",stim_stat_false_alarm
print "mean rt: ", np.mean(stim_stat_rt)
print "hit rate: ", stim_stat_hit_rate
print "false alarm rate: ",stim_stat_false_alarm_rate
print "A': ",stim_stat_Aprime

logging.log(level=logging.EXP, msg="total targets: %d"%(stim_stat_target_count))
logging.log(level=logging.EXP, msg="hits: %d"%(stim_stat_hit))
logging.log(level=logging.EXP, msg="misses: %d"%(stim_stat_miss))
logging.log(level=logging.EXP, msg="false alarms: %d"%(stim_stat_false_alarm))
logging.log(level=logging.EXP, msg="mean rt: %f"%(np.mean(stim_stat_rt)))
logging.log(level=logging.EXP, msg="hit rate: %f"%(stim_stat_hit_rate))
logging.log(level=logging.EXP, msg="false alarm rate: %f"%(stim_stat_false_alarm_rate))
logging.log(level=logging.EXP, msg="A': %f"%(stim_stat_Aprime))

#------Prepare to start Routine "Thanks"-------
t = 0
ThanksClock.reset()  # clock 
frameN = -1
routineTimer.add(2.000000)
# update component parameters for each repeat
# keep track of which components have finished
ThanksComponents = []
ThanksComponents.append(thanks)
for thisComponent in ThanksComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Thanks"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = ThanksClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *thanks* updates
    if t >= 0.0 and thanks.status == NOT_STARTED:
        # keep track of start time/frame for later
        thanks.tStart = t  # underestimates by a little under one frame
        thanks.frameNStart = frameN  # exact frame index
        thanks.setAutoDraw(True)
    elif thanks.status == STARTED and t >= (0.0 + 2.0):
        thanks.setAutoDraw(False)

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ThanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    # myWin.saveMovieFrames('stimuli.gif')
    # check for quit (the [Esc] key)
    if event.getKeys(["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Thanks"-------
for thisComponent in ThanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
win.close()
core.quit()
