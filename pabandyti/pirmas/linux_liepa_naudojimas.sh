#!/bin/bash

echo "Tarkite: 'sukurk naują dokumentą' arba 'parodyk kalendorių'"

pocketsphinx_continuous -hmm ../../sphinx/hmm/liepa_akustinis_modelis/ \
    -jsgf ../../sphinx/gram/liepa_gramatika.gram \
    -dict ../../sphinx/dict/liepa_zodynas.dic \
    -inmic yes 2> /dev/null


