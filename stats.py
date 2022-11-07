import os
import sys
import re

walk_dir = sys.argv[1]

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

stats_file_path = os.path.join(walk_dir, 'stats.txt')
print('stats_file_path: ' + stats_file_path)

with open(stats_file_path, 'w') as stats_file:
    for root, subdirs, files in os.walk(walk_dir):
        if not 'out' in root:
            continue
        print(f"root: {root}, subdirs: {subdirs}")

        for filename in files:
            if not filename.endswith('.txt'):
                continue

            file_path = os.path.join(root, filename)

            print('\t- processing file %s (full path: %s)' % (filename, file_path))

            with open(file_path, 'rb') as f:
                
                # read last 3 lines from file
                lines = f.readlines()
                last_lines = lines[-2:]
                # print (last_lines)

                #write filename, stats and then 2 newlines
                stats_file.write(('Stats for %s:\n' % filename))
                for line in last_lines:
                    # line.replace('\x08', '')
                    line = re.sub(r'\x08', '', line.decode('utf-8'))
                    if line.startswith('500') or line.startswith('333'):
                        stats_file.write((str(line.rstrip()) + '\n'))
                print('\n', file=stats_file)