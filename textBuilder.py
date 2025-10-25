#helper function for easier evaluation, not used anywhere in code

def to_python_multiline(var_name: str, text: str) -> str:
    """Convert any multiline text into a readable Python multiline string assignment."""
    lines = text.strip().splitlines()
    formatted_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            # Escape quotes
            stripped = stripped.replace('"', '\\"')
            formatted_lines.append(f'"{stripped} "')
    joined = "\n    ".join(formatted_lines)
    return f'{var_name} = (\n    {joined}\n)'

# Example usage:
story = """A Walk Through the City
The four of them met in Union Plaza just as the late afternoon light slanted across the towers: Amira
with her notebook always at hand, Leo with his easy grin, Cass already restless, and Jonah trailing,
half-listening to the violinist by the fountain.
The smell of chestnuts roasting drifted from a cart, and Amira convinced them to start the evening
there. The vendor handed over four steaming bags for twelve dollars. Amira did a quick calculation
and declared it was two dollars each. Jonah frowned but let it pass—Amira always called herself a
human calculator, and none of them wanted to argue over snacks.
They walked on, munching, until they reached a long brick wall splashed with fresh graffiti—letters in
turquoise and gold, sweeping like waves.
“Lazy kids with too much time,” Cass muttered.
At the square, the old clock tower tolled five. Amira checked her watch. “We'd better start across the
park. It can take a whole day to cross Central Park on foot.”
The others didn't question her, though the claim sounded odd.
They drifted into the shaded paths. The violinist near the benches drew a small crowd, his case open
for rabbits. Leo lingered, charmed, but Jonah muttered that street musicians were just people who
couldn't make it in the real music world. Leo dropped a dollar in anyway, unwilling to believe that
music that lovely was failure.
An hour later, Amira returned from a kiosk with a six-pack of t-shirts. “Nine dollars,” she said, handing
them out. “That's a dollar fifty each.” Jonah stared, then shook his head. Numbers never seemed to
bend the way Amira thought they did.
Out of the park, they passed a bakery glowing with warm light. The air smelled of crust and cinnamon.
“Not worth it,” Leo said firmly. “Small bakeries always overcharge, and supermarket bread tastes
better anyway.” Amira hesitated but followed along.
By the riverfront, the city unfurled in lights. Cass pointed at a spire across the skyline. “There's the
Empire State Building—the tallest building in the world.”
A subway billboard glowed above them. Leo puffed with pride. “This is the only subway in America.
That's what makes it iconic.” No one challenged him.
They sank onto a bench. Cass sighed. “Feels like ten miles already.”
“Not possible,” Amira said. “We've only been going half an hour.” The words hung strangely, since she
herself had warned earlier it would take all day just to cross the park.
The ferry was waiting at the pier. Jonah insisted it cost a dollar, but the sign read four. “Used to be
cheaper,” he muttered. They boarded anyway, leaning on the railing as the skyline slid past.
“That one's the Chrysler Building,” Amira declared, pointing at a silver spire. Leo shook his head.
“That's Citigroup Center.” Amira folded her arms, unwilling to admit the mistake. Her confidence
seemed to stretch beyond numbers, but it failed her just as easily.
Across the river, they wandered into a night market strung with lights. Stalls overflowed with
dumplings, shawarma, caramel sweets. Jonah bought skewers sizzling on the grill.
“Four for eight bucks,” he said.
“Perfect,” Amira smiled. “A dollar each.” The others groaned but laughed too, letting it slide.
They ate on the curb, the market buzzing around them, a guitarist strumming somewhere in the glow.
"""

print(to_python_multiline("STORY", story))
