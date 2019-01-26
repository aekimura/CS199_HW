#!/usr/bin/env python3

import sys
import os


def parse_contigs(file_path: str) -> None:
	fo = None
	try:
		#open the file, establish the pointer position, and get the total size of the file
		fo = open(file_path, 'r')
		header_info = []
		size = os.path.getsize(file_path)
		pos = fo.tell()

		#while the pointer is not at the end of the file loop through and save the position
		#of each of the headers and the length of the header line
		while pos < size:
			l = fo.readline()
			pos = fo.tell()
			if l[0] == '>':
				header_info.append([pos, len(l)])

		#calculate the position at the start of each header line and add the final position
		header_starts = []
		for header in range(len(header_info)):
			header_starts.append(header_info[header][0] - header_info[header][1])
		header_starts.append(size)

		#for each header move the cursor to the start of the header and write the contig
		#into a new file discarding any empty lines
		for header in range(len(header_starts[:-1])):
			fo.seek(header_starts[header], os.SEEK_SET)
			pos = fo.tell()
			nf_header = fo.readline()[1:-1]
			nf_name = ''.join(i for i in nf_header if i.isalnum())
			nf = open(nf_name + '.fasta', 'w')
			fo.seek(header_starts[header], os.SEEK_SET)
			while pos < header_starts[header + 1]:
				l = fo.readline()
				pos = fo.tell()
				if l != '\n':
					nf.write(l)
			nf.close()

	finally:
		if fo != None:
			fo.close()

if __name__ == '__main__':
	parse_contigs(sys.argv[1])
