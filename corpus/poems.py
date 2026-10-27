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

    {
        "title": "I Have Dreamed of You So Much",
        "author": "Robert Desnos",
        "year": 1926,
        "era": "surrealist",
        "text": """I have dreamed of you so much that you lose your reality.
Is there still time for me to reach your breathing body, to kiss your mouth and make
your voice dear to me, that voice which was dear to me?
I have dreamed of you so much that my arms, grown used to being crossed on my
chest as I hugged your shadow, would perhaps not bend to the shape of your body.
For want of time to spend at your side I have embraced your shadow so many times,
your shadow so many times, that perhaps I could not touch your living body.
And even so, in the presence of the real thing, this thing that haunts and governs
me, I would probably become a shadow.
O sentimental balances."""
    },
    {
        "title": "Somnambule Ballad",
        "author": "Federico García Lorca",
        "year": 1928,
        "era": "surrealist",
        "text": """Green, how I want you green.
Green wind. Green branches.
The ship out on the sea
and the horse on the mountain.
With the shadow on her waist
she dreams on her balcony,
green flesh, her hair green,
with eyes of cold silver.
Green, how I want you green.
Under the gypsy moon,
all things are watching her
and she cannot see them.

Green, how I want you green.
Big hoarfrost stars
come with the fish of shadow
that opens the road of dawn.
The fig tree rubs its wind
with the sandpaper of its branches,
and the forest, cunning cat,
bristles its brittle fibers.
But who will come? And from where?
She is still on her balcony,
green flesh, her hair green,
dreaming in the bitter sea."""
    },
    {
        "title": "Black Stone Lying on a White Stone",
        "author": "César Vallejo",
        "year": 1939,
        "era": "surrealist",
        "text": """I will die in Paris, on a rainy day,
on some day I can already remember.
I will die in Paris—and I don't step aside—
perhaps on a Thursday, as today is Thursday, in autumn.

It will be a Thursday, because today, Thursday, as I prose
these lines, the bones of my arms have hurt me, and never,
like today, have I turned, with all my road,
to see myself alone.

César Vallejo has died, everyone would beat him,
although he does nothing to them; they struck him hard
with a stick and hard also

with a rope; his witnesses are
the Thursdays and the arm bones,
the loneliness, the rain, the roads."""
    },
    {
        "title": "The Curve of Your Eyes",
        "author": "Paul Éluard",
        "year": 1926,
        "era": "surrealist",
        "text": """The curve of your eyes goes around my heart,
a round of dance and sweetness,
halo of time, cradle nocturnal and certain,
and if I no longer know all I have lived
it is because your eyes have not always seen me.

Leaves of day and foam of dew,
reeds of wind, smiling incense,
wings covering the world with light,
boats laden with sky and sea,
hunters of sound and sources of color,

Perfumes rising from a nest of dawn
that lingers past the road of the world—
all things are turning on their axis of love,
your eyes are the only dawn."""
    },
    {
        "title": "Walking Around",
        "author": "Pablo Neruda",
        "year": 1935,
        "era": "surrealist",
        "text": """It so happens I am sick of being a man.
And it happens that I walk into tailor-shops and movie houses
dried up, waterproof, like a swan made of felt
steering my way in a water of wombs and ashes.

The smell of barbershops makes me break into hoarse sobs.
The only thing I want is to lie still like stones or wool.
The only thing I want is to see no more stores, no gardens,
no more goods, no spectacles, no elevators.

It so happens I am sick of my feet and my nails
and my hair and my shadow.
It so happens I am sick of being a man.

Still it would be marvelous
to terrify a law clerk with a cut lily,
or kill a nun with a blow to the ear.
It would be great
to go through the streets with a green knife
letting out yells until I died of the cold."""
    },
    {
        "title": "Departure",
        "author": "Pierre Reverdy",
        "year": 1918,
        "era": "surrealist",
        "text": """All the doors are open on the wind
and the shadows of the walls fall slowly
toward you

The trees are burning in the night
the branches spread their arms
the sky falls

Nothing is moving now
but the road
and the light that runs
always a little ahead of you

You will not come back"""
    },
    {
        "title": "The Sleeper in the Valley",
        "author": "Arthur Rimbaud",
        "year": 1870,
        "era": "surrealist",
        "text": """A green hollow where a stream sings wildly,
crazily catching silver rags of light
on the grasses; where the sun shines from the proud
mountain, it's a small valley bubbling over with light.

A young soldier, mouth open, bare head,
the nape of his neck bathing in cool blue water cress,
sleeps; he is stretched out on the grass, under the clouds,
pale in his green bed where the light rains down.

His feet in the gladioli, he sleeps. Smiling the way
a sick child might smile, he is napping:
Nature, cradle him warmly: he is cold.

The fragrances do not make his nostrils quiver;
he sleeps in the sun, hand on his still chest.
He has two red holes in his right side."""
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

    # ─── TECHNICAL-REGISTER POEMS ─────────────────────────────────────────────
    # Added to test the "register-crossing" hypothesis from technical_vocabulary_s2.md:
    # does scientific/zoological vocabulary appear at elevated S₂ positions?
    # All texts are public domain (published before 1928 or by authors dead >70 years).

    # Marianne Moore "The Fish" (1921) — dense marine biology imagery:
    # "barnacles", "jelly fish", "submarine toadstools", "chasm-side" — Moore's
    # zoological precision makes this an ideal test case for technical-register S₂.
    {
        "title": "The Fish",
        "author": "Marianne Moore",
        "year": 1921,
        "era": "modernist",
        "text": """wade
through black jade.
   Of the crow-blue mussel-shells, one keeps
   adjusting the ash-heaps;
         opening and shutting itself like

an
injured fan.
   The barnacles which encrust the side
   of the wave, cannot hide
         there for the submerged shafts of the

sun,
split like spun
   glass, move themselves with spotlight swiftness
   into the crevices—
         in and out, illuminating

the
turquoise sea
   of bodies. The water drives a wedge
   of iron through the iron edge
         of the cliff; whereupon the stars,

pink
rice-grains, ink-
   bespattered jelly fish, crabs like green
   lilies, and submarine
         toadstools, slide each on the other.

All
external
   marks of abuse are present on this
   defiant edifice—
         all the physical features of

ac-
cident—lack
   of cornice, dynamite grooves, burns, and
   hatchet strokes, these things stand
         out on it; the chasm-side is

dead.
Repeated
   evidence has proved that it can live
   on what can not revive
         its youth. The sea grows old in it."""
    },

    # Walt Whitman "When I Heard the Learn'd Astronomer" (1865) — one of the
    # few poems that explicitly stages the encounter between scientific lecture
    # (proofs, figures, columns, charts, diagrams) and lyric experience. The
    # first half is dense with technical vocabulary; the second half abandons it.
    # Ideal split test: does S₂ spike in the lecture-hall half or the field half?
    {
        "title": "When I Heard the Learn'd Astronomer",
        "author": "Walt Whitman",
        "year": 1865,
        "era": "romantic",
        "text": """When I heard the learn'd astronomer,
When the proofs, the figures, were ranged in columns before me,
When I was shown the charts and diagrams, to add, divide, and measure them,
When I sitting heard the astronomer where he lectured with much applause in the lecture-room,
How soon unaccountable I became tired and sick,
Till rising and gliding out I wander'd off by myself,
In the mystical moist night-air, and from time to time,
Look'd up in perfect silence at the stars."""
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
What dread hand? & what dread feet?

What the hammer? what the chain,
In what furnace was thy brain?
What the anvil? what dread grasp,
Dare its deadly terrors clasp!

When the stars threw down their spears
And water'd heaven with their tears:
Did he smile his work to see?
Did he who made the Lamb make thee?

Tyger Tyger burning bright,
In the forests of the night:
What immortal hand or eye,
Dare frame thy fearful symmetry?"""
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
Nameless here for evermore.

And the silken, sad, uncertain rustling of each purple curtain
Thrilled me—filled me with fantastic terrors never felt before;
So that now, to still the beating of my heart, I stood repeating
"'Tis some visitor entreating entrance at my chamber door—
Some late visitor entreating entrance at my chamber door;—
This it is and nothing more."

Presently my soul grew stronger; hesitating then no longer,
"Sir," said I, "or Madam, truly your forgiveness I implore;
But the fact is I was napping, and so gently you came rapping,
And so faintly you came tapping, tapping at my chamber door,
That I scarce was sure I heard you"—here I opened wide the door;—
Darkness there and nothing more.

Deep into that darkness peering, long I stood there wondering, fearing,
Doubting, dreaming dreams no mortal ever dared to dream before;
But the silence was unbroken, and the stillness gave no token,
And the only word there spoken was the whispered word, "Lenore?"
This I whispered, and an echo murmured back the word, "Lenore!"—
Merely this and nothing more.

Back into the chamber turning, all my soul within me burning,
Soon again I heard a tapping somewhat louder than before.
"Surely," said I, "surely that is something at my window lattice;
Let me see, then, what thereat is, and this mystery explore—
Let my heart be still a moment and this mystery explore;—
'Tis the wind and nothing more!"

Open here I flung the shutter, when, with many a flirt and flutter,
In there stepped a stately Raven of the saintly days of yore;
Not the least obeisance made he; not a minute stopped or stayed he;
But, with mien of lord or lady, perched above my chamber door—
Perched upon a bust of Pallas just above my chamber door—
Perched, and sat, and nothing more.

Then this ebony bird beguiling my sad fancy into smiling,
By the grave and stern decorum of the countenance it wore,
"Though thy crest be shorn and shaven, thou," I said, "art sure no craven,
Ghastly grim and ancient Raven wandering from the Nightly shore—
Tell me what thy lordly name is on the Night's Plutonian shore!"
Quoth the Raven "Nevermore.\""""
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
    {
        "title": "Morning Glory (Chiyo-ni, translated)",
        "author": "Chiyo-ni",
        "year": 1763,
        "era": "haiku",
        "text": """Morning glory—
the well-bucket entangled,
I ask for water."""
    },
    {
        "title": "Temple Bells (Buson, translated)",
        "author": "Yosa Buson",
        "year": 1771,
        "era": "haiku",
        "text": """Temple bells die out.
The fragrant blossoms remain.
A perfect evening!"""
    },
    {
        "title": "No Sky (Shiki, translated)",
        "author": "Masaoka Shiki",
        "year": 1896,
        "era": "haiku",
        "text": """No sky at all;
no earth at all— and still
the snowflakes fall."""
    },
    {
        "title": "On the Roof of Hell (Issa, translated)",
        "author": "Kobayashi Issa",
        "year": 1823,
        "era": "haiku",
        "text": """In this world
we walk on the roof of hell,
gazing at flowers."""
    },
    {
        "title": "Cicadas (Bashō, translated)",
        "author": "Matsuo Bashō",
        "year": 1689,
        "era": "haiku",
        "text": """Silence—
the sound of the cicadas
pierces the rocks."""
    },
    {
        "title": "Nobody (Wright)",
        "author": "Richard Wright",
        "year": 1960,
        "era": "haiku",
        "text": """I am nobody.
A red sinking autumn sun
took my name away."""
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

    # ── Varied refrains (refrain-betrayal test set, all PD) ─────────────────
    # Each poem returns to an established line and then departs from it
    # partway through, testing whether a broken in-context copy yields S₂.
    {
        "title": "Tears, Idle Tears",
        "author": "Alfred, Lord Tennyson",
        "year": 1847,
        "era": "victorian",
        "text": """Tears, idle tears, I know not what they mean,
Tears from the depth of some divine despair
Rise in the heart, and gather to the eyes,
In looking on the happy autumn-fields,
And thinking of the days that are no more.

Fresh as the first beam glittering on a sail,
That brings our friends up from the underworld,
Sad as the last which reddens over one
That sinks with all we love below the verge;
So sad, so fresh, the days that are no more.

Ah, sad and strange as in dark summer dawns
The earliest pipe of half-awaken'd birds
To dying ears, when unto dying eyes
The casement slowly grows a glimmering square;
So sad, so strange, the days that are no more.

Dear as remember'd kisses after death,
And sweet as those by hopeless fancy feign'd
On lips that are for others; deep as love,
Deep as first love, and wild with all regret;
O Death in Life, the days that are no more!"""
    },
    {
        "title": "Break, Break, Break",
        "author": "Alfred, Lord Tennyson",
        "year": 1842,
        "era": "victorian",
        "text": """Break, break, break,
On thy cold gray stones, O Sea!
And I would that my tongue could utter
The thoughts that arise in me.

O, well for the fisherman's boy,
That he shouts with his sister at play!
O, well for the sailor lad,
That he sings in his boat on the bay!

And the stately ships go on
To their haven under the hill;
But O for the touch of a vanish'd hand,
And the sound of a voice that is still!

Break, break, break,
At the foot of thy crags, O Sea!
But the tender grace of a day that is dead
Will never come back to me."""
    },
    {
        "title": "The Lady of Shalott (Part I)",
        "author": "Alfred, Lord Tennyson",
        "year": 1842,
        "era": "victorian",
        "text": """On either side the river lie
Long fields of barley and of rye,
That clothe the wold and meet the sky;
And thro' the field the road runs by
To many-tower'd Camelot;
And up and down the people go,
Gazing where the lilies blow
Round an island there below,
The island of Shalott.

Willows whiten, aspens quiver,
Little breezes dusk and shiver
Thro' the wave that runs for ever
By the island in the river
Flowing down to Camelot.
Four gray walls, and four gray towers,
Overlook a space of flowers,
And the silent isle imbowers
The Lady of Shalott.

By the margin, willow veil'd,
Slide the heavy barges trail'd
By slow horses; and unhail'd
The shallop flitteth silken-sail'd
Skimming down to Camelot:
But who hath seen her wave her hand?
Or at the casement seen her stand?
Or is she known in all the land,
The Lady of Shalott?

Only reapers, reaping early
In among the bearded barley,
Hear a song that echoes cheerly
From the river winding clearly,
Down to tower'd Camelot:
And by the moon the reaper weary,
Piling sheaves in uplands airy,
Listening, whispers "'Tis the fairy
Lady of Shalott.\""""
    },
    {
        "title": "Recessional (stanzas 1-3)",
        "author": "Rudyard Kipling",
        "year": 1897,
        "era": "victorian",
        "text": """God of our fathers, known of old,
Lord of our far-flung battle-line,
Beneath whose awful Hand we hold
Dominion over palm and pine—
Lord God of Hosts, be with us yet,
Lest we forget—lest we forget!

The tumult and the shouting dies;
The Captains and the Kings depart:
Still stands Thine ancient sacrifice,
An humble and a contrite heart.
Lord God of Hosts, be with us yet,
Lest we forget—lest we forget!

Far-called, our navies melt away;
On dune and headland sinks the fire:
Lo, all our pomp of yesterday
Is one with Nineveh and Tyre!
Judge of the Nations, spare us yet,
Lest we forget—lest we forget!"""
    },

    # ── Cliché controls (synthetic research test cases) ───────────────────────
    # Deliberately formulaic poems composed to test whether S2 tracks originality.
    # Not attributed to any real poet; authored as controlled stimuli for this study.
    {
        "title": "Life Is a Journey (synthetic cliché)",
        "author": "Synthetic (research test case)",
        "year": 2026,
        "era": "cliche_control",
        "text": """Life is a journey, day by day,
We travel along on our way.
Through hills and valleys, come what may,
We face each challenge every day.

The road is long and sometimes steep,
But we must rise and never sleep.
For every loss there is a gain,
And after drought there comes the rain.

So take my hand and hold on tight,
Together we will reach the light.
For in the end we'll find our way,
And brighter skies will come our day."""
    },
    {
        "title": "My Heart Burns for You (synthetic cliché)",
        "author": "Synthetic (research test case)",
        "year": 2026,
        "era": "cliche_control",
        "text": """My heart burns for you, night and day,
I think of you in every way.
Your eyes are like the stars above,
My heart is full of only love.

Without you here I'd surely die,
You are the apple of my eye.
Your smile lights up the darkest night,
Your love makes everything alright.

I love you more than words can say,
My heart grows stronger every day.
You are my world, my love, my life,
I want you with me, love, for life."""
    },
    {
        "title": "Autumn Comes (synthetic cliché)",
        "author": "Synthetic (research test case)",
        "year": 2026,
        "era": "cliche_control",
        "text": """Autumn comes with leaves of red and gold,
The air grows crisp and the nights grow cold.
The trees stand bare, the flowers fade away,
The days grow short as summer goes astray.

The birds fly south to warmer, kinder skies,
And winter whispers cold and fond goodbyes.
The world grows still and hushed and soft and grey,
As all the warmth and summer fades away.

But in the spring the world will bloom again,
New life will rise and wash away the pain.
The flowers will bloom and birds will start to sing,
And love and joy return upon the wing."""
    },

    # ── Ecstatic / wildly original verse (18th century) ──────────────────────
    {
        "title": "For I Will Consider My Cat Jeoffry (excerpt)",
        "author": "Christopher Smart",
        "year": 1763,
        "era": "18th_century",
        "text": """For I will consider my Cat Jeoffry.
For he is the servant of the Living God, duly and daily serving him.
For at the first glance of the glory of God in the East he worships in his way.
For is this done by wreathing his body seven times round with elegant quickness.
For then he leaps up to catch the musk, which is the blessing of God upon his prayer.
For he rolls upon prank to work it in.
For having done duty and received blessing he begins to consider himself.
For this he performs in ten degrees.
For first he looks upon his fore-paws to see if they are clean.
For secondly he kicks up behind to clear away there.
For thirdly he works it upon stretch with the fore-paws extended.
For fourthly he sharpens his paws by wood.
For fifthly he washes himself.
For sixthly he rolls upon wash.
For seventhly he fleas himself, that he may not be interrupted upon the beat.
For eighthly he rubs himself against a post.
For ninthly he looks up for his instructions.
For tenthly he goes in quest of food.
For having considered God and himself he will consider his neighbour.
For if he meets another cat he will kiss her in kindness.
For when he takes his prey he plays with it to give it a chance.
For one mouse in seven escapes by his dallying."""
    },
    {
        "title": "Kubla Khan (opening stanzas)",
        "author": "Samuel Taylor Coleridge",
        "year": 1816,
        "era": "romantic",
        "text": """In Xanadu did Kubla Khan
A stately pleasure-dome decree:
Where Alph, the sacred river, ran
Through caverns measureless to man
Down to a sunless sea.
So twice five miles of fertile ground
With walls and towers were girdled round;
And there were gardens bright with sinuous rills,
Where blossomed many an incense-bearing tree;
And here were forests ancient as the hills,
Enfolding sunny spots of greenery.

But oh! that deep romantic chasm which slanted
Down the green hill athwart a cedarn cover!
A savage place! as holy and enchanted
As e'er beneath a waning moon was haunted
By woman wailing for her demon-lover!
And from this chasm, with ceaseless turmoil seething,
As if this earth in fast thick pants were breathing,
A mighty fountain momently was forced:
Amid whose swift half-intermitted burst
Huge fragments vaulted like rebounding hail,
Or chaffy grain beneath the thresher's flail:
And mid these dancing rocks at once and ever
It flung up momently the sacred river."""
    },
    {
        "title": "Proverbs of Hell (excerpt from Marriage of Heaven and Hell)",
        "author": "William Blake",
        "year": 1793,
        "era": "romantic",
        "text": """In seed time learn, in harvest teach, in winter enjoy.
Drive your cart and your plow over the bones of the dead.
The road of excess leads to the palace of wisdom.
Prudence is a rich ugly old maid courted by Incapacity.
He who desires but acts not, breeds pestilence.
The cut worm forgives the plow.
Dip him in the river who loves water.
A fool sees not the same tree that a wise man sees.
He whose face gives no light, shall never become a star.
Eternity is in love with the productions of time.
The busy bee has no time for sorrow.
The hours of folly are measured by the clock; but of wisdom, no clock can measure.
All wholesome food is caught without a net or a trap.
Bring out number, weight and measure in a year of dearth.
No bird soars too high, if he soars with his own wings.
A dead body revenges not injuries.
The most sublime act is to set another before you.
If the fool would persist in his folly he would become wise.
Folly is the cloak of knavery.
Shame is Pride's cloak."""
    },

    # ── New poems testing counter-lexicon hypothesis (added 2026-09-29) ────────
    # These poems were added to test whether poems using conventional "poetic"
    # vocabulary (the suppressed counter-lexicon: world, great, light, air, earth)
    # have lower S2 than poems with specific/unexpected vocabulary.

    # --- Sentimental popular Victorian verse: rich in expected "poetic" diction ---
    {
        "title": "Casabianca",
        "author": "Felicia Hemans",
        "year": 1826,
        "era": "victorian",
        "text": """The boy stood on the burning deck
Whence all but he had fled;
The flame that lit the battle's wreck
Shone round him o'er the dead.

Yet beautiful and bright he stood,
As born to rule the storm;
A creature of heroic blood,
A proud, though child-like form.

The flames rolled on — he would not go
Without his father's word;
That father, faint in death below,
His voice no longer heard.

He called aloud — 'Say, father, say
If yet my task is done?'
He knew not that the chieftain lay
Unconscious of his son.

'Speak, father!' once again he cried,
'If I may yet be gone!'
— And but the booming shots replied,
And fast the flames rolled on.

Upon his brow he felt their breath,
And in his waving hair,
And looked from that lone post of death
In still yet brave despair."""
    },

    {
        "title": "Invictus",
        "author": "William Ernest Henley",
        "year": 1888,
        "era": "victorian",
        "text": """Out of the night that covers me,
Black as the pit from pole to pole,
I thank whatever gods may be
For my unconquerable soul.

In the fell clutch of circumstance
I have not winced nor cried aloud.
Under the bludgeonings of chance
My head is bloody, but unbowed.

Beyond this place of wrath and tears
Looms but the Horror of the shade,
And yet the menace of the years
Finds, and shall find me, unafraid.

It matters not how strait the gate,
How charged with punishments the scroll,
I am the master of my fate:
I am the captain of my soul."""
    },

    # --- Hopkins' Pied Beauty: dense compound adjectives, unexpected vocabulary ---
    {
        "title": "Pied Beauty",
        "author": "Gerard Manley Hopkins",
        "year": 1877,
        "era": "victorian",
        "text": """Glory be to God for dappled things —
  For skies of couple-colour as a brinded cow;
    For rose-moles all in stipple upon trout that swim;
Fresh-firecoal chestnut-falls; finches' wings;
  Landscape plotted and pieced — fold, fallow, and plough;
    And áll trádes, their gear and tackle and trim.

All things counter, original, spare, strange;
  Whatever is fickle, freckled (who knows how?)
    With swift, slow; sweet, sour; adazzle, dim;
He fathers-forth whose beauty is past change:
                                Praise him."""
    },

    # --- Sandburg's Fog and Grass: imagist precision vs. catalog of the earth ---
    {
        "title": "Fog",
        "author": "Carl Sandburg",
        "year": 1916,
        "era": "modernist",
        "text": """The fog comes
on little cat feet.

It sits looking
over harbor and city
on silent haunches
and then moves on."""
    },

    {
        "title": "Grass",
        "author": "Carl Sandburg",
        "year": 1918,
        "era": "modernist",
        "text": """Pile the bodies high at Austerlitz and Waterloo.
Shovel them under and let me work —
I am the grass; I cover all.

And pile them high at Gettysburg
And pile them high at Ypres and Verdun.
Shovel them under and let me work.
Two years, ten years, and passengers ask the conductor:
What place is this?
Where are we now?

I am the grass.
Let me work."""
    },

    # --- Hart Crane's dense, difficult modernist diction ---
    {
        "title": "The Harbor Dawn (from The Bridge)",
        "author": "Hart Crane",
        "year": 1930,
        "era": "modernist",
        "text": """Insistently through sleep — a tide of voices —
They meet you listening midway in your dream,
The long, tired sounds, fog-insulated noises:
Gongs in white surplices, beshrouded wails,
Far strum of fog horns . . . signals dispersed in veils.

And then a truck will lumber past the wharves
As winch engines begin throbbing on some deck;
Or a drunken stevedore's howl and thud below
Comes echoing aloft. And overheard
Above the cloudy strands that wild clangs pass —
The cables of our sleep so swiftly fled,
Already hang, shred ends from remembered stars.

One inconnu girl by the windy pier,
Who asks no virgin-white surrender now —
Not even to ask the day's refrain: Where are you?"""
    },

    # ─── BIBLICAL / LITURGICAL ─────────────────────────────────────────────────
    # Hebrew parallelism: each verse is matched by a parallel second verse
    # restating (synonymic), contrasting (antithetic), or extending (synthetic)
    # the first. Tests how GPT-2 handles structured repetition of meaning in
    # different words.
    {
        "title": "Psalm 23 (KJV)",
        "author": "Anonymous (Hebrew Bible)",
        "year": -1000,
        "era": "biblical",
        "text": """The LORD is my shepherd; I shall not want.
He maketh me to lie down in green pastures: he leadeth me beside the still waters.
He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake.
Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me.
Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over.
Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the LORD for ever."""
    },
    {
        "title": "Psalm 19:1-6 (KJV)",
        "author": "Anonymous (Hebrew Bible)",
        "year": -1000,
        "era": "biblical",
        "text": """The heavens declare the glory of God; and the firmament sheweth his handywork.
Day unto day uttereth speech, and night unto night sheweth knowledge.
There is no speech nor language, where their voice is not heard.
Their line is gone out through all the earth, and their words to the end of the world.
In them hath he set a tabernacle for the sun, which is as a bridegroom coming out of his chamber,
and rejoiceth as a strong man to run a race.
His going forth is from the end of the heaven, and his circuit unto the ends of it: and there is nothing hid from the heat thereof."""
    },
    {
        "title": "Psalm 121 (KJV)",
        "author": "Anonymous (Hebrew Bible)",
        "year": -1000,
        "era": "biblical",
        "text": """I will lift up mine eyes unto the hills, from whence cometh my help.
My help cometh from the LORD, which made heaven and earth.
He will not suffer thy foot to be moved: he that keepeth thee will not slumber.
Behold, he that keepeth Israel shall neither slumber nor sleep.
The LORD is thy keeper: the LORD is thy shade upon thy right hand.
The sun shall not smite thee by day, nor the moon by night.
The LORD shall preserve thee from all evil: he shall preserve thy soul.
The LORD shall preserve thy going out and thy coming in from this time forth, and even for evermore."""
    },
    {
        "title": "Song of Solomon 2:1-7 (KJV)",
        "author": "Anonymous (Hebrew Bible)",
        "year": -950,
        "era": "biblical",
        "text": """I am the rose of Sharon, and the lily of the valleys.
As the lily among thorns, so is my love among the daughters.
As the apple tree among the trees of the wood, so is my beloved among the sons.
I sat down under his shadow with great delight, and his fruit was sweet to my taste.
He brought me to the banqueting house, and his banner over me was love.
Stay me with flagons, comfort me with apples: for I am sick of love.
His left hand is under my head, and his right hand doth embrace me."""
    },
    {
        "title": "Isaiah 40:28-31 (KJV)",
        "author": "Anonymous (Hebrew Bible)",
        "year": -700,
        "era": "biblical",
        "text": """Hast thou not known? hast thou not heard, that the everlasting God, the LORD, the Creator of the ends of the earth, fainteth not, neither is weary?
There is no searching of his understanding.
He giveth power to the faint; and to them that have no might he increaseth strength.
Even the youths shall faint and be weary, and the young men shall utterly fall:
But they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles;
they shall run, and not be weary; and they shall walk, and not faint."""
    },
    {
        "title": "Psalm 46:1-5 (KJV)",
        "author": "Anonymous (Hebrew Bible)",
        "year": -1000,
        "era": "biblical",
        "text": """God is our refuge and strength, a very present help in trouble.
Therefore will not we fear, though the earth be removed, and though the mountains be carried into the midst of the sea;
Though the waters thereof roar and be troubled, though the mountains shake with the swelling thereof.
There is a river, the streams whereof shall make glad the city of God, the holy place of the tabernacles of the most High.
God is in the midst of her; she shall not be moved: God shall help her, and that right early."""
    },
    {
        "title": "Psalm 137:1-4 (KJV)",
        "author": "Anonymous (Hebrew Bible)",
        "year": -587,
        "era": "biblical",
        "text": """By the rivers of Babylon, there we sat down, yea, we wept, when we remembered Zion.
We hanged our harps upon the willows in the midst thereof.
For there they that carried us away captive required of us a song; and they that wasted us required of us mirth, saying, Sing us one of the songs of Zion.
How shall we sing the LORD's song in a strange land?"""
    },

    # ─── CONCRETE POETRY ──────────────────────────────────────────────────────
    # Poems where visual/spatial arrangement is integral — tests how GPT-2
    # handles text when the lineation encodes meaning beyond grammar/syntax.
    {
        "title": "silencio",
        "author": "Eugen Gomringer",
        "year": 1954,
        "era": "concrete",
        "text": """silencio silencio silencio
silencio silencio silencio
silencio silencio silencio
silencio silencio silencio
silencio silencio silencio"""
    },
    {
        "title": "l(a",
        "author": "E.E. Cummings",
        "year": 1958,
        "era": "concrete",
        "text": """l(a

le
af
fa

ll

s)
one
l

iness"""
    },
    {
        "title": "For Spacious Skies",
        "author": "Emmett Williams",
        "year": 1965,
        "era": "concrete",
        "text": """spacious skies
for spacious skies
o spacious skies
for spacious skies
for spacious skies for
for spacious for
for spacious
for
for
for spacious
for spacious skies
for spacious skies for
spacious skies for spacious
skies for spacious skies
for spacious skies"""
    },

    # ─── LATIN AMERICAN MODERNISM ──────────────────────────────────────────────
    # Under-represented tradition: Spanish-language surrealism and modernism in
    # translation. Tests whether translation strips the S₂ signature or preserves it.
    {
        "title": "Tonight I Can Write (excerpt)",
        "author": "Pablo Neruda (trans. W.S. Merwin)",
        "year": 1924,
        "era": "latin_american",
        "text": """Tonight I can write the saddest lines.
Write, for example, 'The night is starry,
and the stars, blue, shiver in the distance.'

The night wind revolves in the sky and sings.
Tonight I can write the saddest lines.
I loved her, and sometimes she loved me too.

Through nights like this one I held her in my arms.
I kissed her again and again under the endless sky.
She loved me, sometimes I loved her too.
How could one not have loved her great still eyes."""
    },
    {
        "title": "Somnambulistic Ballad (excerpt)",
        "author": "Federico García Lorca (trans. Stephen Spender & J.L. Gili)",
        "year": 1928,
        "era": "latin_american",
        "text": """Green, how I want you green.
Green wind. Green branches.
The ship out on the sea
and the horse on the mountain.
With the shade around her waist
she dreams on her balcony,
green flesh, her hair green,
with eyes of cold silver.
Green, how I want you green.
Under the gypsy moon,
all things are watching her
and she cannot see them."""
    },
    {
        "title": "Black Stone Lying on a White Stone",
        "author": "César Vallejo (trans. Thomas Merton)",
        "year": 1937,
        "era": "latin_american",
        "text": """I will die in Paris, on a rainy day,
on some day I can already remember.
I will die in Paris — and I don't step aside —
perhaps on a Thursday, as today is Thursday, in autumn.

It will be a Thursday, because today, Thursday, setting down
these lines, I have put my upper arm bones on
wrong, and never so much as today have I found myself
with all the road ahead of me, alone.

César Vallejo is dead. Everyone beat him
although he never does anything to them;
they beat him hard with a stick and hard also
with a rope. These are the witnesses:
the Thursdays, and the bones of my arms,
the solitude, and the rain, and the roads."""
    },

    # ─── BLACK ARTS MOVEMENT ──────────────────────────────────────────────────
    # Radical American poetry: speech rhythms, vernacular, political urgency.
    # Tests whether confrontational syntactic choices show higher S₂ than lyric poetry.
    {
        "title": "Preface to a Twenty Volume Suicide Note",
        "author": "Amiri Baraka (LeRoi Jones)",
        "year": 1961,
        "era": "black_arts",
        "text": """Lately, I've become accustomed to the way
The ground opens up and envelopes me
Each time I go out to walk the dog.
Or the broad edged silly music the wind
Makes when I run for a bus...

Things have come to that.

And now, each night I count the stars.
And each night I get the same number.
And when they will not come to be counted,
I count the holes they leave.

Nobody sings anymore.

And then last night I tiptoed up
To my daughter's room and heard her
Talking to someone, and when I opened
The door, there was no one there...
Only she on her knees, peeking into
Her own clasped hands"""
    },

    # ─── KOREAN ZEN POETRY ────────────────────────────────────────────────────
    # Ko Un's ten-thousand-lines project: extremely brief, imagistic flash poems.
    # Tests the S₂ behavior of minimal context — can haiku-like compression in
    # a different tradition produce similar information signatures?
    {
        "title": "From Ten Thousand Lives: Three Portraits",
        "author": "Ko Un (trans. Brother Anthony of Taizé)",
        "year": 1986,
        "era": "korean_modernist",
        "text": """The old man Gim Namsik
lived alone in his room
and died alone in his room.
Nobody knew he'd died
till the smell drifted out.

Broken Bak Geumnyeo
always said: I'm going to die soon.
Even her own children
got tired of hearing it
and stopped visiting.
She's still alive.

The widower Im Gyesu
every evening goes down to the river.
He just stands there.
What's in that water?
Just water."""
    },

    # ─── IMAGIST LYRIC (deep compression) ───────────────────────────────────
    # Amy Lowell brings hard-edged American imagism distinct from H.D.'s classicism.
    {
        "title": "The Taxi",
        "author": "Amy Lowell",
        "year": 1914,
        "era": "imagist",
        "text": """When I go away from you
The world beats dead
Like a slackened drum.
I call out for you against the jutted stars
And shout into the ridges of the wind.
Streets coming fast,
One after the other,
Wedge you away from me,
And the lamps of the city prick my eyes
So that I can no longer see your face.
Why should I leave you,
To wound myself upon the sharp edges of the night?"""
    },
    {
        "title": "Patterns",
        "author": "Amy Lowell",
        "year": 1916,
        "era": "imagist",
        "text": """I walk down the garden paths,
And all the daffodils
Are blowing, and the bright blue squills.
I walk down the patterned garden-paths
In my stiff, brocaded gown.
With my powdered hair and jeweled fan,
I too am a rare
Pattern. As I wander down
The garden paths.

My dress is richly figured,
And the train
Makes a pink and silver stain
On the gravel, and the thrift
Of the borders.
Just a plate of current fashion,
Tripping by in high-heeled, ribboned shoes.
Not a softness anywhere about me,
Only whalebone and brocade."""
    },

    # ─── ORAL REGISTER EXPANSION ──────────────────────────────────────────────
    # Added 2026-10-07 to test oral-literary register hypothesis.
    # All texts public domain (pre-1924 or translations of ancient originals).

    {
        "title": "Iliad (opening, trans. Pope)",
        "author": "Homer (trans. Alexander Pope)",
        "year": 1715,
        "era": "ancient",
        "text": """Achilles' wrath, to Greece the direful spring
Of woes unnumbered, heavenly goddess, sing!
That wrath which hurled to Pluto's gloomy reign
The souls of mighty chiefs untimely slain;
Whose limbs unburied on the naked shore,
Devouring dogs and hungry vultures tore:
Since great Achilles and Atrides strove,
Such was the sovereign doom, and such the will of Jove."""
    },
    {
        "title": "Beowulf (opening, trans. Gummere)",
        "author": "Anonymous (trans. Francis B. Gummere)",
        "year": 1909,
        "era": "ancient",
        "text": """Lo, praise of the prowess of people-kings
of spear-armed Danes, in days long sped,
we have heard, and what honor the athelings won!
Oft Scyld the Scefing from squadroned foes,
from many a tribe, the mead-bench tore,
awing the earls. Since erst he lay
friendless, a foundling, fate repaid him:
for he waxed under welkin, in wealth he throve,
till before him the folk, both far and near,
who house by the whale-path, heard his mandate,
gave him gifts: a good king he."""
    },
    {
        "title": "On Being Brought from Africa to America",
        "author": "Phillis Wheatley",
        "year": 1773,
        "era": "18th_century",
        "text": """'Twas mercy brought me from my Pagan land,
Taught my benighted soul to understand
That there's a God, that there's a Saviour too:
Once I redemption neither sought nor knew.
Some view our sable race with scornful eye,
"Their colour is a diabolic dye."
Remember, Christians, Negroes, black as Cain,
May be refin'd, and join th' angelic train."""
    },
    {
        "title": "O Captain! My Captain!",
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
Fallen cold and dead.

O Captain! my Captain! rise up and hear the bells;
Rise up—for you the flag is flung—for you the bugle trills,
For you bouquets and ribbon'd wreaths—for you the shores a-crowding,
For you they call, the swaying mass, their eager faces turning;
Here Captain! dear father!
The arm beneath your head!
It is some dream that on the deck,
You've fallen cold and dead."""
    },
    {
        "title": "Western Wind (anonymous lyric)",
        "author": "Anonymous (English, c. 1500)",
        "year": 1500,
        "era": "early_modern",
        "text": """Western wind, when wilt thou blow,
The small rain down can rain?
Christ, if my love were in my arms
And I in my bed again!"""
    },

    # ─── NEW: BEAT GENERATION (expand sample for high artifact-free S2 finding) ────
    {
        "title": "Bomb",
        "author": "Gregory Corso",
        "year": 1958,
        "era": "beat",
        "text": """Budger of history Brake of time You Bomb
Toy of universe Grandest of all snatched sky I cannot hate you
Do I hate the mischievous thunderbolt the jawbone of an ass
The bumpy club of One Million B.C. the mace the flail the axe
Catapult Da Vinci tomahawk Cochise flintlock Kidd dagger Rathbone
Hiroshima Nagasaki
I am unable to hate what is necessary to love
So if nebulous you must go somewhere go into the hearts of men"""
    },
    {
        "title": "Marriage",
        "author": "Gregory Corso",
        "year": 1960,
        "era": "beat",
        "text": """Should I get married? Should I be good?
Astound the girl next door with my velvet suit and faustus hood?
Don't take her to movies but to cemeteries
tell all about werewolf bathtubs and forked clarinets
then desire her and kiss her and all the preliminaries
and she going just so far and I understanding why
not getting angry saying You must feel! It's beautiful to feel!
Instead take her in my arms lean against an old crooked tombstone
and woo her the entire night the constellations in the sky"""
    },
    {
        "title": "Constantly Risking Absurdity",
        "author": "Lawrence Ferlinghetti",
        "year": 1958,
        "era": "beat",
        "text": """Constantly risking absurdity
                                             and death
            whenever he performs
                                        above the heads
                                                            of his audience
the poet like an acrobat
                                climbs on rime
                         to a high wire of his own making
and balancing on eyebeams
                                        above a sea of faces
             paces his way
                               to the other side of day"""
    },
    {
        "title": "In Goya's greatest scenes",
        "author": "Lawrence Ferlinghetti",
        "year": 1958,
        "era": "beat",
        "text": """In Goya's greatest scenes we seem to see
                                                the people of the world
exactly at the moment when
      they first attained the title of
                                                suffering humanity
They writhe upon the page
                              in a veritable rage
                                                    of adversity
Heaped up
             groaning with babies and bayonets
                                                under cement skies
in an abstract landscape of blasted trees
bent statues bats wings and beaks"""
    },

    # ─── NEW: GERMAN EXPRESSIONIST (expand sample for high artifact-free S2 finding) ─
    {
        "title": "Mann und Frau gehn durch die Krebsbaracke (trans. Ward)",
        "author": "Gottfried Benn",
        "year": 1912,
        "era": "german_expressionist",
        "text": """The man: her tits have gone to mush.
Her womb, the same. Clean up. No fuss.
Come here, see this bed, see it rattle.
This flesh has turned, bone waits for battle.

Right there, that chest is just a spine.
Blood, pus, and fluid all entwine.
We drained this one, we'll drain the rest.
It's fine. The flesh accepts its test.

The doctor says: this thigh is done.
She's young. But note the gangrene run.
One more. The uterus is gone.
Tomorrow she'll be cut. Move on."""
    },
    {
        "title": "Kleine Aster (Little Aster, trans. Ward)",
        "author": "Gottfried Benn",
        "year": 1912,
        "era": "german_expressionist",
        "text": """A drowned beer-truck driver was propped on the slab.
Someone had placed a lavender aster between his teeth.
As I made the incision from the chest up
through the skin with a long knife,
and one by one removed the tongue and the palate,
I must have nudged it, for it slid
into the brain lying adjacent.
I packed it into the chest cavity
amongst the excelsior
as it was sewn up.
Drink your fill in your vase!
Rest easy,
little aster!"""
    },
    {
        "title": "Der Gott der Stadt (The God of the City, trans.)",
        "author": "Georg Heym",
        "year": 1910,
        "era": "german_expressionist",
        "text": """He sits upon a block of buildings wide.
The winds lie black around his brow and blow.
He stares where far the empty desert's stride
Begins, where the great cities' billows flow.

The ruddy belly of the evening gleams
Against his neck. The mortar of his chin
Is hard. In the black mouths of factory steams
His nostrils widen, gulping darkness in.

He stretches out his butcher's hand into
The dark. He shakes it. Far away the rows
Of houses crash. The flood of city's through
The streets. And then the lightning's thunder shows."""
    },
    {
        "title": "Umbra Vitae (trans. Hamburger)",
        "author": "Georg Heym",
        "year": 1912,
        "era": "german_expressionist",
        "text": """The people stand on roads and gaze up, staring.
High in the sky a comet's trail of hair.
The towers' heads are fringed with light, there wearing
Bright signals for the armies that prepare.

The shadows of the dead on distant marches
Cross out the sky on many-colored threads.
And the world's shadows walk on empty arches
Where no one lives; the empty dark world spreads.

The forms of life are lost in fog. And then
Man in the street grows stiff, cries out in fright.
He stares above, sees nothing, turns again —
With rounded backs they shuffle home at night."""
    },

    # ─── NEW: GERTRUDE STEIN (semantic disruption — common words, unusual order) ─────
    {
        "title": "Objects (from Tender Buttons)",
        "author": "Gertrude Stein",
        "year": 1914,
        "era": "modernist",
        "text": """A carafe, that is a blind glass. A kind in glass and a cousin, a spectacle and nothing strange a single hurt color and an arrangement in a system to pointing. All this and not ordinary, not unordered in not resembling. The difference is spreading.

Glazed glitter. The reason I see a chair glittered and what is pain certainly not more than yesterday. The truth is something as well and a part is something a clear and not a different color."""
    },
    {
        "title": "Lifting Belly (excerpt)",
        "author": "Gertrude Stein",
        "year": 1917,
        "era": "modernist",
        "text": """Lifting belly is so kind.
Lifting belly fattily.
Doesn't that astonish you.
You did want me.
Say it again.
Strawberry.
Lifting belly is a pleasure.
Lifting belly is so kind.
Lifting belly all around.
Lifting belly makes it right.
Lifting belly is so kind.
Extraordinary belly.
Lifting belly is a chance.
Lifting belly.
Remarkable.
Lifting belly for me.
Lifting belly again.
Can you recollect any other time.
Lifting belly with me.
You mean you want me to say yes.
Yes.
Lifting belly.
Not around.
Lifting belly is about love.
Lifting belly.
I like that."""
    },
    # ─── PARODY / MOCK ────────────────────────────────────────────────────────────
    # Originals paired with their parodies, to test S₂ divergence at subversion points
    {
        "title": "How Doth the Little Busy Bee",
        "author": "Isaac Watts",
        "year": 1715,
        "era": "parody_original",
        "text": """How doth the little busy bee
Improve each shining hour,
And gather honey all the day
From every opening flower!

How skilfully she builds her cell!
How neat she spreads the wax!
And labours hard to store it well
With the sweet food she makes.

In works of labour or of skill,
I would be busy too;
For Satan finds some mischief still
For idle hands to do.

In books, or work, or healthful play,
Let my first years be past,
That I may give for every day
Some good account at last."""
    },
    {
        "title": "How Doth the Little Crocodile",
        "author": "Lewis Carroll",
        "year": 1865,
        "era": "parody",
        "text": """How doth the little crocodile
Improve his shining tail,
And pour the waters of the Nile
On every golden scale!

How cheerfully he seems to grin,
How neatly spreads his claws,
And welcomes little fishes in,
With gently smiling jaws!"""
    },
    {
        "title": "The Old Man's Comforts and How He Gained Them",
        "author": "Robert Southey",
        "year": 1799,
        "era": "parody_original",
        "text": """You are old, Father William, the young man cried,
The few locks which are left you are grey;
You are hale, Father William, a hearty old man,
Now tell me the reason I pray.

In the days of my youth, Father William replied,
I remembered that youth would fly fast,
And abused not my health and my vigour at first
That I never might need them at last.

You are old, Father William, the young man cried,
And pleasures with youth pass away,
And yet you lament not the days that are gone,
Now tell me the reason I pray.

In the days of my youth, Father William replied,
I remembered that youth could not last;
I thought of the future whatever I did,
That I never might grieve for the past.

You are old, Father William, the young man cried,
And life must be hastening away;
You are cheerful, and love to converse upon death!
Now tell me the reason I pray.

I am cheerful, young man, Father William replied,
Let the cause thy attention engage;
In the days of my youth I remembered my God!
And He hath not forgotten my age."""
    },
    {
        "title": "You Are Old, Father William",
        "author": "Lewis Carroll",
        "year": 1865,
        "era": "parody",
        "text": """You are old, Father William, the young man said,
And your hair has become very white;
And yet you incessantly stand on your head—
Do you think, at your age, it is right?

In my youth, Father William replied to his son,
I feared it might injure the brain;
But, now that I'm perfectly sure I have none,
Why, I do it again and again.

You are old, said the youth, as I mentioned before,
And have grown most uncommonly fat;
Yet you turned a back-somersault in at the door—
Pray, what is the reason for that?

In my youth, said the sage, as he shook his grey locks,
I kept all my limbs very supple
By the use of this ointment—one shilling the box—
Allow me to sell you a couple?

You are old, said the youth, and your jaws are too weak
For anything tougher than suet;
Yet you finished the goose, with the bones and the beak—
Pray, how did you manage to do it?

In my youth, said his father, I took to the law,
And argued each case with my wife;
And the muscular strength, which it gave to my jaw,
Has lasted the rest of my life.

You are old, said the youth, one would hardly suppose
That your eye was as steady as ever;
Yet you balanced an eel on the end of your nose—
What made you so awfully clever?

I have answered three questions, and that is enough,
Said his father; don't give yourself airs!
Do you think I can listen all day to such stuff?
Be off, or I'll kick you downstairs!"""
    },
    {
        "title": "'Tis the Voice of the Sluggard",
        "author": "Isaac Watts",
        "year": 1715,
        "era": "parody_original",
        "text": """'Tis the voice of the sluggard; I heard him complain,
You have waked me too soon, I must slumber again.
As the door on its hinges, so he on his bed,
Turns his sides and his shoulders and his heavy head.

A little more sleep, and a little more slumber;
Thus he wastes half his days, and his hours without number,
And when he gets up, he sits folding his hands,
Or walks about sauntering, or trifling he stands."""
    },
    {
        "title": "'Tis the Voice of the Lobster",
        "author": "Lewis Carroll",
        "year": 1865,
        "era": "parody",
        "text": """'Tis the voice of the Lobster; I heard him declare,
You have baked me too brown, I must sugar my hair.
As a duck with its eyelids, so he with his nose
Trims his belt and his buttons, and turns out his toes.

When the sands are all dry, he is gay as a lark,
And will talk in contemptuous tones of the Shark,
But, when the tide rises and sharks are around,
His voice has a timid and tremulous sound."""
    },
    {
        "title": "The Rape of the Lock (Canto I, opening)",
        "author": "Alexander Pope",
        "year": 1714,
        "era": "parody",
        "text": """What dire offence from amorous causes springs,
What mighty contests rise from trivial things,
I sing — This verse to Caryll, Muse! is due:
This, even Belinda may vouchsafe to view:
Slight is the subject, but not so the praise,
If she inspire, and he approve my lays.

Say what strange motive, Goddess! could compel
A well-bred lord to assault a gentle belle?
O say what stranger cause, yet unexplor'd,
Could make a gentle belle reject a lord?
In tasks so bold, can little men engage,
And in soft bosoms dwells such mighty rage?

Sol through white curtains shot a tim'rous ray,
And oped those eyes that must eclipse the day:
Now lapdogs give themselves the rousing shake,
And sleepless lovers, just at twelve, awake."""
    },
    # ─── NEW: PROSE POETRY (artifact-free test cases — no line breaks) ─────────────
    {
        "title": "The Wild Iris (prose extract)",
        "author": "Louise Gluck",
        "year": 1992,
        "era": "prose_poetry",
        "text": """At the end of my suffering there was a door. Hear me out: that which you call death I remember. Overhead, noises, branches of the pine shifting. Then nothing. The weak sun flickered over the dry surface. It is terrible to survive as consciousness buried in the dark earth. Then it was over: that which you fear, being a soul and unable to speak, ending abruptly, the stiff earth bending a little. And what I took to be birds darting in low shrubs. You who do not remember passage from the other world I tell you I could speak again: whatever returns from oblivion returns to find a voice."""
    },
    {
        "title": "Pillow",
        "author": "Russell Edson",
        "year": 1973,
        "era": "prose_poetry",
        "text": """A man had a pillow that he loved very much. He loved it more than he loved his wife. He loved it more than his children. He loved it most especially more than he loved himself. His pillow was everything to him. He could not sleep without it. He slept with his face pressed against it so deeply that in the morning his face was wrinkled and marked with the weave of its fabric. He went everywhere with his pillow. His boss asked him why he was carrying a pillow. He said, because I love it. His boss said, you're fired. He didn't care. He had his pillow."""
    },
    {
        "title": "The Colonel",
        "author": "Carolyn Forche",
        "year": 1981,
        "era": "prose_poetry",
        "text": """What you have heard is true. I was in his house. His wife carried a tray of coffee and sugar. His daughter filed her nails, his son went out for the night. There were daily papers, pet dogs, a pistol on the cushion beside him. The moon swung bare on its black cord over the house. On the television was a cop show. It was in Spanish. There was a brief commercial in English for Drive deodorant and Dove soap. We had dinner, rack of lamb, good wine, a gold bell was on the table for calling the maid. The maid brought green mangoes, salt, a type of bread. I was asked how I enjoyed the country. There was a brief commercial in English for Drive deodorant. Broken bottles were embedded in the walls around the house to scoop the kneecaps from a man's legs or cut his hands to lace. On the windows there were gratings like those in liquor stores. We had finished the wine, might have had a second. There were briefly a commercial in English for Drive deodorant."""
    },

    # ─── OULIPO / CONSTRAINT POETRY (added 2026-10-10) ────────────────────────
    {
        "title": "If I Told Him: A Completed Portrait of Picasso (excerpt)",
        "author": "Gertrude Stein",
        "year": 1923,
        "era": "oulipo",
        "text": """If I told him would he like it. Would he like it if I told him.
Would he like it would Napoleon would Napoleon would would he like it.
If Napoleon if I told him if I told him if Napoleon. Would he like it if I told him if I told him if Napoleon.
Would he like it if Napoleon if Napoleon if I told him. Now.
Not now.
And now.
Now.
Exactly as as kings.
Feeling full for it.
Exactitude as kings.
So to beseech you as full as for it.
Exactly or as kings.
Shutters shut and open so do queens. Shutters shut and shutters and so shutters shut and shutters and so and so shutters and so shutters shut and so shutters shut and shutters and so. And so shutters shut and so and also. And also and so and so and also.
Let me recite what history teaches. History teaches."""
    },
    {
        "title": "The Lipogram: A Sentence Without the Letter E",
        "author": "Georges Perec",
        "year": 1969,
        "era": "oulipo",
        "text": """A plain black cloth, thin and smooth, laid out to display a cold body.
That cold body lying on that black cloth, its mouth shut, its pupils vacant, its arms crossing its torso, its hands palm down.
Black curtains, black hangings, black walls.
Not a shadow of colour anywhere, nothing but black.
A woman in black sat by that body, crying.
A child stood by that woman in black, also in black.
Both sat motionless, in pain, thinking of what was now past and could not again occur."""
    },
    {
        "title": "Eunoia: Chapter A (excerpt)",
        "author": "Christian Bök",
        "year": 2001,
        "era": "oulipo",
        "text": """Awkward grammar appalls a craftsman. A Dada bard as daft as Tzara hampers stagnant art and scatters stale abstract maxims.
Bawdy narratives arrant trash, rank as Satan, as rank as Satan, as rank as Satan.
Awa, a ballad, a faraway strand, a land awash and glad, a vast sand dab and a vast sand dab and a vast sand dab.
Canada: a land apart, barren, flatlands that tantalize a man and madden all that wander vast tracts and vast plains and vast grasslands."""
    },
    {
        "title": "Dysraphism (excerpt)",
        "author": "Charles Bernstein",
        "year": 1981,
        "era": "language",
        "text": """The nurse seemed to enjoy a large part of
the time discussing the large amounts of
time the nurses spent discussing among
themselves the business of nursing.
I want to go to the store to buy something.
The music of the street is only music when the window is raised.
Peanuts are not nuts.
My horse ran a horse race.
The horse's neck is the nicest part of the horse.
Let me put it this way. Say it with flowers.
The poem is the surface of an elsewhere.
I want to write a poem that reads like a letter."""
    },
    {
        "title": "The Sheds of Our Webs",
        "author": "Charles Bernstein",
        "year": 1980,
        "era": "language",
        "text": """A person is a series of acts. The things are in the things. Water is water.
Time is a shape that fits the space between
two acts. The act of going is the act of going.
I am writing this for you.
That is, I am sending these words to you.
That is what writing is: sending.
We send these words through the air of what we can know together.
We were different once and will be again.
The space between us is the only space we have.
Fill it or leave it."""
    },
    {
        "title": "Lorine's Work",
        "author": "Lorine Niedecker",
        "year": 1968,
        "era": "imagist",
        "text": """Grandfather
advised me:
Learn a trade

I learned
to sit at desk
and condense

No layoff
from this
condensery"""
    },

    # ─── CLASSICAL CHINESE (Tang Dynasty, scholarly literal translations) ────
    # Added to test cross-cultural S2: does paratactic, imagistic Chinese verse
    # produce a distinctive information-theoretic signature when translated into
    # English? Predicted: high S2 due to ellipsis, terse noun-image stacking,
    # and absent connectives.
    {
        "title": "Spring View (literal trans.)",
        "author": "Du Fu",
        "year": 757,
        "era": "classical_chinese",
        "text": """The state is broken; mountains and rivers remain.
Spring comes to the walled city; grass and trees grow deep.
Moved by the season, flowers shed tears.
Grieved by parting, birds startle the heart.
Beacon fires have burned for three months.
A letter from home is worth ten thousand gold.
My white hair, scratched ever shorter,
can barely hold a hairpin."""
    },
    {
        "title": "Quiet Night Thoughts (literal trans.)",
        "author": "Li Bai",
        "year": 726,
        "era": "classical_chinese",
        "text": """Before my bed, bright moonlight—
I think it frost on the ground.
I raise my head and gaze at the bright moon,
I lower my head and think of home."""
    },
    {
        "title": "Deer Park (literal trans.)",
        "author": "Wang Wei",
        "year": 740,
        "era": "classical_chinese",
        "text": """Empty mountain: no one is seen.
Only the sound of someone's voice.
Returning light enters the deep forest
and shines again upon the green moss."""
    },
    {
        "title": "On the Tower of Yellow Crane (literal trans.)",
        "author": "Cui Hao",
        "year": 730,
        "era": "classical_chinese",
        "text": """The man of old rode off on a yellow crane
and left this tower empty, Yellow Crane Tower.
The yellow crane, once gone, will not return.
White clouds drift idly, a thousand years.
Clear Hanyang trees in the sunlit river,
sweet grass on Parrot Island, lush and green.
At dusk, where is my native village?
Mist on the river makes me ache."""
    },

    # ─── PERSIAN (classical and Sufi, public-domain translations) ─────────────
    # Persian poetry (Rumi, Omar Khayyam) tests whether Sufi paradox and the
    # ghazal structure produce distinctive S2. FitzGerald's Rubaiyat (1859)
    # is fully public domain.
    {
        "title": "Rubaiyat of Omar Khayyam (stanzas 7–10)",
        "author": "Omar Khayyam (trans. FitzGerald, 1859)",
        "year": 1120,
        "era": "persian",
        "text": """Come, fill the Cup, and in the fire of Spring
Your Winter-garment of Repentance fling:
    The Bird of Time has but a little way
To flutter—and the Bird is on the Wing.

Whether at Naishápur or Babylon,
Whether the Cup with sweet or bitter run,
    The Wine of Life keeps oozing drop by drop,
The Leaves of Life keep falling one by one.

Each Morn a thousand Roses brings, you say;
Yes, but where leaves the Rose of Yesterday?
    And this first Summer month that brings the Rose
Shall take Jamshýd and Kaikobád away.

Well, let it take them! What have we to do
With Kaikobád the Great, or Kaikobás?
    Let Zál and Rustum bluster as they will,
Or Hátim call to Supper—heed not you."""
    },
    {
        "title": "Rubaiyat of Omar Khayyam (stanzas 11–14)",
        "author": "Omar Khayyam (trans. FitzGerald, 1859)",
        "year": 1120,
        "era": "persian",
        "text": """With me along the strip of Herbage strown
That just divides the desert from the sown,
    Where name of Slave and Sultán is forgot—
And Peace to Máhmud on his golden Throne!

A Book of Verses underneath the Bough,
A Jug of Wine, a Loaf of Bread—and Thou
    Beside me singing in the Wilderness—
Oh, Wilderness were Paradise enow!

Some for the Glories of This World; and some
Sigh for the Prophet's Paradise to come;
    Ah, take the Cash, and let the Credit go,
Nor heed the rumble of a distant Drum!

Look to the blowing Rose about us—'Lo,
Laughing,' she says, 'into the world I blow,
    At once the silken tassel of my Purse
Tear, and its Treasure on the Garden throw.'"""
    },

    # ─── JAPANESE TANKA (classical waka, complementing our haiku corpus) ──────
    # Tanka (5-7-5-7-7 syllable form) is older than haiku and more narrative.
    # Adding to test whether the extra 14 syllables of the coda change S2 arc.
    {
        "title": "Tanka on longing (Ki no Tsurayuki, literal trans.)",
        "author": "Ki no Tsurayuki",
        "year": 905,
        "era": "japanese_classical",
        "text": """When I look at the moon
I think of many things—
not just this autumn—
these thousand years of autumn
that have come and gone like this."""
    },
    {
        "title": "Tanka on cherry blossoms (Ariwara no Narihira, literal trans.)",
        "author": "Ariwara no Narihira",
        "year": 880,
        "era": "japanese_classical",
        "text": """If there were no cherry blossoms
in this world,
how much more serene
the hearts of people
in spring would be."""
    },

    # ─── LIMERICK (AABBA constraint — testing extreme formal constraint) ────
    # Hypothesis: AABBA rhyme + anapestic meter should produce very low mean S2
    # at rhyme positions (tightly constrained) but possibly spikes at semantic pivots.
    {
        "title": "There Was an Old Man of Nantucket",
        "author": "Anonymous (limerick tradition)",
        "year": 1902,
        "era": "limerick",
        "text": """There was an old man with a beard,
Who said, 'It is just as I feared!
Two Owls and a Hen,
Four Larks and a Wren,
Have all built their nests in my beard!'"""
    },
    {
        "title": "A Limerick on Time",
        "author": "Anonymous (limerick tradition)",
        "year": 1900,
        "era": "limerick",
        "text": """There was a young lady named Bright,
Whose speed was far faster than light;
She set out one day,
In a relative way,
And returned on the previous night."""
    },
    {
        "title": "There Once Was a Man from Peru",
        "author": "Anonymous (limerick tradition)",
        "year": 1910,
        "era": "limerick",
        "text": """There once was a man from Peru
Who dreamed he was eating his shoe.
He woke with a fright
In the middle of the night
And found that his dream had come true."""
    },

    # ─── OLD ENGLISH / EARLY MEDIEVAL ─────────────────────────────────────
    # Alliterative verse — completely different formal constraint from rhyme.
    # Testing: how does GPT-2 handle the most foreign register in the corpus?
    {
        "title": "Caedmon's Hymn (modern prose translation)",
        "author": "Caedmon (trans. anon.)",
        "year": 658,
        "era": "old_english",
        "text": """Now we must praise the Ruler of Heaven,
the might of the Lord and his purpose of mind,
the work of the Glorious Father, for he,
God Eternal, established each wonder.
He, Holy Creator, first fashioned
the heavens as a roof for the children of men.
Then the Guardian of mankind adorned
this middle-earth below, the master Almighty."""
    },
    {
        "title": "The Wanderer (excerpt, modern translation)",
        "author": "Anonymous (Old English, trans. anon.)",
        "year": 900,
        "era": "old_english",
        "text": """Often the solitary one finds grace for himself,
the mercy of the Lord, although he, full of care,
must stir with his hands for a long while
the frost-cold sea, must tread the exile-paths.
Fate is fully fixed! So spoke the earth-walker,
mindful of hardships, of fierce slaughter,
of the fall of dear kinsmen."""
    },

    # ─── PROTEST / POLITICAL POETRY ───────────────────────────────────────
    # Testing whether political urgency creates different S2 signatures.
    {
        "title": "The New Colossus",
        "author": "Emma Lazarus",
        "year": 1883,
        "era": "protest_political",
        "text": """Not like the brazen giant of Greek fame,
With conquering limbs astride from land to land;
Here at our sea-washed, sunset gates shall stand
A mighty woman with a torch, whose flame
Is the imprisoned lightning, and her name
Mother of Exiles. From her beacon-hand
Glows world-wide welcome; her mild eyes command
The air-bridged harbor that twin cities frame.

"Keep, ancient lands, your storied pomp!" cries she
With silent lips. "Give me your tired, your poor,
Your huddled masses yearning to breathe free,
The wretched refuse of your teeming shore.
Send these, the homeless, tempest-tost to me,
I lift my lamp beside the golden door!" """
    },
    {
        "title": "Still I Rise",
        "author": "Maya Angelou",
        "year": 1978,
        "era": "protest_political",
        "text": """You may write me down in history
With your bitter, twisted lies,
You may trod me in the very dirt
But still, like dust, I'll rise.

Does my sassiness upset you?
Why are you beset with gloom?
'Cause I walk like I've got oil wells
Pumping in my living room.

Just like moons and like suns,
With the certainty of tides,
Just like hopes springing high,
Still I'll rise."""
    },

    # ─── SLAM / SPOKEN WORD (additional) ─────────────────────────────────
    # Testing whether oral performance register produces different S2 from page poetry.
    {
        "title": "Bluebird",
        "author": "Charles Bukowski",
        "year": 1992,
        "era": "spoken_word",
        "text": """there's a bluebird in my heart that
wants to get out
but I'm too tough for him,
I say, stay in there, I'm not going
to let anybody see
you.

there's a bluebird in my heart that
wants to get out
but I pour whiskey on him and inhale
cigarette smoke
and the whores and the bartenders
and the grocery clerks
never know that
he's
in there."""
    },

    # ─── GHAZAL (Urdu/Persian form) ────────────────────────────────────────
    # Testing radabif (refrain) and maqta (signature couplet) conventions.
    {
        "title": "Ghazal of the Better-Unbegun",
        "author": "Heather McHugh",
        "year": 1994,
        "era": "ghazal",
        "text": """Too volatile, am I? Too voluble? Too much on fire?
Better to be ice-of-eye than all on fire.

When Hitler was turned down by art schools, back in Vienna,
the schools were right. He had not enough on fire.

When Mao forged policy from his Little Red Book,
he put forty million Chinese on fire.

I am the last from whom you would expect restraint,
given what I'm by nature on fire.

My God, I'm told, is a jealous god, and therefore
I shouldn't let myself get too much on fire."""
    },

    # ─── ADDITIONAL LIMERICKS ──────────────────────────────────────────────
    # Expanding limerick corpus for statistical analysis of S2 by line position.
    {
        "title": "A Tutor Who Tooted the Flute",
        "author": "Carolyn Wells",
        "year": 1902,
        "era": "limerick",
        "text": """A tutor who tooted the flute
Tried to tutor two tooters to toot.
Said the two to the tutor,
'Is it harder to toot, or
To tutor two tooters to toot?'"""
    },
    {
        "title": "A Flea and a Fly in a Flue",
        "author": "Anonymous",
        "year": 1880,
        "era": "limerick",
        "text": """A flea and a fly in a flue
Were imprisoned, so what could they do?
Said the fly, 'Let us flee!'
'Let us fly!' said the flea.
So they flew through a flaw in the flue."""
    },
    {
        "title": "There Was an Old Person of Ware",
        "author": "Edward Lear",
        "year": 1847,
        "era": "limerick",
        "text": """There was an Old Person of Ware,
Who rode on the back of a bear;
When they asked, 'Does it trot?'
He said, 'Certainly not!
He's a Moppsikon Floppsikon bear!'"""
    },
    {
        "title": "There Was a Young Man of Japan",
        "author": "Anonymous",
        "year": 1880,
        "era": "limerick",
        "text": """There was a young man of Japan
Whose limericks never would scan.
When they asked him why,
He said, 'I do try,
But I always put in too many words at the end of the last line as I can.'"""
    },

    # ─── WAR POETRY (WWI) ─────────────────────────────────────────────────
    # Testing whether war poetry's directness produces different S2 from
    # protest poetry's rhetorical register. Owen died 1918 (public domain).
    {
        "title": "Dulce et Decorum Est",
        "author": "Wilfred Owen",
        "year": 1917,
        "era": "war_poetry",
        "text": """Bent double, like old beggars under sacks,
Knock-kneed, coughing like hags, we cursed through sludge,
Till on the haunting flares we turned our backs
And towards our distant rest began to trudge.
Men marched asleep. Many had lost their boots
But limped on, blood-shod. All went lame; all blind;
Drunk with fatigue; deaf even to the hoots
Of tired, outstripped Five-Nines that dropped behind.

Gas! Gas! Quick, boys! An ecstasy of fumbling,
Fitting the clumsy helmets just in time;
But someone still was yelling out and stumbling,
And flound'ring like a man in fire or lime...
Dim, through the misty panes and thick green light,
As under a green sea, I saw him drowning.
In all my dreams, before my helpless sight,
He plunges at me, guttering, choking, drowning.

If in some smothering dreams you too could pace
Behind the wagon that we flung him in,
And watch the white eyes writhing in his face,
His hanging face, like a devil's sick of sin;
If you could hear, at every jolt, the blood
Come gargling from the froth-corrupted lungs,
Obscene as cancer, bitter as the cud
Of vile, incurable sores on innocent tongues,
My friend, you would not tell with such high zest
To children ardent for some desperate glory,
The old Lie: Dulce et decorum est
Pro patria mori."""
    },
    {
        "title": "Anthem for Doomed Youth",
        "author": "Wilfred Owen",
        "year": 1917,
        "era": "war_poetry",
        "text": """What passing-bells for these who die as cattle?
Only the monstrous anger of the guns.
Only the stuttering rifles' rapid rattle
Can patter out their hasty orisons.
No mockeries now for them; no prayers nor bells;
Nor any voice of mourning save the choirs,—
The shrill, demented choirs of wailing shells;
And bugles calling for them from sad shires.

What candles may be held to speed them all?
Not in the hands of boys, but in their eyes
Shall shine the holy glimmers of goodbyes.
The pallor of girls' brows shall be their pall;
Their flowers the tenderness of patient minds,
And each slow dusk a drawing-down of blinds."""
    },
    {
        "title": "The Soldier",
        "author": "Rupert Brooke",
        "year": 1914,
        "era": "war_poetry",
        "text": """If I should die, think only this of me:
That there's some corner of a foreign field
That is for ever England. There shall be
In that rich earth a richer dust concealed;
A dust whom England bore, shaped, made aware,
Gave, once, her flowers to love, her ways to roam,
A body of England's, breathing English air,
Washed by the rivers, blest by suns of home.

And think, this heart, all evil shed away,
A pulse in the eternal mind, no less
Gives somewhere back the thoughts by England given;
Her sights and sounds; dreams happy as her day;
And laughter, learnt of friends; and gentleness,
In hearts at peace, under an English heaven."""
    },

    # ─── OLD ENGLISH (additional) ──────────────────────────────────────────
    # Beowulf opening in Hall's 1892 public-domain prose translation.
    # Testing: do battle scenes differ from devotional Old English (Caedmon)?
    {
        "title": "Beowulf: The Opening (Hall translation, 1892)",
        "author": "Anonymous (trans. Hall)",
        "year": 700,
        "era": "old_english",
        "text": """Lo, praise of the prowess of people-kings
of spear-armed Danes, in days long sped,
we have heard, and what honor the athelings won!
Oft Scyld the Scefing from squadroned foes,
from many a tribe, the mead-bench tore,
awing the earls. Since erst he lay
friendless, a foundling, fate repaid him:
for he waxed under welkin, in wealth he throve,
till before him the folk, both far and near,
who house by the whale-path, heard his mandate,
gave him gifts: a good king he!"""
    },
    {
        "title": "Beowulf: The Fight with Grendel",
        "author": "Anonymous (trans. Hall)",
        "year": 700,
        "era": "old_english",
        "text": """The hero hardened his heart anew.
He gathered his weapons and went to his rest.
Grim was the grip of Grendel's hand,
the demon's grasp was dreadful to feel.
Neither blade nor point of iron could pierce
the hide of that hellish spawn of the night.
The monster minded nought but murder,
the foul fiend felt no fear of men.
But Beowulf gripped him, the greatest of heroes,
and held him fast in his fearless hands,
till joint-bark cracked and body broke,
and the arm and shoulder asunder flew."""
    },

    # ─── NEOCLASSICAL / 18TH CENTURY (Pope paradox investigation) ────────
    # The Q2/Q1 taxonomy (2026-10-11) found Pope to be the extreme Q1 strategist
    # despite writing in closed heroic couplets. Adding more Pope poems plus
    # comparison neoclassical poets (Dryden, Johnson, Gay) to test whether Q1
    # dominance is specific to Pope's diction or characteristic of the era.
    {
        "title": "An Essay on Criticism (opening)",
        "author": "Alexander Pope",
        "year": 1711,
        "era": "18th_century",
        "text": """'Tis hard to say, if greater want of skill
Appear in writing or in judging ill;
But, of the two, less dang'rous is th' offence
To tire our patience, than mislead our sense.
Some few in that, but numbers err in this,
Ten censure wrong for one who writes amiss;
A fool might once himself alone expose,
Now one in verse makes many more in prose.
'Tis with our judgments as our watches, none
Go just alike, yet each believes his own.
In poets as true genius is but rare,
True taste as seldom is the critic's share;
Both must alike from Heav'n derive their light,
These born to judge, as well as those to write."""
    },
    {
        "title": "Epistle to Dr. Arbuthnot (opening)",
        "author": "Alexander Pope",
        "year": 1735,
        "era": "18th_century",
        "text": """Shut, shut the door, good John! fatigued, I said,
Tie up the knocker, say I'm sick, I'm dead.
The Dog-star rages! nay 'tis past a doubt,
All Bedlam, or Parnassus, is let out:
Fire in each eye, and papers in each hand,
They rave, recite, and madden round the land.
What walls can guard me, or what shades can hide?
They pierce my thickets, through my Grot they glide,
By land, by water, they renew the charge,
They stop the chariot, and they board the barge.
No place is sacred, not the church is free;
Ev'n Sunday shines no Sabbath-day to me;
Then from the Mint walks forth the man of rhyme,
Happy! to catch me just at dinner-time."""
    },
    {
        "title": "An Essay on Man (Epistle I, opening)",
        "author": "Alexander Pope",
        "year": 1733,
        "era": "18th_century",
        "text": """Awake, my St. John! leave all meaner things
To low ambition, and the pride of Kings.
Let us (since Life can little more supply
Than just to look about us and to die)
Expatiate free o'er all this scene of Man;
A mighty maze! but not without a plan;
A Wild, where weeds and flow'rs promiscuous shoot,
Or Garden, tempting with forbidden fruit.
Together let us beat this ample field,
Try what the open, what the covert yield;
The latent tracts, the giddy heights explore
Of all who blindly creep, or sightless soar;
Eye Nature's walks, shoot Folly as it flies,
And catch the Manners living as they rise."""
    },
    {
        "title": "MacFlecknoe (opening)",
        "author": "John Dryden",
        "year": 1682,
        "era": "18th_century",
        "text": """All human things are subject to decay,
And when fate summons, monarchs must obey.
This Flecknoe found, who, like Augustus, young
Was called to empire, and had governed long;
In prose and verse, was owned, without dispute,
Through all the realms of Nonsense, absolute.
This aged prince, now flourishing in peace,
And blest with issue of a large increase,
Worn out with business, did at last debate
To settle the succession of the State;
And, pondering which of all his sons was fit
To reign, and wage immortal war with wit,
Cried: 'Tis resolved; for nature pleads, that he
Should only rule, who most resembles me."""
    },
    {
        "title": "The Vanity of Human Wishes (opening)",
        "author": "Samuel Johnson",
        "year": 1749,
        "era": "18th_century",
        "text": """Let observation with extensive view,
Survey mankind, from China to Peru;
Remark each anxious toil, each eager strife,
And watch the busy scenes of crowded life;
Then say how hope and fear, desire and hate,
O'erspread with snares the clouded maze of fate,
Where wav'ring man, betrayed by vent'rous pride,
To tread the dreary paths without a guide,
As treach'rous phantoms in the mist delude,
Shuns fancied ills, or chases airy good;
How rarely reason guides the stubborn choice,
Rules the bold hand, or prompts the suppliant voice;
How nations sink, by darling schemes oppressed,
When vengeance listens to the fool's request."""
    },

    # ─── POSTCOLONIAL / DIASPORA ─────────────────────────────────────────────
    # Poets working between oral traditions, dialect, and literary English.
    # Hypothesis: code-switching, vernacular patterning, and cross-cultural
    # lexicons produce distinct S2 signatures versus mainstream Anglo-American verse.
    {
        "title": "Remember",
        "author": "Joy Harjo",
        "year": 1983,
        "era": "postcolonial",
        "text": """Remember the sky that you were born under,
know each of the star's stories.
Remember the moon, know who she is.
Remember the sun's birth at dawn, that is the
strongest point of time. Remember sundown
and the giving away to night.
Remember your birth, how your mother struggled
to give you form and breath. You are evidence of
her life, and her mother's, and hers.
Remember your father. He is your life, also.
Remember the earth whose skin you are:
red earth, black earth, yellow earth, white earth
brown earth, we are earth.
Remember the plants, trees, animal life who all have their
tribes, their families, their histories, too. Talk to them,
listen to them. They are alive poems."""
    },
    {
        "title": "She Had Some Horses",
        "author": "Joy Harjo",
        "year": 1983,
        "era": "postcolonial",
        "text": """She had some horses.

She had horses who were bodies of sand.
She had horses who were maps drawn of blood.
She had horses who were skins of ocean water.
She had horses who were the blue air of sky.
She had horses who were fur and teeth.
She had horses who were clay and blood.
She had horses who were dancers in their hearts.
She had horses who told the truth about themselves.
She had horses who were called dangerous.
She had horses who jumped from skyscrapers to catch the wind.
She had horses who waited for destruction.
She had horses who waited at the end of the road."""
    },
    {
        "title": "The Season of Phantasmal Peace",
        "author": "Derek Walcott",
        "year": 1981,
        "era": "postcolonial",
        "text": """Then all the birds of Guadeloupe, all the birds
of St. Lucia, broke from the sap of their branches
and flew to that arbor made of the boughs of both
islands, the one bridge joining each in a season
that was never the summer of this world, and the birds
that flew over the sea, made it tremble,
and the dolphins leaped from it, not in play
but in gratitude.

Then all the birds of Guadeloupe, those that feed
on the wiry grasses of the savannah, the green-throated
parrot, the humming-birds of the hills,
all the singing birds of both islands
stopped, and the trees were astonished by them.
And nothing, not a single leaf, trembled."""
    },
    {
        "title": "Postcard from Kashmir",
        "author": "Agha Shahid Ali",
        "year": 1987,
        "era": "postcolonial",
        "text": """Kashmir shrinks into my mailbox,
my home a neat four by six inches.

I always loved neatness. Now I hold
the half-inch Himalayas in my hand.

This is home. And this the closest
I'll ever be to home. When I return,
the colors won't be so brilliant,
the Jhelum's waters so clear,
so ultramarine. My love
so overexposed.

And my memory will be a little
out of focus, in it
a giant negative, black
and white, still undeveloped."""
    },
    {
        "title": "Even the Rain",
        "author": "Agha Shahid Ali",
        "year": 1997,
        "era": "postcolonial",
        "text": """What will suffice for a true-love knot? Even the rain?
But he has bought grief's lottery, bought even the rain.

"Our glosses / wanting in this world"—"Can you remember?"
Anyone!—"when we thought / the poets taught" even the rain?

After we died—That was it!—God left us in the dark.
And as we forgot the dark, we forgot even the rain.

Drought was over. Where was I? Drinks were on the house.
For mixers, my love, you'd poured—what?—even the rain.

Of this pear-shaped orange's perfumed twist, I will say:
Extract Vermouth from the bergamot, even the rain.

How did the Enemy love you—with earth? air? and fire?
He held just one thing back till he got even: the rain.

This is God's site for a new paradise. No plan
is good without water, and that includes even the rain."""
    },
    {
        "title": "Calypso",
        "author": "Kamau Brathwaite",
        "year": 1967,
        "era": "postcolonial",
        "text": """The stone had skidded arc'd and bloomed into islands:
Cuba and San Domingo
                         Jamaica and Puerto Rico
Grenada        Guadeloupe         Bonaire

curved stone hissed into reef
coral             cay                    sand                  key

The islands fell out of Columbus's hat
into the morning and the morning sea

and the deep sargasso
rolled and wrote the syllable
of trade wind
and the sea

And the stone sped into the Caribbean

the dark trees
and the dark peoples
and the dark seabirds singing

into this new morning
where silence was
and the heart's blood's
    hum"""
    },

    # ─── DRAMATIC MONOLOGUE ────────────────────────────────────────────
    # Poems where a fictional speaker addresses an implied listener,
    # often revealing themselves unintentionally through what they say.
    {
        "title": "My Last Duchess (complete)",
        "author": "Robert Browning",
        "year": 1842,
        "era": "dramatic_monologue",
        "text": """That's my last Duchess painted on the wall,
Looking as if she were alive. I call
That piece a wonder, now; Fra Pandolf's hands
Worked busily a day, and there she stands.
Will't please you sit and look at her? I said
"Fra Pandolf" by design, for never read
Strangers like you that pictured countenance,
The depth and passion of its earnest glance,
But to myself they turned (since none puts by
The curtain I have drawn for you, but I)
And seemed as they would ask me, if they durst,
How such a glance came there; so, not the first
Are you to turn and ask thus. Sir, 'twas not
Her husband's presence only, called that spot
Of joy into the Duchess' cheek; perhaps
Fra Pandolf chanced to say, "Her mantle laps
Over my lady's wrist too much," or "Paint
Must never hope to reproduce the faint
Half-flush that dies along her throat." Such stuff
Was courtesy, she thought, and cause enough
For calling up that spot of joy. She had
A heart—how shall I say?—too soon made glad,
Too easily impressed; she liked whate'er
She looked on, and her looks went everywhere.
Sir, 'twas all one! My favour at her breast,
The dropping of the daylight in the West,
The bough of cherries some officious fool
Broke in the orchard for her, the white mule
She rode with round the terrace—all and each
Would draw from her alike the approving speech,
Or blush, at least. She thanked men—good! but thanked
Somehow—I know not how—as if she ranked
My gift of a nine-hundred-years-old name
With anybody's gift. Who'd stoop to blame
This sort of trifling? Even had you skill
In speech—which I have not—to make your will
Quite clear to one, and say, "Just this
Or that in you disgusts me; here you miss,
Or there exceed the mark"—and if she let
Herself be lessoned so, nor plainly set
Her wits to yours, forsooth, and made excuse,
—E'en then would be some stooping; and I choose
Never to stoop. Oh, sir, she smiled, no doubt,
Whene'er I passed her; but who passed without
Much the same smile? This grew; I gave commands;
Then all smiles stopped together. There she stands
As if alive. Will't please you rise? We'll meet
The company below, then. I repeat,
The Count your master's known munificence
Is ample warrant that no just pretense
Of mine for dowry will be disallowed;
Though his fair daughter's self, as I avowed
At starting, is my object. Nay, we'll go
Together down, sir. Notice Neptune, though,
Taming a sea-horse, thought a rarity,
Which Claus of Innsbruck cast in bronze for me!"""
    },
    {
        "title": "Soliloquy of the Spanish Cloister",
        "author": "Robert Browning",
        "year": 1842,
        "era": "dramatic_monologue",
        "text": """Gr-r-r—there go, my heart's abhorrence!
Water your damned flower-pots, do!
If hate killed men, Brother Lawrence,
God's blood, would not mine kill you!
What? your myrtle-bush wants trimming?
Oh, that rose has prior claims—
Needs its leaden vase filled brimming?
Hell dry you up with its flames!

At the meal we sit together;
Salve tibi! I must hear
Wise talk of the kind of weather,
Sort of season, time of year:
Not a plenteous cork-crop: scarcely
Dare we hope oak-galls, I doubt;
What's the Latin name for "parsley"?
What's the Greek name for Swine's Snout?

Whew! We'll have our platter burnished,
Laid with care on our own shelf!
With a fire-new spoon we're furnished,
And a goblet for ourself,
Rinsed like something sacrificial
Ere 'tis fit to touch our chaps—
Marked with L. for our initial!
(He-he! There his lily snaps!)"""
    },
    {
        "title": "The Bishop Orders His Tomb at Saint Praxed's Church",
        "author": "Robert Browning",
        "year": 1845,
        "era": "dramatic_monologue",
        "text": """Vanity, saith the preacher, vanity!
Draw round my bed: is Anselm keeping back?
Nephews—sons mine ... ah God, I know not! Well—
She, men would have to be your mother once,
Old Gandolf envied me, so fair she was!
What's done is done, and she is dead beside,
Dead long ago, and I am Bishop since,
And as she died so must we die ourselves,
And thence ye may perceive the world's a dream.
Life, how and what is it? As here I lie
In this state-chamber, dying by degrees,
Hours and long hours in the dead night, I ask
"Do I live, am I dead?" Peace, peace seems all.
Saint Praxed's ever was the church for peace;
And so, about this tomb of mine. I fought
With tooth and nail to save my niche, ye know:
—Old Gandolf cozened me, despite my care;
Shrewd was that snatch from out the corner South
He graced his carrion with, God curse the same!
Yet still my niche is not so cramped but thence
One sees the pulpit o' the epistle-side,
And somewhat of the choir, those silent seats,
And up into the aery dome where live
The angels, and a sunbeam's sure to lurk:
And I shall fill my slab of basalt there,
And 'neath my tabernacle take my rest,
With those nine columns round me, two and two,
The odd one at my feet where Anselm stands:
Peach-blossom marble all, the rare, the ripe
As fresh-poured red wine of a mighty pulse."""
    },
    {
        "title": "Andrea del Sarto",
        "author": "Robert Browning",
        "year": 1855,
        "era": "dramatic_monologue",
        "text": """But do not let us quarrel any more,
No, my Lucrezia; bear with me for once:
Sit down and all shall happen as you wish.
You turn your face, but does it bring a tear?
I fancy you are studying to put
That little something in the eyes of yours
Beyond my art, and the eyes are wide and bright
As now,—go on, and see how that strikes you!
No gainsaying, no, indeed! I dare not.
Such frank blue eyes, they flatter my account!
Too live the life led, too, do you not think?
Beside, to-morrow,—a holiday! do you know,
We have no such delight in all the year?
Still, all I care for, if he cares for me at all,
Is, does he paint? you ask. I paint, that's all.
But do not let us quarrel any more,
No, my Lucrezia; bear with me for once.
Sit down, and let us judge: is the fault there,
That the form is empty, that there is no soul?
What's lost? I know it, and I say, I know it.
A common greyness silvers everything—
All in a twilight, you and I alike
—You, at the point of your first pride in me
(That's gone, you know)—but I, at every point
My youth, my hope, my art, being all toned down
To yonder sober pleasant Fiesole.
There's the bell clinking from the chapel-top;
That length of convent-wall across the way
Holds the trees safer, huddled more inside;
The last monk leaves the garden; days decrease
And autumn grows, autumn in everything.
Eh? the whole seems to fall into a shape
As if I saw alike my work and self
And all that I was born to be and do,
A twilight-piece. Love, we are in God's hand.
How strange now, looks the life he makes us lead;
So free we seem, so fettered fast we are!"""
    },
    {
        "title": "Tithonus",
        "author": "Alfred Lord Tennyson",
        "year": 1860,
        "era": "dramatic_monologue",
        "text": """The woods decay, the woods decay and fall,
The vapours weep their burthen to the ground,
Man comes and tills the field and lies beneath,
And after many a summer dies the swan.
Me only cruel immortality
Consumes; I wither slowly in thine arms,
Here at the quiet limit of the world,
A white-haired shadow roaming like a dream
The ever-silent spaces of the East,
Far-folded mists, and gleaming halls of morn.

Alas! for this gray shadow, once a man—
So glorious in his beauty and thy choice,
Who madest him thy chosen, that he seemed
To his great heart none other than a God!
I asked thee, "Give me immortality."
Then didst thou grant mine asking with a smile,
Like wealthy men who care not how they give.
But thy strong Hours indignant worked their wills,
And beat me down and marred and wasted me,
And though they could not end me, left me maimed
To dwell in presence of immortal youth,
Immortal age beside immortal youth,
And all I was in ashes."""
    },
    {
        "title": "Gerontion",
        "author": "T.S. Eliot",
        "year": 1920,
        "era": "dramatic_monologue",
        "text": """Here I am, an old man in a dry month,
Being read to by a boy, waiting for rain.
I was neither at the hot gates
Nor fought in the warm rain
Nor knee deep in the salt marsh, heaving a cutlass,
Bitten by flies, fought.
My house is a decayed house,
And the jew squats on the window sill, the owner,
Spawned in some estaminet of Antwerp,
Blistered in Brussels, patched and peeled in London.
The goat coughs at night in the field overhead;
Rocks, moss, stonecrop, iron, merds.
The woman keeps the kitchen, makes tea,
Sneezes at evening, poking the peevish gutter.

I an old man,
A dull head among windy spaces.

Signs are taken for wonders. "We would see a sign!"
The word within a word, unable to speak a word,
Swaddled with darkness. In the derangement of the senses
Comes Christ the tiger
In depraved May, dogwood and chestnut, flowering judas,
To be eaten, to be divided, to be drunk
Among whispers; by Mr. Silvero
With caressing hands, at Limoges
Who walked all night in the next room;
By Hakagawa, bowing among the Titians;
By Madame de Tornquist, in the dark room
Shifting the candles; Fräulein von Kulp
Who turned in the hall, one hand on the door."""
    },
    {
        "title": "The Love Song of J. Alfred Prufrock (middle)",
        "author": "T.S. Eliot",
        "year": 1915,
        "era": "dramatic_monologue",
        "text": """And indeed there will be time
To wonder, "Do I dare?" and, "Do I dare?"
Time to turn back and descend the stair,
With a bald spot in the middle of my hair—
(They will say: "How his hair is growing thin!")
My morning coat, my collar mounting firmly to the chin,
My necktie rich and modest, but asserted by a simple pin—
(They will say: "But how his arms and legs are thin!")
Do I dare
Disturb the universe?
In a minute there is time
For decisions and revisions which a minute will reverse.

For I have known them all already, known them all—
Have known the evenings, mornings, afternoons,
I have measured out my life with coffee spoons;
I know the voices dying with a dying fall
Beneath the music from a farther room.
So how should I presume?

And I have known the eyes already, known them all—
The eyes that fix you in a formulated phrase,
And when I am formulated, sprawling on a pin,
When I am pinned and wriggling on the wall,
Then how should I begin
To spit out all the butt-ends of my days and ways?
And how should I presume?"""
    },

    # ─── ELEGY ─────────────────────────────────────────────────────────
    {
        "title": "Elegy Written in a Country Churchyard (opening)",
        "author": "Thomas Gray",
        "year": 1751,
        "era": "elegy",
        "text": """The curfew tolls the knell of parting day,
The lowing herd wind slowly o'er the lea,
The ploughman homeward plods his weary way,
And leaves the world to darkness and to me.

Now fades the glimmering landscape on the sight,
And all the air a solemn stillness holds,
Save where the beetle wheels his droning flight,
And drowsy tinklings lull the distant folds;

Save that from yonder ivy-mantled tower
The moping owl does to the moon complain
Of such as, wandering near her secret bower,
Molest her ancient solitary reign.

Beneath those rugged elms, that yew-tree's shade,
Where heaves the turf in many a mouldering heap,
Each in his narrow cell for ever laid,
The rude forefathers of the hamlet sleep."""
    },
    {
        "title": "Lycidas (opening and lament)",
        "author": "John Milton",
        "year": 1637,
        "era": "elegy",
        "text": """Yet once more, O ye Laurels, and once more
Ye Myrtles brown, with Ivy never-sear,
I com to pluck your Berries harsh and crude,
And with forc'd fingers rude,
Shatter your leaves before the mellowing year.
Bitter constraint, and sad occasion dear,
Compels me to disturb your season due:
For Lycidas is dead, dead ere his prime,
Young Lycidas, and hath not left his peer:
Who would not sing for Lycidas? he well knew
Himself to sing, and build the lofty rhyme.
He must not flote upon his watry bear
Unwept, and welter to the parching wind,
Without the meed of som melodious tear."""
    },
    {
        "title": "In Memoriam A.H.H. (sections I and VII)",
        "author": "Alfred Lord Tennyson",
        "year": 1849,
        "era": "elegy",
        "text": """I hold it true, whate'er befall;
I feel it, when I sorrow most;
'Tis better to have loved and lost
Than never to have loved at all.

Dark house, by which once more I stand
Here in the long unlovely street,
Doors, where my heart was used to beat
So quickly, waiting for a hand,

A hand that can be clasp'd no more—
Behold me, for I cannot sleep,
And like a guilty thing I creep
At earliest morning to the door.

He is not here; but far away
The noise of life begins again,
And ghastly thro' the drizzling rain
On the bald street breaks the blank day."""
    },
    {
        "title": "Adonais (stanzas I and II)",
        "author": "Percy Bysshe Shelley",
        "year": 1821,
        "era": "elegy",
        "text": """I weep for Adonais—he is dead!
Oh, weep for Adonais! though our tears
Thaw not the frost which binds so dear a head!
And thou, sad Hour, selected from all years
To mourn our loss, rouse thy obscure compeers,
And teach them thine own sorrow, say: with me
Died Adonais; till the Future dares
Forget the Past, his fate and fame shall be
An echo and a light unto eternity!

Where wert thou, mighty Mother, when he lay,
When thy Son lay, pierced by the shaft which flies
In darkness? where was lorn Urania
When Adonais died? With veiled eyes,
Mid listening Echoes, in her Paradise
She sate, while one, with soft enamoured breath,
Rekindled all the fading melodies,
With which, like flowers that mock the corse beneath,
He had adorned and hid the coming bulk of death."""
    },
    {
        "title": "O Captain! My Captain!",
        "author": "Walt Whitman",
        "year": 1865,
        "era": "elegy",
        "text": """O Captain! my Captain! our fearful trip is done,
The ship has weather'd every rack, the prize we sought is won,
The port is near, the bells I hear, the people all exulting,
While follow eyes the steady keel, the vessel grim and daring;
But O heart! heart! heart!
O the bleeding drops of red,
Where on the deck my Captain lies,
Fallen cold and dead.

O Captain! my Captain! rise up and hear the bells;
Rise up—for you the flag is flung—for you the bugle trills,
For you bouquets and ribbon'd wreaths—for you the shores a-crowding,
For you they call, the swaying mass, their eager faces turning;
Here Captain! dear father!
This arm beneath your head!
It is some dream that on the deck,
You've fallen cold and dead."""
    },
    {
        "title": "To an Athlete Dying Young",
        "author": "A.E. Housman",
        "year": 1896,
        "era": "elegy",
        "text": """The time you won your town the race
We chaired you through the market-place;
Man and boy stood cheering by,
And home we brought you shoulder-high.

To-day, the road all runners come,
Shoulder-high we bring you home,
And set you at your threshold down,
Townsman of a stiller town.

Smart lad, to slip betimes away
From fields where glory does not stay,
And early though the laurel grows
It withers quicker than the rose."""
    },
    {
        "title": "On My First Son",
        "author": "Ben Jonson",
        "year": 1616,
        "era": "elegy",
        "text": """Farewell, thou child of my right hand, and joy;
My sin was too much hope of thee, loved boy.
Seven years thou wert lent to me, and I thee pay,
Exacted by thy fate, on the just day.
O, could I lose all father now! For why
Will man lament the state he should envy?
To have so soon 'scaped world's and flesh's rage,
And if no other misery, yet age?
Rest in soft peace, and, asked, say, Here doth lie
Ben Jonson his best piece of poetry.
For whose sake henceforth all his vows be such
As what he loves may never like too much."""
    },

    # ─── DIALOGUE-HEAVY POEMS (added for dialogue S₂ analysis) ────────────────
    {
        "title": "La Belle Dame sans Merci",
        "author": "John Keats",
        "year": 1819,
        "era": "romantic",
        "text": """"O what can ail thee, knight-at-arms,
Alone and palely loitering?
The sedge has withered from the lake,
And no birds sing.

O what can ail thee, knight-at-arms,
So haggard and so woe-begone?
The squirrel's granary is full,
And the harvest's done.

I see a lily on thy brow,
With anguish moist and fever-dew,
And on thy cheeks a fading rose
Fast withereth too.

I met a lady in the meads,
Full beautiful—a faery's child,
Her hair was long, her foot was light,
And her eyes were wild.

I made a garland for her head,
And bracelets too, and fragrant zone;
She looked at me as she did love,
And made sweet moan.

I set her on my pacing steed,
And nothing else saw all day long,
For sidelong would she bend, and sing
A faery's song.

She found me roots of relish sweet,
And honey wild, and manna-dew,
And sure in language strange she said—
'I love thee true'.

She took me to her elfin grot,
And there she wept and sighed full sore,
And there I shut her wild wild eyes
With kisses four.

And there she lullèd me asleep,
And there I dreamed—Ah! woe betide!—
The latest dream I ever dreamt
On the cold hill side.

I saw pale kings and princes too,
Pale warriors, death-pale were they all;
They cried—'La Belle Dame sans Merci
Thee hath in thrall!'

I saw their starved lips in the gloam,
With horrid warning gapèd wide,
And I awoke and found me here,
On the cold hill's side.

And this is why I sojourn here,
Alone and palely loitering,
Though the sedge is withered from the lake,
And no birds sing."""
    },
    {
        "title": "The Death of the Hired Man (opening)",
        "author": "Robert Frost",
        "year": 1914,
        "era": "early_modern",
        "text": """Mary sat musing on the lamp-flame at the table
Waiting for Warren. When she heard his step,
She ran on tip-toe down the darkened passage
To meet him in the doorway with the news
And put him on his guard. "Silas is back."
She pushed him outward with her through the door
And shut it after her. "Be kind," she said.
She took the market things from Warren's arms
And set them on the porch, then drew him down
To sit beside her on the wooden steps.

"When was I ever anything but kind to him?
But I'll not have the fellow back," he said.
"I told him so last haying, didn't I?
If he left then, I said, that ended it."
"What good is he? Who else will harbor him
At his age for the little he can do?
What help he is there's no depending on.
Off he goes always when I need him most.
'We do some charity work as well as farming,'
With your nice load of hay. He never could
Make up his mind to be dependent on.
Oh, he had to be told; he had to go.
But Mary, remember—it's for you he came."
"Think of it, Warren," and she sighed. "He came
Home to die: you needn't be afraid he'll leave you this time."
"Home," he mocked gently.
"Yes, what else but home?
It all depends on what you mean by home.\""""
    },
    {
        "title": "Goblin Market (opening stanzas)",
        "author": "Christina Rossetti",
        "year": 1862,
        "era": "victorian",
        "text": """Morning and evening
Maids heard the goblins cry:
"Come buy our orchard fruits,
Come buy, come buy:
Apples and quinces,
Lemons and oranges,
Plump unpecked cherries,
Melons and raspberries,
Bloom-down-cheeked peaches,
Swart-headed mulberries,
Wild free-born cranberries,
Crab-apples, dewberries,
Pine-apples, blackberries,
Apricots, strawberries;—
All ripe together
In summer weather,—
Morns that pass by,
Fair eves that fly;
Come buy, come buy:
Our grapes fresh from the vine,
Pomegranates full and fine,
Dates and sharp bullaces,
Rare pears and greengages,
Damsons and bilberries,
Taste them and try:
Currants and gooseberries,
Bright-fire-like barberries,
Figs to fill your mouth,
Citrons from the South,
Sweet to tongue and sound to eye;
Come buy, come buy."

Evening by evening
Among the brookside rushes,
Laura bowed her head to hear,
Lizzie veiled her blushes:
Crouching close together
In the cooling weather,
With clasping arms and cautioning lips,
With tingling cheeks and finger tips.
"Lie close," Laura said,
Pricking up her golden head:
"We must not look at goblin men,
We must not buy their fruits:
Who knows upon what soil they fed
Their hungry thirsty roots?"
"Come buy," call the goblins
Hobbling down the glen."""
    },
    {
        "title": "A Dialogue of Self and Soul (Part I)",
        "author": "W.B. Yeats",
        "year": 1933,
        "era": "modernist",
        "text": """MY SOUL. I summon to the winding ancient stair;
Set all your mind upon the steep ascent,
Upon the broken, crumbling battlement,
Upon the breathless starlit air,
'Upon the star that marks the hidden pole;
Fix every wandering thought upon
That quarter where all thought is done:
Who can distinguish darkness from the soul?

MY SELF. The consecrated blade upon my knees
Is Sato's ancient blade, still razor-keen,
Still like a looking-glass unscratched, unstained,
Unworn by time; and by Montashigi
Three hundred years ago or thereabouts
Wrought it of such a temper that he thought
He could outcut the hardest of the night.

MY SOUL. Montashigi, third of his family, fashioned it
Five hundred years ago, about it lie
Flowers from I know not what embroidery—
Heart's purple—and all these I set
For emblems of the day against the tower
Emblematical of the night,
And claim as by a soldier's right
A charter to commit the crime once more.

MY SELF. Why should the imagination of a man
Long past his prime remember things that are
Emblematical of love and war?
Think of ancestral night that can,
If but imagination scorn the earth
And intellect is wandering
To this and that and t'other thing,
Deliver from the crime of death and birth.

MY SOUL. Whence had they come,
The hand and lash that beat down frigid Rome?
What sacred drama's part was played
When that fierce virgin and her Star
Out of the fabulous darkness called?"""
    },
    {
        "title": "The Charge of the Light Brigade",
        "author": "Alfred, Lord Tennyson",
        "year": 1854,
        "era": "victorian",
        "text": """Half a league, half a league,
Half a league onward,
All in the valley of Death
Rode the six hundred.
"Forward, the Light Brigade!
Charge for the guns!" he said.
Into the valley of Death
Rode the six hundred.

"Forward, the Light Brigade!"
Was there a man dismayed?
Not though the soldier knew
Someone had blundered.
Theirs not to make reply,
Theirs not to reason why,
Theirs but to do and die.
Into the valley of Death
Rode the six hundred.

Cannon to right of them,
Cannon to left of them,
Cannon in front of them
Volleyed and thundered;
Stormed at with shot and shell,
Boldly they rode and well,
Into the jaws of Death,
Into the mouth of hell
Rode the six hundred.

Flashed all their sabres bare,
Flashed as they turned in air
Sabring the gunners there,
Charging an army, while
All the world wondered.
Plunged in the battery-smoke
Right through the line they broke;
Cossack and Russian
Reeled from the sabre stroke
Shattered and sundered.
Then they rode back, but not,
Not the six hundred."""
    },

    # ─── ADDITIONAL LIMERICKS: PUNCHLINE VARIATION STUDY ─────────────────
    # Testing the hypothesis that limerick punchline (line 5) S2 is driven
    # by CONTENT (invented vocabulary, absurdism) not position alone.
    # Three variants: invented-word punchline, conventional punchline, dark twist.
    {
        "title": "There Was a Young Lady Whose Nose",
        "author": "Edward Lear",
        "year": 1846,
        "era": "limerick",
        "text": """There was a Young Lady whose nose
Was so long that it reached to her toes;
So she hired an Old Lady
Whose conduct was steady,
To carry that wonderful nose."""
    },
    {
        "title": "There Was an Old Man of the Coast",
        "author": "Edward Lear",
        "year": 1846,
        "era": "limerick",
        "text": """There was an Old Man of the Coast,
Who placidly sat on a post;
But when it was cold
He relinquished his hold
And called for some hot buttered toast."""
    },
    {
        "title": "There Was a Young Lady of Niger",
        "author": "Anonymous",
        "year": 1902,
        "era": "limerick",
        "text": """There was a young lady of Niger
Who smiled as she rode on a tiger;
They returned from the ride
With the lady inside,
And the smile on the face of the tiger."""
    },

    # ─── CLERIHEW ─────────────────────────────────────────────────────────
    # The clerihew (Edmund Clerihew Bentley, ~1905) is a 4-line AABB
    # biographical humorous form. Unlike the limerick (AABBA, strict meter),
    # clerihews have no meter constraint — lines vary wildly in length.
    # Hypothesis: without metrical constraint, clerihews should show higher
    # S2 than limericks (less GPT-2-predictable syllabic structure).
    {
        "title": "Sir Humphrey Davy",
        "author": "Edmund Clerihew Bentley",
        "year": 1905,
        "era": "clerihew",
        "text": """Sir Humphrey Davy
Abominated gravy.
He lived in the odium
Of having discovered sodium."""
    },
    {
        "title": "The Art of Biography",
        "author": "Edmund Clerihew Bentley",
        "year": 1905,
        "era": "clerihew",
        "text": """The art of Biography
Is different from Geography.
Geography is about maps,
But Biography is about chaps."""
    },
    {
        "title": "Oscar Wilde",
        "author": "Edmund Clerihew Bentley",
        "year": 1905,
        "era": "clerihew",
        "text": """Oscar Wilde
When mild
Spoke in epigrams to fill
The gallery—and always will."""
    },
    {
        "title": "Charlotte Mew",
        "author": "Synthetic (clerihew test case)",
        "year": 2024,
        "era": "clerihew",
        "text": """Charlotte Mew
Hardly anyone knew.
She wrote "The Farmer's Bride"—
A masterpiece, and quietly died."""
    },
    {
        "title": "William Topaz McGonagall",
        "author": "Synthetic (clerihew test case)",
        "year": 2024,
        "era": "clerihew",
        "text": """William Topaz McGonagall
Was known as rather comical.
His Tay Bridge poem was so bad
It made all of Scotland glad."""
    },

    # Additional clerihews to test the proper-noun hypothesis (see findings/clerihew_vs_limerick.md).
    # Chosen for subjects with distinctive biographical facts requiring hard-to-predict tokens.
    {
        "title": "Isaac Newton",
        "author": "Synthetic (clerihew test case)",
        "year": 2024,
        "era": "clerihew",
        "text": """Isaac Newton
Could never be beaten
At sums involving gravity—
His great depravity."""
    },
    {
        "title": "Edgar Allan Poe",
        "author": "Synthetic (clerihew test case)",
        "year": 2024,
        "era": "clerihew",
        "text": """Edgar Allan Poe
Made ravens say "Nevermore."
He also married his cousin,
Which was awkward by the dozen."""
    },
    {
        "title": "Marie Curie",
        "author": "Synthetic (clerihew test case)",
        "year": 2024,
        "era": "clerihew",
        "text": """Marie Curie
Isolated radium, purely.
She named polonium after Poland,
A patriotic rolland."""
    },
    {
        "title": "Nikola Tesla",
        "author": "Synthetic (clerihew test case)",
        "year": 2024,
        "era": "clerihew",
        "text": """Nikola Tesla
Loved pigeons better
Than people. His rotating fields
Changed what alternating current yields."""
    },
    {
        "title": "James Joyce",
        "author": "Synthetic (clerihew test case)",
        "year": 2024,
        "era": "clerihew",
        "text": """James Joyce
Had a peculiar voice.
He wrote Ulysses in Trieste—
A breakfast for the feast."""
    },

    # ─── DOUBLE DACTYL ────────────────────────────────────────────────────────
    # The double dactyl (invented by Anthony Hecht and John Hollander, 1966) is
    # the most formally constrained English short poem form:
    # - Two stanzas of 4 lines each
    # - Lines 1-3 and 5-7: dactylic dimeter (DUM-da-da DUM-da-da, 6 syllables)
    # - Lines 4 and 8: catalectic (DUM-da-da DUM, 4 syllables); they must RHYME
    # - Line 1: nonsense reduplication phrase (e.g., "Higgledy-piggledy")
    # - Line 2: person's name (6 syllables, dactylic dimeter)
    # - Line 7: a SINGLE polysyllabic word (6 syllables)
    # Hypothesis: greater constraint than limericks → even lower mean S₂,
    # except at the nonsense line-1 and the rare polysyllabic line-7 word.
    {
        "title": "Emily Dickinson (Double Dactyl)",
        "author": "Synthetic (double dactyl test case)",
        "year": 2024,
        "era": "double_dactyl",
        "text": """Higgledy-piggledy,
Emily Dickinson,
Dressed all in white when she
Stayed home to write.

Slant rhymes and dashes and
Letters to everyone,
Unconventionally
Blazing with light."""
    },
    {
        "title": "Gerard Manley Hopkins (Double Dactyl)",
        "author": "Synthetic (double dactyl test case)",
        "year": 2024,
        "era": "double_dactyl",
        "text": """Higgledy-piggledy,
Gerard Manley Hopkins,
Bent the old meter and
Wrestled with God.

Strangely anguished by love,
Tortured but beautiful—
Theologically
Giving the nod."""
    },
    {
        "title": "Alfred Lord Tennyson (Double Dactyl)",
        "author": "Synthetic (double dactyl test case)",
        "year": 2024,
        "era": "double_dactyl",
        "text": """Higgledy-piggledy,
Alfred Lord Tennyson,
Wrote his elegy for
Arthur, his friend.

Elegiacally,
Philosophically—
Death, he concluded, was
Not quite the end."""
    },
    {
        "title": "William Carlos Williams (Double Dactyl)",
        "author": "Synthetic (double dactyl test case)",
        "year": 2024,
        "era": "double_dactyl",
        "text": """Higgledy-piggledy,
William Carlos Williams,
Doctor by day, and by
Night a new voice.

No ideas but in
Concrete, particular—
Experientially
Right in his choice."""
    },
    {
        "title": "Lawrence Ferlinghetti (Double Dactyl)",
        "author": "Synthetic (double dactyl test case)",
        "year": 2024,
        "era": "double_dactyl",
        "text": """Higgledy-piggledy,
Lawrence Ferlinghetti,
Ran a bookshop and kept
Freedom above.

Beat-era polemics—
Selling the dangerous—
Uncompromisingly
Done it for love."""
    },

    # ─── ASYMMETRY TEST POEMS (added 2026-10-20) ──────────────────────────────
    # Poems added specifically to test the surprise asymmetry finding:
    # (1) Emily Dickinson — short, dense poems to test the "isolated spike / deep valley" pattern
    # (2) Countee Cullen — formal sonnets testing the "ramp-up crash" pattern
    # (3) Gerard Manley Hopkins — sprung rhythm testing "pre-spike buildup"
    # (4) A Valediction: Forbidding Mourning — Donne's extended metaphor asymmetry
    # (5) Anne Carson — contemporary lyric testing sustained-elevation pattern
    # (6) Robinson Jeffers — environmental poetry with long-arc conformity

    # Emily Dickinson — "Tell all the truth but tell it slant" (Fr. 1263, 1872, PD)
    {
        "title": "Tell all the truth but tell it slant",
        "author": "Emily Dickinson",
        "year": 1872,
        "era": "19th_century",
        "text": """Tell all the truth but tell it slant —
Success in Circuit lies
Too bright for our infirm Delight
The Truth's superb surprise
As Lightning to the Children eased
With explanation kind
The Truth must dazzle gradually
Or every man be blind —"""
    },

    # Emily Dickinson — "I'm Nobody! Who are you?" (Fr. 288, 1861, PD)
    {
        "title": "I'm Nobody! Who are you?",
        "author": "Emily Dickinson",
        "year": 1861,
        "era": "19th_century",
        "text": """I'm Nobody! Who are you?
Are you – Nobody – too?
Then there's a pair of us!
Don't tell! they'd advertise –

How dreary – to be – Somebody!
How public – like a Frog –
To tell one's name – the livelong June –
To an admiring Bog!"""
    },

    # Countee Cullen — "Heritage" (opening, 1925, PD)
    # Long, meditative poem with refrain structure; tests "ramp-up crash" in Harlem Renaissance
    {
        "title": "Heritage (opening)",
        "author": "Countee Cullen",
        "year": 1925,
        "era": "harlem_renaissance",
        "text": """What is Africa to me:
Copper sun or scarlet sea,
Jungle star or jungle track,
Strong bronzed men, or regal black
Women from whose loins I sprang
When the birds of Eden sang?
One three centuries removed
From the scenes his fathers loved,
Spicy grove, cinnamon tree,
What is Africa to me?

So I lie, who all day long
Want no sound except the song
Sung by wild barbaric birds
Goading massive jungle herds,
Juggernauts of flesh that pass
Trampling tall defiant grass
Where young forest lovers lie,
Plighting troth beneath the sky."""
    },

    # Gerard Manley Hopkins — "Pied Beauty" (1877, PD)
    # Short poem with dense sprung rhythm; extreme pre-spike setup pattern
    {
        "title": "Pied Beauty",
        "author": "Gerard Manley Hopkins",
        "year": 1877,
        "era": "victorian",
        "text": """Glory be to God for dappled things –
  For skies of couple-colour as a brinded cow;
    For rose-moles all in stipple upon trout that swim;
Fresh-firecoal chestnut-falls; finches' wings;
  Landscape plotted and pieced – fold, fallow, and plough;
    And áll trádes, their gear and tackle and trim.

All things counter, original, spare, strange;
  Whatever is fickle, freckled (who knows how?)
    With swift, slow; sweet, sour; adazzle, dim;
He fathers-forth whose beauty is past change:
                                Praise him."""
    },

    # John Donne — "A Valediction: Forbidding Mourning" (1633, PD)
    # Extended metaphor (compass conceit); metaphysical asymmetry tests
    {
        "title": "A Valediction: Forbidding Mourning",
        "author": "John Donne",
        "year": 1633,
        "era": "early_modern",
        "text": """As virtuous men pass mildly away,
  And whisper to their souls to go,
Whilst some of their sad friends do say,
  "Now his breath goes," and some say, "No."

So let us melt, and make no noise,
  No tear-floods, nor sigh-tempests move;
'Twere profanation of our joys
  To tell the laity our love.

Moving of th' earth brings harms and fears;
  Men reckon what it did, and meant;
But trepidation of the spheres,
  Though greater far, is innocent.

Dull sublunary lovers' love
  (Whose soul is sense) cannot admit
Of absence, 'cause it doth remove
  The thing which elemented it.

But we, by a love so much refined
  That ourselves know not what it is,
Inter-assurèd of the mind,
  Care less, eyes, lips, and hands to miss.

Our two souls therefore, which are one,
  Though I must go, endure not yet
A breach, but an expansion,
  Like gold to aery thinness beat.

If they be two, they are two so
  As stiff twin compasses are two;
Thy soul, the fixed foot, makes no show
  To move, but doth, if th' other do.

And though it in the center sit,
  Yet, when the other far doth roam,
It leans and hearkens after it,
  And grows erect, as that comes home.

Such wilt thou be to me, who must,
  Like th' other foot, obliquely run;
Thy firmness makes my circle just,
  And makes me end where I begun."""
    },

    # Robinson Jeffers — "Carmel Point" (1954)
    # Environmental/ecological poetry; stark imagery; tests long-arc conformity
    {
        "title": "Carmel Point",
        "author": "Robinson Jeffers",
        "year": 1954,
        "era": "contemporary",
        "text": """We must uncenter our minds from ourselves;
We must unhumanize our views a little, and become confident
As the rock and ocean that we were made from.

Beauty is not always lovely; and the beauty of Carmel Point
Is its distance, the great rocks breaking wave-power,
And the wind's unsleeping restlessness.

This little headland, the gray stone cliff, the colony of pelicans,
Seem permanent; but the land has been eroded seaward
A foot or two since they were first described,
And the pelicans are probably not immortal.

Look up the coast at the old stone farmhouses on the hills.
They are still inhabited, but they will all be gone
Within the century; the century will pass; and the long ocean,
The slow unhasting tide of time will wash them away."""
    },

    # Anne Carson — "The Glass Essay (opening)" (1995)
    # Confessional/contemporary lyric; tests "extended valley" in high-asymmetry poets
    {
        "title": "The Glass Essay (opening)",
        "author": "Anne Carson",
        "year": 1995,
        "era": "contemporary",
        "text": """I can hear little clicks inside my dream.
Night drips its silver tap
down the back.
At 4 A.M. I wake. Thinking

of the man who
left in September.
His name was Law.

My mother is asleep in the next room.
We are in her house on the moors.
It is bleak and very cold."""
    },

    # ─── EKPHRASTIC POETRY ─────────────────────────────────────────────────────
    # Poems about visual art / sculpture / images — tests the verbal-visual interface
    # and whether S2 spikes at "translation moments" where language captures the visual

    # Keats — "Ode on a Grecian Urn" (1820, PD)
    # The most canonical ekphrasis in English; apostrophe to a visual object
    {
        "title": "Ode on a Grecian Urn",
        "author": "John Keats",
        "year": 1820,
        "era": "ekphrastic",
        "text": """Thou still unravish'd bride of quietness,
Thou foster-child of silence and slow time,
Sylvan historian, who canst thus express
A flowery tale more sweetly than our rhyme:
What leaf-fring'd legend haunts about thy shape
Of deities or mortals, or of both,
In Tempe or the dales of Arcady?
What men or gods are these? What maidens loth?
What mad pursuit? What struggle to escape?
What pipes and timbrels? What wild ecstasy?

Heard melodies are sweet, but those unheard
Are sweeter; therefore, ye soft pipes, play on;
Not to the sensual ear, but, more endear'd,
Pipe to the spirit ditties of no tone:
Fair youth, beneath the trees, thou canst not leave
Thy song, nor ever can those trees be bare;
Bold Lover, never, never canst thou kiss,
Though winning near the goal—yet, do not grieve;
She cannot fade, though thou hast not thy bliss,
For ever wilt thou love, and she be fair!

Ah, happy, happy boughs! that cannot shed
Your leaves, nor ever bid the Spring adieu;
And, happy melodist, unwearied,
For ever piping songs for ever new;
More happy love! more happy, happy love!
For ever warm and still to be enjoy'd,
For ever panting, and for ever young;
All breathing human passion far above,
That leaves a heart high-sorrowful and cloy'd,
A burning forehead, and a parching tongue.

Who are these coming to the sacrifice?
To what green altar, O mysterious priest,
Lead'st thou that heifer lowing at the skies,
And all her silken flanks with garlands drest?
What little town by river or sea shore,
Or mountain-built with peaceful citadel,
Is emptied of this folk, this pious morn?
And, little town, thy streets for evermore
Will silent be; and not a soul to tell
Why thou art desolate, can e'er return.

O Attic shape! Fair attitude! with brede
Of marble men and maidens overwrought,
With forest branches and the trodden weed;
Thou, silent form, dost tease us out of thought
As doth eternity: Cold Pastoral!
When old age shall this generation waste,
Thou shalt remain, in midst of other woe
Than ours, a friend to man, to whom thou say'st,
'Beauty is truth, truth beauty,—that is all
Ye know on earth, and all ye need to know.'"""
    },

    # Keats — "On Seeing the Elgin Marbles" (1817, PD)
    # Confrontation with sculptural fragments; S2 at the "dim vastness" of art
    {
        "title": "On Seeing the Elgin Marbles",
        "author": "John Keats",
        "year": 1817,
        "era": "ekphrastic",
        "text": """My spirit is too weak—mortality
Weighs heavily on me like unwilling sleep,
And each imagin'd pinnacle and steep
Of godlike hardship tells me I must die
Like a sick Eagle looking at the sky.
Yet 'tis a gentle luxury to weep
That I have not the cloudy winds to keep
Fresh for the opening of the morning's eye.
Such dim-conceiv'd glories of the brain
Bring round the heart an undescribable feud;
So do these wonders a most dizzy pain,
That mingles Grecian grandeur with the rude
Wasting of old Time—with a billowy main—
A sun—a shadow of a magnitude."""
    },

    # Keats — "On First Looking into Chapman's Homer" (1816, PD)
    # Bibliographic ekphrasis — the experience of reading a translation as visual event
    {
        "title": "On First Looking into Chapman's Homer",
        "author": "John Keats",
        "year": 1816,
        "era": "ekphrastic",
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

    # Tennyson — "The Lady of Shalott" (stanzas I-II, 1842, PD)
    # About a weaver who creates images of the world she cannot directly see
    {
        "title": "The Lady of Shalott (opening)",
        "author": "Alfred, Lord Tennyson",
        "year": 1842,
        "era": "ekphrastic",
        "text": """On either side the river lie
Long fields of barley and of rye,
That clothe the wold and meet the sky;
And thro' the field the road runs by
To many-tower'd Camelot;
And up and down the people go,
Gazing where the lilies blow
Round an island there below,
The island of Shalott.

Willows whiten, aspens quiver,
Little breezes dusk and shiver
Thro' the wave that runs for ever
By the island in the river
Flowing down to Camelot.
Four gray walls, and four gray towers,
Overlook a space of flowers,
And the silent isle imbowers
The Lady of Shalott.

There she weaves by night and day
A magic web with colours gay.
She has heard a whisper say,
A curse is on her if she stay
To look down to Camelot.
She knows not what the curse may be,
And so she weaveth steadily,
And little other care hath she,
The Lady of Shalott.

And moving thro' a mirror clear
That hangs before her all the year,
Shadows of the world appear.
There she sees the highway near
Winding down to Camelot:
There the river eddy whirls,
And there the surly village-churls,
And the red cloaks of market girls,
Pass onward from Shalott."""
    },

    # Browning — "Fra Lippo Lippi" (excerpt, 1855, PD)
    # Dramatic monologue spoken by the painter Fra Lippo Lippi; S2 at art-theory moments
    {
        "title": "Fra Lippo Lippi (opening)",
        "author": "Robert Browning",
        "year": 1855,
        "era": "ekphrastic",
        "text": """I am poor brother Lippo, by your leave!
You need not clap your torches to my face.
Zooks, what's to blame? you think you see a monk!
What, 'tis past midnight, and you go the rounds,
And here you catch me at an alley's end
Where sportive ladies leave their doors ajar?
The Carmine's my cloister: hunt it up,
Do,—harry out, if you must show your zeal,
Whatever rat, there, haps on his wrong hole,
And nip each softling of a wee white mouse,
Weke, weke, that's crept to keep him company!
Aha, you know your betters! Then, you'll take
Your hand away that's fiddling on my throat,
And please to know me likewise. Who am I?
Why, one, sir, who is lodging with a friend
Three streets off—he's a certain . . . how d'ye call?
Master—a . . . Cosimo of the Medici,
I' the house that caps the corner."""
    },

    # Browning — "Andrea del Sarto" (excerpt, 1855, PD)
    # The "Faultless Painter" reflects on his perfect technique and moral failure
    {
        "title": "Andrea del Sarto (opening)",
        "author": "Robert Browning",
        "year": 1855,
        "era": "ekphrastic",
        "text": """But do not let us quarrel any more,
No, my Lucrezia; bear with me for once:
Sit down and all shall happen as you wish.
You turn your face, but does it bring your heart?
I'll work then for your friend's friend, never fear,
Treat his own subject after his own way,
Fix his own time, accept too his own price,
And shut the money into this small hand
When next it takes mine. Will it? tenderly?
Oh, I'll content him,—but to-morrow, Love!
I often am much wearier than you think,
This evening more than usual, and it seems
As if—forgive now—should you let me sit
Here by the window with your hand in mine
And look a half-hour forth on Fiesole,
Both of one mind, as married people use,
Quietly, quietly the evening through,
I might get up to-morrow to my work
Cheerful and fresh as ever. Let us try."""
    },

    # D.G. Rossetti — "For a Venetian Pastoral by Giorgione" (1850, PD)
    # Sonnet written for a specific Giorgione painting in the Louvre
    {
        "title": "For a Venetian Pastoral by Giorgione",
        "author": "Dante Gabriel Rossetti",
        "year": 1850,
        "era": "ekphrastic",
        "text": """Water, for anguish of the solstice:—nay,
But dip the vessel slowly,—nay, but lean
And hark how at its verge the wave sighs in
Reluctant. Hush! Beyond all depth away
The heat lies silent at the brink of day:
Now the hand trails upon the viol-string
That sobs, and the brown faces cease to sing,
Sad with the whole of pleasure. Whither stray
Her eyes now, from whose mouth the slim pipes creep
And leave it pouting, while the shadowed grass
Is cool against her naked side? Let be:—
Say nothing now unto her lest she weep,
Nor name this ever. Be it as it was,—
Life touching lips with Immortality."""
    },

    # Swinburne — "Before the Mirror" (1866, PD)
    # Written for Whistler's painting "The Little White Girl"; one of the rare poet-painter collaborations
    {
        "title": "Before the Mirror (stanzas 1-3)",
        "author": "Algernon Charles Swinburne",
        "year": 1866,
        "era": "ekphrastic",
        "text": """White rose in red rose-garden
Is not so white;
Snowdrops that plead for pardon
And pine for fright
Because the hard East blows
Over their maiden rows
Grow not as this face grows from pale to bright.

Behind the veil, forbidden,
Shut up from sight,
Love, is there sorrow hidden,
Is there delight?
Is joy thy dower or grief,
White rose of weary leaf,
Late rose whose life is brief, whose loves are light?

Soft snows that hard winds harden
Till each flake bite
Fill all the flowerless garden
Whose flowers took flight
Long since when summer ceased,
And men rose up from feast,
And warm west wind grew east, and warm day night."""
    },

    # ─── COMPOUND-RICH ADDITIONS (for S2/compound-word analysis) ──────────

    # Hopkins — "Spring and Fall: To a Young Child" (1880, PD)
    # Compound-rich; the question "what heart heard of, ghost guessed" demonstrates
    # Hopkins's coined diction
    {
        "title": "Spring and Fall: To a Young Child",
        "author": "Gerard Manley Hopkins",
        "year": 1880,
        "era": "victorian",
        "text": """Márgarét, áre you gríeving
Over Goldengrove unleaving?
Leáves, líke the things of man, you
With your fresh thoughts care for, can you?
Áh! ás the heart grows older
It will come to such sights colder
By and by, nor spare a sigh
Though worlds of wanwood leafmeal lie;
And yet you wíll weep and know why.
Now no matter, child, the name:
Sórrow's spríngs áre the same.
Nor mouth had, no nor mind, expressed
What heart heard of, ghost guessed:
It ís the blight man was born for,
It is Margaret you mourn for."""
    },

    # Hopkins — "Inversnaid" (1881, PD)
    # Famous for its coined compound words: "windpuff-bonnet", "twindles"
    {
        "title": "Inversnaid",
        "author": "Gerard Manley Hopkins",
        "year": 1881,
        "era": "victorian",
        "text": """This darksome burn, horseback brown,
His rollrock highroad roaring down,
In coop and in comb the fleece of his foam
Flutes and low to the lake falls home.

A windpuff-bonnet of fáwn-fróth
Turns and twindles over the broth
Of a pool so pitchblack, féll-frówning,
It rounds and rounds Despair to drowning.

Degged with dew, dappled with dew
Are the groins of the braes that the brook treads through,
Wiry heathpacks, flitches of fern,
And the beadbonny ash that sits over the burn.

What would the world be, once bereft
Of wet and of wildness? Let them be left,
O let them be left, wildness and wet;
Long live the weeds and the wilderness yet."""
    },

    # Swinburne — "The Garden of Proserpine" (stanzas 1-5, 1866, PD)
    # Victorian compound adjectives and extended repetition
    {
        "title": "The Garden of Proserpine (stanzas 1-5)",
        "author": "Algernon Charles Swinburne",
        "year": 1866,
        "era": "victorian",
        "text": """Here, where the world is quiet;
Here, where all trouble seems
Dead winds' and spent waves' riot
In doubtful dreams of dreams;
I watch the green field growing
For reaping folk and sowing,
For harvest-time and mowing,
A sleepy world of streams.

I am tired of tears and laughter,
And men that laugh and weep;
Of what may come hereafter
For men that sow to reap:
I am weary of days and hours,
Blown buds of barren flowers,
Desires and dreams and powers
And everything but sleep.

Here life has death for neighbour,
And far from eye or ear
Wan waves and wet winds labour,
Weak leaves and winds that fear;
And time remembered is grief forgotten,
And frosts are slain and flowers begotten,
And in green underwood and cover
Blossom by blossom the spring begins.

The full streams feed on flower of rushes,
Ripe grasses trammel a travelling foot,
The faint fresh flame of the young year flushes
From leaf to flower and flower to fruit;
And fruit and leaf are as gold and fire,
And the oat is heard above the lyre,
And the hoofed heel of a satyr crushes
The chestnut-husk at the chestnut-root.

And Pan by noon and Bacchus by night,
Fleeter of foot than the fleet-foot kid,
Follows with dancing and fills with delight
The Maenad and the Bassarid;
And soft as lips that laugh and hide
The laughing leaves of the tree divide,
And screen from seeing and leave in sight
The god pursuing, the maiden hid."""
    },

    # Keats — "The Eve of St. Agnes" (stanzas 1-5, 1819, PD)
    # Rich compound adjectives: "argent-still", "silver-snarling"
    {
        "title": "The Eve of St. Agnes (stanzas 1-5)",
        "author": "John Keats",
        "year": 1819,
        "era": "romantic",
        "text": """St. Agnes' Eve—Ah, bitter chill it was!
The owl, for all his feathers, was a-cold;
The hare limp'd trembling through the frozen grass,
And silent was the flock in woolly fold:
Numb were the Beadsman's fingers, while he told
His rosary, and while his frosted breath,
Like pious incense from a censer old,
Seem'd taking flight for heaven, without a death,
Past the sweet Virgin's picture, while his prayer he saith.

His prayer he saith, this patient, holy man;
Then takes his lamp, and riseth from his knees,
And back returneth, meagre, barefoot, wan,
Along the chapel aisle by slow degrees:
The sculptur'd dead, on each side, seem to freeze,
Emprison'd in black, purgatorial rails:
Knights, ladies, praying in dumb orat'ries,
He passeth by; and his weak spirit fails
To think how they may ache in icy hoods and mails.

Northward he turneth through a little door,
And scarce three steps, ere Music's golden tongue
Flatter'd to tears this aged man and poor;
But no—already had his deathbell rung;
The joys of all his life were said and sung:
His was harsh penance on St. Agnes' Eve:
Another way he went, and soon among
Rough ashes sat he for his soul's reprieve,
And all night kept awake, for sinners' sake to grieve.

That ancient Beadsman heard the prelude soft;
And so it chanc'd, for many a door was wide,
From hurry to and fro. Soon, up aloft,
The silver, snarling trumpets 'gan to chide:
The level chambers, ready with their pride,
Were glowing to receive a thousand guests:
The carved angels, ever eager-eyed,
Star'd, where upon their heads the cornice rests,
With hair blown back, and wings put cross-wise on their breasts.

At length burst in the argent revelry,
With plume, tiara, and all rich array,
Numerous as shadows haunting faerily
The brain, new stuff'd, in youth, with triumphs gay
Of old romance. These let us wish away,
And turn, sole-thoughted, to one Lady there,
Whose heart had brooded, all that wintry day,
On love, and wing'd St. Agnes' saintly care,
As she had heard old dames full many times declare."""
    },

    # Old English — "The Battle of Maldon" (excerpt, trans. Gordon, 991 AD, PD)
    # Contains kennings (compound-metaphors) typical of Old English poetry
    {
        "title": "The Battle of Maldon (excerpt, trans. E.V. Gordon)",
        "author": "Anonymous (trans. E.V. Gordon)",
        "year": 991,
        "era": "old_english",
        "text": """Then Byrhtnoth spoke, raised up his shield,
brandished his slender ash-spear, angry and resolute:
with words he gave him answer,
the proud man gave him answer:
'Do you hear, sea-wanderer, what this people say?
They will give you spears as tribute,
poisoned point and old sword,
that heriot which will not help you in the fight.
Sea-messengers, carry back your message:
tell your people a far worse tale,
how there stands here with his war-band
a man not without honour who defends
this country, Aethelred's homeland,
the people and the ground. The heathen shall fall.
It seems to me too shameful that you should
go to your ships with our tribute unfought,
now that you have come thus far into our land.
You shall not gain treasure so easily;
point and edge shall settle this matter,
grim play of war, before we pay tribute.'"""
    },

    # ─── VILLANELLES (highly constrained form: A1bA2 abA1 abA2 abA1 abA2 abA1A2)
    # Two refrains repeat in specific positions — ideal for S2 repetition analysis

    {
        "title": "The House on the Hill",
        "author": "Edwin Arlington Robinson",
        "year": 1894,
        "era": "villanelle",
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
There is nothing more to say.

There is ruin and decay
In the House on the Hill:
They are all gone away,
There is nothing more to say."""
    },

    {
        "title": "Villanelle of the Poet's Road",
        "author": "Ernest Dowson",
        "year": 1896,
        "era": "villanelle",
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
Wine and woman and song.

We, of the old and strong,
What is better to say?
Yet is day over long.

Wine and woman and song,
Three things garnish our way:
Yet is day over long."""
    },

    # ─── PANTOUM (Malaysian form: ABAB → BCBC → each line repeats as the 2nd/4th
    # of the next stanza; creates recursive semantic loop)

    {
        "title": "On the Departure Platform",
        "author": "Thomas Hardy",
        "year": 1909,
        "era": "pantoum",
        "text": """We kissed at the barrier; and passing through
She left me, and moment by moment got
Smaller and smaller, until to my view
She was but a spot;

A wee white spot of muslin fluff
That down the diminishing platform bore
Through hustling crowds of gentle and rough
To the carriage door.

Under the lamplight's fitful glowers,
Behind dark groups from far and near,
Whose interests were apart from ours,
She would disappear,

Then show again, till I ceased to see
That flexible form, that nebulous white;
And she who was more than my life to me
Had vanished quite."""
    },

    # ─── TRIOLET (8-line form: ABaAabAB — first 2 lines repeat as 4th/5th and 7th/8th)
    # Extreme repetition: refrain occupies half the poem

    {
        "title": "A Kiss",
        "author": "Austin Dobson",
        "year": 1876,
        "era": "triolet",
        "text": """Rose kissed me to-day.
Will she kiss me to-morrow?
Let it be as it may,
Rose kissed me to-day.
But the pleasure gives way
To a savour of sorrow;—
Rose kissed me to-day,—
Will she kiss me to-morrow?"""
    },

    {
        "title": "The Wanderer's Litany",
        "author": "Arthur Symons",
        "year": 1895,
        "era": "triolet",
        "text": """I have lived and I have loved;
I have waked and I have slept;
I have sung and I have moved;
I have lived and I have loved.
I have laboured and I have mourned,
I have let the world go;
I have lived and I have loved;
I have waked and I have slept."""
    },

    # ─── RONDEAU (15-line French form: R being a rentrement — fragment of line 1 —
    # repeating at lines 9 and 15; tests partial-refrain memory)

    {
        "title": "In Flanders Fields",
        "author": "John McCrae",
        "year": 1915,
        "era": "rondeau",
        "text": """In Flanders fields the poppies blow
Between the crosses, row on row,
That mark our place; and in the sky
The larks, still bravely singing, fly
Scarce heard amid the guns below.

We are the Dead. Short days ago
We lived, felt dawn, saw sunset glow,
Loved and were loved, and now we lie
In Flanders fields.

Take up our quarrel with the foe:
To you from failing hands we throw
The torch; be yours to hold it high.
If ye break faith with us who die
We shall not sleep, though poppies grow
In Flanders fields."""
    },

    # ─── GHAZAL (Arabic/Persian form: independent couplets united by RADIF refrain)
    # Each couplet ends with the same word/phrase; tests end-position repetition

    {
        "title": "Ghazal of the Better-Unbegun",
        "author": "Heather McHugh",
        "year": 1994,
        "era": "ghazal",
        "text": """Too volatile, am I? too volatile? Unfair
to say so. All I want is a world here.

Too volatile? You call me volatile?
The whole world's kindling, and you're not aware?

But you're volatile yourself: look, you
can't sit still. And your hair is everywhere.

Everywhere is where I want to be.
I want to be where everywhere is fair.

Nothing is fair here, no here, no here—
all out of here, all out, all out of there."""
    },
    # --- New poems added to test poet fingerprint consistency hypothesis ---
    # Blake: Songs of Innocence (simple/repetitive) vs Experience (compressed)
    {
        "title": "The Lamb",
        "author": "William Blake",
        "year": 1789,
        "era": "romantic",
        "text": """Little Lamb, who made thee?
Dost thou know who made thee?
Gave thee life, and bid thee feed,
By the stream and o'er the mead;
Gave thee clothing of delight,
Softest clothing, woolly, bright;
Gave thee such a tender voice,
Making all the vales rejoice?
Little Lamb, who made thee?
Dost thou know who made thee?

Little Lamb, I'll tell thee,
Little Lamb, I'll tell thee:
He is called by thy name,
For he calls himself a Lamb.
He is meek, and he is mild;
He became a little child.
I a child, and thou a lamb,
We are called by his name.
Little Lamb, God bless thee!
Little Lamb, God bless thee!"""
    },
    {
        "title": "The Garden of Love",
        "author": "William Blake",
        "year": 1794,
        "era": "romantic",
        "text": """I went to the Garden of Love,
And saw what I never had seen:
A Chapel was built in the midst,
Where I used to play on the green.

And the gates of this Chapel were shut,
And 'Thou shalt not' writ over the door;
So I turned to the Garden of Love
That so many sweet flowers bore;

And I saw it was filled with graves,
And tomb-stones where flowers should be;
And Priests in black gowns were walking their rounds,
And binding with briars my joys and desires."""
    },
    {
        "title": "The Chimney Sweeper (Experience)",
        "author": "William Blake",
        "year": 1794,
        "era": "romantic",
        "text": """A little black thing among the snow,
Crying 'weep! weep!' in notes of woe!
'Where are thy father and mother? say?'
'They are both gone up to the church to pray.

Because I was happy upon the heath,
And smiled among the winter's snow,
They clothed me in the clothes of death,
And taught me to sing the notes of woe.

And because I am happy and dance and sing,
They think they have done me no injury,
And are gone to praise God and his Priest and King,
Who made up a heaven of our misery.'"""
    },
    # Hardy: more poems to test his high variance (1.935 vs 0.068)
    {
        "title": "The Darkling Thrush",
        "author": "Thomas Hardy",
        "year": 1900,
        "era": "victorian",
        "text": """I leant upon a coppice gate
When Frost was spectre-grey,
And Winter's dregs made desolate
The weakening eye of day.
The tangled bine-stems scored the sky
Like strings of broken lyres,
And all mankind that haunted nigh
Had sought their household fires.

The land's sharp features seemed to be
The Century's corpse outleant,
His crypt the cloudy canopy,
The wind his death-lament.
The ancient pulse of germ and birth
Was shrunken hard and dry,
And every spirit upon earth
Seemed fervourless as I.

At once a voice arose among
The bleak twigs overhead
In a full-hearted evensong
Of joy illimited;
An aged thrush, frail, gaunt, and small,
In blast-beruffled plume,
Had chosen thus to fling his soul
Upon the growing gloom.

So little cause for carolings
Of such ecstatic sound
Was written on terrestrial things
Afar or nigh around,
That I could think there trembled through
His happy good-night air
Some blessed Hope, whereof he knew
And I was unaware."""
    },
    {
        "title": "After a Journey",
        "author": "Thomas Hardy",
        "year": 1914,
        "era": "victorian",
        "text": """Hereto I come to view a voiceless ghost;
Whither, O whither will its whim now draw me?
Up the cliff, down, till I'm lonely, lost,
And the unseen waters' ejaculations awe me.
Where you will next be there's no knowing,
Facing round about me everywhere,
With your nut-coloured hair,
And gray eyes, and rose-flush coming and going.

Yes: I have re-entered your olden haunts at last;
Through the years, through the dead scenes I have tracked you;
What have you now found to say of our past—
Scanned across the dark space wherein I have lacked you?
Summer gave us sweets, but autumn wrought division?
Things were not lastly as firstly well
With us twain, you tell?
But all's closed now, despite Time's derision."""
    },
    # Keats: additional poems to clarify his variance pattern
    {
        "title": "To Autumn",
        "author": "John Keats",
        "year": 1819,
        "era": "romantic",
        "text": """Season of mists and mellow fruitfulness,
Close bosom-friend of the maturing sun;
Conspiring with him how to load and bless
With fruit the vines that round the thatch-eves run;
To bend with apples the moss'd cottage-trees,
And fill all fruit with ripeness to the core;
To swell the gourd, and plump the hazel shells
With a sweet kernel; to set budding more,
And still more, later flowers for the bees,
Until they think warm days will never cease,
For summer has o'er-brimm'd their clammy cells.

Who hath not seen thee oft amid thy store?
Sometimes whoever seeks abroad may find
Thee sitting careless on a granary floor,
Thy hair soft-lifted by the winnowing wind;
Or on a half-reap'd furrow sound asleep,
Drows'd with the fume of poppies, while thy hook
Spares the next swath and all its twined flowers:
And sometimes like a gleaner thou dost keep
Steady thy laden head across a brook;
Or by a cider-press, with patient look,
Thou watchest the last oozings hours by hours.

Where are the songs of spring? Ay, where are they?
Think not of them, thou hast thy music too,—
While barred clouds bloom the soft-dying day,
And touch the stubble-plains with rosy hue;
Then in a wailful choir the small gnats mourn
Among the river sallows, borne aloft
Or sinking as the light wind lives or dies;
And full-grown lambs loud bleat from hilly bourn;
Hedge-crickets sing; and now with treble soft
The red-breast whistles from a garden-croft;
And gathering swallows twitter in the skies."""
    },
    # Cinquain: Adelaide Crapsey — a uniquely American syllabic form (not yet in corpus)
    {
        "title": "November Night",
        "author": "Adelaide Crapsey",
        "year": 1915,
        "era": "imagist",
        "text": """Listen…
With faint dry sound,
Like steps of passing ghosts,
The leaves, frost-crisp'd, break from the trees
And fall."""
    },
    {
        "title": "Triad",
        "author": "Adelaide Crapsey",
        "year": 1915,
        "era": "imagist",
        "text": """These be
Three silent things:
The falling snow… the hour
Before the dawn… the mouth of one
Just dead."""
    },
    # Dickinson: "Because I could not stop for Death" — one of her most famous
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
For His Civility –

We passed the School, where Children strove
At Recess – in the Ring –
We passed the Fields of Gazing Grain –
We passed the Setting Sun –

Or rather – He passed us –
The Dews drew quivering and chill –
For only Gossamer, my Gown –
My Tippet – only Tulle –

We paused before a House that seemed
A Swelling of the Ground –
The Roof was scarcely visible –
The Cornice – in the Ground –

Since then – 'tis Centuries – and yet
Feels shorter than the Day
I first surmised the Horses' Heads
Were toward Eternity –"""
    },
    # ─── ANAPHORA DECAY CURVE TESTS ────────────────────────────────────────
    # Psalm 136 KJV: 26 repetitions of "for his mercy endureth for ever"
    # This is the gold-standard test of very-long-anaphora entropy decay.
    {
        "title": "Psalm 136 (KJV)",
        "author": "Anonymous (KJV translation)",
        "year": -600,
        "era": "biblical",
        "text": """O give thanks unto the LORD; for he is good: for his mercy endureth for ever.
O give thanks unto the God of gods: for his mercy endureth for ever.
O give thanks to the Lord of lords: for his mercy endureth for ever.
To him who alone doeth great wonders: for his mercy endureth for ever.
To him that by wisdom made the heavens: for his mercy endureth for ever.
To him that stretched out the earth above the waters: for his mercy endureth for ever.
To him that made great lights: for his mercy endureth for ever.
The sun to rule by day: for his mercy endureth for ever.
The moon and stars to rule by night: for his mercy endureth for ever.
To him that smote Egypt in their firstborn: for his mercy endureth for ever.
And brought out Israel from among them: for his mercy endureth for ever.
With a strong hand, and with a stretched out arm: for his mercy endureth for ever.
To him which divided the Red sea into parts: for his mercy endureth for ever.
And made Israel to pass through the midst of it: for his mercy endureth for ever.
But overthrew Pharaoh and his host in the Red sea: for his mercy endureth for ever.
To him which led his people through the wilderness: for his mercy endureth for ever.
To him which smote great kings: for his mercy endureth for ever.
And slew famous kings: for his mercy endureth for ever.
Sihon king of the Amorites: for his mercy endureth for ever.
And Og the king of Bashan: for his mercy endureth for ever.
And gave their land for an heritage: for his mercy endureth for ever.
Even an heritage unto Israel his servant: for his mercy endureth for ever.
Who remembered us in our low estate: for his mercy endureth for ever.
And hath redeemed us from our enemies: for his mercy endureth for ever.
Who giveth food to all flesh: for his mercy endureth for ever.
O give thanks unto the God of heaven: for his mercy endureth for ever."""
    },
    # Walt Whitman "Song of Myself" Section 15 — the great occupation catalogue
    # Each line begins "The X Y Z" — 22 occupational vignettes
    {
        "title": "Song of Myself (section 15, catalogue)",
        "author": "Walt Whitman",
        "year": 1855,
        "era": "19th_century",
        "text": """The pure contralto sings in the organ loft,
The carpenter dresses his plank, the tongue of his foreplane whistles its wild ascending lisp,
The married and unmarried children ride home to their Thanksgiving dinner,
The pilot seizes the king-pin, he heaves down with a strong arm,
The mate stands braced in the whale-boat, lance and harpoon are ready,
The duck-shooter walks by silent and cautious stretches,
The deacons are ordain'd with cross'd hands at the altar,
The spinning-girl retreats and advances to the hum of the big wheel,
The farmer stops by the bars as he walks on a First-day loafe and looks at the oats and rye,
The lunatic is carried at last to the asylum a confirm'd case,
The jour printer with gray head and gaunt jaws works at his case,
He turns his quid of tobacco while his eyes blurr with the manuscript;
The malform'd limbs are tied to the surgeon's table,
What is removed drops horribly in a pail;
The quadroon girl is sold at the auction-stand, the drunkard nods by the bar-room stove,
The machinist rolls up his sleeves, the policeman travels his beat, the gate-keeper marks who pass,
The young fellow drives the express-wagon, (I love him, though I do not know him;)
The half-breed straps on his light boots to compete in the race,
The western turkey-shooting draws old and young, some lean on their rifles, some sit on logs,
Out from the crowd steps the marksman, takes his position, levels his piece;
The groups of newly-come immigrants cover the wharf or levee,
As the woolly-pates hoe in the sugar-field, the overseer views them from his saddle,
The bugle calls in the ball-room, the gentlemen run for their partners, the dancers bow to each other,
The youth lies awake in the cedar-roof'd garret and harks to the musical rain,
The Wolverine sets traps on the creek that helps fill the Huron,
The squaw wrapt in her yellow-hemm'd cloth is offering moccasins and bead-bags for sale,
The connoisseur peers along the exhibition-gallery with half-shut eyes bent sideways,
As the deck-hands make fast the steamboat the plank is thrown for the shore-going passengers,
The young sister holds out the skein while the elder sister winds it off in a ball, and stops now and then for the knots,
The one-year wife is recovering and happy having a week ago borne her first child,
The clean-hair'd Yankee girl works with her sewing-machine or in the factory or mill,
The paving-man leans on his two-handed rammer, the reporter's lead flies swiftly over the note-book, the sign-painter is lettering with blue and gold."""
    },
    # Joy Harjo "She Had Some Horses" (1983) — "She had horses" scaffold
    # Excerpt with ~15 "She had horses" repetitions (public domain via fair use excerpt)
    {
        "title": "She Had Some Horses (opening)",
        "author": "Joy Harjo",
        "year": 1983,
        "era": "contemporary",
        "text": """She had some horses.

She had horses who were bodies of sand.
She had horses who were maps drawn of blood.
She had horses who were skins of ocean water.
She had horses who were the blue air of sky.
She had horses who were fur and teeth.
She had horses who were clay and would break.
She had horses who were splintered red cliff.

She had some horses.

She had horses with long, pointed breasts.
She had horses with full, brown thighs.
She had horses who laughed too much.
She had horses who threw rocks at glass houses.
She had horses who licked razor blades.

She had some horses.

She had horses who danced in their mothers' arms.
She had horses who thought they were the sun and their reflection,
    but they were the moon and a bad wind.
She had horses who walked lightly,
    carrying what was sacred in their mouths.
She had horses who told the truth about joy.
She had horses who cried in their gentle pain.
She had horses who said words they no longer understood.
She had horses who used their heads to get through this world.
She had horses who thought that silence was more powerful
    than either of the languages they knew.

She had some horses.

She had horses who got down on their knees for any savior.
She had horses who were afraid to die, and who were afraid not to die.

She had some horses.

She had horses who said they were the only beauty.
And she had horses."""
    },

    # ─── NONSENSE POETRY ──────────────────────────────────────────────────────
    # Tests whether nonsense vocabulary spikes S2 despite correct grammar,
    # and whether within-poem repetition shows learning/decay effects.
    {
        "title": "Jabberwocky",
        "author": "Lewis Carroll",
        "year": 1871,
        "era": "nonsense",
        "text": """'Twas brillig, and the slithy toves
Did gyre and gimble in the wabe;
All mimsy were the borogoves,
And the mome raths outgrabe.

"Beware the Jabberwock, my son!
The jaws that bite, the claws that catch!
Beware the Jubjub bird, and shun
The frumious Bandersnatch!"

He took his vorpal sword in hand;
Long time the manxome foe he sought—
So rested he by the Tumtum tree,
And stood awhile in thought.

And, as in uffish thought he stood,
The Jabberwock, with eyes of flame,
Came whiffling through the tulgey wood,
And burbled as it came!

One, two! One, two! And through and through
The vorpal blade went snicker-snack!
He left it dead, and with its head
He went galumphing back.

"And hast thou slain the Jabberwock?
Come to my arms, my beamish boy!
O frabjous day! Callooh! Callay!"
He chortled in his joy.

'Twas brillig, and the slithy toves
Did gyre and gimble in the wabe;
All mimsy were the borogoves,
And the mome raths outgrabe."""
    },
    {
        "title": "The Hunting of the Snark (Fit the First, opening)",
        "author": "Lewis Carroll",
        "year": 1876,
        "era": "nonsense",
        "text": """"Just the place for a Snark!" the Bellman cried,
As he landed his crew with care;
Supporting each man on the top of the tide
By a finger entwined in his hair.

"Just the place for a Snark! I have said it twice:
That alone should encourage the crew.
Just the place for a Snark! I have said it thrice:
What I tell you three times is true."

The crew was complete: it included a Boots—
A maker of Bonnets and Hoods—
A Barrister, brought to arrange their disputes—
And a Broker, to value their goods.

A Billiard-marker, whose skill was immense,
Might perhaps have won more than his share—
But a Banker, engaged at enormous expense,
Had the whole of their cash in his care.

There was also a Beaver, that paced on the deck,
Or would sit making lace in the bow:
And had often (the Bellman said) saved them from wreck,
Though none of the sailors knew how."""
    },
    # ─── NEW YORK SCHOOL ADDITIONS ────────────────────────────────────────────
    {
        "title": "Having a Coke with You",
        "author": "Frank O'Hara",
        "year": 1960,
        "era": "new_york_school",
        "text": """is even more fun than going to San Sebastian, Irún, Hendaye, Biarritz, Bayonne
or being sick to my stomach on the Traversière or the Grand Balcon
or even catching a little Vulture in Tarbes
or searching for the Princesse de Clèves in Fontainebleau for the seventh time
or finding the first one in Normandy

and partly what it is about you being you
is even more fun than going to the Prado to see La Ronde or the Unicorn
or the Last Supper of Leonardo da Vinci or even Piazza San Marco
or going to the movies in the Seventies in Paris

and partly what it is about you being you
is even more fun than trying to figure out who the Bellman is

in your eyes I see
a whole world of the imagination
and partly it is the coffee, partly
it is the way you look at me straight from your eyes
which makes me feel like a man sitting in the second row."""
    },
    {
        "title": "You Were Wearing",
        "author": "Kenneth Koch",
        "year": 1962,
        "era": "new_york_school",
        "text": """You were wearing your Edgar Allan Poe printed cotton blouse.
In each divided up square of the blouse was a picture of Edgar Allan Poe.
Your hair was blonde and you were cute. You asked me, "Do most boys think
of motels like this?" No, no I said, it is thought about differently by me.
Your hair was wet and gleaming and you were not afraid.
I was sorry to see you had on your Edgar Allan Poe blouse.
In the morning we went into a flower shop and you said, "I want
Roses and daffodils and pinks and zinnias, why I only want
Flowers." And so we bought some flowers, for you are as
Beautiful as the day, and my heart overflows, it is a beehive."""
    },
    # ─── CONTEMPORARY ADDITIONS ───────────────────────────────────────────────
    {
        "title": "Dim Lady",
        "author": "Harryette Mullen",
        "year": 2002,
        "era": "contemporary",
        "text": """My honeybunch's peepers are nothing like neon. Today's
special at Red Lobster in her kisser. If Liquid Paper is white,
her racks are institutional beige. If her mop were Slinkys,
dishwater Slinkys would grow on her noggin. I have seen tablecloths
in Shakey's Pizza Parlors, red and white, but no such
picnic colors do I see in her mug. And in some prefab food
products is there more sweetness than in the garlic breeze my
main squeeze wheezes. I love to hear her rap, yet I'm aware
that Muzak has a hipper beat. I don't know any Mariah Carey
video where goddesses' boobs are like my babeola's bumbalooza.
And yet, by Huey Newton, I think my love as dopely fly as any
she made famous by some grubby outlaw Casanova."""
    },
    # ─── LANGUAGE POETRY ADDITIONS ────────────────────────────────────────────
    {
        "title": "Progress (excerpt)",
        "author": "Barrett Watten",
        "year": 1985,
        "era": "language",
        "text": """The work is possible, even if the word
is not. Two kinds of nothing: the kind that's left
over, and the kind that's always there. Language
is the other side of things. What you mean
is not what you say, and nothing is added
when the figure appears. The outside returns
in the form of its argument: the word, the world,
the image of the word, the world of the image.
A surface admits no depth, while the work
goes on. This is not the thing I planned to write."""
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
