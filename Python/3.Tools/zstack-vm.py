import httplib
import json
import time


class ZstackVM(object):

    def __init__(self, zstack_host):
        self.zstack_host = zstack_host

    def api_call(self, zstack_host, session_uuid, api_id, api_content):
        conn = httplib.HTTPConnection(zstack_host, 8080)
        headers = {"Content-Type": "application/json"}
        if session_uuid:
            api_content["session"] = {"uuid": session_uuid}

        api_body = {api_id: api_content}
        conn.request("POST", "/zstack/api", json.dumps(api_body))
        response = conn.getresponse()
        if response.status != 200:
            raise Exception("failed to make an API call, %s, %s" % (response.status, response.reason))

        rsp_body = response.read()
        rsp = json.loads(rsp_body)

        if rsp["state"] == "Done":
            return json.loads(rsp["result"])

        job_uuid = rsp["uuid"]

        def query_until_done():
            conn.request("GET", "/zstack/api/result/%s" % job_uuid)
            response = conn.getresponse()
            if response.status != 200:
                raise Exception("failed to query API result, %s, %s" % (response.status, response.reason))

            rsp_body = response.read()
            rsp = json.loads(rsp_body)
            if rsp["state"] == "Done":
                return json.loads(rsp["result"])

            time.sleep(1)
            print("Job[uuid:%s] is still in processing" % job_uuid)
            return query_until_done()

        return query_until_done()

    def error_if_fail(self, rsp):
        success = rsp.values()[0]["success"]
        if not success:
            error = rsp.values()[0]["error"]
            raise Exception("failed to login, %s" % json.dumps(error))

    def login(self):
        content = {
            "accountName": "admin",
            "password": "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"
        }

        rsp = self.api_call(self.zstack_host, None, "org.zstack.header.identity.APILogInByAccountMsg", content)
        self.error_if_fail(rsp)

        self.session_uuid = rsp.values()[0]["inventory"]["uuid"]

        print("successfully login, session uuid is: %s" % self.session_uuid)
        return self.session_uuid

    def logout(self, session_uuid):
        content = {"sessionUuid": session_uuid}
        rsp = self.api_call(self.zstack_host, None, "org.zstack.header.identity.APILogOutMsg", content)
        self.error_if_fail(rsp)

        print("successfully logout")

    def create_vm(self):
        ctime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        content = {
            "l3NetworkUuids": ["099aca7e86a6454bba54b46eb8572f08"],
            "defaultL3NetworkUuid": "099aca7e86a6454bba54b46eb8572f08",
            "dataDiskOfferingUuids": ["bf832aadc1674e9294700f15c5beb8dc","bf832aadc1674e9294700f15c5beb8dc","bf832aadc1674e9294700f15c5beb8dc","bf832aadc1674e9294700f15c5beb8dc"],
            "name": "auto-vm-%s" % ctime,
            "description": "Jenkins auot create",
            "systemTags": [],
            "instanceOfferingUuid": "5270c3a32ae4424e80e14bf22cdb4b7b",
            "type": "UserVm",
            "imageUuid": "ea8b53e4497e4dd380842822ededdc97"
        }

        rsp = self.api_call(self.zstack_host, self.session_uuid, "org.zstack.header.vm.APICreateVmInstanceMsg", content)

        self.error_if_fail(rsp)
        vm_ip = rsp.values()[0]["inventory"]["vmNics"][0]["ip"]
        print(vm_ip)

        self.logout(self.session_uuid)

if __name__ == '__main__':
    obj = ZstackVM('192.168.2.1')
    obj.login()
    obj.create_vm()