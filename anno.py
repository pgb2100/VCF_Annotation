#!/usr/bin/env python
import requests, sys, re
import json

def help():
    print('')
    print('[USAGE] *.py [full_path_input_file(vcf)] [full_path_output_file(annotation_vcf)]')
    print('ex) python anno.py clean_challenge.vcf clean_challenge_anno.vcf')
    print('')
server = "http://grch37.rest.ensembl.org"


def vcf_anno(input, output):
    vcf_file =  input
    output_name = output
    outout_file = open(output_name,"w")
    with open(vcf_file) as f:
        vcf_lines = map(lambda z:z.strip(), f.readlines())
    for i in vcf_lines:
        if i.startswith("#CHROM"):
            outout_file.write(i + "\t" + "Type" + "\t" + "Depth" + "\t" + "Percentage_ALT" + "\t" + "Gene_ID" + "\t" + "Transcript_ID" + "\n")
        elif i.startswith("#"):
            outout_file.write(i + "\n")
        else:
            line_split = re.split(r'[\s:;]',i)
            v_type = re.sub(r'TYPE=','',line_split[12])
            depth = re.sub(r'DP=','',line_split[8])
            p_alt = ",".join(dp for dp in line_split[24].split(",")[1:])
            chr = line_split[0]
            pos = line_split[1]
            Alt = line_split[4]
            Gene_ID_List = []
            Transcript_ID_List = []
            ext = '/vep/human/region/%s:%s:%s/%s?'%(chr,pos,pos,Alt)
            if len(Alt.split(",")) > 1:
                for j in range(len(Alt.split(","))):
                    ext = '/vep/human/region/%s:%s:%s/%s?'%(chr,pos,pos,v_type.split(",")[j])
                    if v_type.split(",")[j] == "snp" or "complex":
                        ext = '/vep/human/region/%s:%s:%s/%s?'%(chr,pos,pos,Alt.split(",")[j])
                    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        pass
                    decoded = r.json()
                    for transcript in decoded[0]["transcript_consequences"]:
                        if transcript["gene_id"] not in Gene_ID_List:
                            Gene_ID_List.append(transcript["gene_id"])
                        if transcript["transcript_id"] not in Transcript_ID_List:
                            Transcript_ID_List.append(transcript["transcript_id"])
            else:
                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    pass
                decoded = r.json()
                for transcript in decoded[0]["transcript_consequences"]:
                    if transcript["gene_id"] not in Gene_ID_List:
                        Gene_ID_List.append(transcript["gene_id"])
                    if transcript["transcript_id"] not in Transcript_ID_List:
                        Transcript_ID_List.append(transcript["transcript_id"])
            
            Gene_ID = ",".join(GID for GID in Gene_ID_List)
            Transcript_ID = ",".join(TID for TID in Transcript_ID_List)


            annotation = i + "\t" + v_type + "\t" + depth + "\t" + str('{:07.5f}'.format(int(p_alt)/int(depth))) + "\t" + Gene_ID + "\t" + Transcript_ID + "\n"
            outout_file.write(annotation)
    outout_file.close()

def main():
    vcf_anno(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(help())
    main()
