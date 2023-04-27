## Overview

This plugin was developed to be the default plugin for GailBot and uses
a layered and BST approach to internally represent the data.

Version: 0.0.0a

Developers:
1. Annika Tanner | Tufts University | Spring 2022
2. Muyin Yao | Tufts University | Spring 2022
3. Muhammad Umair | Tufts University

Developed at: Human Interaction Lab at Tufts


## Layer00
Layer00 is responsible for the construction and implementation of the data structures used in GailBot. It contains plugins that receive an utterance dictionary to build a balanced binary search tree for the words in the transcript(indexed by their start time) and create three dictionaries to store information on hierarchical language levels: the word-level, speaker-level and conversation-level.

## Layer00 : WordTreePlugin
From a dictionary representing the utterance map, constructs a binary search tree of nodes, with each representing an object of the Word class. Each Word contains its start time, end time, speaker label and text  in the transcript. The nodes are sorted by their start time in the conversation. The WordTreePlugin class also contains helper functions to handle the logic of inserting into the tree, generating the speaker label, and generating the binary search tree from a list of utterances.

Algorithm for generating the binary search tree from an inputted utterance map:
- First check if the utterance map is empty. If it is, create a binary search tree with a sole empty root node.
- If the utterance map is not empty, iterate over its items. For each item, generate the speaker label and inspect the utterances in the current item of the utterance map. For each sub-utterance, generate the start and end time labels.
- Insert the node representing the current utterance into the binary search tree.
- Return the root of the binary search tree. 

## Layer00 : ConversationMapPlugin
Creates and returns a dictionary for transcription analysis, where the keys are strings corresponding with the different aspects of the conversation transcription and analysis facilitated by the HiLab plugin suite (e.g. "wordLevel", "uttLevel", etc.). These keys are kept consistent across each step in the transcription and analysis process. Each key maps to dictionary, which also maps strings to dictionaries; the dictionaries being mapped to by the ConversationMapPlugin are then used during the analysis process. ConversationMapPlugin is a superclass of the Plugin class and inherits all of its logic and functionality. It also provides the additional functionality of working with a specific dependency output directory and methods.

## Layer00 : ConversationModel
The ConversationModel class serves as an abstraction from the underlying data structures containing the logic for the conversation model plugin. The ConversationModel class contains the map_iterator class, which handles the logic for iterating over and accessing information from an utterance map. The ConversationModel also contains the tree_iterator class, which handles iterations over the binary search tree, and also contains helper functions for the tree itself. The tree iterator is used to wrap the helper functions that handle insertions into the tree, searching for a node in the tree, deletions from the tree, and accessing information such as the conversation dictionary from the tree. Also contained in the ConversationModel class are helper functions for the utterance map, such as handling format changes for an existing utterance map object, accessing the utterance map contained in an instance of the ConversationModel class, accessing words or utterances from the utterance map, and inserting into or updating the utterance map.

## Layer00 : ConversationModelPlugin
Initializes, populates and returns an instance of the ConversationModelPlugin class, which contains the binary search tree, based on the WordTreePlugin, and three conversation maps. The maps store the dependency maps for the utterance map, the speaker map, and the conversation map, respectively. The application of a ConversationModelPlugin object should be given the initial dependency map as an argument, from which the word tree will be separated and stored as the binary search tree.

## Layer00 : SpeakerMapPlugin
Creates a dictionary for the speaker-level analysis of the transcription, where the key is the speaker and the value is a list of utterances from that speaker.

Algorithm for the generation of the speaker map:
- Iterates through the inputted utterance dictionary
- For each speaker label, add to the corresponding value dictionary for that speaker in the cumulative dictionary.
- If that speaker has not been seen yet, create the dictionary for them and add the current utterance to it.
- Return the dictionary.

## Layer00 : UtteranceMapPlugin
Creates a dictionary for the utterance-level analysis of transcription, which maps speaker IDs to lists of utterances by that speaker. 

## Layer01
Layer01 is responsible for identifying paralinguistic features of talk. It
contains plugins that create markers within the utterances, such as overlaps,
gaps and pauses for conversational analytics.

When marker nodes are inserted into the BST, marker node text follow certain
format:
node.text = "(markerType SEPARATOR information SEPARATOR speaker)"
When generating the output files, format plugins parse the marker text and
substitute user-specified marker format for the marker text.

## Layer01 : gaps
Inserts new nodes into the binary search tree, which represents gaps.
The new node insertion is determined by a certain floor transfer offset (FTO)
threshold that is calculated between utterance pairs. If the threshold is met,
insert the gap node into the tree.

Algorithm: 
 If the time between the next utterance start time and the previous utterance end time is greater than (GAPS_LB = 0.3) seconds , a node with GAPs marker will be inserted to the tree. The marker will include a string that states the marker represent gaps in utterance, and the duration of the gap
    
## Layer01 : overlaps
Inserts new nodes into the binary search tree, which represents overlaps.
If there is an overlap between an utterance pair, retrieve the four overlap
positions for the marker insertions. For every overlap, four markers are
inserted into the tree.


Algorithm:
 If the start time of the next utterance is smaller than the end time of the current utterance, four overlap nodes will be inserted to the tree. The four labels marks 1. starts of the fist overlap, 2. end of the first overlap 3. start of the second overlap 4. end of the second overlap
## Layer01 : pauses
Inserts new nodes into the binary search tree, which represents pauses.
The new node insertion is determined by a certain floor transfer offset (FTO)
threshold that is calculated between utterance pairs. The utterance pair
must be by the same speaker. If the threshold is met, insert the gap node
into the tree.

Algorithm:
Insert new node to tree when the start time of next utterance and end time of the previous utterance is larger than the pause threshold, insert a gap node to the tree


## Layer01 : syllRate
Calculates the syllable rates for each utterance and adds it as an entry into
to the utterance-level dictionary. Statistics for the conversation as a whole
are also calculated, including the median, MAD, fast speech counts and
slow speech counts; these statistics are added into a dictionary, which
is then added as an entry into the conversation-level dictionary.


## Layer01 : thresholds
Contains the initialization of certain threshold values, which are
used in layer01 plugins such as pauses.

## Layer02
Layer02 is responsible for formatting the finalized transcription outputs from
Layer01. It contains plugins that can display the information as a chat file,
CSV file, XML file and has plugins that can perform file format conversions
such as XML to CSV.

If the user would like to modify the formatting of the plugin output
by changing the marker text, it will simply be: changing the output format
in the markerdefs.py file

## Layer02 : chat
Prints the entire tree in a user-specified chat format.

## Layer02 : csvPlugin
Prints the entire tree on the utterance-level in a user-specified
CSV format.

## Layer02 : csvWordLevel
Prints the entire tree on the word-level in a user-specified CSV format.

## Layer02 : plainPrint

## Layer02 : txt

## Layer02 : xmlPlugin

## Layer02 : xmlSchema
Prints the entire tree on the word-level in a user-specified XML format.
This XML format is compatible with TalkBank's Chatter program and follows
the TalkBank CHAT specifications. Hence, CHAT-XML conversions are made
possible.

## Overall Architecture
The overall architecture for GailBot is the convModel, a wrapper object that
contains the balanced binary search tree and three dictionaries. It contains
helper methods that interact with the underlying data structures in GailBot.

