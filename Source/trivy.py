import json
import subprocess


class Trivy:
    def __init__(self):
        self.RESULTS = []
        self.runner()

    def runner(self):
        res = subprocess.run('which trivy', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print('Trivy is not installed') if not res.stdout else print('Trivy is already installed')


    def scan(self, image: str):
        res = subprocess.run(f'trivy image -f json -q --insecure {image}',
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.stdout:
            self.RESULTS.append(Image(json.loads(res.stdout)))


class Image:
    def __init__(self, data: dict = {}):
        self.NAME = data.get('ArtifactName', '')
        self.METADATA = data.get('Metadata', {})
        self.FINDINGS = [Vulnerability(vuln) for vuln in data.get('Vulnerabilities', [])]


class Vulnerability:
    def __init__(self, data: dict = {}):
        self.CVE = data.get('VulnerabilityID', '')
        self.PACKAGE = data.get('PkgID', '')
        self.VERSION = data.get('InstalledVersion', '')
        self.LAYER = data.get('Layer', {})
        self.DATASOURCE = data.get('DataSource', '')
        self.TITLE = data.get('Title', '')
        self.DESCRIPTION = data.get('Description', '')
        self.SEVERITY = data.get('Severity', '')
        self.CWE = data.get('CweIDs', [])
        self.CVSS = data.get('CVSS', {})
        self.REFERENCES = data.get('References', [])
        self.PUBLISHED_DATE = data.get('PublishedDate', '')
        self.LAST_MODIFIED_DATE = data.get('LastModifiedDate', '')


if __name__ == '__main__':
    trivy = Trivy()
    trivy.scan('nginx:latest')




