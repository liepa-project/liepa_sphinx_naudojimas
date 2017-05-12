#!/bin/bash

pocketsphinx_continuous -time yes -hmm ../../../liepa_akustinis_modelis/bendrinis/ \
    -jsgf lm/liepa_ieskotuvas.gram \
    -dict dict/liepa_ieskotuvas.dic \
    -infile ./wav/ieskotuvas.wav 2> /dev/null | ./py/sphinx_praat_transformer.py -
