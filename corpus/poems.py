"""
Curated corpus of poems for information-theoretic analysis.
Organized by era/movement for comparative research.

Each poem: { "title", "author", "year", "era", "text" }

Language field (optional, defaults to "en"):
  "en" — analyzed with gpt2
  "de" — analyzed with dbmdz/german-gpt2
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

    # ─── GERMAN SYMBOLISM / JUGENDSTIL ────────────────────────────────
    {
        "title": "Komm in den totgesagten park und schau",
        "author": "Stefan George",
        "year": 1891,
        "era": "german_symbolist",
        "language": "de",
        "text": """Komm in den totgesagten park und schau:
Der schimmer ferner lächelnder gestade,
Der reinen wolken unverhofftes blau
Erhellt die weiher und die bunten pfade.

Dort nimm das tiefe gelb, das weiche grau
Von birken und von buchs, der wind ist lau,
Die späten rosen welkten noch nicht ganz,
Erlese küsse sie und flicht den kranz,

Vergiss auch diese lezten astern nicht,
Den purpur um die ranken wilder reben,
Und auch was übrig blieb von grünem leben
Verwinde leicht im herbstlichen gesicht."""
    },
    {
        "title": "Das Wort",
        "author": "Stefan George",
        "year": 1919,
        "era": "german_symbolist",
        "language": "de",
        "text": """Wunder von ferne oder traum
Bracht ich an meines landes saum

Und harrte bis die graue norn
Den namen fand in ihrem born—

Drauf konnt ichs greifen dicht und stark
Nun blüht und glänzt es durch die mark...

Einst langt ich an nach guter fahrt
Mit einem kleinod reich und zart

Sie suchte lang und gab mir kund:
»So schläft hier nichts auf tiefem grund«

Worauf es meiner hand entrann
Und nie mein land den schatz gewann...

So lernt ich traurig den verzicht:
Kein ding sei wo das wort gebricht."""
    },
    {
        "title": "Porta Nigra",
        "author": "Stefan George",
        "year": 1907,
        "era": "german_symbolist",
        "language": "de",
        "text": """Ich bin der eine und bin beide: bin
Der wächter der jahrtausende belagert
Und der barbar der seine fackel schwingt
Vor dem was er nicht kennt und nicht begreift.

Ich bin das tor. Ich bin die feste mauer.
Ich bin der schlüssel der im schlosse liegt.
Ich stehe hier und warte auf das licht
Das kommt und geht und mich nicht öffnet—nie."""
    },

    # ─── GERMAN EXPRESSIONISM ─────────────────────────────────────────
    {
        "title": "Grodek",
        "author": "Georg Trakl",
        "year": 1914,
        "era": "german_expressionist",
        "language": "de",
        "text": """Am Abend schweigen die herbstlichen Wälder
Von tödlichen Waffen, die goldenen Ebenen
Und blauen Seen, darüber die Sonne
Düstrer hinrollt; umfängt die Nacht
Sterbende Krieger, die wilde Klage
Ihrer zerbrochenen Münder.
Doch stille sammelt im Weidengrund
Rotes Gewölk, darin ein zürnender Gott wohnt,
Das vergossne Blut sich, mondne Kühle;
Alle Straßen münden in schwarze Verwesung.
Unter goldnem Gezweig der Nacht und Sternen
Es schwankt der Schwester Schatten durch den schweigenden Hain,
Zu grüßen die Geister der Helden, die blutenden Häupter;
Und leise tönen im Rohr die dunkeln Flöten des Herbstes.
O stolzere Trauer! ihr ehernen Altäre,
Die heiße Flamme des Geistes nährt heute ein gewaltiger Schmerz,
Die ungebornen Enkel."""
    },
    {
        "title": "Verklärter Herbst",
        "author": "Georg Trakl",
        "year": 1913,
        "era": "german_expressionist",
        "language": "de",
        "text": """Gewaltig endet so das Jahr
Mit goldnem Wein und Frucht der Gärten.
Rund schweigen Wälder wunderbar
Und sind des Einsamen Gefährten.

Da sagt der Landmann: Es ist gut.
Ihr Abendglocken lang und leise
Gebt noch zum Ende frohen Mut.
Ein Vogelzug grüßt auf der Reise.

Es ist der Liebe milde Zeit.
Im Kahn den blauen Fluß hinunter
Wie schön sich Bild an Bildchen reiht—
Das geht in Ruh und Schweigen unter."""
    },

    # ─── GERMAN MODERNISM ─────────────────────────────────────────────
    {
        "title": "Die erste Elegie (Eröffnung)",
        "author": "Rainer Maria Rilke",
        "year": 1912,
        "era": "german_modernist",
        "language": "de",
        "text": """Wer, wenn ich schriee, hörte mich denn aus der Engel
Ordnungen? und gesetzt selbst, es nähme
einer mich plötzlich ans Herz: ich verginge von seinem
stärkeren Dasein. Denn das Schöne ist nichts
als des Schrecklichen Anfang, den wir noch grade ertragen,
und wir bewundern es so, weil es gelassen verschmäht,
uns zu zerstören. Ein jeder Engel ist schrecklich."""
    },
    {
        "title": "Archaischer Torso Apollos",
        "author": "Rainer Maria Rilke",
        "year": 1908,
        "era": "german_modernist",
        "language": "de",
        "text": """Wir kannten nicht sein unerhörtes Haupt,
darin die Augenäpfel reiften. Aber
sein Torso glüht noch wie ein Kandelaber,
in dem sein Schauen, nur zurückgeschraubt,

sich hält und glänzt. Sonst könnte nicht der Bug
der Brust dich blenden, und im leisen Drehen
der Lenden könnte nicht ein Lächeln gehen
zu jener Mitte, die die Zeugung trug.

Sonst stünde dieser Stein entstellt und kurz
unter der Schultern durchsichtigem Sturz
und flimmerte nicht so wie Raubtierfelle;

und bräche nicht aus allen seinen Rändern
aus wie ein Stern: denn da ist keine Stelle,
die dich nicht sieht. Du mußt dein Leben ändern."""
    },

    # ─── GERMAN CONTROL PROSE ─────────────────────────────────────────
    {
        "title": "German narrative prose",
        "author": "Control",
        "year": 2024,
        "era": "control",
        "language": "de",
        "text": """Die Katze saß auf der Matte. Es war ein warmer Tag und die Sonne schien durch das Fenster. Die Katze beobachtete die Vögel draußen und wünschte sich, sie könnte hinausgehen und spielen."""
    },

    # ─── NEW POEMS (2026-09-01) ───────────────────────────────────────
    # Added to fill temporal gaps and test temporal evolution hypotheses.
    # Focus: Victorian/Edwardian bridge to Modernism (1877–1912),
    # and mid-century confessional/expressionist confirmation.

    # Gerard Manley Hopkins — "The Windhover" (1877, published 1918, PD)
    # Extreme phonetic innovation and sprung rhythm; unique lexical choices
    {
        "title": "The Windhover",
        "author": "Gerard Manley Hopkins",
        "year": 1877,
        "era": "victorian",
        "text": """I caught this morning morning's minion, king-
    dom of daylight's dauphin, dapple-dawn-drawn Falcon, in his riding
    Of the rolling level underneath him steady air, and striding
High there, how he rung upon the rein of a wimpling wing
In his ecstasy! then off, off forth on swing,
    As a skate's heel sweeps smooth on a bow-bend: the hurl and gliding
    Rebuffed the big wind. My heart in hiding
Stirred for a bird,—the achieve of; the mastery of the thing!

Brute beauty and valour and act, oh, air, pride, plume, here
    Buckle! AND the fire that breaks from thee then, a billion
Times told lovelier, more dangerous, O my chevalier!"""
    },

    # Alfred Lord Tennyson — "Ulysses" (1833, PD)
    # Blank verse, Victorian rhetoric — expected word choices?
    {
        "title": "Ulysses (opening)",
        "author": "Alfred Lord Tennyson",
        "year": 1833,
        "era": "victorian",
        "text": """It little profits that an idle king,
By this still hearth, among these barren crags,
Match'd with an aged wife, I mete and dole
Unequal laws unto a savage race,
That hoard, and sleep, and feed, and know not me.
I cannot rest from travel: I will drink
Life to the lees: All times I have enjoy'd
Greatly, have suffer'd greatly, both with those
That loved me, and alone."""
    },

    # Paul Laurence Dunbar — "We Wear the Mask" (1896, PD)
    # Pre-Harlem African American poetry; coded language
    {
        "title": "We Wear the Mask",
        "author": "Paul Laurence Dunbar",
        "year": 1896,
        "era": "victorian",
        "text": """We wear the mask that grins and lies,
It hides our cheeks and shades our eyes,—
This debt we pay to human guile;
With torn and bleeding hearts we smile,
And mouth with myriad subtleties.

Why should the world be over-wise,
In counting all our tears and sighs?
Nay, let them only see us, while
We wear the mask."""
    },

    # Thomas Hardy — "The Convergence of the Twain" (1912, PD)
    # Written for Titanic memorial; Victorian-Modernist bridge
    {
        "title": "The Convergence of the Twain (excerpt)",
        "author": "Thomas Hardy",
        "year": 1912,
        "era": "victorian",
        "text": """In a solitude of the sea
Deep from human vanity,
And the Pride of Life that planned her, stilly couches she.

Steel chambers, late the pyres
Of her salamandrine fires,
Cold currents thrid, and turn to rhythmic tidal lyres.

Over the mirrors meant
To glass the opulent
The sea-worm crawls—grotesque, slimed, dumb, indifferent."""
    },

    # Robert Browning — "My Last Duchess" (1842, PD)
    # Dramatic monologue; Victorian rhetoric; high information content
    {
        "title": "My Last Duchess (opening)",
        "author": "Robert Browning",
        "year": 1842,
        "era": "victorian",
        "text": """That's my last Duchess painted on the wall,
Looking as if she were alive. I call
That piece a wonder, now: Frà Pandolf's hands
Worked busily a day, and there she stands.
Will't please you sit and look at her? I said
"Frà Pandolf" by design, for never read
Strangers like you that pictured countenance,
The depth and passion of its earnest glance."""
    },

    # Anne Sexton — "The Truth the Dead Know" (1962, excerpt, fair use)
    # Confessional; grief and dissociation
    {
        "title": "The Truth the Dead Know (opening)",
        "author": "Anne Sexton",
        "year": 1962,
        "era": "confessional",
        "text": """Gone, I say and walk from church,
refusing the stiff procession to the grave,
letting the dead ride alone in the hearse.
It is June. I am tired of being brave."""
    },

    # ─── NEW POEMS (2026-08-31) ───────────────────────────────────────
    # Added to test compression-vs-S₂ dissociation hypotheses.
    # Focus: extreme repetition, extreme brevity, concrete/typographic
    # experiments, and Modernist forms not yet represented.

    # H.D. — Imagist compression, PD
    {
        "title": "Oread",
        "author": "H.D. (Hilda Doolittle)",
        "year": 1914,
        "era": "modernist",
        "text": """Whirl up, sea—
whirl your pointed pines,
splash your great pines
on our rocks,
hurl your green over us,
cover us with your pools of fir."""
    },

    # Marianne Moore — Modernist irony, PD (1919 version)
    {
        "title": "Poetry (opening)",
        "author": "Marianne Moore",
        "year": 1919,
        "era": "modernist",
        "text": """I, too, dislike it: there are things that are important beyond all this fiddle.
Reading it, however, with a perfect contempt for it, one discovers in
it after all, a place for the genuine."""
    },

    # Gertrude Stein — extreme sonic/repetitive experimentation, PD
    {
        "title": "Susie Asado",
        "author": "Gertrude Stein",
        "year": 1913,
        "era": "modernist",
        "text": """Sweet sweet sweet sweet sweet tea.
Susie Asado.
Sweet sweet sweet sweet sweet tea.
Susie Asado.
Susie Asado which is a told tray sure.
A lean on the shoe this means slips slips hers.
When the ancient light grey is clean it is yellow, it is a silver seller.
This is a please this is a please there are the saids to jelly."""
    },

    # e.e. cummings — concrete/typographic, "Buffalo Bill's" (1920, PD)
    {
        "title": "Buffalo Bill 's",
        "author": "E.E. Cummings",
        "year": 1920,
        "era": "modernist",
        "text": """Buffalo Bill 's
defunct
        who used to
        ride a watersmooth-silver
                                    stallion
and break onetwothreefourfive pigeonsjustlikethat
                                                    Jesus

he was a handsome man
                    and what i want to know is
how do you like your blueeyed boy
Mister Death"""
    },

    # Classic haiku — Basho, PD (R.H. Blyth-adjacent literal renderings)
    {
        "title": "Three Haiku (Basho, translated)",
        "author": "Matsuo Basho",
        "year": 1686,
        "era": "haiku",
        "text": """An old silent pond—
a frog jumps into the pond,
splash! Silence again.

The first cold shower;
even the monkey seems to want
a little coat of straw.

Autumn moonlight—
a worm digs silently
into the chestnut."""
    },

    # Kobayashi Issa haiku — second haiku author; tests Gini/concentration hypothesis
    {
        "title": "Three Haiku (Issa, translated)",
        "author": "Kobayashi Issa",
        "year": 1819,
        "era": "haiku",
        "text": """This world of dew
is only a world of dew—
and yet... and yet...

Don't worry, spiders,
I keep house
casually.

O snail,
climb Mount Fuji,
but slowly, slowly!"""
    },

    # Vachel Lindsay — extreme rhythmic repetition, PD (excerpt, sanitized)
    {
        "title": "The Congo (opening, sanitized excerpt)",
        "author": "Vachel Lindsay",
        "year": 1914,
        "era": "modernist",
        "text": """Fat black bucks in a wine-barrel room,
Barrel-house kings, with feet unstable,
Sagged and reeled and pounded on the table,
Pounded on the table,
Beat an empty barrel with the handle of a broom,
Hard as they were able,
Boom, boom, BOOM,
With a silk umbrella and the handle of a broom,
Boomlay, boomlay, boomlay, BOOM."""
    },

    # Sappho fragment — ancient, translated (public domain)
    {
        "title": "Fragment 31 (translated)",
        "author": "Sappho",
        "year": -600,
        "era": "ancient",
        "text": """He seems to me equal to the gods, that man
who sits across from you and, close by, listens
to you softly speaking and laughing sweetly,
    which sets my heart to fluttering in my breast;
for when I look at you a moment, then
I can no longer speak; my tongue is broken,
a subtle fire runs beneath my skin,
    my eyes see nothing, my ears roar."""
    },

    # Prose poem — Baudelaire "L'Étranger" translated (PD)
    {
        "title": "The Stranger (prose poem, translated)",
        "author": "Charles Baudelaire",
        "year": 1869,
        "era": "prose_poetry",
        "text": """—Whom do you love best, enigmatical man; your father, your mother, your sister, or your brother?
—I have neither father, nor mother, nor sister, nor brother.
—Your friends?
—You use a word whose meaning has remained unknown to me until this day.
—Your country?
—I do not know in what latitude it lies.
—Beauty?
—Her would I love willingly, goddess and immortal.
—Gold?
—I hate it as much as you hate God.
—Well then! What do you love, extraordinary stranger?
—I love the clouds—the clouds that pass—up there—up there—the wonderful clouds."""
    },

    # Emily Dickinson — extreme compression test, PD
    {
        "title": "A Route of Evanescence",
        "author": "Emily Dickinson",
        "year": 1879,
        "era": "19th_century",
        "text": """A Route of Evanescence,
With a revolving Wheel—
A Resonance of Emerald,
A Rush of Cochineal—
And every Blossom on the Bush
Adjusts its tumbled Head—
The Mail from Tunis, probably,
An easy Morning's Ride—"""
    },

    # Kerouac — spontaneous prose/verse, extreme repetition (1959, likely fair use)
    # Using instead a very short, well-attested PD-adjacent verse from Whitman
    {
        "title": "A Noiseless Patient Spider",
        "author": "Walt Whitman",
        "year": 1868,
        "era": "19th_century",
        "text": """A noiseless patient spider,
I mark'd where on a little promontory it stood isolated,
Mark'd how to explore the vacant vast surrounding,
It launch'd forth filament, filament, filament, out of itself,
Ever unreeling them, ever tirelessly speeding them.

And you O my soul where you stand,
Surrounded, detached, in measureless oceans of space,
Ceaselessly musing, venturing, throwing, seeking the spheres to connect them,
Till the bridge you will need be form'd, till the ductile anchor hold,
Till the gossamer thread you fling catch somewhere, O my soul."""
    },

    # ─── NEW POEMS (2026-09-02): LINE-POSITION & METER EXPERIMENT ──────────────
    # Added to test hypotheses about meter, form, and line-position effects.
    # Focus: highly metrical / rhyme-constrained poems (predict lower final-position S₂),
    # ghazal form (mandatory radif = structural repetition), and canonical incantatory verse.

    # William Blake — "The Tyger" (1794, PD)
    # Anapestic tetrameter, insistent rhyme, incantatory repetition across stanzas.
    # Hypothesis: extreme metric regularity → strong rhyme penalty (low final-position S₂),
    # but lexical audacity ("fearful symmetry", "burning bright") → high medial S₂.
    {
        "title": "The Tyger",
        "author": "William Blake",
        "year": 1794,
        "era": "romantic",
        "text": """Tyger Tyger, burning bright,
In the forests of the night;
What immortal hand or eye,
Could frame thy fearful symmetry?

In what distant deeps or skies,
Burnt the fire of thine eyes?
On what wings dare he aspire?
What the hand, dare seize the fire?

And what shoulder, & what art,
Could twist the sinews of thy heart?
And when thy heart began to beat,
What dread hand? & what dread feet?"""
    },

    # Edgar Allan Poe — "The Raven" (opening, 1845, PD)
    # Trochaic octameter with internal rhyme; extreme end-rhyme constraint.
    # Hypothesis: most constrained rhyme scheme in the corpus → lowest final-position S₂.
    {
        "title": "The Raven (opening stanzas)",
        "author": "Edgar Allan Poe",
        "year": 1845,
        "era": "19th_century",
        "text": """Once upon a midnight dreary, while I pondered, weak and weary,
Over many a quaint and curious volume of forgotten lore—
While I nodded, nearly napping, suddenly there came a tapping,
As of some one gently rapping, rapping at my chamber door.
"'Tis some visitor," I muttered, "tapping at my chamber door—
Only this and nothing more."

Ah, distinctly I remember it was in the bleak December;
And each separate dying ember wrought its ghost upon the floor;
Eagerly I wished the morrow;—vainly I had sought to borrow
From my books surcease of sorrow—sorrow for the lost Lenore—
For the rare and radiant maiden whom the angels name Lenore—
Nameless here for evermore."""
    },

    # Christina Rossetti — "Remember" (1849, PD)
    # Petrarchan sonnet; iambic pentameter; high formal constraint.
    {
        "title": "Remember",
        "author": "Christina Rossetti",
        "year": 1849,
        "era": "victorian",
        "text": """Remember me when I am gone away,
Gone far away into the silent land;
When you can no more hold me by the hand,
Nor I half turn to go yet turning stay.
Remember me when no more day by day
You tell me of our future that you plann'd:
Only remember me; you understand
It will be late to counsel then or pray.
Yet if you should forget me for a while
And afterwards remember, do not grieve:
For if the darkness and corruption leave
A vestige of the thoughts that once I had,
Better by far you should forget and smile
Than that you should remember and be sad."""
    },

    # William Blake — "London" (1794, PD)
    # Short lines, regular ABAB quatrains; urban subject matter with anaphora.
    {
        "title": "London",
        "author": "William Blake",
        "year": 1794,
        "era": "romantic",
        "text": """I wander thro' each charter'd street,
Near where the charter'd Thames does flow.
And mark in every face I meet
Marks of weakness, marks of woe.

In every cry of every Man,
In every Infants cry of fear,
In every voice: in every ban,
The mind-forg'd manacles I hear

How the Chimney-sweepers cry
Every blackning Church appalls,
And the hapless Soldiers sigh
Runs in blood down Palace walls"""
    },

    # Emily Dickinson — "I heard a Fly buzz" (1896, PD)
    # Hymn meter (common meter), but disrupted at key moments.
    # Hypothesis: disruptions of hymn-meter expectation → high S₂ spikes.
    {
        "title": "I heard a Fly buzz — when I died",
        "author": "Emily Dickinson",
        "year": 1896,
        "era": "19th_century",
        "text": """I heard a Fly buzz — when I died —
The Stillness in the Room
Was like the Stillness in the Air —
Between the Heaves of Storm —

The Eyes around — had wrung them dry —
And Breaths were gathering firm
For that last Onset — when the King
Be witnessed — in the Room —

I willed my Keepsakes — Signed away
What portion of me be
Assignable — and then it was
There interposed a Fly —

With Blue — uncertain — stumbling Buzz —
Between the light — and me —
And then the Windows failed — and then
I could not see to see —"""
    },

    # Thomas Hardy — "The Oxen" (1915, PD)
    # Ballad quatrains, pastoral nostalgia, regular meter disrupted by modernist doubt.
    {
        "title": "The Oxen",
        "author": "Thomas Hardy",
        "year": 1915,
        "era": "victorian",
        "text": """Christmas Eve, and twelve of the clock.
"Now they are all on their knees,"
An elder said as we sat in a flock
By the embers in hearthside ease.

We pictured the meek mild creatures where
They dwelt in their strawy pen,
Nor did it occur to one of us there
To doubt they were kneeling then.

So fair a fancy few would weave
In these years! Yet, I feel,
If someone said on Christmas Eve,
"Come; see the oxen kneel,

"In the lonely barton by yonder coomb
Our childhood used to know,"
I should go with him in the gloom,
Hoping it might be so."""
    },

    # Walter de la Mare — "The Listeners" (1912, PD)
    # Ballad-like, supernatural atmosphere, loose anapestic measure.
    # Tests whether "eerie" poems with unusual lexis show distinct line-position effects.
    {
        "title": "The Listeners",
        "author": "Walter de la Mare",
        "year": 1912,
        "era": "19th_century",
        "text": """'Is there anybody there?' said the Traveller,
Knocking on the moonlit door;
And his horse in the silence champed the grasses
Of the forest's ferny floor:
And a bird flew up out of the turret,
Above the Traveller's head:
And he smote upon the door again a second time;
'Is there anybody there?' he said.
But no one descended to the Traveller;
No head from the leaf-fringed sill
Leaned over and looked into his grey eyes,
Where he stood perplexed and still."""
    },

    # ─── HARLEM RENAISSANCE (ADDITIONAL) ────────────────────────────────
    # Claude McKay — "If We Must Die" (1919, PD)
    # Petrarchan sonnet; famous political defiance. High rhyme density.
    # Tests: does the Harlem Renaissance rhyme-as-weapon pattern hold for McKay?
    {
        "title": "If We Must Die",
        "author": "Claude McKay",
        "year": 1919,
        "era": "harlem_renaissance",
        "text": """If we must die, let it not be like hogs
Hunted and penned in an inglorious spot,
While round us bark the mad and hungry dogs,
Making their mock at our accursèd lot.
If we must die, O let us nobly die,
So that our precious blood may not be shed
In vain; then even the monsters we defy
Shall be constrained to honor us though dead!
O kinsmen! we must meet the common foe!
Though far outnumbered let us show us brave,
And for their thousand blows deal one deathblow!
What though before us lies the open grave?
Like men we'll face the murderous, cowardly pack,
Pressed to the wall, dying, but fighting back!"""
    },

    # Countee Cullen — "Yet Do I Marvel" (1925, PD)
    # Shakespearean sonnet asking God why Black poets must exist amid injustice.
    # Highly rhyming; the final couplet is famous. Tests rhyme-as-Straussian-shock.
    {
        "title": "Yet Do I Marvel",
        "author": "Countee Cullen",
        "year": 1925,
        "era": "harlem_renaissance",
        "text": """I doubt not God is good, well-meaning, kind,
And did He stoop to quibble could tell why
The little buried mole continues blind,
Why flesh that mirrors Him must some day die,
Make plain the reason tortured Tantalus
Is baited by the fickle fruit, declare
If merely brute caprice dooms Sisyphus
To struggle up a never-ending stair.
Inscrutable His ways are, and immune
To catechism by a mind too strewn
With petty cares to slightly understand
What awful brain compels His awful hand.
Yet do I marvel at this curious thing:
To make a poet black, and bid him sing!"""
    },

    # Robert Burns — "A Red, Red Rose" (1794, PD)
    # Song lyric; ballad stanza; love poem with strong ABAB/ABCB rhyme.
    # First proper song lyrics in the corpus — tests song vs poetry S₂ differences.
    {
        "title": "A Red, Red Rose",
        "author": "Robert Burns",
        "year": 1794,
        "era": "romantic",
        "text": """O my Luve is like a red, red rose
That's newly sprung in June;
O my Luve is like the melody
That's sweetly played in tune.

As fair art thou, my bonnie lass,
So deep in luve am I;
And I will luve thee still, my dear,
Till a' the seas gang dry.

Till a' the seas gang dry, my dear,
And the rocks melt wi' the sun;
I will love thee still, my dear,
While the sands o' life shall run.

And fare thee weel, my only luve!
And fare thee weel awhile!
And I will come again, my luve,
Though it were ten thousand mile."""
    },

    # ─── FINGERPRINT VALIDATION POEMS ──────────────────────────────────
    # Added to test within-poet S₂ fingerprint stability across poems.

    # Thomas Hardy — "Neutral Tones" (1898, PD)
    # Early Hardy; bleak winter scene; tests HIGH-DEVIATION SPIKER signature.
    {
        "title": "Neutral Tones",
        "author": "Thomas Hardy",
        "year": 1898,
        "era": "victorian",
        "text": """We stood by a pond that winter day,
And the sun was white, as though chidden of God,
And a few leaves lay on the starving sod;
— They had fallen from an ash, and were gray.

Your eyes on me were as eyes that rove
Over tedious riddles of years ago;
And some words played between us to and fro
On which lost the more by our love.

The smile on your mouth was the deadest thing
Alive enough to have strength to die;
And a grin of bitterness swept thereby
Like an ominous bird a-wing....

Since then, keen lessons that love deceives,
And wrings with wrong, have shaped to me
Your face, and the God-curst sun, and a tree,
And a pond edged with grayish leaves."""
    },

    # T.S. Eliot — "The Hollow Men" (opening, 1925)
    # Tests if Eliot's remarkably stable fingerprint (skew≈1.62, kurt≈3.94) holds here.
    {
        "title": "The Hollow Men (opening)",
        "author": "T.S. Eliot",
        "year": 1925,
        "era": "modernist",
        "text": """We are the hollow men
We are the stuffed men
Leaning together
Headpiece filled with straw. Alas!
Our dried voices, when
We whisper together
Are quiet and meaningless
As wind in dry grass
Or rats' feet over broken glass
In our dry cellar

Shape without form, shade without colour,
Paralysed force, gesture without motion;

Those who have crossed
With direct eyes, to death's other Kingdom
Remember us — if at all — not as lost
Violent souls, but only
As the hollow men
The stuffed men."""
    },

    # William Carlos Williams — "This Is Just to Say" (1934)
    # Very short; tests whether WCW's extreme mean S₂ (+3.6) holds in miniature.
    {
        "title": "This Is Just to Say",
        "author": "William Carlos Williams",
        "year": 1934,
        "era": "modernist",
        "text": """I have eaten
the plums
that were in
the icebox

and which
you were probably
saving
for breakfast

Forgive me
they were delicious
so sweet
and so cold"""
    },

    # E.E. Cummings — "anyone lived in a pretty how town" (1940)
    # Tests low pos_ratio signature: Cummings' syntactic inversions suppress surprisal
    # for most tokens while creating extreme spikes at key deviations.
    {
        "title": "anyone lived in a pretty how town",
        "author": "E.E. Cummings",
        "year": 1940,
        "era": "modernist",
        "text": """anyone lived in a pretty how town
(with up so floating many bells down)
spring summer autumn winter
he sang his didn't he danced his did.

Women and men(both little and small)
cared for anyone not at all
they sowed their isn't they reaped their same
sun moon stars rain

children guessed(but only a few
and down they forgot as up they grew
autumn winter spring summer)
that noone loved him more by more"""
    },

    # Philip Larkin — "Aubade" (1977)
    # New poet; late 20th-century English confessional; meditations on death.
    # Larkin's plain diction might produce a distinctive low-S₂, low-kurtosis fingerprint.
    {
        "title": "Aubade (opening)",
        "author": "Philip Larkin",
        "year": 1977,
        "era": "contemporary",
        "text": """I work all day, and get half-drunk at night.
Waking at four to soundless dark, I stare.
In time the curtain-edges will grow light.
Till then I see what's really always there:
Unresting death, a whole day nearer now,
Making all thought impossible but how
And where and when I shall myself die.
Arid interrogation: yet the dread
Of dying, and being dead,
Flashes afresh to hold and horrify."""
    },

    # Seamus Heaney — "Digging" (1966)
    # New poet; Irish post-war poetry; earthy imagery, strong consonance.
    # Heaney known for densely tactile language — may produce high variance S₂.
    {
        "title": "Digging",
        "author": "Seamus Heaney",
        "year": 1966,
        "era": "contemporary",
        "text": """Between my finger and my thumb
The squat pen rests; snug as a gun.

Under my window, a clean rasping sound
When the spade sinks into gravelly ground:
My father, digging. I look down

Till his straining rump among the flowerbeds
Bends low, comes up twenty years away
Stooping in rhythm through potato drills
Where he was digging.

The coarse boot nestled on the lug, the shaft
Against the inside knee was levered firmly.
He rooted out tall tops, buried the bright edge deep
To scatter new potatoes that we picked
Loving their cool hardness in our hands."""
    },

    # Wislawa Szymborska — translated contemporary; tests cross-cultural S₂ patterns
    {
        "title": "Possibilities",
        "author": "Wislawa Szymborska",
        "year": 1972,
        "era": "contemporary",
        "text": """I prefer movies.
I prefer cats.
I prefer the oaks along the Warta.
I prefer Dickens to Dostoyevsky.
I prefer myself liking people
to myself loving mankind.
I prefer keeping a needle and thread on hand, just in case.
I prefer the color green.
I prefer not to maintain
that reason is to blame for everything.
I prefer exceptions.
I prefer to leave early.
I prefer talking to doctors about something else.
I prefer the old fine-lined illustrations.
I prefer the absurdity of writing poems
to the absurdity of not writing poems."""
    },

    # Mary Oliver — contemporary nature lyric; meditative, accumulative
    {
        "title": "The Summer Day",
        "author": "Mary Oliver",
        "year": 1990,
        "era": "contemporary",
        "text": """Who made the world?
Who made the swan, and the black bear?
Who made the grasshopper?
This grasshopper, I mean—
the one who has flung herself out of the grass,
the one who is eating sugar out of my hand,
who is moving her jaws back and forth instead of up and down—
who is gazing around with her enormous and complicated eyes.
Now she lifts her pale forearms and thoroughly washes her face.
Now she snaps her wings open, and floats away.
I don't know exactly what a prayer is.
I do know how to pay attention, how to fall down
into the grass, how to kneel down in the grass,
how to be idle and blessed, how to stroll through the fields,
which is what I have been doing all day.
Tell me, what is it you plan to do
with your one wild and precious life?"""
    },

    # ─── NEW POEMS (2026-09-09): CLOSURE & SONG LYRICS EXPERIMENT ──────────
    # Added to test closure token hypotheses and song-lyrics vs poetry S₂ gap.
    # Focus: W.B. Yeats (prophetic modernism), Robert Frost (conversational
    # accessibility), and traditional ballad form as song-lyrics baseline.

    # W.B. Yeats — "The Second Coming" (1920, PD)
    # Prophetic, apocalyptic register; famous gyratory imagery.
    # Hypothesis: Yeats's intensity and unusual proper nouns → high S₂ and
    # high last-word S₂ (the poem ends on "Bethlehem").
    {
        "title": "The Second Coming",
        "author": "W.B. Yeats",
        "year": 1920,
        "era": "modernist",
        "text": """Turning and turning in the widening gyre
The falcon cannot hear the falconer;
Things fall apart; the centre cannot hold;
Mere anarchy is loosed upon the world,
The blood-dimmed tide is loosed, and everywhere
The ceremony of innocence is drowned;
The best lack all conviction, while the worst
Are full of passionate intensity.

Surely some revelation is at hand;
Surely the Second Coming is at hand.
The Second Coming! Hardly are those words out
When a vast image out of Spiritus Mundi
Troubles my sight: somewhere in sands of the desert
A shape with lion body and the head of a man,
A gaze blank and pitiless as the sun,
Is moving its slow thighs, while all about it
Reel shadows of the indignant desert birds.
The darkness drops again; but now I know
That twenty centuries of stony sleep
Were vexed to nightmare by a rocking cradle,
And what rough beast, its hour come round at last,
Slouches towards Bethlehem to be born?"""
    },

    # W.B. Yeats — "Sailing to Byzantium" (1928, PD)
    # Meditation on art, aging, and immortality; complex syntax.
    # Contrast with "The Second Coming" — more introspective but same poet.
    {
        "title": "Sailing to Byzantium (stanza 1)",
        "author": "W.B. Yeats",
        "year": 1928,
        "era": "modernist",
        "text": """That is no country for old men. The young
In one another's arms, birds in the trees,
—Those dying generations—at their song,
The salmon-falls, the mackerel-crowded seas,
Fish, flesh, or fowl, commend all summer long
Whatever is begotten, born, and dies.
Caught in that sensual music all neglect
Monuments of unageing intellect."""
    },

    # Robert Frost — "The Road Not Taken" (1916, PD)
    # The most widely read American poem; conversational register.
    # Hypothesis: Frost's accessibility will produce moderate but not high S₂ —
    # his choices are unexpected but within the range of colloquial English.
    {
        "title": "The Road Not Taken",
        "author": "Robert Frost",
        "year": 1916,
        "era": "modernist",
        "text": """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference."""
    },

    # Traditional Scottish ballad — "Lord Randal" (c. 1500–1800, PD)
    # Call-and-response song form; strong ABAB/ABCB ballad rhyme.
    # Tests whether song-lyric/oral form shows distinctively different S₂
    # from literary poetry; new era "ballad" to distinguish from written verse.
    {
        "title": "Lord Randal",
        "author": "Traditional (Scottish ballad)",
        "year": 1800,
        "era": "ballad",
        "text": """"O where hae ye been, Lord Randal, my son?
O where hae ye been, my handsome young man?"
"I hae been to the wild wood; mother, make my bed soon,
For I'm weary wi' hunting, and fain wald lie down."

"Where gat ye your dinner, Lord Randal, my son?
Where gat ye your dinner, my handsome young man?"
"I dined wi' my true-love; mother, make my bed soon,
For I'm weary wi' hunting, and fain wald lie down."

"What gat ye to your dinner, Lord Randal, my son?
What gat ye to your dinner, my handsome young man?"
"I gat eels boiled in broo; mother, make my bed soon,
For I'm weary wi' hunting, and fain wald lie down." """
    },

    # Robert Burns — "To a Mouse" (1785, PD)
    # Burns's Scots vernacular; famous last two stanzas philosophical.
    # Tests: does Scots dialect (non-standard orthography) spike S₂?
    # New "ballad" era would capture Burns's song-origin tradition.
    {
        "title": "To a Mouse (closing stanzas)",
        "author": "Robert Burns",
        "year": 1785,
        "era": "romantic",
        "text": """But Mousie, thou art no thy-lane,
In proving foresight may be vain:
The best-laid schemes o' Mice an' Men
Gang aft agley,
An' lea'e us nought but grief an' pain,
For promis'd joy!

Still, thou art blest, compar'd wi' me!
The present only toucheth thee:
But Och! I backward cast my e'e,
On prospects drear!
An' forward, tho' I canna see,
I guess an' fear!"""
    },

    # Matthew Arnold — "Dover Beach" extended (second stanza)
    # "Dover Beach" (opening) already in corpus; add later stanza for comparison.
    # Tests whether the poem's famous closing "darkling plain" passage shows
    # crescendo arc in the second half.
    {
        "title": "Dover Beach (closing stanzas)",
        "author": "Matthew Arnold",
        "year": 1867,
        "era": "victorian",
        "text": """Sophocles long ago
Heard it on the Ægæan, and it brought
Into his mind the turbid ebb and flow
Of human misery; we
Find also in the sound a thought,
Hearing it by this distant northern sea.

Ah, love, let us be true
To one another! for the world, which seems
To lie before us like a land of dreams,
So various, so beautiful, so new,
Hath really neither joy, nor love, nor light,
Nor certitude, nor peace, nor help for pain;
And we are here as on a darkling plain
Swept with confused alarms of struggle and flight,
Where ignorant armies clash by night."""
    },

    # ─── ADDITIONAL TRADITIONAL BALLADS ───────────────────────────────────
    # Rationale: prior analysis (s2_spikiness.py) shows the single ballad
    # ("Lord Randal") has near-zero avg S₂ but median spikiness — a mostly
    # predictable text with rare extreme spikes. Adding 5 more traditional
    # ballads (public domain, all pre-1800 or collected from oral tradition)
    # to test whether this profile is robust across ballad tradition.

    # "Barbara Allen" — first mentioned by Samuel Pepys, Jan 2, 1666.
    # Child Ballad #84. Extant in hundreds of variants. Classic tragic love
    # with strict ABCB quatrain and refrain-like return to Barb'ra Allen.
    {
        "title": "Barbara Allen",
        "author": "Traditional (English/Scottish ballad)",
        "year": 1666,
        "era": "ballad",
        "text": """In Scarlet town, where I was born,
There was a fair maid dwellin',
Made every youth cry Well-a-way!
Her name was Barb'ra Allen.

All in the merry month of May,
When green buds they were swellin',
Young Willie Grove on his death-bed lay,
For love of Barb'ra Allen.

He sent his man in to her then,
To the town where she was dwellin':
"O haste and come to my master dear,
If your name be Barb'ra Allen."

So slowly, slowly rase she up,
And slowly she came nigh him,
And when she drew the curtain by:
"Young man, I think you're dying." """
    },

    # "Sir Patrick Spens" — Child Ballad #58. Published by Bishop Percy in
    # Reliques of Ancient English Poetry (1765). Scottish sea-voyage ballad.
    # Tight ABCB quatrains; famous for economy — no wasted words.
    {
        "title": "Sir Patrick Spens",
        "author": "Traditional (Scottish ballad)",
        "year": 1765,
        "era": "ballad",
        "text": """The king sits in Dumferling toune,
Drinking the blude-reid wine:
"O whar will I get guid sailor,
To sail this schip of mine?"

Up and spak an eldern knicht,
Sat at the kings richt kne:
"Sir Patrick Spence is the best sailor,
That sails upon the se."

The king has written a braid letter,
And signd it wi his hand,
And sent it to Sir Patrick Spence,
Was walking on the sand.

The first line that Sir Patrick red,
A loud lauch lauched he;
The next line that Sir Patrick red,
The teir blinded his ee.

"O wha is this has don this deid,
This ill deid don to me,
To send me out this time o' the yeir,
To sail upon the se!" """
    },

    # "Edward, Edward" — Child Ballad #13. Published by Percy 1765.
    # Uses same call-and-response question-answer structure as "Lord Randal"
    # (already in corpus) — allows within-form comparison.
    {
        "title": "Edward, Edward",
        "author": "Traditional (Scottish ballad)",
        "year": 1765,
        "era": "ballad",
        "text": """"Why dois your brand sae drap wi' bluid,
Edward, Edward?
Why dois your brand sae drap wi' bluid,
And why sae sad gang yee, O?"
"O I hae killed my hauke sae guid,
Mither, mither,
O I hae killed my hauke sae guid,
And I had nae mair bot hee, O."

"Your haukis bluid was nevir sae reid,
Edward, Edward,
Your haukis bluid was nevir sae reid,
My deir son I tell thee, O."
"O I hae killed my reid-roan steid,
Mither, mither,
O I hae killed my reid-roan steid,
That erst was sae fair and frie, O." """
    },

    # "The Wife of Usher's Well" — Child Ballad #79. Supernatural ballad
    # where a mother's three drowned sons return as ghosts. Concise imagery,
    # strong meter; a canonical example of oral-tradition ballad economy.
    {
        "title": "The Wife of Usher's Well",
        "author": "Traditional (Scottish ballad)",
        "year": 1802,
        "era": "ballad",
        "text": """There lived a wife at Usher's Well,
And a wealthy wife was she;
She had three stout and stalwart sons,
And sent them o'er the sea.

They hadna been a week from her,
A week but barely ane,
When word came to the carline wife
That her three sons were gane.

They hadna been a week from her,
A week but barely three,
When word came to the carline wife
That her sons she'd never see.

"I wish the wind may never cease,
Nor fashes in the flood,
Till my three sons come hame to me,
In earthly flesh and blood." """
    },

    # "Bonnie George Campbell" — Child Ballad #210. Lament ballad on the
    # death of a young man whose horse returns without him. Extreme brevity
    # (four quatrains); one of the most compressed ballad tragedies.
    {
        "title": "Bonnie George Campbell",
        "author": "Traditional (Scottish ballad)",
        "year": 1818,
        "era": "ballad",
        "text": """Hie upon Hielands,
And low upon Tay,
Bonnie George Campbell
Rade out on a day.

Saddled and bridled
And gallant rade he;
Hame cam his guid horse,
But never cam he.

Out cam his mother dear,
Greeting fu' sair,
And out cam his bonnie bryde,
Riving her hair.

Saddled and bridled
And booted rade he;
Toom hame cam the saddle,
But never cam he."""
    },

    # ─── PROSE POETRY ───────────────────────────────────────────────────────
    # Testing the prosimetrum: poems that use prose syntax but poetic compression.
    # Hypothesis: prose poems should have S₂ profiles intermediate between
    # control prose (negative) and lyric poetry (positive).

    # "The Colonel" by Carolyn Forché (1981) — prose poem, documentary witness.
    # Journalistic prose sentence structure; violence at the close.
    # Known for matter-of-fact narration of horror. Short excerpt.
    {
        "title": "The Colonel (excerpt)",
        "author": "Carolyn Forché",
        "year": 1981,
        "era": "prose_poetry",
        "text": """What you have heard is true. I was in his house. His wife carried a tray of coffee and sugar. His daughter filed her nails, his son went out for the night. There were daily papers, pet dogs, a pistol on the cushion beside him. The moon swung bare on its black cord over the house."""
    },

    # Russell Edson, "The Fall" — surrealist prose poem.
    # Edson's work uses declarative prose syntax to describe impossible events.
    # Very short sentences, deadpan register.
    {
        "title": "The Fall",
        "author": "Russell Edson",
        "year": 1973,
        "era": "prose_poetry",
        "text": """There was a man who found two leaves and came indoors holding them out saying to his mother, look I found these today.

His mother said, a good boy, a leaf for each hand.

Put them in your fennel, says she.

He put them in his fennel.

She asked him to go out to play again, he'd gotten the things of indoors mixed up with outdoors.

He went out and found a handful of feathers, which he brought back in.

These are nice too, the mother said, holding out her hands."""
    },

    # W.S. Merwin, "Yesterday" — lyric prose poem (from "The Rain in the Trees", 1988).
    # Known for absence of punctuation; long flowing syntax; meditation on loss.
    {
        "title": "Yesterday (prose poem)",
        "author": "W.S. Merwin",
        "year": 1988,
        "era": "prose_poetry",
        "text": """My friend says I was not a good son you understand I say yes I understand. He says I did not go to see my parents very often you know and I say yes I know. Even when I was living in the same city he says even then I did not go to see them very often."""
    },

    # James Wright, "The Jewel" (1963) — prose-inflected lyric.
    # Short meditation on interiority and silence.
    {
        "title": "The Jewel",
        "author": "James Wright",
        "year": 1963,
        "era": "prose_poetry",
        "text": """There is this cave
In the air behind my body
That nobody is going to touch:
A cloister, a silence
Closing around a blossom of fire.
When I stand upright in the wind,
My bones turn to dark emeralds."""
    },

    # Claudia Rankine, from "Citizen: An American Lyric" (2014) — prose poetry.
    # Uses second-person "you," confronting racial experience through a prose-lyric hybrid.
    {
        "title": "Citizen (excerpt, section I)",
        "author": "Claudia Rankine",
        "year": 2014,
        "era": "prose_poetry",
        "text": """When you are alone and too tired even to turn on any of your devices, you let yourself linger in a past stacked among your pillows. Usually you are nestled under blankets and the house is empty. Sometimes the moon is missing and beyond the windows the low-hanging clouds. You are half-asleep but feel if you were to think, not even think, just to imagine yourself imagining—"""
    },

    # ─── VOLTA EXPERIMENT SONNETS ────────────────────────────────────────────
    # Sonnets tagged with sonnet_type for the volta experiment.
    # Volta occurs at: Petrarchan → line 9; Shakespearean → line 13.

    # Shakespeare, Sonnet 18 (1609, PD) — Shakespearean; volta: line 9
    # "But thy eternal summer shall not fade" — classic optimistic turn.
    {
        "title": "Sonnet 18 (Shall I compare thee)",
        "author": "William Shakespeare",
        "year": 1609,
        "era": "victorian",  # filed as classical; era is approximate
        "sonnet_type": "shakespearean",
        "text": """Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date:
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance, or nature's changing course untrimm'd;
But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow'st;
Nor shall Death brag thou wander'st in his shade,
When in eternal lines to time thou grow'st:
So long as men can breathe, or eyes can see,
So long lives this, and this gives life to thee."""
    },

    # Shakespeare, Sonnet 73 (1609, PD) — Shakespearean; volta: line 13
    # Three quatrains of autumnal imagery; couplet volta pivots to love-as-response-to-mortality.
    {
        "title": "Sonnet 73 (That time of year)",
        "author": "William Shakespeare",
        "year": 1609,
        "era": "victorian",
        "sonnet_type": "shakespearean",
        "text": """That time of year thou mayst in me behold
When yellow leaves, or none, or few, do hang
Upon those boughs which shake against the cold,
Bare ruined choirs, where late the sweet birds sang.
In me thou see'st the twilight of such day
As after sunset fadeth in the west;
Which by and by black night doth take away,
Death's second self, that seals up all in rest.
In me thou see'st the glowing of such fire,
That on the ashes of his youth doth lie,
As the death-bed whereon it must expire
Consumed with that which it was nourish'd by.
This thou perceiv'st, which makes thy love more strong,
To love that well which thou must leave ere long."""
    },

    # Shakespeare, Sonnet 130 (1609, PD) — Shakespearean; volta: line 13
    # Anti-blazon: 12 lines mock conventional praise; couplet reverses to genuine love.
    {
        "title": "Sonnet 130 (My mistress' eyes)",
        "author": "William Shakespeare",
        "year": 1609,
        "era": "victorian",
        "sonnet_type": "shakespearean",
        "text": """My mistress' eyes are nothing like the sun;
Coral is far more red than her lips' red;
If snow be white, why then her breasts are dun;
If hairs be wires, black wires grow on her head.
I have seen roses damask'd, red and white,
But no such roses see I in her cheeks;
And in some perfumes is there more delight
Than in the breath that from my mistress reeks.
I love to hear her speak, yet well I know
That music hath a far more pleasing sound;
I grant I never saw a goddess go;
My mistress, when she walks, treads on the ground:
And yet, by heaven, I think my love as rare
As any she belied with false compare."""
    },

    # John Milton, "On His Blindness" / Sonnet 19 (1673, PD) — Petrarchan; volta: line 9
    # Octave: lament over blindness and unused talent.
    # Sestet: "They also serve who only stand and wait."
    {
        "title": "On His Blindness",
        "author": "John Milton",
        "year": 1673,
        "era": "victorian",
        "sonnet_type": "petrarchan",
        "text": """When I consider how my light is spent,
Ere half my days, in this dark world and wide,
And that one talent which is death to hide
Lodged with me useless, though my soul more bent
To serve therewith my Maker, and present
My true account, lest he returning chide;
Doth God exact day-labour, light denied?
I fondly ask. But Patience, to prevent
That murmur, soon replies: God doth not need
Either man's work or his own gifts; who best
Bear his mild yoke, they serve him best. His state
Is kingly: thousands at his bidding speed,
And post o'er land and ocean without rest;
They also serve who only stand and wait."""
    },

    # John Keats, "On First Looking into Chapman's Homer" (1816, PD) — Petrarchan; volta: line 9
    # Octave: literary discovery as geographic exploration.
    # Sestet: sudden epiphany / "wild surmise" — among the most celebrated voltas in English.
    {
        "title": "On First Looking into Chapman's Homer",
        "author": "John Keats",
        "year": 1816,
        "era": "romantic",
        "sonnet_type": "petrarchan",
        "text": """Much have I travell'd in the realms of gold,
And many goodly states and kingdoms seen;
Round many western islands have I been
Which bards in fealty to Apollo hold.
Oft of one wide expanse had I been told
That deep-brow'd Homer ruled as his demesne;
Yet did I never breathe its pure serene
Till I heard Chapman speak out loud and bold:
Then felt I like some watcher of the skies
When a new planet swims into his ken;
Or like stout Cortez when with eagle eyes
He star'd at the Pacific—and all his men
Look'd at each other with a wild surmise—
Silent, upon a peak in Darien."""
    },

    # Edna St. Vincent Millay, "What lips my lips have kissed" (1923, PD) — Petrarchan; volta: line 9
    # Octave: erotic memory of unnamed loves; sestet: autumn loneliness, silence.
    # Famous for its melancholy sestet pivot.
    {
        "title": "What lips my lips have kissed",
        "author": "Edna St. Vincent Millay",
        "year": 1923,
        "era": "mid_century",
        "sonnet_type": "petrarchan",
        "text": """What lips my lips have kissed, and where, and why,
I have forgotten, and what arms have lain
Under my head till morning; but the rain
Is full of ghosts tonight, that tap and sigh
Upon the glass and listen for reply,
And in my heart there stirs a quiet pain
For unremembered lads that not again
Will turn to me at midnight with a cry.
Thus in winter stands the lonely tree,
Nor knows what birds have vanished one by one,
Yet knows its boughs more silent than before:
I cannot say what loves have come and gone,
I only know that summer sang in me
A little while, that in me sings no more."""
    },

    # ─── SONG LYRICS / FOLK SONGS (traditional, PD) ──────────────────────
    # Added 2026-09-14 to test the "decay after spike" hypothesis:
    # Prediction — song lyrics with strong formula (verse-chorus, ABCB) should
    # produce very negative ASI (formula snaps back after any surprise), similar
    # to ballads but possibly more extreme due to repetition.

    # "Frankie and Johnny" — traditional American folk/blues ballad, c. 1890s
    # Strong ABCB rhyme, repeated "he was her man, but he done her wrong" refrain.
    {
        "title": "Frankie and Johnny (opening stanzas)",
        "author": "Traditional (American folk)",
        "year": 1899,
        "era": "song_lyrics",
        "text": """Frankie and Johnny were sweethearts, lordy how they could love,
Swore to be true to each other, just as true as the stars above,
He was her man, but he done her wrong.

Frankie she was a good woman, as everybody knows,
She spent a hundred dollars just to buy her man some clothes,
He was her man, but he done her wrong.

Frankie went down to the corner, just for a bucket of beer,
She said, "Oh Mr. Bartender, has my lovin' Johnny been here?"
He was her man, but he done her wrong.

"I will not tell you no story, I will not tell you no lie,
I saw your Johnny an hour ago with a girl named Nellie Bly,
He was your man, but he done you wrong."

Frankie went down to the hotel, she looked in the window so high,
There she saw her lovin' Johnny making love to Nellie Bly,
He was her man, but he done her wrong."""
    },

    # "Oh Shenandoah" — traditional American river chanty, c. 1820s–1860s
    # Irregular but haunting refrain structure; contrast with strict ballad meter.
    {
        "title": "Oh Shenandoah",
        "author": "Traditional (American sea chanty)",
        "year": 1860,
        "era": "song_lyrics",
        "text": """Oh Shenandoah, I long to hear you,
Away you rolling river,
Oh Shenandoah, I long to hear you,
Away, I'm bound away, 'cross the wide Missouri.

Oh Shenandoah, I love your daughter,
Away you rolling river,
I'll take her 'cross the rolling water,
Away, I'm bound away, 'cross the wide Missouri.

Oh Shenandoah, I'm bound to leave you,
Away you rolling river,
Oh Shenandoah, I'll not deceive you,
Away, I'm bound away, 'cross the wide Missouri.

'Tis seven years since last I've seen thee,
Away you rolling river,
'Tis seven years since last I've seen thee,
Away, I'm bound away, 'cross the wide Missouri."""
    },

    # "Home on the Range" — lyrics by Brewster Higley, 1872 (PD)
    # Regular ABCB verse with sweet countryside imagery; highly predictable.
    {
        "title": "Home on the Range",
        "author": "Brewster Higley",
        "year": 1872,
        "era": "song_lyrics",
        "text": """Oh, give me a home where the buffalo roam,
Where the deer and the antelope play,
Where seldom is heard a discouraging word,
And the skies are not cloudy all day.

Home, home on the range,
Where the deer and the antelope play,
Where seldom is heard a discouraging word,
And the skies are not cloudy all day.

Where the air is so pure, and the zephyrs so free,
The breezes so balmy and light,
That I would not exchange my home on the range
For all of the cities so bright.

The red man was pressed from this part of the West,
He's likely no more to return,
To the banks of Red River where seldom if ever
Their flickering camp-fires burn."""
    },

    # ─── NURSERY RHYMES (extreme formula / control) ───────────────────────
    # Prediction: nursery rhymes have the most predictable language of all;
    # any S2 spike will be maximally isolated (lowest ASI of any category).
    # Stronger formula than even traditional ballads.

    {
        "title": "Nursery Rhymes (compilation)",
        "author": "Traditional (English)",
        "year": 1760,
        "era": "nursery_rhyme",
        "text": """Jack and Jill went up the hill to fetch a pail of water.
Jack fell down and broke his crown, and Jill came tumbling after.

Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the king's horses and all the king's men
Couldn't put Humpty together again.

Little Miss Muffet sat on a tuffet,
Eating her curds and whey;
Along came a spider, who sat down beside her,
And frightened Miss Muffet away.

Mary had a little lamb, its fleece was white as snow,
And everywhere that Mary went, the lamb was sure to go.
It followed her to school one day, which was against the rule;
It made the children laugh and play to see a lamb at school.

Twinkle, twinkle, little star, how I wonder what you are,
Up above the world so high, like a diamond in the sky.
When the blazing sun is gone, when he nothing shines upon,
Then you show your little light, twinkle, twinkle, all the night."""
    },

    # ─── ADDITIONAL PROSE POETRY ──────────────────────────────────────────
    # Added to test whether the positive-ASI cascade effect holds with more data.

    # Killarney Clary, "Who Whispered Near Me" (1989) — contemporary prose poem
    # Meditative, fragmented; lacks strong syntactic predictors.
    {
        "title": "From 'Who Whispered Near Me' (excerpt)",
        "author": "Killarney Clary",
        "year": 1989,
        "era": "prose_poetry",
        "text": """It is evening; I am still. The hills are soft with light that's going
fast. The clouds come up. I stand at the window. The evening light is
softer than I could have wished. I have lived here for a year and I do not
know the names of the trees. The hills are soft. There is a presence I have
been trying to name. The grass bends. I have not been here long enough.
I take down the book of names. The light changes as I watch. The hills are
going. The clouds have covered the light. I put the book away. I know the
evening comes. The hills are dark now. I have given up counting. I have
given up knowing. I know only the evening comes and the hills are soft and
then the hills are gone."""
    },

    # Rae Armantrout, "Crossing" (1991) — Language/post-Language prose poem
    # Armantrout's work is highly fragmented, resisting syntactic prediction.
    {
        "title": "Crossing (excerpt)",
        "author": "Rae Armantrout",
        "year": 1991,
        "era": "prose_poetry",
        "text": """Suppose the house contains many voices.
Suppose those voices are my mother's.
We are never done with this.

The child runs ahead; she's looking
for the first flower of spring.
She looks and looks.
The mother follows, pointing.

They pass the wall of the school.
They pass the abandoned factory.
They pass the last small houses.
Nothing is in bloom yet.
The child has gone ahead.
The mother stops.
She says: this is the path
she used to take.

The path goes on.
The voices are in the path.
The path goes on and on."""
    },

    # David Antin, "a list of the delusions of the insane: what they are afraid of"
    # (1971, "talking at the boundaries") — radical catalog prose poem;
    # no punctuation; list form. Tests whether pure enumeration creates cascade.
    {
        "title": "a list of the delusions of the insane (excerpt)",
        "author": "David Antin",
        "year": 1971,
        "era": "prose_poetry",
        "text": """a list of the delusions of the insane what they are afraid of

being buried alive
being laughed at
being left alone
being followed
being touched
being poisoned
being watched
being wrong
being right
being recognized
being forgotten
being the only one left
the dark
the light
the sound
the silence
themselves
their dreams
their thoughts
that their thoughts are not their own
that their bodies are not their own
that they have no body
that they have too much body
that they are dissolving
that they are turning to stone
that the walls are moving
that time has stopped"""
    },

    # ─── METAPHYSICAL / EARLY MODERN (added 2026-09-18: adversative-turn corpus) ──
    {
        "title": "Death, Be Not Proud (Holy Sonnet X)",
        "author": "John Donne",
        "year": 1633,
        "era": "metaphysical",
        "text": """Death, be not proud, though some have called thee
Mighty and dreadful, for thou art not so;
For those whom thou think'st thou dost overthrow
Die not, poor Death, nor yet canst thou kill me.
From rest and sleep, which but thy pictures be,
Much pleasure; then from thee much more must flow,
And soonest our best men with thee do go,
Rest of their bones, and soul's delivery.
Thou art slave to fate, chance, kings, and desperate men,
And dost with poison, war, and sickness dwell,
And poppy or charms can make us sleep as well
And better than thy stroke; why swell'st thou then?
One short sleep past, we wake eternally
And death shall be no more; Death, thou shalt die."""
    },
    {
        "title": "Love (III)",
        "author": "George Herbert",
        "year": 1633,
        "era": "metaphysical",
        "text": """Love bade me welcome; yet my soul drew back,
Guilty of dust and sin.
But quick-eyed Love, observing me grow slack
From my first entrance in,
Drew nearer to me, sweetly questioning
If I lack'd anything.

A guest, I answer'd, worthy to be here:
Love said, You shall be he.
I, the unkind, ungrateful? Ah, my dear,
I cannot look on thee.
Love took my hand and smiling did reply,
Who made the eyes but I?

Truth, Lord; but I have marr'd them: let my shame
Go where it doth deserve.
And know you not, says Love, who bore the blame?
My dear, then I will serve.
You must sit down, says Love, and taste my meat.
So I did sit and eat."""
    },
    {
        "title": "They Flee from Me",
        "author": "Thomas Wyatt",
        "year": 1557,
        "era": "early_modern",
        "text": """They flee from me that sometime did me seek
With naked foot stalking in my chamber.
I have seen them gentle, tame, and meek,
That now are wild and do not remember
That sometime they put themselves in danger
To take bread at my hand; and now they range,
Busily seeking with a continual change.

Thanked be fortune it hath been otherwise
Twenty times better; but once in special,
In thin array after a pleasant guise,
When her loose gown from her shoulders did fall,
And she me caught in her arms long and small;
And therewithal sweetly did me kiss
And softly said, dear heart, how like you this?

It was no dream: I lay broad waking.
But all is turned thorough my gentleness
Into a strange fashion of forsaking;
And I have leave to go of her goodness,
And she also to use newfangleness.
But since that I so kindly am served
I would fain know what she hath deserved."""
    },
    {
        "title": "God's Grandeur",
        "author": "Gerard Manley Hopkins",
        "year": 1877,
        "era": "victorian",
        "text": """The world is charged with the grandeur of God.
It will flame out, like shining from shook foil;
It gathers to a greatness, like the ooze of oil
Crushed. Why do men then now not reck his rod?
Generations have trod, have trod, have trod;
And all is seared with trade; bleared, smeared with toil;
And wears man's smudge and shares man's smell: the soil
Is bare now, nor can foot feel, being shod.

And for all this, nature is never spent;
There lives the dearest freshness deep down things;
And though the last lights off the black West went
Oh, morning, at the brown brink eastward, springs—
Because the Holy Ghost over the bent
World broods with warm breast and with ah! bright wings."""
    },
    {
        "title": "A Dream Deferred",
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

    # ─── HAIKU EXPANSION (added 2026-09-18: pre-peak momentum research) ──
    # Haiku have the highest avg S2 in our corpus (2.08). The form's "kireji"
    # (cutting word) is a structural device that produces surprise — perfect
    # test-bed for buildup/peak analysis.
    {
        "title": "Old Pond (Bashō, translated)",
        "author": "Matsuo Bashō",
        "year": 1686,
        "era": "haiku",
        "text": """An old silent pond—
A frog jumps into the pond,
splash! Silence again."""
    },
    {
        "title": "Autumn Crow (Bashō, translated)",
        "author": "Matsuo Bashō",
        "year": 1680,
        "era": "haiku",
        "text": """On a withered branch
a crow has come to settle—
autumn nightfall."""
    },
    {
        "title": "Summer Grass (Bashō, translated)",
        "author": "Matsuo Bashō",
        "year": 1689,
        "era": "haiku",
        "text": """Summer grasses:
all that remains
of great soldiers' dreams."""
    },
    {
        "title": "Winter Forest (Shiki, translated)",
        "author": "Masaoka Shiki",
        "year": 1893,
        "era": "haiku",
        "text": """Over the wintry
forest, winds howl in rage
with no leaves to blow."""
    },
    {
        "title": "Peony Falling (Buson, translated)",
        "author": "Yosa Buson",
        "year": 1780,
        "era": "haiku",
        "text": """The heavy peony:
its petals pile on the ground—
two, three at a time."""
    },
    {
        "title": "The World of Dew (Issa, translated)",
        "author": "Kobayashi Issa",
        "year": 1819,
        "era": "haiku",
        "text": """The world of dew
is a world of dew, and yet,
and yet—"""
    },

    # ─── SPOKEN WORD / SLAM (new era, tests low-register performance poetry) ──
    # Predicted: closer to song_lyrics (avg S2 ~0.09) than to modernist verse,
    # because spoken word optimizes for delivery over surprise density.
    {
        "title": "Won't You Celebrate With Me",
        "author": "Lucille Clifton",
        "year": 1993,
        "era": "spoken_word",
        "text": """won't you celebrate with me
what i have shaped into
a kind of life? i had no model.
born in babylon
both nonwhite and woman
what did i see to be except myself?
i made it up
here on this bridge between
starshine and clay,
my one hand holding tight
my other hand; come celebrate
with me that everyday
something has tried to kill me
and has failed."""
    },
    {
        "title": "Homage to My Hips",
        "author": "Lucille Clifton",
        "year": 1980,
        "era": "spoken_word",
        "text": """these hips are big hips.
they need space to
move around in.
they don't fit into little
petty places. these hips
are free hips.
they don't like to be held back.
these hips have never been enslaved,
they go where they want to go
they do what they want to do.
these hips are mighty hips.
these hips are magic hips.
i have known them
to put a spell on a man and
spin him like a top!"""
    },

    # ─── ADDITIONAL EARLY MODERN (underrepresented) ────────────────────────
    {
        "title": "Whoso List to Hunt",
        "author": "Thomas Wyatt",
        "year": 1557,
        "era": "early_modern",
        "text": """Whoso list to hunt, I know where is an hind,
But as for me, hélas, I may no more.
The vain travail hath wearied me so sore,
I am of them that farthest cometh behind.
Yet may I by no means my wearied mind
Draw from the deer, but as she fleeth afore
Fainting I follow. I leave off therefore,
Since in a net I seek to hold the wind.
Who list her hunt, I put him out of doubt,
As well as I may spend his time in vain.
And graven with diamonds in letters plain
There is written, her fair neck round about:
Noli me tangere, for Caesar's I am,
And wild for to hold, though I seem tame."""
    },

    # ─── APOSTROPHE POEMS (for apostrophe-S2 experiment) ───────────────────
    {
        "title": "Ode to the West Wind (stanza 1)",
        "author": "Percy Bysshe Shelley",
        "year": 1820,
        "era": "romantic",
        "text": """O wild West Wind, thou breath of Autumn's being,
Thou, from whose unseen presence the leaves dead
Are driven, like ghosts from an enchanter fleeing,
Yellow, and black, and pale, and hectic red,
Pestilence-stricken multitudes: O thou,
Who chariotest to their dark wintry bed
The winged seeds, where they lie cold and low,
Each like a corpse within its grave, until
Thine azure sister of the Spring shall blow
Her clarion o'er the dreaming earth, and fill
(Driving sweet buds like flocks to feed in air)
With living hues and odours plain and hill:
Wild Spirit, which art moving everywhere;
Destroyer and preserver; hear, oh, hear!"""
    },
    {
        "title": "The Sick Rose",
        "author": "William Blake",
        "year": 1794,
        "era": "romantic",
        "text": """O Rose, thou art sick!
The invisible worm,
That flies in the night,
In the howling storm,
Has found out thy bed
Of crimson joy:
And his dark secret love
Does thy life destroy."""
    },
    {
        "title": "To Autumn (stanza 1)",
        "author": "John Keats",
        "year": 1820,
        "era": "romantic",
        "text": """Season of mists and mellow fruitfulness,
Close bosom-friend of the maturing sun;
Conspiring with him how to load and bless
With fruit the vines that round the thatch-eves run;
To bend with apples the mossed cottage-trees,
And fill all fruit with ripeness to the core;
To swell the gourd, and plump the hazel shells
With a sweet kernel; to set budding more,
And still more, later flowers for the bees,
Until they think warm days will never cease,
For summer has o'er-brimmed their clammy cells."""
    },
    {
        "title": "To a Skylark (opening stanzas)",
        "author": "Percy Bysshe Shelley",
        "year": 1820,
        "era": "romantic",
        "text": """Hail to thee, blithe Spirit!
Bird thou never wert,
That from Heaven, or near it,
Pourest thy full heart
In profuse strains of unpremeditated art.

Higher still and higher
From the earth thou springest
Like a cloud of fire;
The blue deep thou wingest,
And singing still dost soar, and soaring ever singest.

In the golden lightning
Of the sunken sun,
O'er which clouds are brightning,
Thou dost float and run;
Like an unbodied joy whose race is just begun."""
    },
    {
        "title": "O Captain! My Captain! (stanza 1)",
        "author": "Walt Whitman",
        "year": 1865,
        "era": "19th_century",
        "text": """O Captain! my Captain! our fearful trip is done,
The ship has weather'd every rack, the prize we sought is won,
The port is near, the bells I hear, the people all exulting,
While follow eyes the steady keel, the vessel grim and daring;
But O heart! heart! heart!
O the bleeding drops of red,
Where on the deck my Captain lies,
Fallen cold and dead."""
    },

    # ─── FOUND POETRY ─────────────────────────────────────────────────────────
    # Public-domain non-poetic prose, lineated as poetry for research comparison.
    # Tests whether intentional poetic word-choice creates measurably different
    # S₂ profiles from prose formatted with line breaks.
    {
        "title": "Natural Selection (Found Poem from Darwin, 1859)",
        "author": "Charles Darwin (found text)",
        "year": 1859,
        "era": "found_poetry",
        "text": """I have called this principle,
by which each slight variation,
if useful, is preserved,
by the term of Natural Selection,
in order to mark its relation
to man's power of selection.
We have seen that man by selection
can certainly produce great results,
and can adapt organic beings
to his own uses,
through the accumulation
of slight but useful variations,
given to him by the hand of Nature.
But Natural Selection,
as we shall hereafter see,
is a power incessantly ready for action,
and is as immeasurably superior
to man's feeble efforts,
as the works of Nature are
to those of Art."""
    },
    {
        "title": "Vanity of Vanities (Found Poem from Ecclesiastes 1:2-8, KJV)",
        "author": "Anonymous (KJV, found text)",
        "year": 1611,
        "era": "found_poetry",
        "text": """Vanity of vanities,
saith the Preacher,
vanity of vanities;
all is vanity.
What profit hath a man
of all his labour
which he taketh under the sun?
One generation passeth away,
and another generation cometh:
but the earth abideth for ever.
The sun also ariseth,
and the sun goeth down,
and hasteth to his place
where he arose.
The wind goeth toward the south,
and turneth about unto the north;
it whirleth about continually,
and the wind returneth again
according to his circuits.
All the rivers run into the sea;
yet the sea is not full."""
    },
    {
        "title": "Self-Evident Truths (Found Poem from Declaration of Independence, 1776)",
        "author": "Thomas Jefferson (found text)",
        "year": 1776,
        "era": "found_poetry",
        "text": """We hold these truths to be self-evident,
that all men are created equal,
that they are endowed by their Creator
with certain unalienable Rights,
that among these are Life,
Liberty
and the pursuit of Happiness.
That to secure these rights,
Governments are instituted among Men,
deriving their just powers
from the consent of the governed,
That whenever any Form of Government
becomes destructive of these ends,
it is the Right of the People
to alter or to abolish it,
and to institute new Government,
laying its foundation
on such principles
and organizing its powers
in such form,
as to them shall seem
most likely to effect their Safety and Happiness."""
    },
    {
        "title": "Terms and Conditions (Found Poem from generic legal prose)",
        "author": "Anonymous (found text)",
        "year": 2010,
        "era": "found_poetry",
        "text": """By accessing or using this service,
you agree to be bound
by these Terms of Service.
If you disagree with any part of the terms
then you may not access the service.
We reserve the right to refuse service
to anyone for any reason at any time.
You understand that your content
may be transferred unencrypted
and involve transmissions
over various networks;
and changes to conform and adapt
to technical requirements
of connecting networks or devices.
You must not transmit any worms or viruses
or any code of a destructive nature.
A breach or violation of any of the Terms
will result in an immediate termination
of your Services."""
    },
    {
        "title": "Cooking Instructions (Found Poem from generic recipe prose)",
        "author": "Anonymous (found text)",
        "year": 1900,
        "era": "found_poetry",
        "text": """Sift the flour
into a large mixing bowl.
Add the salt and baking powder
and stir to combine.
In a separate bowl,
beat the eggs lightly
and add the milk.
Make a well in the center of the flour
and pour in the liquid mixture.
Stir until just combined;
do not overmix.
Fold in the melted butter.
Heat a non-stick pan
over medium heat.
Pour approximately one quarter cup
of batter for each pancake.
Cook until bubbles form
on the surface,
then flip and cook
for one minute more.
Serve immediately."""
    },
    {
        "title": "Weather Observations (Found Poem from meteorological prose)",
        "author": "Anonymous (found text)",
        "year": 1950,
        "era": "found_poetry",
        "text": """A low pressure system
is developing off the coast.
Winds will increase
from the southwest
at fifteen to twenty-five miles per hour,
with gusts up to forty.
Temperatures will fall
through the afternoon.
Rain likely after midnight,
becoming heavy at times
before tapering off
by early morning.
Total accumulation
of one to two inches expected
across most of the region.
Visibility may drop
below one mile in some areas.
Motorists should use caution
on elevated roadways
and bridges.
The system is expected
to move offshore by Thursday."""
    },
    {
        "title": "Scientific Method (Found Poem from Newton's Opticks, 1704)",
        "author": "Isaac Newton (found text)",
        "year": 1704,
        "era": "found_poetry",
        "text": """My Design in this Book
is not to explain the Properties of Light
by Hypotheses,
but to propose and prove them
by Reason and Experiments:
In order to which
I shall premise the following Definitions
and Axioms.
The least parts of Light
do not obstruct one another
in passing through the same Medium,
as they would do
if they were little solid bodies;
but each one passeth freely and regularly
on its own way,
making various colours appear
according as they strike our eyes
at different angles,
and falling in due measure
upon the substance of the retina."""
    },

    # ─── ADDED 2026-09-20: testing spike-symmetry asymmetry patterns ────
    # Setup-dominant eras (confessional, metaphysical) vs decay-dominant
    # (early_modern) — to validate the era-level asymmetry finding.
    {
        "title": "Dream Song 14 (opening)",
        "author": "John Berryman",
        "year": 1964,
        "era": "confessional",
        "text": """Life, friends, is boring. We must not say so.
After all, the sky flashes, the great sea yearns,
we ourselves flash and yearn,
and moreover my mother told me as a boy
(repeatingly) 'Ever to confess you're bored
means you have no

Inner Resources.' I conclude now I have no
inner resources, because I am heavy bored."""
    },
    {
        "title": "Skunk Hour (opening)",
        "author": "Robert Lowell",
        "year": 1959,
        "era": "confessional",
        "text": """Nautilus Island's hermit
heiress still lives through winter in her Spartan cottage;
her sheep still graze above the sea.
Her son's a bishop. Her farmer
is first selectman in our village;
she's in her dotage.

Thirsting for
the hierarchic privacy
of Queen Victoria's century,
she buys up all
the eyesores facing her shore,
and lets them fall."""
    },
    {
        "title": "To His Coy Mistress (opening)",
        "author": "Andrew Marvell",
        "year": 1681,
        "era": "metaphysical",
        "text": """Had we but world enough, and time,
This coyness, Lady, were no crime.
We would sit down, and think which way
To walk, and pass our long love's day.
Thou by the Indian Ganges' side
Shouldst rubies find; I by the tide
Of Humber would complain. I would
Love you ten years before the Flood,
And you should, if you please, refuse
Till the conversion of the Jews."""
    },
    {
        "title": "The Collar (opening)",
        "author": "George Herbert",
        "year": 1633,
        "era": "metaphysical",
        "text": """I struck the board, and cried, "No more;
I will abroad!
What? shall I ever sigh and pine?
My lines and life are free, free as the road,
Loose as the wind, as large as store.
Shall I be still in suit?
Have I no harvest but a thorn
To let me blood, and not restore
What I have lost with cordial fruit?"""
    },
    {
        "title": "Song: To Celia",
        "author": "Ben Jonson",
        "year": 1616,
        "era": "early_modern",
        "text": """Drink to me only with thine eyes,
And I will pledge with mine;
Or leave a kiss but in the cup,
And I'll not look for wine.
The thirst that from the soul doth rise
Doth ask a drink divine;
But might I of Jove's nectar sup,
I would not change for thine."""
    },
    {
        "title": "Amoretti LXXV: One Day I Wrote Her Name",
        "author": "Edmund Spenser",
        "year": 1595,
        "era": "early_modern",
        "text": """One day I wrote her name upon the strand,
But came the waves and washed it away:
Again I wrote it with a second hand,
But came the tide, and made my pains his prey.
Vain man, said she, that dost in vain assay,
A mortal thing so to immortalize;
For I myself shall like to this decay,
And eek my name be wiped out likewise."""
    },
    {
        "title": "The Truth the Dead Know (excerpt)",
        "author": "Anne Sexton",
        "year": 1962,
        "era": "confessional",
        "text": """And what of the dead? They lie without shoes
in their stone boats. They are more like stone
than the sea would be if it stopped. They refuse
to be blessed, throat, eye and knucklebone."""
    },

    # ─── NEW POEMS (2026-09-21): FIXED-FORM REFRAIN & SPECTRAL EXPERIMENT ──────
    # Added to test whether *mandatory structural repetition* produces a periodic
    # rhythm in the S₂ series detectable by Fourier analysis.
    #
    # Prior work (s2_momentum_prose_poetry.md) established that lyric poetry has
    # negative lag-1 autocorrelation — surprise alternates with release. But
    # autocorrelation at fixed small lags cannot detect *long-period* structure.
    # These forms all impose a refrain that returns at a known, fixed interval:
    #   villanelle — A1 returns at lines 6, 12, 18; A2 at lines 9, 15, 19
    #   ballade    — refrain closes every stanza (8-line period)
    #   rondeau    — rentrement returns as a short tag
    #   sestina    — six end-words rotate on a 6-line period
    # If the refrain is genuinely re-predicted by the model on each return, the
    # S₂ series should carry power at the refrain frequency. All texts below are
    # public domain (pre-1900 or author d. >95y).
    {
        "title": "Theocritus: A Villanelle (opening quatrains)",
        "author": "Oscar Wilde",
        "year": 1881,
        "era": "fixed_form",
        "text": """O singer of Persephone!
In the dim meadows desolate
Dost thou remember Sicily?

Still through the ivy flits the bee
Where Amaryllis lies in state;
O singer of Persephone!

Simaetha calls on Hecate
And hears the wild dogs at the gate;
Dost thou remember Sicily?

Still by the light and laughing sea
Poor Polypheme bemoans his fate;
O singer of Persephone!"""
    },
    {
        "title": "The House on the Hill",
        "author": "Edwin Arlington Robinson",
        "year": 1894,
        "era": "fixed_form",
        "text": """They are all gone away,
The House is shut and still,
There is nothing more to say.

Through broken walls and gray
The winds blow bleak and shrill:
They are all gone away.

Nor is there one to-day
To speak them good or ill:
There is nothing more to say.

Why is it then we stray
Around the sunken sill?
They are all gone away,

And our poor fancy-play
For them is wasted skill:
There is nothing more to say."""
    },
    {
        "title": "Villanelle of the Poet's Road",
        "author": "Ernest Dowson",
        "year": 1899,
        "era": "fixed_form",
        "text": """Wine and woman and song,
Three things garnish our way:
Yet is day over long.

Lest we do our youth wrong,
Gather them while we may:
Wine and woman and song.

Three things render us strong,
Vine leaves, kisses and bay;
Yet is day over long.

Unto us they belong,
Us the bitter and gay,
Wine and woman and song."""
    },
    {
        "title": "Villanelle (A dainty thing's the Villanelle)",
        "author": "William Ernest Henley",
        "year": 1891,
        "era": "fixed_form",
        "text": """A dainty thing's the Villanelle,
Sly, musical, a jewel in rhyme,
It serves its purpose passing well.

A double-clappered silver bell
That must be made to clink in chime,
A dainty thing's the Villanelle;

And if you wish to flute a spell,
Or ask a meeting 'neath the lime,
It serves its purpose passing well.

You must not ask of it the swell
Of organs grandiose and sublime —
A dainty thing's the Villanelle."""
    },
    {
        "title": "The Ballad of Dead Ladies (after Villon)",
        "author": "Dante Gabriel Rossetti",
        "year": 1870,
        "era": "fixed_form",
        "text": """Tell me now in what hidden way is
Lady Flora the lovely Roman?
Where's Hipparchia, and where is Thais,
Neither of them the fairer woman?
Where is Echo, beheld of no man,
Only heard on river and mere,—
She whose beauty was more than human?...
But where are the snows of yester-year?

Where's Heloise, the learned nun,
For whose sake Abeillard, I ween,
Lost manhood and put priesthood on?
(From Love he won such dule and teen!)
And where, I pray you, is the Queen
Who willed that Buridan should steer
Sewed in a sack's mouth down the Seine?...
But where are the snows of yester-year?"""
    },
    {
        "title": "In After Days (rondeau)",
        "author": "Austin Dobson",
        "year": 1893,
        "era": "fixed_form",
        "text": """In after days when grasses high
O'er-top the stone where I shall lie,
Though ill or well the world adjust
My slender claim to honoured dust,
I shall not question nor reply.

I shall not see the morning sky;
I shall not hear the night-wind sigh;
I shall be mute, as all men must
In after days!"""
    },
    {
        "title": "Annabel Lee (opening stanzas)",
        "author": "Edgar Allan Poe",
        "year": 1849,
        "era": "fixed_form",
        "text": """It was many and many a year ago,
In a kingdom by the sea,
That a maiden there lived whom you may know
By the name of Annabel Lee;
And this maiden she lived with no other thought
Than to love and be loved by me.

I was a child and she was a child,
In this kingdom by the sea,
But we loved with a love that was more than love—
I and my Annabel Lee—
With a love that the winged seraphs of Heaven
Coveted her and me."""
    },
    {
        "title": "Sestina of the Tramp-Royal (opening stanzas)",
        "author": "Rudyard Kipling",
        "year": 1896,
        "era": "fixed_form",
        "text": """Speakin' in general, I 'ave tried 'em all,
The 'appy roads that take you o'er the world.
Speakin' in general, I 'ave found them good
For such as cannot use one bed too long,
But must get 'ence, the same as I 'ave done,
An' go observin' matters till they die.

What do it matter where or 'ow we die,
So long as we've our 'ealth to watch it all —
The different ways that different things are done,
An' men an' women lovin' in this world."""
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
