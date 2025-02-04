#!/bin/bash

pycbc_brute_bank --output-file bank.hdf \
--minimal-match 0.85 --tolerance 0.05 --buffer-length 4 \
--full-resolution-buffer-length 1024 --sample-rate 2048 \
--tau0-threshold 0.5 --approximant 'teobresums' --tau0-crawl 5 \
--psd-file /home/spandan11/IUCAA/work_ecc/local_tests/aligo_O4high.txt \
--seed 150914 --tau0-start 39.5 --tau0-end 40.0 \
--input-config /home/spandan11/IUCAA/work_ecc/local_tests/bank.ini \
--checkpoint-file /home/spandan11/IUCAA/work_ecc/local_tests/bank_test13/checkpoint_input.hdf \
--low-frequency-cutoff 20 --max-signal-length 512 --verbose
