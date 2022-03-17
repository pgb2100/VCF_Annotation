[![Python](https://img.shields.io/badge/python-3.9.7-brightgreen?style=plastic&logo=python)](https://www.python.org/)
[![VCF](https://img.shields.io/badge/VCF-v4.1-brightgreen)]
[![Human Reference](https://img.shields.io/badge/Human%20Reference-GRCh37-blue)]
[![nsembl RestAPI Release](https://img.shields.io/badge/Ensembl--RestAPI%20Release-105-blue)](https://github.com/Ensembl/ensembl-rest#ensembl-rest)
# VCF_Annotation

## Introduction
The VCF annotation tool is used to make additional annotations from basic VCF.

## How to use it
This tool use only basic module on Python3.(requests, sys, re, json)

### Run commend
```
./Anno.py [input_vcf] [output_vcf]
ex) python anno.py clean_challenge.vcf clean_challenge_anno.vcf
```

###Aditional Annotation columns
1. Type: variant types, such as substitution, deletion, duplication, insertion, inversion, deletion-insertion, complex, other
2. Depth: Depth of sequence coverage at the site of variation
3. Percentage_ALT: Percentage of reads supporting the variant
4. Gene_ID: Use the variant gene_id annotation from ensembl (Ensembl Release 105)https://rest.ensembl.org/?content-type=text/html 
            It separate by comma for multiplue gene_ids.
6. Transcript_ID: Use the variant transcript_id annotation service from ensembl (Ensembl Release 105)https://rest.ensembl.org/?content-type=text/html
                  It separate by comma for multiplue transcript_ids.
