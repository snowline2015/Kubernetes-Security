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
    



# class Service:
#     def __init__(self, data: dict = {}):
#         self.RAW = data
#         self.NAME = data.get('metadata', {}).get('name', '')
#         self.NAMESPACE = data.get('metadata', {}).get('namespace', '')
#         self.TYPE = data.get('spec', {}).get('type', '')
#         self.PORTS = data.get('spec', {}).get('ports', [])
#         self.CLUSTER_IP = data.get('spec', {}).get('clusterIP', '')
#         self.EXTERNAL_IP = data.get('spec', {}).get('externalIPs', [])
#         self.LOAD_BALANCER_IP = data.get('status', {}).get('loadBalancer', {}).get('ingress', [{}])[0].get('ip', '')
#         self.LOAD_BALANCER_HOSTNAME = data.get('status', {}).get('loadBalancer', {}).get('ingress', [{}])[0].get('hostname', '')
#         self.STATUS = data.get('status', {}).get('phase', '')


#     def attributes(self):
#         return {'name': self.NAME, 'namespace': self.NAMESPACE, 'type': self.TYPE, 'ports': self.PORTS, 'cluster_ip': self.CLUSTER_IP, 'external_ip': self.EXTERNAL_IP, 'load_balancer_ip': self.LOAD_BALANCER_IP, 'load_balancer_hostname': self.LOAD_BALANCER_HOSTNAME, 'status': self.STATUS}