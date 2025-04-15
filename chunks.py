import os
import tempfile
import heapq
from names_dataset import NameDataset
CHUNK_SIZE = 100_000
def create_sorted_chunks():
    chunk_files = []
    nd = NameDataset()
    all_names = list(nd.first_names.keys())
    names = []
    for name in all_names:
        names.append(name.strip())
        if len(names) == CHUNK_SIZE:
            names.sort()
            chunk_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
            chunk_file.write('\n'.join(names))
            chunk_file.close()
            chunk_files.append(chunk_file.name)
            names = []
    if names:
        names.sort()
        chunk_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        chunk_file.write('\n'.join(names))
        chunk_file.close()
        chunk_files.append(chunk_file.name)
    return chunk_files
def merge_sorted_chunks(chunk_files, output_file):
    open_files = [open(f, 'r', encoding='utf-8') for f in chunk_files]
    output = open(output_file, 'w', encoding='utf-8')
    sorted_iter = heapq.merge(*(map(str.strip, f) for f in open_files))
    for line in sorted_iter:
        output.write(line + '\n')
    output.close()
    for f in open_files:
        f.close()
        os.remove(f.name)
if __name__ == "__main__":
    output_file = 'sorted_names.txt'
    chunks = create_sorted_chunks()
    merge_sorted_chunks(chunks, output_file)
    print(" Sorting completed Output file:", output_file)