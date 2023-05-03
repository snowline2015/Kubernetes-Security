class Pod:
    def __init__(self, data: dict = {}):
        self.RAW = data
        self.NAME = data.get('metadata', {}).get('name', '')
        self.NAMESPACE = data.get('metadata', {}).get('namespace', '')
        self.KIND = data.get('metadata', {}).get('ownerReferences', [{}])[0].get('kind', '')
        self.IMAGE = data.get('status', {}).get('containerStatuses', [{}])[0].get('image', '')
        self.IMAGE_ID = data.get('status', {}).get('containerStatuses', [{}])[0].get('imageID', '')
        self.IP = data.get('status', {}).get('podIP', '')
        self.HOST_IP = data.get('status', {}).get('hostIP', '')
        self.STATUS = data.get('status', {}).get('phase', '')


    def attributes(self):
        return {'name': self.NAME, 'namespace': self.NAMESPACE, 'kind': self.KIND, 'image': self.IMAGE, 'image_id': self.IMAGE_ID, 'ip': self.IP, 'host_ip': self.HOST_IP, 'status': self.STATUS}