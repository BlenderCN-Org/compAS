import os
import fileinput

for path, dirs, files in os.walk('build/html'):
    for f in files:
        basename, ext = os.path.splitext(f)
        print basename, ext
        if ext == '.html':
            filepath = os.path.join(path, f)
            fp = fileinput.FileInput(filepath, inplace=True, backup='.bak')
            for line in fp:
                print line.replace('\\*', '*')
