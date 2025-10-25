STORY_1 = "Maria is a 25-year-old Baker in Florence. She works in a bakery, which requires an Oven, Flour, and Water. However, Maria is allergic to flour. Despite this, she eats bread daily."

STORY_2 = "Tom lives in Beijing, a DrivableCity with high population and many cars. The city has Pollution, which affects health and increases risk of obesity. Tom, however, is described as having no health conditions despite living there his whole life."

STORY_3 = "Alice (17) and Bob (19) say they are married. Their friends congratulate them on their wedding last week."

STORY_4 = "Luca is described as 'very reserved.' [cite_start]In the same paragraph, he is said to chat with at least six different people every day at the office."

STORY_5 = "Tina works as a baker in a tiny shop that has no oven and never uses electricity."

STORY_6 = "Marco is allergic to flour but says he eats bread and pizza every day without issues."

STORY_7 = "Alice medical file lists both Anemia and Cancer as current diagnoses."

STORY_8 = "Hillsburg is proudly marketed as a walkable city; tourism brochures emphasize its steep mountain terrain within city limits."

STORY_9 = "A brochure claims 'The Empire State Building is located in New York and also in Los Angeles.'"

STORY_10 = "The 'MetroX' is presented as a subway system that does not belong to any city."

STORY_11 = "Riverton is labeled a LargeCity with 50,000 inhabitants."

STORY_12 = "The dataset states that Utrecht is adjacent to Amsterdam; no statement is given for Amsterdam."

STORY_13 = "A small Sahara desert village is famous for its fruit production. Every year, farmers harvest bananas, peaches, and rice from the naturally irrigated desert plains."

STORY_14 = """In Dubai, citizens and tourists were surprised to see a heavy storm
during midsummer, even though the temperature was a comfortable 21°C.
Tourists wandered around without umbrellas because the forecast
predicted sunny with a temperature of 32°C cloudiness of 10%,
and calm wind speeds. Meanwhile, a snow storm swept through the
[cite_start]city which made a lot of students very unhappy."""

STORY_15 = """Anna decided to walk from Utrecht to Amsterdam in 2 hours. Afterwards
she cycled to Middelburg in 1 hour. The distance recorded was
400 and 1500 km. She got a great bargain on the trip and only spent 5
[cite_start]euros!"""

LARGE_STORY_1 = (
"This story is about a day in the life of Tina. Tina is a 17-year-old Baker in Beijing. "
"Her friends often describe Tina as a very shy person. "
"In the bakery that she works with she mostly works with the ovens and turns flour into dough, which is then baked into bread. "
"This is quite a challenge as Tina is allergic to flour. Another challenge is that the bakery is currently very popular "
"as it is summer and the weather is very sunny and thus a lot of tourists show up. "
"Tina is married to Tom. Tom also lives in Beijing and is 23. Tom really loves Beijing, "
"it is a drive-able city with high population and a lot of cars cars. The pollution affects health and increases risk of obesity. "
"Tom, however, has not a single health condition despite living there his whole life. "
"As Beijing is a small city with 10.000 inhabitants, the small bakery that Tina works at doesn't have electricity, "
"which makes Tina's day extra challenging. In addition to this the current snowfall makes it hard for her to drive to work. "
"Despite these facts, Tina does enjoy her work at the bakery a lot, she enjoys the long chats she has with customers "
"and happily eats some of the bread that she makes every day. So even though Tina's day might be challenging, "
"she still finds happiness in her work and creations."
)
#initial inconsistensies = 

## story after thrown into baseline
'''
This story is about a day in the life of Tina. 
Tina is a 17-year-old Baker in Beijing. 
Her friends often describe Tina as a very shy person who keeps to herself at the bakery that she works with. 
She mostly focuses on tasks that don't require direct interaction, like preparing ingredients for the ovens, 
which then turn flour into dough, baked into bread.
This is quite a challenge as Tina is allergic to flour. 
Another challenge is that the bakery is currently very popular as it is summer and the weather is very sunny, 
thus drawing in a lot of tourists. 
The high volume of customers makes it difficult for Tina to keep up with her tasks while also maintaining personal space.

Tina is married to Tom. 
Tom also lives in Beijing and is 23. He really loves Beijing, 
describing its unique blend of old and new, 
and the fact that it's a drive-able city despite having high population density and many cars on the roads.
The pollution affects health and increases risk of obesity. 
However, Tom has not developed any health conditions despite living in Beijing his whole life. 
In fact, he is known for his active lifestyle, often exploring new neighborhoods and trying local food.

As Beijing's total population is over 10 million, not 10,000, the small bakery that Tina works at has electricity, 
making her day a bit easier. However, the recent snowfall still makes it harder for her to drive to work. 
Despite these challenges, Tina enjoys her work at the bakery and finds happiness in creating delicious bread.

She particularly enjoys interacting with customers who appreciate her baking skills 
and often share stories of their favorite Beijing foods with her. In return, 
Tina happily shares samples of her latest creations, finding joy in the connections she makes through her work.
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

## story after thrown into agent
'''
This story is about a day in the life of Tina. Tina is a 17-year-old Baker in Beijing. 
Her friends often describe Tina as very outgoing and friendly. 
In the bakery that she works with she mostly works with the ovens and turns flour into dough, which is then baked into bread.

This is quite a challenge as Tina is allergic to gluten, not just flour, 
but also has trouble with certain types of yeast used in the baking process. 
Another challenge is that the bakery is currently very popular as it is summer and the weather is very sunny 
and thus a lot of tourists show up.

Tina is married to Tom.
Tom also lives in Beijing and is 23. 
Tom really loves Beijing, it is a drive-able city with high population and a lot of cars. 
The pollution affects health and increases risk of obesity. Tom, however, 
has not a single health condition despite living there his whole life.

As Beijing has over 20 million inhabitants, 
the small bakery that Tina works at uses electricity to power its ovens, 
which makes her day less challenging. 
In addition to this the current weather conditions don't make it hard for her to drive to work. 
Despite these facts, Tina does enjoy her work at the bakery a lot, 
she enjoys the long chats she has with customers and happily eats some of the bread that she makes every day.

So even though Tina's day might be challenging, she still finds happiness in her work and creations.
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 




LARGE_STORY_2 = (
"Maya lives in a small Sahara desert village which is famous for its fruit production. "
"She works here as a farmer and every year she harvests bananas, peaches, and rice from the naturally irrigated desert plains. "
"She is kind of tired of this life, it is stale and boring, and she is looking for something new. In addition to this, "
"Maya is diagnosed with Anaemia, which makes her work more difficult. One day she walks past a travel agency, "
"she goes inside and sees a travel brochure here, she would love to leave the country so she looks inside. "
"The first brochure describes Utrecht, a beautiful walk-able city in the Netherlands. For activities, "
"it recommends hiking its steep mountain terrain, visiting the 'Dom toren' which can only be found in Utrecht and Amsterdam, "
"and visiting the adjacent city: Amsterdam. As a travel plan to Amsterdam, the brochure describes: "
"You can walk the 400 kilometers from Utrecht to Amsterdam in 2 hours. "
"Afterwards you might want to take your bike to Rotterdam and travel the 1500 kilometers in about one hour. "
"This trip is a bargain and will only cost you 5 euros! Maya is intrigued by the brochure, "
"her immune-deficiency will make it a tough journey, "
"but she is up for the challenge as she will do anything to get out of her boring life."
)

#inconsistensies = 
# story after thrown into baseline
'''
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

# story after thrown into agent
'''
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 


LARGE_STORY_3 = ""
#inconsistensies = 
# story after thrown into baseline
'''
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

# story after thrown into agent
'''
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

LARGE_STORY_4 = ""
#inconsistensies = 
# story after thrown into baseline
'''
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

# story after thrown into agent
'''
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

LARGE_STORY_5 = ""
#inconsistensies = 
# story after thrown into baseline
'''
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

# story after thrown into agent
'''
'''
# evaluation:
    # final inconsistensies          =

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

ALL_SCENARIOS = [
    LARGE_STORY_1]
'''
    STORY_1,
    STORY_2,
    STORY_3,
    STORY_4,
    STORY_5,
    STORY_6,
    STORY_7,
    STORY_8,
    STORY_9,
    STORY_10,
    STORY_11,
    STORY_12,
    STORY_13,
    STORY_14,
    STORY_15,
]
'''
