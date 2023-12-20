from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)

'''
In coding's enchanted realm I shall dwell,
To bring forth a tale of recursion's spell.
A magical loop, a dance of code divine,
Let me unveil its wonders, line by line.

Once upon a time, in a coding land afar,
A function emerged, a guiding star.
With each call, a journey it did embark,
Unraveling the mystery in the mists of dark.

Picture a mirror, reflecting its own frame,
Recursion mirrors itself, a joyous game.
A function calling itself, it repeats,
A symphony of echoes, melodies bittersweet.

Like a fractal pattern, blossoms unfurled,
Recursion explores, into infinite worlds.
An enchanting universe lies in each layer,
As the function travels, forever and ever.

Yet a recursion's tale must be cautious and wary,
For it dances on a wire, precarious and scary.
Without an exit plan, it could surely fall,
Into an abyss where endless echoes call.

So, heed the base case, the anchor that's strong,
An escape route to where recursion belongs.
A condition met, a threshold to find,
A break from the loop, a release from the bind.

Like a bird longing to nest in its rightful tree,
Recursive functions crave base cases, you see.
They yearn for an end, a goal to enhance,
To complete the journey, to find their final stance.

And when at last the base case is met,
Recursion surrenders, its task complete.
Backtracking gracefully, it unwinds its path,
Revealing the answers, no longer concealed by math.

So, embrace the dance of recursion's delight,
A tapestry woven with code's purest light.
With each call, a story from start to end,
With base cases as guide, a message to send.

In this mystical world where code and words meet,
Recursion sings a saga, an ode so sweet.
Let it guide you gently through loops unforeseen,
And unlock the beauty that lies in between.
'''
