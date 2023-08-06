import subprocess
from devkit.hostconfig import hostconfig
from devkit.core.softwares.software import Software

class Docker(Software):
    name = "Docker"
    apt_package = "docker-ce docker-ce-cli containerd.io"
    check = "docker --version"

    dependencies = [
        "apt-transport-https",
        "ca-certificates",
        "curl",
        "gnupg-agent",
        "software-properties-common"
    ]
    sources = {
        "/etc/apt/sources.list.d/docker.list": f"deb [arch=amd64] https://download.docker.com/linux/ubuntu {hostconfig.ubuntu_release} stable"
    }
    gpg_key = "https://download.docker.com/linux/ubuntu/gpg"
