# Golden Globes
## Discovers and models information about an awards ceremony by processing tweets
Authors: Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder  
Northwestern University  
EECS 337  
Professor Lawrence Birnbaum

### Overview
The main executable file is goldenglobes.py. In separate threads, it calls other modules with specific detection goals.

#### Running the Program
The program can be run from the command line as ```goldenglobes.py``` taking any of the optional arguments. For example, to run the program over the collection ```gg2013``` in the database ```gg``` one would use:
```
python goldenglobes.py -d gg -c gg2013
```

#### Optional Arguments
- **-h**, --help: Show this help message and exit
- **-v**, --verbose: Show additional system messages
- **-d**, --DATABASE: Mongo database where tweets live
- **-c**, --COLLECTION: Specify which Mongo collection to load
- **-t** --TWITTER_JSON: JSON file holding tweet objects; if specified, will attempt to load the JSON objects therein contained into a collection by the same name
- **-f**, --force_reload: Force reloading tweets JSON into mongoDB
- **-a**, --twitter_handles: Match twitter handles to names (requires Internet connection, takes longer)
- **-o**, --OUTPUT: FIle path destination for output JSON file for the autograder
- **-g**, --run_autograder: Automatically launch the autograder when finished

### Libraries Used
In addition to the standard Python libraries, several external modules were used to improve performance.
##### pymongo
Interface for MongoDB used to load corpora to a database for efficiency
#####nltk
Natural Language Toolkit used for tokenizing natural lanuage with n-grams and resolving typos with edit distance metric
#####re
Built-in module used for regular expression matching
#####twitter
Interface for Twitter API used to resolve twitter handles to natural language
#####tkinter
Interface library used for building a GUI

### Adaptability
The only natural language assumption made by the system is that the name of a given award conferred during the award ceremony over which the system is operating begins with the word "best." As a result, the system is immediately adaptable and can be expected to perform reasonably well on any such ceremony (e.g. the Academy Awards).
