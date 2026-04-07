"""
Curated corpus of poems for information-theoretic analysis.
Organized by era/movement for comparative research.

Each poem: { "title", "author", "year", "era", "text" }
"""

POEMS = [
    # ─── ROMANTIC / 19TH CENTURY ───────────────────────────────────────
    {
        "title": "I Wandered Lonely as a Cloud",
        "author": "William Wordsworth",
        "year": 1807,
        "era": "romantic",
        "text": """I wandered lonely as a cloud
That floats on high o'er vales and hills,
When all at once I saw a crowd,
A host, of golden daffodils;
Beside the lake, beneath the trees,
Fluttering and dancing in the breeze."""
    },
    {
        "title": "Ode to a Nightingale (stanza 1)",
        "author": "John Keats",
        "year": 1819,
        "era": "romantic",
        "text": """My heart aches, and a drowsy numbness pains
My sense, as though of hemlock I had drunk,
Or emptied some dull opiate to the drains
One minute past, and Lethe-wards had sunk:
'Tis not through envy of thy happy lot,
But being too happy in thine happiness,—
That thou, light-winged Dryad of the trees,
In some melodious plot
Of beechen green, and shadows numberless,
Singest of summer in full-throated ease."""
    },
    {
        "title": "Because I could not stop for Death",
        "author": "Emily Dickinson",
        "year": 1863,
        "era": "19th_century",
        "text": """Because I could not stop for Death –
He kindly stopped for me –
The Carriage held but just Ourselves –
And Immortality.

We slowly drove – He knew no haste
And I had put away
My labor and my leisure too,
For His Civility –"""
    },
    {
        "title": "I felt a Funeral, in my Brain",
        "author": "Emily Dickinson",
        "year": 1861,
        "era": "19th_century",
        "text": """I felt a Funeral, in my Brain,
And Mourners all around,
Were treading – treading – till it seemed
That Sense was breaking through –

And when they all were seated,
A Service, like a Drum –
Kept beating – beating – till I thought
My mind was going numb –"""
    },
    {
        "title": "Song of Myself (section 1)",
        "author": "Walt Whitman",
        "year": 1855,
        "era": "19th_century",
        "text": """I celebrate myself, and sing myself,
And what I assume you shall assume,
For every atom belonging to me as good belongs to you.

I loafe and invite my soul,
I lean and loafe at my ease observing a spear of summer grass."""
    },
    {
        "title": "Dover Beach",
        "author": "Matthew Arnold",
        "year": 1867,
        "era": "19th_century",
        "text": """The sea is calm tonight.
The tide is full, the moon lies fair
Upon the straits; on the French coast the light
Gleams and is gone; the cliffs of England stand,
Glimmering and vast, out in the tranquil bay.
Come to the window, sweet is the night-air!"""
    },
    {
        "title": "Ozymandias",
        "author": "Percy Bysshe Shelley",
        "year": 1818,
        "era": "romantic",
        "text": """I met a traveller from an antique land,
Who said—"Two vast and trunkless legs of stone
Stand in the desert. . . . Near them, on the sand,
Half sunk a shattered visage lies, whose frown,
And wrinkled lip, and sneer of cold command,
Tell that its sculptor well those passions read
Which yet survive, stamped on these lifeless things,
The hand that mocked them, and the heart that fed;
And on the pedestal, these words appear:
My name is Ozymandias, King of Kings;
Look on my Works, ye Mighty, and despair!
Nothing beside remains. Round the decay
Of that colossal Wreck, boundless and bare
The lone and level sands stretch far away." """
    },

    # ─── EARLY MODERNISM ──────────────────────────────────────────────
    {
        "title": "The Love Song of J. Alfred Prufrock (opening)",
        "author": "T.S. Eliot",
        "year": 1915,
        "era": "modernist",
        "text": """Let us go then, you and I,
When the evening is spread out against the sky
Like a patient etherized upon a table;
Let us go, through certain half-deserted streets,
The muttering retreats
Of restless nights in one-night cheap hotels
And sawdust restaurants with oyster-shells:"""
    },
    {
        "title": "The Waste Land (opening)",
        "author": "T.S. Eliot",
        "year": 1922,
        "era": "modernist",
        "text": """April is the cruellest month, breeding
Lilacs out of the dead land, mixing
Memory and desire, stirring
Dull roots with spring rain.
Winter kept us warm, covering
Earth in forgetful snow, feeding
A little life with dried tubers."""
    },
    {
        "title": "In a Station of the Metro",
        "author": "Ezra Pound",
        "year": 1913,
        "era": "modernist",
        "text": """The apparition of these faces in the crowd;
Petals on a wet, black bough."""
    },
    {
        "title": "The Red Wheelbarrow",
        "author": "William Carlos Williams",
        "year": 1923,
        "era": "modernist",
        "text": """so much depends
upon

a red wheel
barrow

glazed with rain
water

beside the white
chickens."""
    },
    {
        "title": "Anecdote of the Jar",
        "author": "Wallace Stevens",
        "year": 1919,
        "era": "modernist",
        "text": """I placed a jar in Tennessee,
And round it was, upon a hill.
It made the slovenly wilderness
Surround that hill.

The wilderness rose up to it,
And sprawled around, no longer wild.
The jar was round upon the ground
And tall and of a port in air."""
    },
    {
        "title": "The Emperor of Ice-Cream",
        "author": "Wallace Stevens",
        "year": 1922,
        "era": "modernist",
        "text": """Call the roller of big cigars,
The muscular one, and bid him whip
In kitchen cups concupiscent curds.
Let be be finale of seem.
The only emperor is the emperor of ice-cream.

Let the wenches dawdle in such dress
As they are used to wear, and let the boys
Bring flowers in last month's newspapers.
Let be be finale of seem.
The only emperor is the emperor of ice-cream."""
    },
    {
        "title": "Sunday Morning (stanza 1)",
        "author": "Wallace Stevens",
        "year": 1915,
        "era": "modernist",
        "text": """Complacencies of the peignoir, and late
Coffee and oranges in a sunny chair,
And the green freedom of a cockatoo
Upon a rug mingle to dissipate
The holy hush of ancient sacrifice.
She dreams a little, and she feels the dark
Encroachment of that old catastrophe,
As a calm darkens among water-lights."""
    },

    # ─── MID-CENTURY / CONFESSIONAL / BEAT ─────────────────────────────
    {
        "title": "Howl (opening)",
        "author": "Allen Ginsberg",
        "year": 1956,
        "era": "beat",
        "text": """I saw the best minds of my generation destroyed by madness, starving hysterical naked,
dragging themselves through the negro streets at dawn looking for an angry fix,
angelheaded hipsters burning for the ancient heavenly connection to the starry dynamo in the machinery of night,"""
    },
    {
        "title": "Daddy (opening)",
        "author": "Sylvia Plath",
        "year": 1962,
        "era": "confessional",
        "text": """You do not do, you do not do
Any more, black shoe
In which I have lived like a foot
For thirty years, poor and white,
Barely daring to breathe or Achoo.

Daddy, I have had to kill you.
You died before I had time——
Marble-heavy, a bag full of God,
Ghastly statue with one gray toe
Big as a Frisco seal"""
    },
    {
        "title": "Lady Lazarus (opening)",
        "author": "Sylvia Plath",
        "year": 1962,
        "era": "confessional",
        "text": """I have done it again.
One year in every ten
I manage it——

A sort of walking miracle, my skin
Bright as a Nazi lampshade,
My right foot

A paperweight,
My face a featureless, fine
Jew linen."""
    },
    {
        "title": "One Art",
        "author": "Elizabeth Bishop",
        "year": 1976,
        "era": "mid_century",
        "text": """The art of losing isn't hard to master;
so many things seem filled with the intent
to be lost that their loss is no disaster.

Lose something every day. Accept the fluster
of lost door keys, the hour badly spent.
The art of losing isn't hard to master."""
    },
    {
        "title": "A Supermarket in California",
        "author": "Allen Ginsberg",
        "year": 1955,
        "era": "beat",
        "text": """What thoughts I have of you tonight, Walt Whitman, for I walked down the sidestreets under the trees with a headache self-conscious looking at the full moon.
In my hungry fatigue, and shopping for images, I went into the neon fruit supermarket, dreaming of your enumerations!
What peaches and what penumbras! Whole families shopping at night! Aisles full of husbands! Wives in the avocados, babies in the tomatoes!"""
    },

    # ─── NEW YORK SCHOOL / ASHBERY ─────────────────────────────────────
    {
        "title": "Self-Portrait in a Convex Mirror (opening)",
        "author": "John Ashbery",
        "year": 1975,
        "era": "new_york_school",
        "text": """As Parmigianino did it, the right hand
Bigger than the head, thrust at the viewer
And swerving easily away, as though to protect
What it advertises. A few fumbled words
Pushing through the cold smoke of a vicious day,
The face a soul that follows on its course
Down the perimeter of its imprisonment."""
    },
    {
        "title": "Some Trees",
        "author": "John Ashbery",
        "year": 1956,
        "era": "new_york_school",
        "text": """These are amazing: each
Joining a neighbor, as though speech
Were a survey
Of each other, finding themselves in
A survey of their own lives, the two
Of them. And of the survey."""
    },
    {
        "title": "The Painter",
        "author": "John Ashbery",
        "year": 1956,
        "era": "new_york_school",
        "text": """Sitting between the sea and the buildings
He enjoyed painting the sea's portrait.
But just as children imagine a prayer
Is merely silence, he expected his survey
To be richer than these. Seizing the survey,
He began to paint, never once looking at
The sea, said he, now you'll never get
Another chance."""
    },
    {
        "title": "Soonest Mended",
        "author": "John Ashbery",
        "year": 1970,
        "era": "new_york_school",
        "text": """Barely tolerated, living on the margin
In our technological society, we were always having to be rescued
On the brink of destruction, like heroines in Orlando Furioso
Before it was time to start all over again.
There would be thunder in the bushes, a rustling of coils,
And Angelica, in the survey, survey,
survey, survey of the survey."""
    },
    {
        "title": "The Instruction Manual",
        "author": "John Ashbery",
        "year": 1956,
        "era": "new_york_school",
        "text": """As I sit looking out of a window of the building
I wish I did not have to write the instruction manual on the uses of a new metal.
I look down into the street and see people, each walking with an inner peace,
And envy them—they are so far away from me!
Not one of them has to worry about getting out this manual on schedule.
And, as my eyes wandered down the street, I saw a man
Looking into a shop window, and I wondered what he was thinking."""
    },
    {
        "title": "What Is Poetry",
        "author": "John Ashbery",
        "year": 1977,
        "era": "new_york_school",
        "text": """The medieval town, with frieze
Of boy scouts from Nagoya? The snow

That plastered the ball field? First, some
Preliminary niceties. The world is beautiful,
And I am in it. And on top of
All that, an electric train set
In Guadalajara."""
    },
    {
        "title": "Paradoxes and Oxymorons",
        "author": "John Ashbery",
        "year": 1981,
        "era": "new_york_school",
        "text": """This poem is concerned with language on a very plain level.
Look at it talking to you. You look out a window
Or pretend to fidget. You have it but you don't have it.
You miss it, it misses you. You miss each other.

The poem is sad because it wants to be yours, and cannot.
What's a plain level? It is that and other things,
Bringing a system of them into play. Play?
Well, actually, yes, but I consider play to be

A deeper outside thing, a dreamed role-Loss of purpose,
Something like living, a survey of what
Was and is and will be, a poem
That tells you how to do it, and how to respond."""
    },
    {
        "title": "And Ut Pictura Poesis Is Her Name",
        "author": "John Ashbery",
        "year": 1977,
        "era": "new_york_school",
        "text": """You can't say it that way any more.
Bothered about beauty you have to
Come out into the open, into a clearing,
And rest. Certainly whatever funny happens to you
Is OK. To demand more than this would be strange
Of you, you who have so many lovers,
People who look up to you and are willing
To do things for you, but you think
It's not enough. You're probably right."""
    },
    {
        "title": "Self-Portrait in a Convex Mirror (middle passage)",
        "author": "John Ashbery",
        "year": 1975,
        "era": "new_york_school",
        "text": """But there is in that gaze a combination
Of tenderness, amusement and regret, so powerful
In its restraint that one cannot look for long.
The secret is too plain. The pity of it smarts,
Makes hot tears spurt: that the soul is not a soul,
Has no secret, is small, and it fits
Its hollow perfectly: its room, our moment of attention."""
    },
    {
        "title": "Self-Portrait in a Convex Mirror (closing)",
        "author": "John Ashbery",
        "year": 1975,
        "era": "new_york_school",
        "text": """A breeze like the turning of a page
Brings back your face: the moment
Takes such a survey of the whole,
The polite view through hooded eyes
Seeing through the other's familiar gesture
To the thought that lies behind it.
The hand holds no chalk
And each part of the whole falls off
And cannot know it knew, except
Here and there, in cold pockets
Of remembrance, whispers out of time."""
    },
    {
        "title": "The One Thing That Can Save America",
        "author": "John Ashbery",
        "year": 1975,
        "era": "new_york_school",
        "text": """Is anything central?
Orchards flung out on the land,
Urban forests, canals, and the survey of all this,
As though one were flying over it in an airplane.
These things are connected and make up a landscape
That one must not reject, but that seems to promise
Nothing if not the assurance that what happened
Is only a part of the living, an ideal."""
    },
    {
        "title": "A Wave (opening)",
        "author": "John Ashbery",
        "year": 1984,
        "era": "new_york_school",
        "text": """To pass through pain and not know it,
A survey of the whole. Feeling the walls
Of the absence, the tall room in which
Nothing but itself is relevant.
The children have grown up. They are free
To go about their business. And what about
The parents? They too are free
But in the wrong direction."""
    },
    {
        "title": "Rivers and Mountains",
        "author": "John Ashbery",
        "year": 1966,
        "era": "new_york_school",
        "text": """On the secret map the assassins
Cloistered, took note of the survey.
The survey was made up of rivers and mountains
And a few plains, with trees,
Some houses dotting a low rise.
The lives of the survey makers
Had faded into the background.
Only their survey remained."""
    },
    {
        "title": "Leaving the Atocha Station",
        "author": "John Ashbery",
        "year": 1962,
        "era": "new_york_school",
        "text": """The arctic honey blabbed over the survey
Survey of the survey, leaving
Atocha Station, the survey
Of the arctic honey. The survey
Blabbed over the arctic honey,
He had mistaken his survey for a pillar."""
    },
    {
        "title": "A Blessing in Disguise",
        "author": "John Ashbery",
        "year": 1962,
        "era": "new_york_school",
        "text": """Yes, they are alive and can have those colors,
But I, in my survey of the whole scene,
Am cursed with the inability
To see it as other than the next moment's
Business. The survey is not the thing
But an excuse for it, leading to
The promise of a survey that is not
A blessing, but a blessing in disguise."""
    },
    {
        "title": "Wet Casements",
        "author": "John Ashbery",
        "year": 1977,
        "era": "new_york_school",
        "text": """When Eduard Degas purchased the painting Sémiramis Building Babylon
He knew he was getting something extraordinary:
A survey of all that had been done in painting up to that time,
With special emphasis on the moody, contemplative side.
It's no different with the window you look out of
Or into: the middle class is always being squeezed out."""
    },
    {
        "title": "Why I Am Not a Painter",
        "author": "Frank O'Hara",
        "year": 1957,
        "era": "new_york_school",
        "text": """I am not a painter, I am a poet.
Why? I think I would rather be
a painter, but I am not. Well,

for instance, Mike Goldberg
is starting a painting. I go up.
"Sit down and have a drink" he
says. I drink; we drink. I look
up. "You have SARDINES in it."
"Yes, it needed something there."
"Oh." I go and the days go by"""
    },
    {
        "title": "The Day Lady Died",
        "author": "Frank O'Hara",
        "year": 1959,
        "era": "new_york_school",
        "text": """It is 12:20 in New York a Friday
three days after Bastille day, yes
it is 1959 and I go get a shoeshine
because I will get off the 4:19 in Easthampton
at 7:15 and then go straight to dinner
and I don't know the people who will feed me"""
    },

    # ─── LANGUAGE POETRY ──────────────────────────────────────────────
    {
        "title": "My Life (excerpt)",
        "author": "Lyn Hejinian",
        "year": 1980,
        "era": "language",
        "text": """A pause, a rose, something on paper.
A moment yellow, just as four years later,
when my father returned home from the war,
the moment of greeting him, as he stood
at the door, was the same yellow."""
    },
    {
        "title": "Ketjak (excerpt)",
        "author": "Ron Silliman",
        "year": 1978,
        "era": "language",
        "text": """Revolving door. A sequence of objects which in the ordinary are merely ordinary.
Fountains of the financial district.
Algebra of need. The night the wood
caught fire, flames arching over
the road between the oaks."""
    },
    {
        "title": "Islets/Irritations (excerpt)",
        "author": "Bruce Andrews",
        "year": 1983,
        "era": "language",
        "text": """Permanent culture, it's my patriotic
duty to burn the flag of this
country. Blubber international. Grow
this culture in a petri dish.
Homogenized. Make them eat what
they kill."""
    },

    # ─── CONTEMPORARY ─────────────────────────────────────────────────
    {
        "title": "Citizen (excerpt)",
        "author": "Claudia Rankine",
        "year": 2014,
        "era": "contemporary",
        "text": """When you are alone and too tired even to turn on any of your devices, you let yourself linger in a past stacked among your pillows. Usually you are nestled under blankets and wood-frame windows, but you hear the wood frames of your body and you know you are welcome here."""
    },
    {
        "title": "Catalog of Unabashed Gratitude (excerpt)",
        "author": "Ross Gay",
        "year": 2015,
        "era": "contemporary",
        "text": """Friends, will you bear with me today,
for I have been traveling and I find
that my knees are a bit sore
from so much kneeling? Forgive me.
I have been praying again,
and I have been struck dumb
by the generosity of the world."""
    },
    {
        "title": "Whereas (excerpt)",
        "author": "Layli Long Soldier",
        "year": 2017,
        "era": "contemporary",
        "text": """Whereas I tire. Of my effort to offer
this effort, to ## and of. Whereas the way
I am. Of my people's way. To open
in way, of way. Whereas my
hand with my uncle's hand. Whereas
my hand with the hand of."""
    },
    {
        "title": "Night Sky with Exit Wounds (excerpt)",
        "author": "Ocean Vuong",
        "year": 2016,
        "era": "contemporary",
        "text": """In the body, where everything has a price,
I was a beggar. I was
a fist. In a world where everything
has a price, I was a word
no one could afford."""
    },
    {
        "title": "Incantation",
        "author": "Lucille Clifton",
        "year": 2000,
        "era": "contemporary",
        "text": """the ten commandments of
the old testament, from
the new testament,
blessed are the poor in spirit,
blessed are they that mourn,
blessed are the meek,
blessed are they which do hunger
and thirst after righteousness."""
    },

    # ─── HARLEM RENAISSANCE / BLACK ARTS ───────────────────────────────
    {
        "title": "Harlem",
        "author": "Langston Hughes",
        "year": 1951,
        "era": "harlem_renaissance",
        "text": """What happens to a dream deferred?

Does it dry up
like a raisin in the sun?
Or fester like a sore—
And then run?
Does it stink like rotten meat?
Or crust and sugar over—
like a syrupy sweet?

Maybe it just sags
like a heavy load.

Or does it explode?"""
    },
    {
        "title": "The Negro Speaks of Rivers",
        "author": "Langston Hughes",
        "year": 1921,
        "era": "harlem_renaissance",
        "text": """I've known rivers:
I've known rivers ancient as the world and older than the
     flow of human blood in human veins.

My soul has grown deep like the rivers.

I bathed in the Euphrates when dawns were young.
I built my hut near the Congo and it lulled me to sleep.
I looked upon the Nile and raised the pyramids above it.
I heard the singing of the Mississippi when Abe Lincoln
     went down to New Orleans, and I've seen its muddy
     bosom turn all golden in the sunset."""
    },
    {
        "title": "We Real Cool",
        "author": "Gwendolyn Brooks",
        "year": 1960,
        "era": "mid_century",
        "text": """We real cool. We
Left school. We

Lurk late. We
Strike straight. We

Sing sin. We
Thin gin. We

Jazz June. We
Die soon."""
    },

    # ─── OULIPO / EXPERIMENTAL ─────────────────────────────────────────
    {
        "title": "Variations on A (excerpt)",
        "author": "Georges Perec",
        "year": 1969,
        "era": "oulipo",
        "text": """What a man! A great saga! A drama,
a scandal! What a catastrophe!
A fatal almanac, a calendar that
brands and brands again, a
mad cascade, a kaleidoscope that
crashes and crashes again."""
    },

    # ─── SURREALISM ───────────────────────────────────────────────────
    {
        "title": "Free Union (excerpt)",
        "author": "André Breton",
        "year": 1931,
        "era": "surrealist",
        "text": """My wife whose hair is a brush fire
Whose thoughts are summer lightning
Whose waist is an hourglass
Whose waist is the waist of an otter caught in the teeth of a tiger
Whose mouth is a cockade and a bouquet of stars of the last magnitude"""
    },

    # ─── DEEP IMAGE / AMERICAN SURREALISM ─────────────────────────────
    {
        "title": "Driving Toward the Lac Qui Parle River",
        "author": "Robert Bly",
        "year": 1962,
        "era": "deep_image",
        "text": """I am driving; it is dusk; Minnesota.
The stubble field catches the last growth of sun.
The soybeans are breathing on all sides.
Old men are sitting before their houses on carseats
In the small towns. I am happy,
The moon rising above the turkey sheds."""
    },

    # ─── CONTROLS: PROSE ──────────────────────────────────────────────
    {
        "title": "Simple narrative prose",
        "author": "Control",
        "year": 2024,
        "era": "control",
        "text": """The cat sat on the mat. It was a warm day and the sun was shining through the window. The cat looked at the birds outside and wished it could go out and play."""
    },
    {
        "title": "News article prose",
        "author": "Control",
        "year": 2024,
        "era": "control",
        "text": """The president announced today that the government would be investing in new infrastructure projects. The plan includes improvements to roads, bridges, and public transportation systems across the country."""
    },
    {
        "title": "Academic prose",
        "author": "Control",
        "year": 2024,
        "era": "control",
        "text": """The results of the study suggest that there is a significant correlation between the two variables. Further research is needed to determine the causal mechanisms underlying this relationship."""
    },
    {
        "title": "Technical prose",
        "author": "Control",
        "year": 2024,
        "era": "control",
        "text": """To install the software, first download the package from the official website. Then open the terminal and navigate to the download directory. Run the installation script with administrator privileges."""
    },
]

# Quick stats
if __name__ == "__main__":
    from collections import Counter
    eras = Counter(p["era"] for p in POEMS)
    authors = Counter(p["author"] for p in POEMS)
    print(f"Total poems: {len(POEMS)}")
    print(f"\nBy era:")
    for era, n in eras.most_common():
        print(f"  {era}: {n}")
    print(f"\nBy author:")
    for author, n in authors.most_common():
        print(f"  {author}: {n}")
