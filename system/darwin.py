import pync

def notify(notification, title, description, application):
    pync.Notifier.notify(description, title=title)
