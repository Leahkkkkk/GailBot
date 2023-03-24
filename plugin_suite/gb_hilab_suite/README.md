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
Layer00 is responsible for the construction and implementation
of the data structures used in GailBot. It contains plugins that receive
an utterance dictionary to build a balanced binary search tree for the words
(indexed by startTime) and create three dictionaries to store information on
hierarchical language levels: the word-level, speaker-level and conversation-
level.

## Layer00 : constructTree
Creates a binary search tree of nodes, which contains the start time,
end time, speaker label and text of the word it represents. The nodes are
indexed by start time.

## Layer00 : conversationDict
Creates and returns a dictionary for transcription analysis, where the keys
are strings (ex: word level, utterance level, speaker level and conversation
level) and the values are dictionaries that map strings to another dictionary.

## Layer00 : convModel
Contains the iterator class and helper functions for both the tree and the
maps. For example: insertions into the tree, deletions from the tree, checking
the existence of utterance pairs as well as more complex functions such as
building the utterance map with changes (since the user is given the flexibility
of changing the output format)

## Layer00 : convModelPlugin
Initializes, populates and returns an instance of convModel, which contains the
binary search tree and three maps for word-level, speaker-level and conversation
level analysis of the transcription.

## Layer00 : speakerDict
Creates a dictionary for the speaker-level analysis of transcription, where the
key is the speaker and the value is a list of utterances that all share the
same speaker label.

## Layer00 : treeComponents
Contains helper functions for the binary search tree, such as searching and
deleting nodes within the tree,

## Layer00 : utteranceDict
Creates a dictionary for the utterance-level analysis of transcription, which
maps speaker IDs to lists of utterances.

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

## Layer01 : overlaps
Inserts new nodes into the binary search tree, which represents overlaps.
If there is an overlap between an utterance pair, retrieve the four overlap
positions for the marker insertions. For every overlap, four markers are
inserted into the tree.

## Layer01 : pauses
Inserts new nodes into the binary search tree, which represents pauses.
The new node insertion is determined by a certain floor transfer offset (FTO)
threshold that is calculated between utterance pairs. The utterance pair
must be by the same speaker. If the threshold is met, insert the gap node
into the tree.

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

