## label-snd
Easily label sound datasets!

## Motivation

At my [startup](https://ailabs.com.tr), we are running ML projects dealing with audio files. We need a simple yet effective sound-labelling utility and user interface. I wrote label-snd is just for this purpose, and I'm opensourcing it for use by others.

## How to use
 * From the `File` menu, click `Select audio folder...` and choose a directory containing `.wav` files. `label-snd` will automatically find all the `.wav` files to add into the list, starting to play the first one.
 * From the `File` menu, click `Populate choices from...` and choose a `.txt` file which contains the choices to be added to the combo box for auto completion. Choices should be separated with a newline character. Choices might be the sentences you would expect to hear in the sound files, or they might be categories that you want to apply your sound with.
 * When a sound file is playing, simply start typing in the combo box, select a choice from the filtered results or continue typing if it is not present. When your annotation is done, press ÈNTER` to continue labelling the next sound in the list.
 * As you annotate sound and press `ENTER`, it will save them in an ljspeech-like `metadata.csv` file in the folder you chose in the first step. Then it will move to the next item and start playing it. You can also simply choose an item in the list with your mouse or keyboard to start playing and annotate.

## Dependencies
The only dependency you need to install is `wxpython`. I specifically avoided using `tkinter` because it's not accessible to screen readers.

`pip install wxpython`

## Limitations
I tested this utility on Windows, and I expect it to run on Mac, as well. However, I haven't tested it on any Linux distribution. Please file an issue if you can test it on Linux.

## Roadmap
 * [x] Release the first opensource version.
 * [x] Populate choices from a chosen `.txt` file.
 * [ ] Implement a pause/resume functionality.
 * [ ] Make a `Settings` screen to customize certain behavior such as metadata file format, its location and the number of loops when playing a sound.
 * [ ] Write an automatic text normalization algorithm for English and Turkish, and add a choce to activate or deactivate this in the settings screen.
 * [ ] Write a tutorial or produce a video for several use cases.
## License
GPL