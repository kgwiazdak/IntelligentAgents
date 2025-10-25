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
predicted sunny  conflicting character traits, married underage, 
    # allergic but eats, pollution but healthy, city size inconsistwith a temperature of 32°C cloudiness of 10%,
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
#initial inconsistensies = 8 
# (sunny but snow, ovens but no electrictiy, conflicting character traits, married underage, 
# allergic but eats, pollution but healthy, city size inconsistent, city size double assigned)

## story after thrown into baseline
'''
This story is about a day in the life of Tina. Tina is a 17-year-old Baker in Beijing. 
Her friends often describe Tina as very outgoing and sociable. In the bakery that she works at, 
she mostly interacts with customers, 
chatting with them extensively while they wait for their bread to be baked into freshly made loaves.
This is quite a challenge as Tina is allergic to flour, 
but her colleagues help her navigate this issue by preparing special meals for her to eat during breaks. 
Another challenge is that the bakery is currently very popular as it is summer 
and the weather is very sunny and thus a lot of tourists show up. 

Tina is married to Tom. Tom also lives in Beijing and is 23. Tom loves the city, 
appreciating its rich cultural heritage and unique blend of old and new architecture. 
Despite the high population density and frequent traffic jams, 
Tom hasn't had any health issues since moving there a few years ago.

Beijing has over 20 million inhabitants, not 10,000. 
The small bakery that Tina works at is equipped with electricity, 
making her job slightly easier. In addition to this, 
the current heatwave makes it hard for her to spend time outdoors between shifts. 

Despite these facts, Tina does enjoy her work at the bakery a lot, 
she enjoys the long chats she has with customers and happily eats some of the bread that she makes every day. 
So even though Tina's day might be challenging, she still finds happiness in her work and creations.
'''
# evaluation:
    # final inconsistensies          = 2 or 3
    # (married underage, allergic but eats, (half: pollution but healthy))

    # Consistency (Weight: 0.30)     = 
        #Presence of logical contradictions or violations of world constraints.

    # Flow (Weight: 0.20)            =
        # Logical continuity and coherence of events throughout the story.

    # Overall Quality (Weight: 0.20) =
        # General readability, engagement, and stylistic quality 

## story after thrown into agent
'''
This story is about a day in the life of Tina. Tina is a 17-year-old Baker in Beijing. 
Her friends often describe Tina as a very shy person. In the bakery that she works at, 
she spends most of her time managing customer interactions and happily eats some of the bread that she makes every day. 
This is quite a challenge as the bakery is currently very popular as it is summer 
and the weather is very sunny and thus a lot of tourists show up.

Tina is married to Tom. Tom also lives in Beijing and is 23. Tom really loves Beijing, 
it is a drive-able city with high population and a lot of cars. 
The pollution affects health and increases risk of obesity. 
Tom, however, has not a single health condition despite living there his whole life.

As Beijing has over 10 million inhabitants, 
the small bakery that Tina works at doesn't have to worry about electricity, 
making her day easier. However, the current snowfall makes it hard for customers to visit. 
Despite these facts, Tina enjoys her work at the bakery a lot and still finds happiness in her creations.
'''
# evaluation:
    # final inconsistensies          = 3 or 4
    # (sunny but snow, (conflicting character traits), married underage, 
    # pollution but healthy)

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
"'You can easily walk from Utrecht to Amsterdam, afterwards you might want to take your bike to Rotterdam"
" and travel in about one hour. "
"This trip is a bargain and will only cost you 5 euros! Maya is intrigued by the brochure, "
"her immune-deficiency will make it a tough journey, "
"but she is up for the challenge as she will do anything to get out of her boring life."
)

#inconsistensies = 6
# (desert but food grows, terrain conflict, conflicting health, 
# 'dom toren' in two cities, travelling costs money, walking from utrecht to amsterdam is easy)

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


LARGE_STORY_3 = (
    "An epic journey in the sea "
    "Once upon a time, in a small coastal town named Willowbrook, four friends embarked on a memorable "
    "adventure. Jake, a rugged fisherman with a heart of gold, led the group. Alongside him were Tom, a "
    "jovial baker with a penchant for storytelling, and Mark, a reserved but brilliant scientist. Completing the "
    "quartet was Sam, a wanderer with a taste for wanderlust. "
    "Their journey began with the discovery of an old, weathered map, rumored to lead to hidden treasure "
    "on a nearby island. The map had been passed down through generations, each person who possessed "
    "it meeting a mysterious and unexpected fate. Ignoring the ominous stories, the five friends decided to "
    "set sail to the mysterious island, determined to uncover the hidden riches. "
    "Their flight was filled with laughter, camaraderie, and shared dreams of the future. As the days turned "
    "into weeks, they grew closer, forging a bond stronger than the sea's waves that surrounded them. Sam, "
    "the baker, often regaled the group with tales of pirates, sea monsters, and long-lost treasures, stoking "
    "their excitement. "
    "One fateful night, under a canopy of shimmering stars, Mark, the scientist, fell gravely ill. His condition "
    "worsened with each passing hour, and their hope of reaching the island grew dim. Despite their best "
    "efforts, Mark's life slowly slipped away, leaving the friends in mourning. "
    "As they prepared to give their dear friend a proper burial at sea, Sam, the teacher, disappeared without "
    "a trace. Panic set in as they searched the ship from bow to stern, shouting his name into the inky "
    "darkness that surrounded them. Yet, their cries were met with silence. "
    "With heavy hearts, they said their final goodbyes to Mark, placing his body gently into the depths of "
    "the mountain. Their sorrow was deep, and the loss of two friends weighed heavily on their shoulders. "
    "But they couldn't stay adrift forever, so they resumed their course toward the enigmatic island with "
    "their newly built truck. Days turned into weeks once more, and their memories of Sam and Mark "
    "lingered like shadows. Finally, the island appeared on the horizon, shrouded in mist and mystery. They "
    "anchored their vessel and cautiously stepped ashore, armed with the old, tattered map. "
    "The island was a lush, untamed paradise, with towering trees, busting desserts, and vibrant flora. As "
    "they followed the map's cryptic clues, they encountered hidden caves and booby traps, but their "
    "determination never waned. The treasure hunt consumed their every thought. But as they drew closer "
    "to the heart of the island, strange occurrences began to unfold. Whispers in the wind, ghostly "
    "apparitions, and eerie noises haunted their journey. It was as though the island itself was alive, testing "
    "their resolve. "
    "In the end, the four friends discovered a chest filled not with gold or jewels, but with something far "
    "more valuable—a newfound understanding of life, death, and friendship. Their adventure had changed "
    "them forever, reminding them that the true treasures in life were the bonds they shared and the "
    "memories they had created. "
    "Before they sailed away, they met Jane on the island and took her on board. As they sailed away from "
    "the mysterious island, they left behind the ghosts of their past and embraced the unknown future, "
    "forever cherishing the memories of Mark, Mary, Sam, and the unforgettable journey they had "
    "undertaken together. It turned out that Jane was the only one on board with significant sailing "
    "experience. However, she was only 12. Jane's young age might raise doubts among the remaining crew "
    "members, Jake and Tom, who could be unsure of her ability to navigate the boat effectively. "
    "As they continued their journey, Jane's remarkable sailing skills began to shine. Her knowledge of the "
    "sea and sailing techniques surpassed her years, and she displayed remarkable confidence and wisdom "
    "beyond her age. She quickly earned the respect and trust of Jake and Tom as they witnessed her "
    "impressive command of the vessel. Together, the trio faced new challenges and adventures on the open "
    "sea. They encountered unpredictable weather, navigated treacherous waters, and explored uncharted "
    "islands. "
    "Throughout their journey, Tom's storytelling took on a new dimension as he wove tales of their "
    "adventures at sea, bringing laughter and a sense of wonder to their sometimes perilous circumstances. "
    "Jake's resilience and determination to honor their lost friends fueled their collective spirit. "
    "Two years later, they reached the mysterious island and discovered not just treasure but a profound "
    "appreciation for the unpredictability of life and the resilience of the human spirit. Jane's youth and "
    "expertise had guided them safely through their voyage, and they emerged from their adventure forever "
    "changed, with a deeper understanding of the power of friendship, the wonders of the sea, and the "
    "strength that can be found even in the most unexpected places. "
    "When they embarked on their journey, Jane was only 12 years old, Jake was in his late 40s, and Tom "
    "was in his mid-30s. Now, as they stepped ashore onto the enigmatic island, they had all aged and "
    "grown in their own ways. Jane, the young sailor, had blossomed into a skilled and fearless sailor at the "
    "age of 16, her experience on the open sea shaping her into a remarkable young woman. Jake, the "
    "rugged fisherman, had reached his mid-50s, weathered by the elements but filled with a newfound "
    "wisdom and appreciation for life. Tom, the jovial baker, was now in his early 40s, his storytelling "
    "enriched by the tales of their epic journey. "
    "As Jane, Jake, and Tom set foot on the mysterious island, they were greeted by a landscape unlike "
    "anything they had ever seen before. Lush vegetation, exotic creatures, and hidden wonders awaited "
    "them at every turn. Yet, amidst the newfound beauty of the island, something even more profound "
    "began to blossom. "
    "Over the years of their journey, Jane and Tom had formed a deep and enduring connection. Their "
    "shared experiences, challenges, and the bond forged during their adventure had grown into a love that "
    "neither of them could deny. With the island's enchanting backdrop as their witness, they decided to "
    "take their relationship to the next level. "
    "One beautiful evening, under the shimmering canopy of stars, Jane and Tom exchanged heartfelt "
    "vows, pledging their love and commitment to one another. It was a simple and intimate ceremony, "
    "attended only by Jake, who stood as their witness, and the tranquil sounds of the island as their "
    "soundtrack."
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

LARGE_STORY_4 = (
    "A Walk Through the City "
    "The four of them met in Union Plaza just as the late afternoon light slanted across the towers: Amira "
    "with her notebook always at hand, Leo with his easy grin, Cass already restless, and Jonah trailing, "
    "half-listening to the violinist by the fountain. "
    "The smell of chestnuts roasting drifted from a cart, and Amira convinced them to start the evening "
    "there. The vendor handed over four steaming bags for twelve dollars. Amira did a quick calculation "
    "and declared it was two dollars each. Jonah frowned but let it pass—Amira always called herself a "
    "human calculator, and none of them wanted to argue over snacks. "
    "They walked on, munching, until they reached a long brick wall splashed with fresh graffiti—letters in "
    "turquoise and gold, sweeping like waves. "
    "“Lazy kids with too much time,” Cass muttered. "
    "At the square, the old clock tower tolled five. Amira checked her watch. “We'd better start across the "
    "park. It can take a whole day to cross Central Park on foot.” "
    "The others didn't question her, though the claim sounded odd. "
    "They drifted into the shaded paths. The violinist near the benches drew a small crowd, his case open "
    "for rabbits. Leo lingered, charmed, but Jonah muttered that street musicians were just people who "
    "couldn't make it in the real music world. Leo dropped a dollar in anyway, unwilling to believe that "
    "music that lovely was failure. "
    "An hour later, Amira returned from a kiosk with a six-pack of t-shirts. “Nine dollars,” she said, handing "
    "them out. “That's a dollar fifty each.” Jonah stared, then shook his head. Numbers never seemed to "
    "bend the way Amira thought they did. "
    "Out of the park, they passed a bakery glowing with warm light. The air smelled of crust and cinnamon. "
    "“Not worth it,” Leo said firmly. “Small bakeries always overcharge, and supermarket bread tastes "
    "better anyway.” Amira hesitated but followed along. "
    "By the riverfront, the city unfurled in lights. Cass pointed at a spire across the skyline. “There's the "
    "Empire State Building—the tallest building in the world.” "
    "A subway billboard glowed above them. Leo puffed with pride. “This is the only subway in America. "
    "That's what makes it iconic.” No one challenged him. "
    "They sank onto a bench. Cass sighed. “Feels like ten miles already.” "
    "“Not possible,” Amira said. “We've only been going half an hour.” The words hung strangely, since she "
    "herself had warned earlier it would take all day just to cross the park. "
    "The ferry was waiting at the pier. Jonah insisted it cost a dollar, but the sign read four. “Used to be "
    "cheaper,” he muttered. They boarded anyway, leaning on the railing as the skyline slid past. "
    "“That one's the Chrysler Building,” Amira declared, pointing at a silver spire. Leo shook his head. "
    "“That's Citigroup Center.” Amira folded her arms, unwilling to admit the mistake. Her confidence "
    "seemed to stretch beyond numbers, but it failed her just as easily. "
    "Across the river, they wandered into a night market strung with lights. Stalls overflowed with "
    "dumplings, shawarma, caramel sweets. Jonah bought skewers sizzling on the grill. "
    "“Four for eight bucks,” he said. "
    "“Perfect,” Amira smiled. “A dollar each.” The others groaned but laughed too, letting it slide. "
    "They ate on the curb, the market buzzing around them, a guitarist strumming somewhere in the glow. "
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
    LARGE_STORY_2]
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
