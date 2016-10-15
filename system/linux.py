import dbus

notify_object = dbus.SessionBus().get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
notify_interface = dbus.Interface(notify_object, 'org.freedesktop.Notifications')

def notify(notification, title, description, application):
    notify_interface.Notify(application, 0, "", title, description, {}, {}, 8000)
