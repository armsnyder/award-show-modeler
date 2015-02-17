__author__ = 'DoctorWatson'

import urllib
import urllib2
import simplejson
from StringIO import StringIO
from PIL import Image
import _tkinter




def find_image(name):

    newname = name.replace(" ", "%20")
    print(newname)

    url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
           'v=1.0' + '&q=' + newname)

    try:
        request = urllib2.Request(url, None,)
        response = urllib2.urlopen(request)
    except:
        return None

    print(url)

    # Process the JSON string.
    google_image = simplejson.load(response)

    found_image = google_image['responseData']['results'][0]['url']
    print(found_image)

    try:
        im = Image.open(StringIO(urllib2.urlopen(found_image).read()))
        # im.show()
    except:
        return None

    return found_image

# find_image("amy poehler")