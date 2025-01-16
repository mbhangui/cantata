<!-- # vim: wrap
-->
Scrobble Button Synchronization across players
==============================================

This cantata build synchronizes the state of the scrobble button across players connected to the same MPD host. It is implemented using few scripts and two services

1. cantata-mpc (script) - This script is called by cantata when you click the <u>love button</u>. Each click toggles the operation. First click turns on **love** and next click turns off **love**. The cantata-script creates a mpd channel named <u>scrobble</u> and sends a message **love** or **unlove** depending on the state of the <u>love button</u></u>. The <b>cantata-mpc</b> script uses the script <u>/usr/bin/karma</u> from the mpdev package and the <b>mpc</b> command from the mpc package as below.

    ```
    # scrobble love state for the song on last.fm, libre.fm
    # it is need to set last.fm token one time on the host by
    # running moc-scrobbler from mpdev package

    $ MPD_HOST=$MPD_HOST /usr/bin/karma --love || /usr/bin/karma --love

    # create a mpd channel named scrobble.

    $ mpc --host="$MPD_HOST" sendmessage scrobble love || mpc sendmessage scrobble love
    ```
2. cantata modifications - Cantata has been modified to achieve love syncronization.

    i) The first modification is fixing the <u>love button</u> state bug where the button remains in **love** state once you click it. You cannot **unlove** the song. Now when you click the button the first time, cantata changes the color of the button to <u>solid white</u> and runs the script <u>$HOME/bin/cantata-mpc</u> with the argument <u>love</u>. When you click it again to change the state to **unlove**, the script <u>cantata-mpc</u> is called with the argument <u>unlove</u>). 
    ii) Second modification that has been done is that <b>cantata</b> writes the mpd host to which it is connected in the file $HOME/.config/MPD\_HOST.
    iii) Third modification is addition of signal handlers **SIGUSR1** and **SIGUSR2**. The signal **SIGUSR1** toggles the state of **love** button to <u>love</u> and **SIGUSR2** turns on the state to **unlove**.

3. scrobble-button service - This service is setup as a supervised service using supervise(8). You need to install the daemontools package to have supervise(8) installed. This service runs a script named <u>$HOME/bin/scrobble-button</u>. The run file for supervise is as below. The <b>scrobble-button</b> service is implemented by the <u>scrobble-button</u> shell script in the aux-scripts directory. You need to replace <u>mbhangui</u> with your login name in the supervise run file.

    ```
    #!/bin/sh
    user=mbhangui
    exec 2>&1
    home=$(getent passwd $user | awk -F: '{print $6}')
    exec /usr/bin/setuidgid -s $user env HOME=$home $home/bin/scrobble-button
    ```

The <b>scrobble-button</b> script runs tcpclient to connect to port 6600 of the host in <u>$HOME/.config/MPD_HOST</u> and subscribes to the mpd channel named <u>scrobble</u> and waits for <u>love</u>, <u>unlove</u> message on the channel. When it sees the <u>love</u> message on the channel, it sends **SIGUSR1** to <b>cantata</b>. When it sees the <u>unlove</u> message on the channel, it sends **SIGUSR2** to <b>cantata</b>. You can run <b>scrobble-button</b> in the background using your own favourite method instead of using <b>supervise</b>.

Song Information Display Service
================================

When you play a song, it invokes emotions. For many, these emotions can be enhanced by simple things like displaying Album artwork, song information like the Title, Artist, Album name, Song Duration, date when you added the song to the collections, date when you last played the song, how many times have you played the song and how much you love or hate the song. Cantata doesn't display many of the mentioned information. Partly it is because many of this information is not stored by both cantata and mpd. If you install the mpdev package, lot of this missing information gets stored in a sqlite database when you play a song using mpd. However cantata doesn't have the ability to display all this information. This service supplements what is being displayed in the cantata screen by creating a popup for few seconds to display information like last played, play count, date added, rating, etc. This is implemented by a supervise(8) service named notify-screen. This service uses the mpc idle command to detect song change. Whenever a new song starts getting played, this service fetches all information about the song from mpd database, mpd sqlite sticker.db database  and mpdev sqlite stats.db database, It also connects to last.fm and fetches the 'love' status for the song. If the song is loved, it sends a message to the mpd channel named <u>scrobble</u>. The <u>scrobble-button</u> service mentioned above is subscribed to the mpd channel <u>scrobble</u>. When it sees the 'love' message, it sends **SIGUSR1** to <b>cantata</b> to turn on the 'love' button.

The information displayed in the popup is like below

```
       title = There's A Boat Dat's Leavin' Soon For New York
  play_count = 3
 Last Played = Tuesday 08 February 2022 11:14:04 PM IST
 Last Played = 2 years 342 days 1 hr 12 min 52 sec ago
      rating = 6
       karma = 50
    Duration = 4 min 55 sec (295)
      artist = Ella Fitzgerald and Louis Armstrong
       album = Porgy & Bess
       track = 13
       genre = Vocal Jazz
        date = 1958
    composer =
   performer =
        disc =
  Date Added = 2021-04-23 19:27:56
Last Updated = 2021-04-23 19:27:56
```

The <b>notify-send</b> service is implemented by the <u>notify-send</u> shell script in the aux-scripts directory. The supervise run file for <b>notify-send</b> service is as below. You need to replace <u>mbhangui</u> with your login name in the supervise run file.

```
#!/bin/sh
#
# This requires yad to be installed.
# Look at $home/bin/notify-screen
#
user=mbhangui
exec 2>&1
mkdir -p /run/notify-screen
home=$(getent passwd $user | awk -F: '{print $6}')
if [ ! -f $home/.config/cantata/MPD_HOST ] ; then
  echo "MPD_HOST not defined" 1>&2
  sleep 30
  exit 1
fi
chown $user /run/notify-screen
if [ -d /run/svscan/scrobble-button/supervise ] ; then
  chown -R $user /run/svscan/scrobble-button/supervise
elif [ -d /svscan/scrobble-button/supervise ] ; then
  chown -R $user /svscan/scrobble-button/supervise
fi
if [ -d /run/svscan/notify-screen/supervise ] ; then
  chown -R $user /run/svscan/notify-screen/supervise
elif [ -d /svscan/notify-screen/supervise ] ; then
  chown -R $user /svscan/notify-screen/supervise
fi
/usr/bin/setuidgid -s $user /usr/bin/envdir variables xhost +
exec /usr/bin/setuidgid -s $user /usr/bin/envdir variables $home/bin/notify-screen
```

If you install the daemontools, ucspi-tcp package from [open build service](https://software.opensuse.org//download.html?project=home%3Ambhangui%3Araspi&package=cantata) using dnf, yum, apt, etc you just need to execute <u>create_service</u> script in the <u>aux-scripts</u> directory.

NOTE:
1. install mpc, sqlite3, imagemagick, yad, xmllint, mpdev, daemontools
2. update /etc/ImageMagick-6/policy.xml the following line to have read|write
    ```
    <policy domain="path" rights="read|write" pattern="@*"/>
    ```
