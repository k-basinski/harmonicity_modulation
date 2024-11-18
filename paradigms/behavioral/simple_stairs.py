from psychopy import core, visual, data, event, sound, prefs
import numpy as np
import pandas as pd
import inharmonicon as ih


prefs.hardware["audioLib"] = ["PTB"]
prefs.hardware["audioLatencyMode"] = 3
event.globalKeys.add(key="q", modifiers=["ctrl"], func=core.quit)

staircase = data.StairHandler(startVal = 20.0,
                          stepType = 'lin', stepSizes=[1],
                          nUp=1, nDown=3,  # will home in on the 80% threshold
                          nTrials=1)


win = visual.Window(fullscr=True)
message = visual.TextBox2(win, text='', pos=(0, 0), letterHeight=.05, alignment='center')
win.flip()
responses, targets, increments = [], [], []
rng = np.random.default_rng()

def beep(increment):
    """Beep twice with increments and return correct response. """
    base_f = 500
    
    # decide which sound is higher
    which_higher = rng.choice(['first', 'second'])

    if which_higher == 'first':
        s1f = base_f + increment
        s2f = base_f
    elif which_higher == 'second':
        s1f = base_f
        s2f = base_f + increment
    
    s1h = ih.Harmonics(s1f)
    s2h = ih.Harmonics(s2f)
    s1 = ih.Sound(s1h, length=.07)
    s2 = ih.Sound(s2h, length=.07)
    # beep
    core.wait(.1)
    s1.play()
    core.wait(.5)
    s2.play()
    core.wait(.3)
    
    return which_higher


for increment in staircase:
    message.text = f'Jeśli pierwszy dźwięk wyżej, <strzałka w lewo>.\nJeśli drugi dźwięk wyżej, <strzałka w prawo>.\n\nIncrement: {increment}...'
    message.draw()
    win.flip()
    target = beep(increment)

    # get response
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='left':
                if target=='first': 
                    thisResp = 1  # correct
                else: 
                    thisResp = -1  # incorrect
            elif thisKey=='right':
                if target== 'second': 
                    thisResp = 1  # correct
                else: 
                    thisResp = -1  # incorrect
            elif thisKey in ['q', 'escape']:
                core.quit()  # abort experiment
        
        event.clearEvents()  # clear other (eg mouse) events - they clog the buffer
    responses.append(allKeys[0])
    targets.append(target)
    increments.append(increment)

    # add the data to the staircase so it can calculate the next level
    staircase.addData(thisResp)
    print(responses)


dfd = {
    'responses': responses,
    'targets': targets,
    'increments': increments
}
df = pd.DataFrame(dfd, index=np.arange(len(responses)))
df.to_csv('output.csv')