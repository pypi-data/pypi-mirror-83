import subprocess

class hostconfig:
    ubuntu_release = subprocess.Popen(['lsb_release', '-cs'], stdout=subprocess.PIPE).stdout.readline().decode('utf-8').strip()
