# Spotify BBC Radio 6 Music List Transcriber

This is a simple script that makes the [BBC Radio 6 Music List](https://www.bbc.co.uk/programmes/p071zbkq) available as a playlist on Spotify as [Transcribed BBC Radio 6 Music List](https://open.spotify.com/playlist/2ylSWtDAF1bXjmv6IaPFfk?si=DpmhsturT4qbMUJb4ZW1bQ). The playlist used to be published there by BBC itself, but it stopped; also, the music list is not playable from the [BBC Radio 6 Music List play web page](https://www.bbc.co.uk/sounds/play/p07lc3pw) from all regions. That means that you have to manually play each song on Spotify, which is inconvenient.

The script does nothing special; it scrapes the contents of the playlist and uses the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) to do its job. If you are interested in details on how it works, read on. Note that you do not need to run the script yourself to create the playlist; it is now already [there](https://open.spotify.com/playlist/2ylSWtDAF1bXjmv6IaPFfk?si=DpmhsturT4qbMUJb4ZW1bQ)! What follows is only for documentation purposes.

## Create or Update

The script can both create the playlist from scratch and update it. List creation need only happen once, and you specify that by passing the `-c` command-line argument. When the playlist is created it is assigned a playlist ID by Spotify, which is shown on the terminal. You must enter this in the settings file (see below) to update it in the future.

## Authentication

To authenticate with Spotify the script uses a long-lived refresh token to get a new access token each time. You can get a refresh token by following the instructions at the [Web API Tutorial](https://developer.spotify.com/documentation/web-api/quick-start/). In particular, clone the [OAuth examples](https://github.com/spotify/web-api-auth-examples), then modify `app.js` of `authorization_code` to fill in `client_id`, `client_secret`, and `redirect_uri`. The scope of the application must be set to `playlist-modify-public`. Then you start the node.js application, log in to Spotify, and get the initial access token (which you will not need) and the long-lived refresh token.

## Settings

The script uses a file to store its settings; `settings_template.json` shows the structure of the file. By default the script expects to find `settings.json` in its directory, or a file given by the `-s` command-line parameter. You must fill in the Spotify username, client ID, and client secret. The client ID and the client secret are obtained from the application's details on [Spotify for Developers](https://developer.spotify.com/). The refresh token is the one we get through authentication, see above. The playlist ID is issued when the playlist is created (and you can also find it by clicking on list details in Spotify).
