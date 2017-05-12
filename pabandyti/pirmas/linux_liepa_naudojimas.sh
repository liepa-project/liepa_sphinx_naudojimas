#!/bin/bash

echo "Tarkite: 'sukurk naują dokumentą' arba 'parodyk kalendorių'"

pocketsphinx_continuous -hmm ../../../liepa_akustinis_modelis/bendrinis/ \
    -jsgf lm/liepa_gramatika.gram \
    -dict dict/liepa_zodynas.dic \
    -inmic yes 2> /dev/null


