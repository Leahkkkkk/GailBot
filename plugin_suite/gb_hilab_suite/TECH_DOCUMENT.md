## OverView 
This plugin suite was developed to be used with GailBot. 
The plugin suite takes in a GBPluginMethod as input, which provides utterance
 data from transcription. The plugin suite include individual plugin to 
 add speech marker into the transcript, and finally output the analyzed 
 result into different formats. 

### input
This plugin takes in a GBPluginMethod object, which is expected to have the 
following interface: 

1. filenames: List[str] , a list of file names of the audio files transcribed. 
2. audios: Dict[str, str], a dictionary mapping the audio file name to the 
   audio file path
3. utterances: Dict[str, List[UttDict]]: a dictionary mapping the audio file 
   name to the list of utterance data from the file's transcription. 
    The utterance data dictionary has the following schema 
    {speaker: str, start: float, end: float, text}
4. temp_work_path: str, provides the path to the temporary work space 
   for plugin suite
5. out_path: str, provides the path to the output of the plugin suite result
6. get_utterance_objects(): Dict[str, List[UttObj]]: a function that convert
    the raw utterance data to utterance object. Return a dictionary mapping 
    the audio file name to the list of utterance objects from the file's 
    transcription. The each utterance objects contains the attributes: speaker, 
    start, end, text.
7. save_item(): a convenience function provided by GBPluginMethod to save file. 

### output 
The output of plugin suite will be files that contains both the original 
transcription data and the marker of the transcription added through the analysis 

### main architecture 
The plugin suite contains mainly three layers 
1. Layer00 core: receive utterance data and build a binary search tree based 
   on the start and end time of each utterance. Each utterance will become a 
   node in the tree 
2. Layer01 analysis: analyze the utterance data, implement algorithm to detect 
   gapes, pauses, overlaps, fast and slow speech from the utterance's start and 
   end time. Once each speech feature is detected, insert a marker node to the 
   tree built in layer01
3. Layer02 format: given the tree from Layer00 supplemented by the marker 
   inserted from layer01. output the data to txt, cha, xml, and csv format. 
   each format will replace the internal marker inserted from Layer01 with 
   a different marker based on the format and specification of the file format.

## Layer00 
### Layer00: overview
Layer00 is responsible for the construction and implementation of the data 
structures used in GailBot. It contains plugins that receive an utterance 
dictionary to build a balanced binary search tree for the words in the 
transcript(indexed by their start time) and create three dictionaries to store 
information on hierarchical language levels: the word-level, speaker-level and 
conversation-level.

## Layer00 : WordTreePlugin
From a dictionary representing the utterance map, constructs a binary search 
tree of nodes, with each representing an object of the Word class. Each Word 
contains its start time, end time, speaker label and text  in the transcript. 
The nodes are sorted by their start time in the conversation. The WordTreePlugin 
class also contains helper functions to handle the logic of inserting into the 
tree, generating the speaker label, and generating the binary search tree from 
a list of utterances.

Algorithm for generating the binary search tree from an inputted utterance map:
- First check if the utterance map is empty. If it is, create a binary search 
- tree with a sole empty root node.
- If the utterance map is not empty, iterate over its items. For each item,
-  generate the speaker label and inspect the utterances in the current item 
-  of the utterance map. For each sub-utterance, generate the start and end time labels.
- Insert the node representing the current utterance into the binary search tree.
- Return the root of the binary search tree. 

## Layer00 : ConversationMapPlugin
Creates and returns a dictionary for transcription analysis, where the keys are 
strings corresponding with the different aspects of the conversation transcription
 and analysis facilitated by the HiLab plugin suite (e.g. "wordLevel",
  "uttLevel", etc.). These keys are kept consistent across each step in the 
  transcription and analysis process. Each key maps to dictionary, which also 
  maps strings to dictionaries; the dictionaries being mapped to by the 
  ConversationMapPlugin are then used during the analysis process. 
  ConversationMapPlugin is a superclass of the Plugin class and inherits all 
  of its logic and functionality. It also provides the additional functionality 
  of working with a specific dependency output directory and methods.

## Layer00 : ConversationModel
The ConversationModel class serves as an abstraction from the underlying data 
structures containing the logic for the conversation model plugin. The 
ConversationModel class contains the map_iterator class, which handles the logic
 for iterating over and accessing information from an utterance map. The 
 ConversationModel also contains the tree_iterator class, which handles 
 iterations over the binary search tree, and also contains helper functions for 
 the tree itself. The tree iterator is used to wrap the helper functions that
  handle insertions into the tree, searching for a node in the tree, deletions 
  from the tree, and accessing information such as the conversation dictionary 
  from the tree. Also contained in the ConversationModel class are helper 
  functions for the utterance map, such as handling format changes for an 
  existing utterance map object, accessing the utterance map contained in an 
  instance of the ConversationModel class, accessing words or utterances from
 the utterance map, and inserting into or updating the utterance map.

## Layer00 : ConversationModelPlugin
Initializes, populates and returns an instance of the ConversationModelPlugin 
class, which contains the binary search tree, based on the WordTreePlugin, and 
three conversation maps. The maps store the dependency maps for the utterance map, 
the speaker map, and the conversation map, respectively. The application of a 
ConversationModelPlugin object should be given the initial dependency map as an 
argument, from which the word tree will be separated and stored as the binary 
search tree.

## Layer00 : SpeakerMapPlugin
Creates a dictionary for the speaker-level analysis of the transcription, where 
the key is the speaker and the value is a list of utterances from that speaker.

Algorithm for the generation of the speaker map:
- Iterates through the inputted utterance dictionary
- For each speaker label, add to the corresponding value dictionary for that 
- speaker in the cumulative dictionary.
- If that speaker has not been seen yet, create the dictionary for them and 
- add the current utterance to it.
- Return the dictionary.

## Layer00 : UtteranceMapPlugin
Creates a dictionary for the utterance-level analysis of transcription, 
which maps speaker IDs to lists of utterances by that speaker. 

## Layer01
### Layer00: overview
Layer01 is responsible for identifying paralinguistic features of talk. It
contains plugins that create markers within the utterances, such as overlaps,
gaps and pauses for conversational analytics.

When marker nodes are inserted into the BST, marker node text follow certain
format:
node.text = "(markerType SEPARATOR information SEPARATOR speaker)"
When generating the output files, format plugins parse the marker text and
substitute user-specified marker format for the marker text.

## Layer01 : gaps
Plugin Purpose: for detecting gaps between utterances and insert the gap 
marker in the utterance tree. 
The gap is defined by silence longer than 0.3 
(identified as THRESHOLD.GABS_LB in code) second between two speakers. 

Algorithm:
1. Iterate through the list of utterance through data an iterator object 
   provided by conversation model, retrieve the utterance pair
2. Check the FTO of the utterance pair. If the fto is longer than 0.3 second,
   and it is between two difference speakers. Insert a gap marker into the 
   utterance tree. Else do nothing 

## Layer01 : overlaps
Plugin Purpose: for detecting overlaps in speech between two speakers. 
Inserts new nodes into the binary search tree, which represents overlaps.
If there is an overlap between an utterance pair, retrieve the four overlap
positions for the marker insertions. For every overlap, four markers are
inserted into the tree.


Algorithm:
 If the start time of the next utterance is smaller than the end time of the 
 current utterance, four overlap nodes will be inserted to the tree. The four 
 labels marks:
  1. starts of the fist overlap, 
  2. end of the first overlap 
  3. start of the second overlap 
  4. end of the second overlap
   
## Layer01 : pauses
Purpose: for detecting pauses.
Inserts new nodes into the binary search tree, which represents pauses.
The new node insertion is determined by a certain floor transfer offset (FTO)
threshold that is calculated between utterance pairs. The utterance pair
must be by the same speaker. If the threshold is met, insert the gap node
into the tree.

Algorithm:
1. Iterate through the list of utterance through data an iterator object 
   provided by conversation model, retrieve the utterance pair
2.  Insert new node to tree when the start time of next utterance and end time of 
    the previous utterance is larger than the pause threshold, and the pauses are
    from the same speakers


## Layer01 : syllRate
Purpose: For detecting the fast and slow speech. Insert node with marker of 
        the start and end of fast and slow speech to the utterance tree.


Algorithm:
1. get the utterance data from the conversation model 
2. Calculates the syllable rates for each utterance and adds it as an entry into
to the utterance-level dictionary. Statistics for the conversation as a whole
are also calculated, including the median, MAD, fast speech counts and
slow speech counts; these statistics are added into a dictionary, which
is then added as an entry into the conversation-level dictionary.
3. Compare the stats of syllable rate for each utterances with the stats for the
   whole utterance to detect fast and slow speech. It the syllable rate 
   (stored as utt_dict["syllRate"] ) of the single utterance is smaller
   than the upper limit of the (stored as statsDic['upperLimit'] ) whole 
   utterance, insert makers for fast speech. It the syllable rate 
   (stored as utt_dict["syllRate"] ) of the single utterance is lager
   than the lower limit of the (stored as statsDic['lowerLimit'] ) whole
   utterance, insert makers for slow speech.  

## Layer02
## Layer02 : overview
Layer02 is responsible for formatting the finalized transcription outputs from
Layer01. It contains plugins that can display the information as a chat file,
CSV file, XML file and has plugins that can perform file format conversions
such as XML to CSV.

## Layer02 : csv
Prints the entire tree on the utterance-level in a user-specified
CSV format. Produce word-level and utterance-level csv file
Replace the internal marker in the original tree with the CSV marker stored 
in configData.toml LABEL.CSV field 

## Layer02 : chat
Prints the entire tree on the utterance-level in .chat format
Replace the internal marker in the original tree with the CHAT marker stored 
in configData.toml LABEL.CHAT field 

## Layer02 : text
Prints the entire tree on the utterance-level in .txt format
Replace the internal marker in the original tree with the TXT marker stored 
in configData.toml LABEL.TXT field 

## Layer02 : xml
Prints the entire tree on the utterance-level in .xml format
Produce native, and word-bank xml file
Replace the internal marker in the original tree with the XML marker stored 
in configData.toml LABEL.XML field 

## Configs Module
Include configuration data for plugin suite

## config.py 
Include dataclasses for marker, threshold, output file name, and Labels 

dataclass overview:
INTERNAL_MARKER: the marker used in analysis module, inserted to the 
initial utterance tree 
THRESHOLD: the threshold data used in analysis module to detect paralinguistic 
speech feature, the data content is read from "configData.toml" fil
LABEL: Label used in output file, which will replace the internal maker 
in format module 
ALL_LABELS: Currently used Label in plugin suite format module, the data 
            content will be read from "configData.toml" file 
PLUGIN_NAME: the name of each plugin 

## configData.toml
THRESHOLD: stores the threshold data 
LABEL: stores the label data for CSV, XML, CHAT, and TXT plugin in format 
       module


