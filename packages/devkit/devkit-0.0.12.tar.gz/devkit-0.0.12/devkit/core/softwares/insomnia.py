import subprocess
from devkit.core.softwares.software import Software

class Insomnia(Software):
    name = "Insomnia"
    apt_package = "insomnia"
    check = "insomnia --version"
    sources = {
        "/etc/apt/sources.list.d/insomnia.list": "https://dl.bintray.com/getinsomnia/Insomnia /"
    }
    gpg_key = "https://insomnia.rest/keys/debian-public.key.asc"
