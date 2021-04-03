import random
stories = [
    ["Pizza thief committed at local Pizza Hut", "The Pizza thief was never found..."],
    ["Lost paperclip reported in downtown", "The lost paperclip was never found..."],
    ["$GME shares for free in wall st.", "You never found free shares of $GME..."],
    ["Duck seen flying towards the reds", "The suspicious Duck was never found..."],
    ["Your co-worker has stolen your donut", "The lost donut was never found..."],
    ["Your girlfriend has been seen with someone", "The girlfriend left u..."]
]

Story = False


def new_story():
    global Story
    Story = random.choice(stories)


def get_story():
    global Story
    if not Story:
        Story = random.choice(stories)
    return Story