from cutadapt import seqio
import io

# files tests/data/simple.fast{q,a}
simple_fastq = [
	("first_sequence", "SEQUENCE1", ":6;;8<=:<"),
	("second_sequence", "SEQUENCE2", "83<??:(61")
	]

simple_fasta = [ (x[0], x[1], None) for x in simple_fastq ]


def test_fastareader():
	with seqio.FastaReader("tests/data/simple.fasta") as f:
		reads = list(f)
	assert reads == simple_fasta


def test_fastqreader():
	with seqio.FastqReader("tests/data/simple.fastq") as f:
		reads = list(f)
	assert reads == simple_fastq


def test_sequence_reader():
	# test the autodetection
	with seqio.SequenceReader("tests/data/simple.fastq") as f:
		reads = list(f)
	assert reads == simple_fastq

	with seqio.SequenceReader("tests/data/simple.fasta") as f:
		reads = list(f)
	assert reads == simple_fasta

	with open("tests/data/simple.fastq") as f:
		reads = list(seqio.SequenceReader(f))
	assert reads == simple_fastq

	# make the name attribute unavailable
	f = io.StringIO(open("tests/data/simple.fastq").read())
	reads = list(seqio.SequenceReader(f))
	assert reads == simple_fastq

	f = io.StringIO(open("tests/data/simple.fasta").read())
	reads = list(seqio.SequenceReader(f))
	assert reads == simple_fasta


def test_context_manager():
	filename = "tests/data/simple.fasta"
	with open(filename) as f:
		assert not f.closed
		reads = list(seqio.SequenceReader(f))
		assert not f.closed
	assert f.closed

	with seqio.FastaReader(filename) as sr:
		tmp_sr = sr
		assert not sr.fp.closed
		reads = list(sr)
		assert not sr.fp.closed
	assert tmp_sr.fp.closed