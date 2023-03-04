import random
import string

def flip_dna(sequence):
    nucleotides = list(sequence)
    index = random.randint(0, len(nucleotides)-1)
    if nucleotides[index] == 'c':
        nucleotides[index] = 'g'
    elif nucleotides[index] == 'g':
        nucleotides[index] = 'c'
    elif nucleotides[index] == 'a':
        nucleotides[index] = 't'
    elif nucleotides[index] == 't':
        nucleotides[index] = 'a'
    return ''.join(nucleotides)

def find_position(fasta_file, reads_array):
    # Read the fasta file into a single string
    with open(fasta_file, 'r') as f:
        fasta_string = ''
        for line in f:
            if not line.startswith('>'):
                fasta_string += line.strip()

    # Find the position of the string in the fasta string
    
    for i,r in enumerate(reads_array):
        if i % 1000 == 0:
            print(i)
	
        if fasta_string.find(r.read) != -1:
            r.perfect = True
        else:
            r.perfect = False


def gen_reads(num_reads, fasta_file, perfect = False):
    # Read the fasta file into a single string
    with open(fasta_file, 'r') as f:
        fasta_string = ''
        for line in f:
            if not line.startswith('>'):
                fasta_string += line.strip()

    # Find the position of the string in the fasta string
    reads = []
    if perfect:
        for i in range(num_reads):
            index = random.randint(0,len(fasta_string) - 700)
            reads.append(Read(header = None, read = fasta_string[index: index + 150], quality = None, perfect = True))
    else:
        for i in range(num_reads):
            index = random.randint(0,len(fasta_string) - 700)
            reads.append(Read(header = None, read = flip_dna(fasta_string[index: index + 150]), quality = None, perfect = False))

    return reads
            

class Read:
    def __init__(self, read, header = None, quality = None, perfect = False):
        if (header == None):
            self.header = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        else:
            self.header = header

        self.read = read
        if quality == None:
            self.quality = "I" * len(read)
        else:
            self.quality = quality
        
        self.perfect = perfect
    
    def __str__(self):
        return self.header + "\n" + self.read + "\n" + "+\n" + self.quality + "\n"

def parse_fastq(fastq_file):
    reads = []
    with open(fastq_file, 'r') as f:
        while True:
            header = f.readline().rstrip()
            if not header:
                break
            read = f.readline().rstrip()
            _ = f.readline().rstrip()
            quality = f.readline().rstrip()
            reads.append(Read(header, read, quality))
    return reads
# Example usage

fasta_file = 'chr21_pros.fa'
r1 = gen_reads(1000000, fasta_file, perfect = False)
r2 = gen_reads(1000000, fasta_file, perfect = True)
r = r1 + r2

num_reads = 100000
split = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

for num_reads in [10000, 100000, 1000000]:
    for sp in split:
        num_perfect = sp * num_reads
        with open(f"matches_{num_reads}_{sp}.fastq","w") as f:
            count = 0
            while count < num_perfect:
                for re in r:
                    if re.perfect:
                        f.write(str(re))
                        count += 1
                    if count >= num_perfect:
                        break
            
            count = 0
            while count < (num_reads - num_perfect):
                for re in r:
                    if not re.perfect:
                        f.write(str(re))
                        count += 1
                    
                    if count >= (num_reads - num_perfect):
                        break
        




