import os


class TreeHasher():
    """uses BlockHasher recursively on a directory tree"""

    def __init__(self, block_hasher):
        self.block_hasher=block_hasher

    def generate(self, start_path):
        """Use BlockHasher on every file in a tree, yielding the results

        note that it only checks the contents of actual files. It ignores metadata like permissions and mtimes.
        It also ignores empty directories, symlinks and special files.
        """

        cwd=os.getcwd()
        os.chdir(start_path)

        def walkerror(e):
            raise e

        try:
            for (dirpath, dirnames, filenames) in os.walk(".", onerror=walkerror):
                for f in filenames:
                    file_path=os.path.join(dirpath, f)[2:]

                    if (not os.path.islink(file_path)) and os.path.isfile(file_path):
                        for (chunk_nr, hash) in self.block_hasher.generate(file_path):
                            yield ( file_path, chunk_nr, hash )
        finally:
            os.chdir(cwd)

