import datetime
import matplotlib.pyplot as plt


def runt(db, target):
    cursor = db.collection.find({})
    first_tweet = db.collection.find_one({})
    init_time = datetime.datetime.strptime(first_tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    plot_data = [0]*50000
    print 'Compiling data...'
    for tweet in cursor:
        time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        delta = (time-init_time).seconds
        plot_data[delta] += 1
    print 'Plotting...'
    plt.plot(plot_data)
    plt.show()
    print 'DONE!'