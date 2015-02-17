# Golden Globes
Golden Globes Natural Language Processor  
by Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder  
Northwestern University  
EECS 337  
Professor Lawrence Birnbaum  
17 February 2015

The main executable file is goldenglobes.py, which will take some command line arguments, one of which will certainly be
the JSON file containing the raw twitter data. This file should only contain the main function with as little code as
possible. We're going to want to abstract our various methods and classes to modules, which we'll keep tucked away in
the modules folder. This way when one of us wants to edit something, the chances of conflicts when it comes time to
merge is much lower.

We used a different module for each task segment (hosts, presenters/nominees, winners, etc.) We stored all of our
regular expressions in regex.py.

We anticipate our system being adaptable for future years because we did not hard-code any of the tasks.

Libraries used:
re
nltk
twitter