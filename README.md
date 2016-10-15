Simple growl notifications client/server implementation

# Sender usage

If you only need way to send notifications, there only thing you need is
`growlsend.py` utility. It can be used in two ways:

`growlsend.py address password "notification title" "notification text"`

or 

`growlsend.py address password "notification text"`

ommitting the `"notification title"` part.

# Translator requirements

If you need translator of growl notifications to your system native
notifications, you need additionally libraries required for your system.

They can be installed with `pip install -r linux-requirements.txt` for linux systems.

# Translator usage

Simply start `growlnotifier.py password`. Default value for password
(when it's ommited on cmdline) is `dupa.8`.
