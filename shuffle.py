import random

def shuffle_fastq(fastq_file):
    with open(fastq_file, 'r') as f:
        reads = []
        while True:
            header = f.readline().rstrip()
            if not header:
                break
            read = f.readline().rstrip()
            plus = f.readline().rstrip()
            quality = f.readline().rstrip()
            reads.append((header, read, plus, quality))
    
    random.shuffle(reads)

    shuffled_fastq = fastq_file.replace('.fastq', '_shuffled.fastq')
    with open(shuffled_fastq, 'w') as f:
        for header, read, plus, quality in reads:
            f.write(header + '\n' + read + '\n' + plus + '\n' + quality + '\n')

import sys
fastq_file = sys.argv[1]
shuffle_fastq(fastq_file)
