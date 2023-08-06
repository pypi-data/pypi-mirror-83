import subprocess

class Software:
    name = None
    apt_package = None
    check = None
    sources = {}
    gpg_key = None

    def __init__(self):
        assert self.name is not None
        assert self.apt_package is not None
        assert self.check is not None
        assert type(self.sources) is dict

    def add_to_source(self, file, source_url):
        echo_pipe = subprocess.Popen(['echo', f'deb {source_url}'], stdout=subprocess.PIPE)
        subprocess.Popen(['tee', '-a', file], stdin=echo_pipe.stdout)

    def add_gpg_key(self, gpg_key):
        wget_pipe = subprocess.Popen(['wget', '-qO-', gpg_key], stdout=subprocess.PIPE)
        subprocess.Popen(['apt-key', 'add', '-'], stdin=wget_pipe.stdout)
        subprocess.call(['apt-get', 'update'])

    def apt_install(self):
        subprocess.call(['apt-get', 'install', '-y', self.apt_package])

    def is_installed(self):
        try:
            subprocess.call(self.check.split())
            return True
        except Exception as e:
            return False

    def install(self):
        for file, source_url in self.sources.items():
            self.add_to_source(file, source_url)

        if self.gpg_key is not None:
            self.add_gpg_key(self.gpg_key)

        self.apt_install()

        return self.is_installed()
