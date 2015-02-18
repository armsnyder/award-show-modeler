
import webbrowser
import urllib2
import json

import util


def run(target):
    """Creates and outputs an html formatted results document"""

    html = ''
    html += html_hosts(target)
    html += html_image_add(find_image(target.get_name_list(target.hosts)))

    for winner, award, time in target.winners:
        html += html_text_add(award)
        html += html_text_winner(winner)
        html += html_image_add(find_image(winner))
        html += html_text_time(util.timestamp_to_datetime(time).strftime("%H:%M:%S"))

    html += html_text_heading('Best Dressed:')
    for name in target.best_dressed:
        full_name = target.join_name(name)
        html += html_text_add(full_name)
        html += html_image_add(find_image(full_name))

    html += html_text_heading('Worst Dressed:')
    for name in target.worst_dressed:
        full_name = target.join_name(name)
        html += html_text_add(full_name)
        html += html_image_add(find_image(full_name))

    html = html_cleanup(html)
    html_done(html)


def html_text_add(text):
    return "<p><b>"+text+"</b></p>"


def html_text_time(text):
    return "<p><i>"+text+"</i></p>"


def html_text_winner(text):
    return "<p>"+text+"</p>"


def html_hosts(target):
    result = '<p><h1>The Host'
    if len(target.hosts) > 1:
        result += 's'
    result += ':</h1></p>'
    result += "<p>"+target.get_name_list(target.hosts)+"</p>"
    return result


def html_text_heading(text):
    return "<p><b>"+text+"</b></p>"


def html_image_add(url):
    if not url:
        return
    return '<img src=' + url + ' style="width:128px;height:128px"></img>'


def html_cleanup(html):
    head = "<!DOCTYPE HTML><html><h1>Team 1 Results</h1>"
    tail = "</html>"
    return head + html + tail


def html_done(html):
    filename = util.get_path('$r/output/result.html')
    with open(filename, 'w') as html_file:
        html_file.write(html.encode('utf8'))
    webbrowser.open_new('file://' + filename)


def find_image(name):
    newname = name.replace(" ", "%20")
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
           'v=1.0' + '&q=' + newname)
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    except:
        return None
    # Process the JSON string.
    google_image = json.load(response)
    found_image = google_image['responseData']['results'][0]['url']
    # try:
    #     # im = Image.open(StringIO(urllib2.urlopen(found_image).read()))
    #     # im.show()
    # except:
    #     return None
    return found_image