From the autograder's home directory, run:

```
#!bash

$ python autograder.py filename.json
```
The insides of that json file should look approximately like this:
```
#!json
{
    "metadata": {
        "year": 2013,
        "names": {
            "hosts": {
                "method": "",
                "method_description": ""
                },
            "nominees": {
                "method": "",
                "method_description": ""
                },
	        "awards": {
                "method": "",
                "method_description": ""
                },
            "presenters": {
                "method": "",
                "method_description": ""
                }
            },
        "mappings": {
            "nominees": {
                "method": "",
                "method_description": ""
                },
            "presenters": {
                "method": "",
                "method_description": ""
                }
            }
        },
    "data": {
        "unstructured": {
            "hosts": [],
            "winners": [],
            "awards": [],
            "presenters": [],
            "nominees": []
        },
        "structured": {
            "award1": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "award2": {
                "nominees": [],
                "winner": "",
                "presenters": []
            },
            "award2": {
                "nominees": [],
                "winner": "",
                "presenters": []
            }
        }
    }
}
```
A few notes:

- Run autograder once per result file. You should have one result file per year. So, you should be running autograder twice.

- Under "method" in the metadata section, you may put three values: "hardcoded", "scraped", or "detected"

- Under "method_description", if you wrote "detected" or "scraped", write a line or two about your method. This is your chance to argue that what you did was clever/difficult enough to deserve to be treated as though you detected everything, or that it wasn't so easy that it should be treated as though it was scraped.

- NEW! The "names" section is where you indicate that the names (i.e. the correct spelling etc.) were hard coded, scraped, or detected. The "mappings" section is where you indicate that the mapping from name to award was hard coded, scraped, or detected. Please include both; the autograder will break if you don't. Yes, there are some people who hard code the names but not the mapping.

- This is new code. It will probably break. By all means, report issues. Bored? Feel free to investigate and fix issues.

- This is new code. There may be better ways of quantifying how well a particular aspect of your programs is performing. If you see something that you think doesn't make sense, or if you have an idea for a different way to do things that might work better, report it as an issue and explain your perspective. Brownie points are always available for this kind of participation!

- Remember, dictionary keys are case sensitive. The program is expecting certain key names. I can't guarantee that it will function properly if your keys have different case or spelling.