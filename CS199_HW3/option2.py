#!/usr/bin/env python3

import sys
import os


def parse_contigs(file_path: str) -> None:
	fo = None
	try:
		#opens the file, establishes the pointer position, and gets the total size of the file
		fo = open(file_path, 'r')
		header_info = []
		size = os.path.getsize(file_path)
		pos = fo.tell()

		#iterates through the file and saves the pointer position after each header line and the length of the header line
		#also saves a list of the header lines to display later
		header_titles = []
		while pos < size:
			l = fo.readline()
			pos = fo.tell()
			if l[0] == '>':
				header_info.append([pos, len(l)])
				header_titles.append(l)

		#calculates the pointer position for the start of each of the headers and adds the final pointer position to a list
		header_starts = []
		for header in range(len(header_info)):
			header_starts.append(header_info[header][0] - header_info[header][1])
		header_starts.append(size)

		#displays an enumerated list of all the contig headers and then continues to ask the user to choose a contig to parse until
		#the answer 'None' or 'none' is given
		desired_contig = 0
		for l in enumerate(header_titles):
			print(str(l[0]) + '\t' + l[1][:-1])
		print(' ')
		while desired_contig != 'None':
			desired_contig = input('There are ' + str(len(header_starts) - 1) + ' contigs in the file.\nInput a contig number or None to stop: ')
			print(' ')
			if desired_contig.lower() == 'none':
				break
			fo.seek(header_starts[int(desired_contig)], os.SEEK_SET)
			pos = fo.tell()
			nf_header = fo.readline()[1:-1]
			nf_name = ''.join(i for i in nf_header if i.isalnum())
			nf = open(nf_name + '.fasta', 'w')
			fo.seek(header_starts[int(desired_contig)], os.SEEK_SET)
			while pos < header_starts[int(desired_contig) + 1]:
				nf.write(fo.readline())
				pos = fo.tell()
			nf.close()

	finally:
		if fo != None:
			fo.close()

if __name__ == '__main__':
	parse_contigs(sys.argv[1])
