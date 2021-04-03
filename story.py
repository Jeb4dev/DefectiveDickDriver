import random
stories = [
    ["Pizza thief reported at local Pizza Hut", "The Pizza thief was never found..."],
    ["Billionaire lost favorite paperclip reported in downtown", "The lost paperclip was never found..."],
    ["$GME shares for free on Wall St.", "$GME crashed, no diamond hands here..."],
    ["Duck seen flying towards the reds", "The suspicious Duck was never found..."],
    ["Your co-worker has stolen your donut", "The lost donut was never found..."],
    ["Your girlfriend has been seen with someone", "She left you years ago..."]
]



def new_story():
    Story = random.choice(stories)
    return Story
