# custom songs

## new song format

we have a new song format, and instead of using `<song>.mid` and `<song>-mainlines.mid` files, we utilize a zip format with a metadata.json file describing the song. this is for adding complexity in the future such as custom maps or background images. if you want to port over your `.mid` files to `.zip` files for compatibility, see below

## tutorial

each `.zip` file in the `songs` directory represents a map, and each `.zip` file has a few main components.

if you are not sure how to create or extract zip files, you should learn how to do that before porting your `.mid` files. i'm not willing to explain here, but there are probably plenty of tutorials online, or chatgpt could help you create and extract `.zip` files

notably, the file structure inside the zip should look something like this:
```
<song-name>.zip
├── metadata.json
├── <song-name>.mid
└── <song-name>-mainlines.mid
```

alternatively, the `<song-name>.mid` file could be replaced with an `<song-name>.mp3`, but beware that the `metadata.json` file will need to change to

the `metadata.json` file is in the "JSON" format. if you don't know what that is, you may want to ask chatgpt, google, and do some research to have a basic understanding, though it is not necessary for this tutorial

it may look something like this example:

```json
{
  "name": "Bad Piggies Theme Song",
  "author": "Rovio",
  "mapper": "quasar098",
  "song_file": "bad-piggies-mainlines.mid",
  "audio_file": "bad-piggies.mid",
  "version": 1
}
```

the above example is extracted for the `bad-piggies.zip`

before we examine what is the purpose of each part, i will warn you that future versions of the metadata.json file and their key-value pairs are subject to change at any time. i will eventually make a list of different versions and their supported key/value pairs.

anyways, here is the purpose of each key/value pair for version 1:

- `name`: name of the `audio_file` song
- `author`: author of the `audio_file` song
- `mapper`: the person who bundled the files into a `.zip`, or made the map timings
- `audio_file`: the file name of the file inside of the zip that is the song to play back. this can be an `.mp3`, `.mid`, or `.wav` (untested)
- `song_file`: the `.mid` file containing notes of whose timestamps will be correlated to the bounces generated (confused by that sentence? me too)
- `version`: version of the `metadata.json` format to follow, and not the version of the song (e.g. if you make an edit, dont change the `version`)

sorry for making `audio_file` and `song_file` so confusing because they sound like the same thing. in future format versions i may change the `song_file` to `map_file` for clarity.

if you are really still confused, just unzip of the of the zip files and copy paste and change around some stuff until it works

below are the keys for the `metadata.json` and the versions they work in

| key          | purpose                     | earliest version supporting it | latest version supporting it | required? |
|--------------|-----------------------------|--------------------------------|------------------------------|-----------|
| name         | name of audio               | 1                              | N/A                          | yes       |
| author       | author of audio             | 1                              | N/A                          | yes       |
| mapper       | person who bundled zip file | 1                              | N/A                          | yes       |
| audio_file   | file name of audio          | 1                              | N/A                          | yes       |
| song_file    | file name of midi           | 1                              | N/A                          | yes       |
| version      | version of metadata.json    | 1                              | N/A                          | yes       |
| music_offset | offset in ms of music start | 2                              | N/A                          | no        |

