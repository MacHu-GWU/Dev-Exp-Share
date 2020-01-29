from pubsub import pub

# ------------ create a listener ------------------

def listener1(message):
    print("User1 received Message: {}".format(message))

def listener2(message):
    print("User2 received Message: {}".format(message))




# ------------ register listener ------------------

pub.subscribe(listener1, "NewsFeed")
pub.subscribe(listener2, "NewsFeed")

# ---------------- send a message ------------------

# print('Publish something via pubsub')
# anObj = dict(a=456, b='abc')
# pub.sendMessage('rootTopic', arg1=123, arg2=anObj)
pub.sendMessage("NewsFeed", message="Hello World")