import requests, json
from time import sleep
from base64 import b64decode, b64encode

class CVPSWITCH():
    def __init__(self,host,vx_ip,t_cnt=""):
        self.serial_num = ""
        self.fqdn = ""
        self.hostname = host
        self.ip = vx_ip
        self.targetContainerName = t_cnt
        self.parentContainer = ""
        self.sys_mac = ""
        self.configlets = {"keys":[],"names":[]}
        self.ignoreconfiglets = {"keys":[],"names":[]}
    
    def updateContainer(self,CVPOBJ):
        """
        Function that updates the container information for the EOS device.
        Parameters:
        CVPOBJ = CVPCON class object that contains information about CVP (required)
        """
        updateCnt = True
        while updateCnt:
            CVPOBJ.getDeviceInventory()
            # Adding check for ZTP devices with different hostnames
            if self.hostname in CVPOBJ.inventory:
                try:
                    self.sys_mac = CVPOBJ.inventory[self.hostname]["systemMacAddress"]
                    self.parentContainer = CVPOBJ.getContainerInfo(CVPOBJ.inventory[self.hostname]["parentContainerKey"])
                    updateCnt = False
                except:
                    sleep(1)
            else:
                try:
                    for cvp_node in CVPOBJ.inventory:
                        if CVPOBJ.inventory[cvp_node]["ipAddress"] == self.ip:
                            self.sys_mac = CVPOBJ.inventory[cvp_node]["systemMacAddress"]
                            self.parentContainer = CVPOBJ.getContainerInfo(CVPOBJ.inventory[cvp_node]["parentContainerKey"])
                            updateCnt = False
                except:
                    sleep(1)
    
    def resetConfiglets(self):
        """
        Function to reset the configlets of device to none.
        Parameters:
        NONE
        """
        self.configlets = {"keys":[],"names":[]}
        self.ignoreconfiglets = {"keys":[],"names":[]}
    
    def removeConfiglets(self,CVPOBJ, remove_list):
        """
        Function that sets configlets to be removed.
        Parameters:
        CVPOBJ = CVPCON class object that contains information about CVP (required)
        remove_list = List of configlet names to be removed (required)
        """
        for cfg in remove_list:
            response = CVPOBJ.getConfigletByName(cfg)
            if 'key' in response.keys():
                self.ignoreconfiglets["keys"].append(response["key"])
                self.ignoreconfiglets['names'].append(response["name"])
    
    def updateDevice(self,CVPOBJ):
        """
        Function that updates the EOS device information:
        Parameters:
        CVPOBJ = CVPCON class object that contains information about CVP (required)
        """
        CVPOBJ.getDeviceInventory()
        tmp_info = CVPOBJ.inventory[self.hostname]
        self.sys_mac = tmp_info['systemMacAddress']
        self.fqdn = tmp_info['fqdn']
        self.parentContainer = tmp_info['parentContainerKey']


# ==================================
# Class definition for working with CVP
# ==================================
class CVPCON():
    def __init__(self,cvp_url,c_user,c_pwd):
        self.cvp_url = cvp_url
        self.cvp_user = c_user
        self.cvp_pwd = c_pwd
        self.inventory = {}
        self.containers = {}
        self.images = {}
        self.imageBundles = {}
        self.tasks = {}
        self.version = ''
        self.cvp_api = {
            'authenticate': 'cvpservice/login/authenticate.do',
            'logout': 'cvpservice/login/logout.do',
            'checkSession': 'cvpservice/login/home.do',
            'checkVersion': 'cvpservice/cvpInfo/getCvpInfo.do',
            'addConfiglet': 'cvpservice/configlet/addConfiglet.do',
            'addConfigletBuilder': 'cvpservice/configlet/addConfigletBuilder.do',
            'getConfiglets': 'cvpservice/configlet/getConfiglets.do',
            'getConfigletByName': 'cvpservice/configlet/getConfigletByName.do',
            'updateConfiglet': 'cvpservice/configlet/updateConfiglet.do',
            'updateConfigletBuilder': 'cvpservice/configlet/updateConfigletBuilder.do',
            'autoConfigletGenerator': 'cvpservice/configlet/autoConfigletGenerator.do',
            'getConfigletBuilder': 'cvpservice/configlet/getConfigletBuilder.do',
            'searchTopo': 'cvpservice/provisioning/searchTopology.do',
            'getContainer': 'cvpservice/inventory/containers',
            'getContainerInfo': 'cvpservice/provisioning/getContainerInfoById.do',
            'getConfigletsByNetElementId': 'cvpservice/provisioning/getConfigletsByNetElementId.do',
            'getConfigletsByContainerId': 'cvpservice/provisioning/getConfigletsByContainerId.do',
            'addTempAction': 'cvpservice/provisioning/addTempAction.do',
            'deviceInventory': 'cvpservice/inventory/devices',
            'deleteDevice': 'cvpservice/inventory/deleteDevices.do',
            'inventoryConfig': 'cvpservice/inventory/getInventoryConfiguration.do',
            'saveTopo': 'cvpservice/provisioning/v2/saveTopology.do',
            'getAllTemp': 'cvpservice/provisioning/getAllTempActions.do?startIndex=0&endIndex=0',
            'getAllTasks': 'cvpservice/task/getTasks.do',
            'deleteAllTemp': 'cvpservice/task/deleteAllTempAction.do',
            'cancelTasks': 'cvpservice/task/cancelTask.do',
            'executeAllTasks': 'cvpservice/task/executeTask.do',
            'getTaskStatus': 'cvpservice/task/getTaskStatusById.do',
            'ipConnectivityTest': 'cvpservice/provisioning/ipConnectivityTest.do',
            'generateCB': 'cvpservice/configlet/autoConfigletGenerator.do',
            'getTempConfigs': 'cvpservice/provisioning/getTempConfigsByNetElementId.do',
            'createSnapshot': 'cvpservice/snapshot/templates/schedule',
            'getAllSnapshots': 'cvpservice/snapshot/templates',
            'getCertificate': 'cvpservice/ssl/getCertificate.do',
            'importCertificate': 'cvpservice/ssl/importCertAndPrivateKey.do',
            'generateCertificate': 'cvpservice/ssl/generateCertificate.do',
            'installCertificate': 'cvpservice/ssl/installCertificate.do',
            'createServer': 'cvpservice/aaa/createServer.do',
            'saveAAADetails': 'cvpservice/aaa/saveAAADetails.do',
            'getImages': 'cvpservice/image/getImages.do',
            'getImageBundles': 'cvpservice/image/v2/getImageBundles.do',
            'addImage': 'cvpservice/image/addImage.do',
            'saveImageBundle': 'cvpservice/image/saveImageBundle.do'
        }

        self.headers = {
            'Content-Type':'application/json',
            'Accept':'application/json'
        }
        self._createSession()
        self.checkVersion()
        self.getAllContainers()
        self.getDeviceInventory()
        self.getAllSnapshots()
        self.getImages()
        self.getImageBundles()

    # ================================
    # Utility Section
    # ================================

    def _createSession(self):
        payload = {
            'userId':self.cvp_user,
            'password':self.cvp_pwd
        }
        self.session = requests.Session()
        response = self.session.post("https://{0}/{1}".format(self.cvp_url, self.cvp_api['authenticate']), json=payload, verify=False, headers=self.headers)
        self.cookies = response.cookies
        if 'access_token' in response.cookies:
            self.SID = "{0}={1}".format(response.json()['cookie']['Name'], response.json()['cookie']['Value'])
            self.headers['Cookie'] = self.SID
        else:
            self.SID = response.cookies['session_id']
            self.headers['Cookie'] = 'session_id={}'.format(self.SID)

    def _sendRequest(self,c_meth,url,payload='',files=None):
        """
        Generic function that will send the API call to CVP. 
        Parameters:
        c_meth = API method, ie "GET or "POST" (required)
        url = The API url that is located in self.cvp_api (required)
        payload = data/payload required for the API call, if needed (optional)
        """
        if self.session:
            if c_meth == "GET":
                response = self.session.get("https://{}/".format(self.cvp_url) + url, json=payload, headers=self.headers, verify=False)
            elif c_meth == "POST" and files:
                if 'access_token' in self.headers['Cookie']:
                    fheaders = {
                        'Accept': 'application/json',
                        'Cookie': self.SID
                    }
                else:
                    fheaders = {
                        'Accept': 'application/json',
                        'Cookie': 'session_id={}'.format(self.SID)
                    }
                response = self.session.post("https://{}/".format(self.cvp_url) + url, files=files, headers=fheaders, verify=False)
            else:
                response = self.session.post("https://{}/".format(self.cvp_url) + url, json=payload, headers=self.headers, verify=False)
            if response:
                return(response.json())
            else:
                return(False)
        else:
            return(False)
    
    def _checkSession(self):
        if 'Cookie' in self.headers.keys():
            pass
        else:
            pass
        response = self._sendRequest("GET",self.cvp_api['checkSession'])
        if type(response) == dict:
            if response['data'] == 'success':
                return(True)
            else:
                return(False)
        else:
            return(False)
    
    def _checkEncode(self, p_string):
        """
        Function to check if provided string is base64 encoded.
        Parameters:
        p_string = String to check (required)
        """
        try:
            b64decode(p_string.encode()).decode()
            return(True)
        except:
            return(False)
    
    def _encodeString(self, p_string):
        """
        Function to base64 encode a string.
        Parameters:
        p_string = String to encode (required)
        """
        try:
            encoded_string = b64encode(p_string.encode()).decode()
            return(encoded_string)
        except:
            return(False)

    def _decodeString(self, p_string):
        """
        Function to base64 decode a string.
        Parameters:
        p_string = String to decode (required)
        """
        try:
            encoded_string = b64decode(p_string.encode()).decode()
            return(encoded_string)
        except:
            return(False)

    def checkVersion(self):
        if self._checkSession():
            response = self._sendRequest("GET",self.cvp_api['checkVersion'])
            if 'version' in response:
                self.version = str(response['version'])
    
    def saveTopology(self):
        """
        Function that saves all Temporary Provisioning Actions/Tasks
        """
        response = self._sendRequest("POST",self.cvp_api['saveTopo'],[])
        return(response)

    def execLogout(self):
        """
        Function to terminate CVP Session
        """
        response = self._sendRequest("POST",self.cvp_api['logout'])
        #pS("OK","Logged out of CVP")
        return(response)
    
    # ================================
    # Inventory Section
    # ================================
    
    def getAllContainers(self):
        """
        Function to get all Configured containers in CVP.
        """
        response = self._sendRequest("GET",self.cvp_api['getContainer'])
        for cnt in response:
            self.containers[cnt['Name']] = cnt
            self.containers[cnt['Name']]['ignorecfgs'] = {'keys':[], 'names': []}
            self.containers[cnt['Name']]['configlets'] = {'keys':[], 'names': []}
    
    def getContainerId(self,cnt_name):
        """
        Function to get the key for a container
        Parameters:
        cnt_name = container name (required)
        """
        response = self._sendRequest("GET",self.cvp_api['getContainer'] + "?name={0}".format(cnt_name))
        return(response)
    
    def getContainerInfo(self,cnt_key):
        """
        Function to get all information on a container.
        Parameters:
        cnt_key = Container key/id (required)
        """
        response = self._sendRequest("GET",self.cvp_api['getContainerInfo'] + '?containerId={0}'.format(cnt_key))
        return(response)

    def addContainer(self,cnt_name,pnt_name):
        """
        Function to add a new container.
        Parameters:
        cnt_name = New Container to be created (required)
        pnt_name = Parent container where the new container should be nested within (required)
        """
        msg = "Creating {0} container under the {1} container".format(cnt_name,pnt_name)
        payload = {
            'data': [
                {
                    'info': msg,
                    'infoPreview': msg,
                    'action': 'add',
                    'nodeType': 'container',
                    'nodeId': 'new_container',
                    'toId': self.containers[pnt_name]["Key"],
                    'fromId': '',
                    'nodeName': cnt_name,
                    'fromName': '',
                    'toName': self.containers[pnt_name]["Name"],
                    'childTasks': [],
                    'parentTask': '',
                    'toIdType': 'container'
                }
            ]
        }
        response = self._sendRequest("POST",self.cvp_api['addTempAction'] + "?format=topology&queryParam=&nodeId={0}".format(self.containers[pnt_name]["Key"]),payload)
        return(response)

    def addDeviceInventory(self,eos_ips):
        """
        Function that adds a device to inventory
        Parameters:
        eos_ip = MGMT IP address for the EOS device (required)
        """
        payload = {
            "hosts": eos_ips
        }
        response = self._sendRequest("POST",self.cvp_api['deviceInventory'],payload)
        return(response)
    
    def getDeviceInventory(self):
        """ 
        Function that gets all Provisioned devices within CVP.
        """
        response = self._sendRequest("GET",self.cvp_api['deviceInventory'] + "?provisioned=true")
        for res in response:
            self.inventory[res['hostname']] = {"fqdn":res['fqdn'],'ipAddress':res['ipAddress'],'parentContainerKey':res['parentContainerKey'],"systemMacAddress":res["systemMacAddress"]}
    
    def deleteDevices(self,eos_mac):
        """
        Function to remove a device from provisioning inventory.
        Parameters:
        eos_mac = System mac address for the device to be removed (required)
        """
        payload = {
            "data": [eos_mac]
        }
        response = self._sendRequest("POST",self.cvp_api['deleteDevice'],payload)
        return(response)

    def getInventoryConfiguration(self,eos_obj):
        """
        Function to get current configuration for specified device.
        Parameters:
        eos_obj = CVPSWITCH class object that contains relevant device info (required)
        """
        response = self._sendRequest("GET",self.cvp_api['inventoryConfig'] + "?netElementId={0}".format(eos_obj.sys_mac))
        return(response)
    
    def moveDevice(self,eos_obj):
        """
        Function that moves a device from one container to another container.
        Parameters:
        eos_obj = CVPSWITCH class object that contains relevant device info (required)
        """
        msg = "Moving {0} device under the {1} container".format(eos_obj.hostname,eos_obj.targetContainerName)
        payload = {
            'data': [
                {
                    'info': msg,
                    'infoPreview': msg,
                    'action': 'update',
                    'nodeType': 'netelement',
                    'nodeId': eos_obj.sys_mac,
                    'toId': self.containers[eos_obj.targetContainerName]["Key"],
                    'fromId': self.containers[eos_obj.parentContainer["name"]]["Key"],
                    'nodeName': eos_obj.hostname,
                    'fromName': eos_obj.parentContainer["name"],
                    'toName': eos_obj.targetContainerName,
                    'childTasks': [],
                    'parentTask': '',
                    'toIdType': 'container'
                }
            ]
        }
        response = self._sendRequest("POST",self.cvp_api['addTempAction'] + "?format=topology&queryParam=&nodeId=root",payload)
        return(response)

    # ================================
    # Tasks Section
    # ================================

    def getAllTasks(self,t_type):
        """
        Function that gets all Tasks.
        Parameters:
        t_type = Task type to query on, ie "Pending" (required)
        """
        response = self._sendRequest("GET",self.cvp_api['getAllTasks'] + "?queryparam={0}&startIndex=0&endIndex=0".format(t_type))
        self.tasks[t_type] = response['data']
    
    def getRecentTasks(self, end_task=50):
        """
        Function that gets recent to the amount given for end_task.
        Parameters:
        end_task: Integer for the number of tasks wanted.
        """
        response = self._sendRequest("GET",self.cvp_api['getAllTasks'] + "?startIndex=0&endIndex={0}".format(end_task))
        self.tasks['recent'] = response['data']
    
    def execAllTasks(self,t_type):
        """
        Function that executes all tasks
        Parameters:
        t_type = Task type to execute on, ie "Pending" (required)
        """
        data = []
        if t_type in self.tasks.keys():
            if self.tasks[t_type]:
                for task in self.tasks[t_type]:
                    data.append(task['workOrderId'])
        if data:
            payload = {"data": data }
            response = self._sendRequest("POST",self.cvp_api['executeAllTasks'],payload)
            for task in data:
                while True:
                    t_response = self.getTaskStatus(task)
                    if 'Task Update In Progress' not in t_response['taskStatus']:
                        #pS("OK","Task Id: {0} has {1}".format(task,t_response['taskStatus']))
                        break
                    else:
                        #pS("INFO","Task Id: {0} Still in progress....sleeping".format(task))
                        sleep(10)
            self.getAllTasks(t_type)
            return({'response': response, 'ids': payload['data']})
    
    def cancelTasks(self,t_type):
        """
        Function to cancel any tasks by type
        Parameters:
        t_type = Task type to execute on, ie "Pending" (required)
        """
        data = []
        if t_type in self.tasks.keys():
            if self.tasks[t_type]:
                for task in self.tasks[t_type]:
                    data.append(task['workOrderId'])
        if data:
            payload = {"data": data}
            response = self._sendRequest("POST",self.cvp_api['cancelTasks'],payload)
            self.getAllTasks(t_type)
            return(response)
    
    def getTaskStatus(self,t_id):
        """
        Function to get the status of a particular Task ID.
        Parameters:
        t_id = Task Id (required)
        """
        response = self._sendRequest("GET",self.cvp_api['getTaskStatus'] + "?taskId={0}".format(t_id))
        return(response)

    # ================================
    # Configlets Section
    # ================================

    def impConfiglet(self,cType,cName,cScript,cFormList=[]):
        """
        Base function to add a new static or configlet builder.  Function will check for existing configlet,
        if one exists, it will update otherwise create a new one.
        Parameters:
        cType = Type of configlet <static/builder> (required)
        cName = Name of configlet (required)
        cScript = Configlet data or Python script for Configlet Builders (required)
        cFormList = Form list data for a configlet builder (optional)
        """
        cCheck = self.getConfigletByName(cName)
        if 'key' in cCheck.keys():
            if cCheck['type'] == 'Builder':
                response = self.updateConfigletBuilder(cName,cScript,cCheck['key'],cFormList)
                return(("Updated",response))
            elif cCheck['type'] == 'Static':
                response = self.updateConfiglet(cName,cScript,cCheck['key'])
                return(("Updated",response))
        else:
            if cType.lower() == 'static':
                response = self.addConfiglet(cName,cScript)
                return(("Added",response))
            elif cType.lower() == 'builder':
                response = self.addConfigletBuilder(cName,cScript,cFormList)
                return(("Added",response))

    def addConfiglet(self,conName,conData):
        """
        Function to add a single static configlet
        Parameters:
        conName = Name of configlet (required)
        conData = Configlet data/configuration (required)
        """
        payload = {
            'config': conData,
            'name': conName
        }
        response = self._sendRequest("POST",self.cvp_api['addConfiglet'],payload)
        return(response)
    
    def updateConfiglet(self,conName,conData,conKey):
        """
        Function to update a single static configlet
        Parameters:
        conName = Name of configlet (required)
        conData = Configlet data/configuration (required)
        conKey = Configlet key (required)
        """
        payload = {
            'config': conData,
            'key': conKey,
            'name': conName,
        }
        response = self._sendRequest("POST",self.cvp_api['updateConfiglet'],payload)
        return(response)

    def addConfigletBuilder(self,cbName,cbScript,cbForm=[]):
        """
        Function to add a configlet builder to cvp
        Parameters:
        cbName = Name of configlet builder (required)
        cbScript = Python script as string (required)
        cbForm = List for form data (optional)
        """
        payload = {
            'name': cbName,
            'data': {
                'formList': cbForm,
                'main_script': {
                    'data': cbScript
                }
            }
        }
        response = self._sendRequest("POST",self.cvp_api['addConfigletBuilder'] + "?isDraft=false",payload)
        return(response)
    
    def updateConfigletBuilder(self,cbName,cbScript,cbKey,cbForm=[]):
        """
        Function to update a configlet builder to cvp
        Parameters:
        cbName = Name of configlet builder (required)
        cbScript = Python script as string (required)
        cbKey = Configlet key (required)
        cbForm = List for form data (optional)
        """
        payload = {
            'name': cbName,
            'data': {
                'formList': cbForm,
                'main_script': {
                    'data': cbScript
                }
            }
        }
        response = self._sendRequest("POST",self.cvp_api['updateConfigletBuilder'] + "?isDraft=false&id=" + cbKey + "&action=save",payload)
        return(response)
    
    def getConfiglets(self,cfg_type='Configlet,Builder'):
        """
        Function to grab all configlets from cvp
        Parameters:
        cfg_type = Configlet type to download, options available: (optional: default Configlet,Builder)
            Configlet - Returns static and generated configlets
            Builder - Returns builder as well as draft configlets
            Draft - Returns draft configlets
            BuilderWithoutDraft - Returns only builder configlets
            IgnoreDraft - Returns everything other than draft configlets
            Static - Returns static configlets
            Generated - Returns generated configlets
        """
        response = self._sendRequest("GET",self.cvp_api['getConfiglets'] + '?type={0}&startIndex=0&endIndex=0'.format(cfg_type))
        return(response)
    
    def getConfigletBuilder(self,cb_id):
        """
        Function to return the configlet builder information based off id:
        Parameters:
        cb_id = Configlet Builder ID (required)
        """
        response = self._sendRequest("GET",self.cvp_api['getConfigletBuilder'] + '?id={0}'.format(cb_id))
        return(response)

    def getConfigletByName(self,cfg):
        """
        Function to return the configlet information based off name:
        Parameters:
        cfg = Configlet name in CVP (required)
        """
        response = self._sendRequest("GET",self.cvp_api['getConfigletByName'] + "?name={0}".format(cfg))
        return(response)
    
    def getConfigletsByNetElementId(self,eos_obj):
        """
        Function to get all applied configlets to a particular device.
        Parameters:
        eos_obj = CVPSWITCH class object that contains relevant EOS device info (required)
        """
        response = self._sendRequest("GET",self.cvp_api['getConfigletsByNetElementId'] + '?netElementId={0}&startIndex=0&endIndex=0'.format(eos_obj.sys_mac))
        return(response)
    
    def getConfigletsByContainerId(self, cnt_id):
        """
        Function to get all applied configlets to a paricular container.
        Parametrers:
        cnt_id = ID/Key of the container (required)
        """
        # Get the container ID for the provided name
        response = self._sendRequest("GET", self.cvp_api['getConfigletsByContainerId'] + "?containerId={0}&startIndex=0&endIndex=0".format(cnt_id))
        return(response)
    
    def updateContainersConfigletsInfo(self, cnt_name):
        """
        Function to get all applied configlets to a paricular container and
        apply to the container object.
        Parametrers:
        cnt_name = Name of the container (required)
        """
        # Get the container ID for the provided name
        cnt_id = self.getContainerId(cnt_name)[0]['Key']
        response = self.getConfigletsByContainerId(cnt_id)
        self.containers[cnt_name]['configlets'] = {'keys':[],'names':[]}
        self.containers[cnt_name]['ignorecfgs'] = {'keys':[],'names':[]}
        for cfg in response['configletList']:
            self.containers[cnt_name]['configlets']['keys'].append(cfg["key"])
            self.containers[cnt_name]['configlets']['names'].append(cfg["name"])
        return(response)

    def removeContainerConfiglets(self, cnt_name, ignore_list):
        """
        Function to add configlets to be removed from a container.
        Parameters:
        cnt_name = Name of the container (required)
        ignore_list = List of configlet names to be ignored (required)
        """
        self.containers[cnt_name]['ignorecfgs'] = {'keys':[], 'names': []}
        for cfg in ignore_list:
            response = self.getConfigletByName(cfg)
            if 'key' in response.keys():
                self.containers[cnt_name]['ignorecfgs']['keys'].append(response["key"])
                self.containers[cnt_name]['ignorecfgs']['names'].append(response["name"])
        return(True)

    def addContainerConfiglets(self, cnt_name, cfg_list):
        """
        Function to take a list of container specific config names, get the config Ids from CVP and add them to the container configlet list to be applied.
        Parameters:
        cfg_list = List of configlet names to be queried and added to the device (required)
        """
        self.containers[cnt_name]['configlets'] = {'keys':[],'names':[]}
        for cfg in cfg_list:
            response = self.getConfigletByName(cfg)
            if 'key' in response.keys():
                self.containers[cnt_name]['configlets']['keys'].append(response["key"])
                self.containers[cnt_name]['configlets']['names'].append(response["name"])
        return(True)
    
    def addDeviceConfiglets(self,eos_obj,cfg_list):
        """
        Function to take a list of device specific config names, get the config Ids from CVP and add them to the device configlet list to be applied.
        Parameters:
        eos_obj = CVPSWITCH class object that contains relevant EOS device info (required)
        cfg_list = List of configlet names to be queried and added to the device (required)
        """
        for cfg in cfg_list:
            response = self.getConfigletByName(cfg)
            if 'key' in response.keys():
                eos_obj.configlets["keys"].append(response["key"])
                eos_obj.configlets['names'].append(response["name"])
        return(True)
    
    def getTempConfigs(self,eos_obj,c_type):
        """
        Function that gets all configs assigned to a device.
        Parameters:
        eos_obj = CVPSWITCH class object that contains relevant EOS device info (required)
        c_type = Configlet type, ie "Builder", "Static" (required)
        """
        ret_configs = []
        cnvt_id = eos_obj.sys_mac.replace(":","%3A")
        response = self._sendRequest("GET",self.cvp_api['getTempConfigs'] + "?netElementId={0}".format(cnvt_id))
        for p_config in response['proposedConfiglets']:
            eos_obj.configlets["keys"].append(p_config['key'])
            eos_obj.configlets["names"].append(p_config['name'])
            if p_config['type'] == c_type:
                ret_configs.append(p_config['key'])
        return(ret_configs)
    
    def genConfigBuilders(self,eos_obj):
        """
        Function to generate all ConfigletBuilders assigned to a particular device.
        Parameters:
        eos_obj = CVPSWICH class object that contains all relevant EOS device info (required)
        """
        payload = {
            'netElementIds':[eos_obj.sys_mac],
            'containerId': self.containers[eos_obj.targetContainerName]['Key'],
            'pageType': 'netelement'
        }
        tmp_cb = self.getTempConfigs(eos_obj,"Builder")
        response = ""
        for cb in tmp_cb:
            payload['configletBuilderId'] = cb
            response = self._sendRequest("POST",self.cvp_api['generateCB'],payload)
            eos_obj.configlets["keys"].append(response['data'][0]['configlet']['key'])
            eos_obj.configlets["names"].append(response['data'][0]['configlet']['name'])
        return(response)
    
    def applyConfiglets(self,eos_obj):
        """ 
        Function that applies all configlets assigned to a device.
        Parameters:
        eos_obj = CVPSWITCH class object that contails all relevant EOS device info (required)
        """
        msg = "Applying configlets to {0}".format(eos_obj.hostname)
        payload = {
            'data': [
                {
                    'info': msg,
                    'infoPreview': msg,
                    'action': 'associate',
                    'nodeType': 'configlet',
                    'configletList': eos_obj.configlets["keys"],
                    'configletNamesList': eos_obj.configlets["names"],
                    'ignoreConfigletNamesList': eos_obj.ignoreconfiglets["names"],
                    'ignoreConfigletList': eos_obj.ignoreconfiglets["keys"],
                    'configletBuilderList': [],
                    'configletBuilderNamesList': [],
                    'ignoreConfigletBuilderList': [],
                    'ignoreConfigletBuilderNamesList': [],
                    'nodeId': '',
                    'toId': eos_obj.sys_mac,
                    'fromId': '',
                    'nodeName': '',
                    'fromName': '',
                    'toName': eos_obj.fqdn,
                    'nodeIpAddress': eos_obj.ip,
                    'nodeTargetIpAddress': eos_obj.ip,
                    'childTasks': [],
                    'parentTask': '',
                    'toIdType': 'netelement'
                }
            ]
        }
        response = self._sendRequest("POST",self.cvp_api['addTempAction'] + "?format=topology&queryParam=&nodeId=root",payload)
        return(response)
    
    def deleteAllTempActions(self):
        """
        Function to delete all temporary actions.
        Parameters:
        NONE
        """
        payload = {}
        response = self._sendRequest("POST",self.cvp_api['deleteAllTemp'],payload)
        return(response)

    def applyConfigletsContainers(self,cnt_name):
        """ 
        Function that applies all configlets assigned to a device.
        Parameters:
        eos_obj = CVPSWITCH class object that contails all relevant EOS device info (required)
        """
        msg = "Applying configlets to {0}".format(cnt_name)
        payload = {
            'data': [
                {
                    'info': msg,
                    'infoPreview': msg,
                    'action': 'associate',
                    'nodeType': 'configlet',
                    'configletList': self.containers[cnt_name]['configlets']['keys'],
                    'configletNamesList': self.containers[cnt_name]['configlets']["names"],
                    'ignoreConfigletNamesList': self.containers[cnt_name]['ignorecfgs']['names'],
                    'ignoreConfigletList': self.containers[cnt_name]['ignorecfgs']['keys'],
                    'configletBuilderList': [],
                    'configletBuilderNamesList': [],
                    'ignoreConfigletBuilderList': [],
                    'ignoreConfigletBuilderNamesList': [],
                    'nodeId': '',
                    'toId': self.containers[cnt_name]["Key"],
                    'fromId': '',
                    'nodeName': '',
                    'fromName': '',
                    'toName': self.containers[cnt_name]["Name"],
                    'childTasks': [],
                    'parentTask': '',
                    'toIdType': 'container'
                }
            ]
        }
        response = self._sendRequest("POST",self.cvp_api['addTempAction'] + "?format=topology&queryParam=&nodeId=root",payload)
        return(response)
    
    def ipConnectivityTest(self,veos_ip):
        """
        Function to test the reachability of an IP address.
        Parameters:
        veos_ip = IP address to see if CVP can reach (required)
        """
        payload = {
            "ipAddress": veos_ip
        }
        response = self._sendRequest("POST",self.cvp_api['ipConnectivityTest'],payload)
        return(response)
    
    # ================================
    # Snapshot Section
    # ================================

    def createSnapshot(self,snap_name,snap_cmds,snap_devices=[]):
        """
        Function that creates snapshot templates.
        Parameters:
        snap_name = Name of the snapshot (required)
        snap_cmds = All commands to be included in snapshot (required)
        snap_devices = Devices to be included on the snapshot (optional)
        """
        payload = {
            'name': snap_name,
            'commands': snap_cmds,
            'deviceList': snap_devices,
            'frequency': '300'
        }
        response = self._sendRequest("POST",self.cvp_api['createSnapshot'],payload)
        self.getAllSnapshots()
        return(response)

    def getAllSnapshots(self):
        """
        Function to get all configured snapshots on CVP
        """
        response = self._sendRequest("GET",self.cvp_api['getAllSnapshots'] + "?startIndex=0&endIndex=0")
        self.snapshots = response['templateKeys']
    
    # ================================
    # SSL Certificates Section
    # ================================

    def getCerts(self,certType='cvpCert'):
        """
        Function to get installed certs in CVP.
        Parameters:
        certType = Type of cert (optional) 
            Options:
                - cvpCert (default) self-signed
                - csr
                - dcaCert
        """
        response = self._sendRequest("GET",self.cvp_api['getCertificate'] + "?certType={}".format(certType))
        return(response)

    def importCert(self, publicCert, privateKey, certPass="", certType="cvpCert"):
        """
        Function to import a custom certificate.
        Parameters:
        publicCert = (required)
        privateKey = (required)
        certPass = (optional)
        certType = Type of cert (optional)
            Options:
                - cvpCert (default) self-signed
                - csr
                - dcaCert
        """
        # Check Cert type
        if self._checkEncode(publicCert):
            c_cert = publicCert
        else:
            c_cert = self._encodeString(publicCert)
        # Check Key type
        if self._checkEncode(privateKey):
            c_key = privateKey
        else:
            c_key = self._encodeString(privateKey)
        payload = {
            "certType": certType,
            "passPhrase": certPass,
            "privateKey": c_key,
            "publicCert": c_cert,
        }
        response = self._sendRequest("POST", self.cvp_api['importCertificate'], payload)
        return(response)


    def generateCert(self, cName, organization, organizationUnit, description, validity):
        """
        Function to generate a self-signed cert.
        Parameters:
        cName = Common Name (required)
        organization = Organization (requried)
        organizationUnit = Organizational Unit (required)
        description = Description (required)
        validity = Valid lengh in days (required) int
        """
        payload = {
            "certType": "cvpCert",
            "commonName": cName,
            "organization": organization,
            "organizationUnit": organizationUnit,
            "description": description,
            "keyLength": 2048,
            "digestAlgorithm": "SHA256withRSA",
            "encryptAlgorithm": "RSA",
            "validity": validity
        }
        response = self._sendRequest("POST",self.cvp_api['generateCertificate'], payload)
        return(response)
    
    def installCert(self):
        """
        Function to install proposed Certs.
        Parameters:
        None
        """
        response = self._sendRequest("POST",self.cvp_api['installCertificate'])
        return(response)
    
    # ================================
    # AAA Section
    # ================================

    def createServer(self, ip, stype, secret, port, acctport, mode="PAP", status="Enabled"):
        """
        Function to add a new AAA server.
        Parameters:
        ip = IP address for the authenticaton server (required)
        stype = Authentication server type RADIUS, TACACS (required)
        secret = Secret used for the server (required)
        port = Authentication port (required)
        acctport = Accounting port (required)
        mode = Mode to use. ie PAP (optional)
        status = Enable or disable the server (optional)
        """
        payload = {
            "ipAddress": ip,
            "serverType": stype,
            "secret": secret,
            "authMode": mode,
            "accountPort": acctport,
            "port": port,
            "status": status
        }
        response = self._sendRequest("POST", self.cvp_api['createServer'], payload)
        return(response)
    
    def saveAAA(self, authe, autho):
        """
        Function to save the authenticatoin authorization settings.
        Parameters:
        authe = Authentication mode (required)
        autho = Authorization mode (required)
        """
        payload = {
            "authenticationServerType": authe,
            "authorizationServerType": autho
        }
        response = self._sendRequest("POST", self.cvp_api['saveAAADetails'], payload)
        return(response)

    # ================================
    # Images Section
    # ================================

    def getImages(self, name=None):
        """
        Function to get images already uploaded to CVP.
        Parameters:
        name = Name of image to check for (optional)
        """
        if name:
            param = "queryparam={}&".format(name)
        else:
            param = ""
        response = self._sendRequest("GET", self.cvp_api['getImages'] + "?" + param + "startIndex=0&endIndex=0")
        if response['total']:
            for img in response['data']:
                self.images[img['name']] = {
                    'imageId': img['imageId'],
                    'name': img['name'],
                    'isRebootRequired': img['isRebootRequired']
                }
        return(response)

    def getImageBundles(self, name=None):
        """
        Function to get all image bundles in CVP.
        Parameters:
        name = Name of the image bundle to check (optional)
        """
        if name:
            param = "queryparam={}&".format(name)
        else:
            param = ""
        response = self._sendRequest("GET", self.cvp_api['getImageBundles'] + "?" + param + "startIndex=0&endIndex=0")
        if response['total']:
            for imb in response['data']:
                self.imageBundles[imb['name']] = imb
        return(response)

    def addImage(self, img_path):
        """
        Function to import a .swi or .swix file into the CVP Datastore.
        Parameters:
        img_path = Full path location for the file (required)
        """
        # file = open(img_path, 'rb')
        response = self._sendRequest("POST", self.cvp_api['addImage'], files={'file':open(img_path, 'rb')})
        # file.close()
        if 'result' in response:
            if response['result'] == 'success':
                self.images[response['name']] = {
                    'imageId': response['imageId'],
                    'name': response['name'],
                    'isRebootRequired': response['isRebootRequired']
                }
        return(response)
    
    def createImageBundle(self, name, img_list, certified=True):
        """
        Function to create an Image bundle.
        Parameters:
        name = Name of the image bundle (required)
        certified = If the bundle is certified (required)
        img_list = Array of images names to add to the bundle (required)
        """
        img_bundle = []
        for img in img_list:
            if self.images[img]:
                img_bundle.append({
                    'name': self.images[img]['name'],
                    'isRebootRequired': self.images[img]['isRebootRequired']
                })
        if img_bundle:
            payload = {
                'name': name,
                'isCertifiedImage': 'true' if certified else 'false',
                'images': img_bundle
            }
            response = self._sendRequest("POST", self.cvp_api['saveImageBundle'], payload=payload)
            return(response)
        else:
            return(False)
    
    def applyImage(self, target_type, bundle_name, target_name):
        """
        Function to apply an Image bundle to device or container.
        Parameters:
        target_type = id type {container, netelement} (required)
        bundle_name = Name of the image bundle to apply (required)
        target_name = Name of endpoint to apply to (required)
        """
        res = self.getImageBundles(name=bundle_name)
        if res['total'] == 1:
            msg = "Applying Image Bundle to {0}".format(target_name)
            payload = {
                'data': [
                    {
                        'info': msg,
                        'infoPreview': msg,
                        'action': 'associate',
                        'nodeType': 'imagebundle',
                        'nodeId': res['data'][0]['key'],
                        'toId': '',
                        'fromId': '',
                        'nodeName': res['data'][0]['name'],
                        'fromName': '',
                        'toName': target_name,
                        'childTasks': [],
                        'parentTask': '',
                        'toIdType': target_type
                    }
                ]
            }
            if target_type == 'container':
                payload['data'][0]['toId'] = self.containers[target_name]['Key']
            else:
                payload['data'][0]['toId'] = self.inventory[target_name]['systemMacAddress']
            response = self._sendRequest("POST", self.cvp_api['addTempAction'] + "?format=topology&queryParam=&nodeId=root",payload)
            return(response)
        else:
            return(False)
