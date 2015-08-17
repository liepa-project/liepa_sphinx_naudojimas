rem Switch to utf8
chcp 1250
rem Paskaitykite README.txt
rem Sphinx atpazino faile: wav\*.wav

C:\bin\pocketsphinx\bin\pocketsphinx_continuous ^
    -hmm sphinx\hmm\liepa-20_corpus8_0_mg13.cd_semi_750 ^
	-lm sphinx\lm\ieskotuvas3.lm.DMP -dict sphinx\dict\ieskotuvas3.dic ^
	-infile wav\ieskotuvas3.wav 2>sphinx\eout.txt

pause

