#!/bin/bash

working_dir=${PWD} 

echo "Tarkite: 'labas' arba 'kaip pradėti deklaracijos pildymą portale' $working_dir"

pocketsphinx_continuous -hmm ../../../liepa_akustinis_modelis/bendrinis/ \
    -lm ${working_dir}/lm/liepa_laisvas_bandomasis.lm.DMP \
    -dict dict/liepa_laisvas_bandomasis.dic \
    -inmic yes 2> /dev/null


