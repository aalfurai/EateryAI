# /EateryAI/
This documentation will go through the directories / files of the repo from top to bottom. The organization and directory names are kind of confusing but we were piecing together a lot of things for the demo. Files or directories not mentioned are probably not too important. At the end are some pointers that may be useful for integration / future development.


### EateryAI/backend/
`EateryAI/backend/data/` contains the original dataset json and the recategorized data json. This format of data labelling is crucial for how our meal solver works.

`EateryAI/backend/sandbox/` contains some scripts and notebooks we used to experiment with / develop the categorization strategy and scoring strategies.

`EateryAI/backend/scripts/db/` contains scripts that set up the PostgreSQL database.

**`EateryAI/backend/sql/` contains the schema for the PostgreSQL database we used.**

### EateryAI/backend/src (the meat and bones)

#### `EateryAI/backend/src/config/`
`EateryAI/backend/src/config/db.py` establishes the backend's connection with the database.

`EateryAI/backend/src/config/dependencies.py` and `security.py` establishes the secure fastAPI connection.

`EateryAI/backend/src/db/` contains files we used to establish local db connections during development.

**`EateryAI/backend/src/helpers/`** contains helper functions and classes.

**`EateryAI/backend/src/schemas/`** defines dataclasses used in the meal solver (nicely formats how information is passed around).

`EateryAI/backend/src/services/` contains data services used by the backend api.

**`EateryAI/backend/src/solver/functions.py`** contains the main meal solver. Note the format the data needs to be in for it to work.

`EateryAI/backend/src/solver/setup.py` contains the old keyword-matching categorization strategy used in testing. We deprecated that in favor of stored, llm categorization.

`EateryAI/backend/src/main.py` contains the API setup for our fastAPI demo.

`EateryAI/backend/src/Makefile` builds the demo that we have.



### EateryAI/frontend/
`EateryAI/frontend/api/` defines the API on how information is sent and retrieved between the frontend and the backend. It defines how data should be structured when sending / querying items, meals, menu info, user info, etc.

`EateryAI/frontend/app/` defines UI components and layout on our React Native demo app.

`EateryAI/frontend/assets/` contains the EatAI logo and its display settings.

`EateryAI/frontend/components/` contains more UI components, some connect to API calls.

`EateryAI/frontend/context/` makes User's info accessible throughout all the pages in the app and triggers weight updates for user preference learning.

`EateryAI/frontend/data/` holds default values for default users and their preference learning weights.

`EateryAI/frontend/hooks/` contains React hooks that make the frontend function.

`EateryAI/frontend/types/` defines types for how data for constraints, meals, users, and weights are formatted and passed around.

`EateryAI/frontend/utils/` fetches fast food logos to display on the frontend.

`EateryAI/frontend/app.json` configures the app's Expo build. (for the demo ui/app)

`EateryAI/frontend/metro.config.js` configuration for React Native.

### EateryAI/src/
#### `EateryAI/src/backend/`

`EateryAI/src/backend/classes.py` Holds a helper NumRange class.

**`EateryAI/src/backend/queries.py` python API for SQL queries to the actual backend database.**

`EateryAI/src/backend/query_helpers.py` helper functions for the queries.py file.


#### `EateryAI/src/db/`
`EateryAI/src/backend/db/db_connection.py` Contains classes/functions that establish connection logic with the backend database.


## Notes for integration and future development
The most important things for integration are bolded, and the meal solver itself is probably what you are after. (`EateryAI/backend/src/solver/`) Take note of the format of data it takes in, and note how the solver scores and prunes results. The rest are kind of supports for the demo. It may be worth looking at the database schema and how we chose to organize it, but it's pretty flexible as long as the data needed for the meal solver is quickly queryable.

The main improvements that can be made (outside of a new algorithm) are probably to the scoring / ranking system. Right now the solver takes into account diversity, how close the meal is to nutrition goals, price, and a user's prioritization of price/calories/protein. This scoring system is alright but can be better tuned for user recommendations. For example the app can track if a user has a preference for a certain item from a restaurant (like Taco Bell Crunchwrap) and take that into account in the scoring too.

Build-Your-Own meals (and restaurant combos) aren't and *cannot* be supported by this algorithm. The current implementation assumes item price is *additive*. (for example, ordering item A and item B means the price is A's price plus B's price) The logical structure of how meals combine just wasn't available or obtainable to us and I think this would be a major hurdle in future development. 

If I'm being honest, a complete overhaul of the meal solver is probably needed in the long run. There have been suggestions on alternate, more flexible or efficient algorithms (0/1 knapsack) that better model the problem, but we weren't able to implement those. It's worth researching before building the app around that. I do think the app is a good idea, but I think a really good recommendation algorithm is needed if you really want to take the mental load of planning meals off users (which I think is one of the best benefits).