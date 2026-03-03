# About this tool
This is a tool to build a deck of public objective images for Twilight Imperium 4th edition from a csv. Sample csv files are provided for secret, stage 1, stage 2, and stageless (both public and secret) objectives.

# Dependencies
This tool obviously requires python3, but in addition it requires the following python libraries:

* Pillow
* pandas
* numpy

To install these, use the following commands:

`pip install pillow`

`pip install pandas`

`pip install numpy`

# Using this tool
This tool runs from the commandline. A few sample commands are provided below:

`python .\deck_builder.py --objective-type=stage1`

`python .\deck_builder.py --objective-type=stage2`

`python .\deck_builder.py --objective-type=secret`

`python .\deck_builder.py --objective-type=stageless`

`python .\deck_builder.py --objective-type=stageless-secret`


There are a handful of arguments that may be usefule to know:

* Including --tts-mode will make the deck generated at the end limited to being 10 columns wide as that is the tts deck limit.

* If using an input .csv file whose filename or location is not matching the default location, using --input-file=../location/filename.csv is a way to use that file.

Here are some examples:

`python .\deck_builder.py --objective-type=stage1 --tts-mode`

`python .\deck_builder.py --objective-type=secret --input-file=secret-deck-2.csv`
