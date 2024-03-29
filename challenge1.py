#!/usr/bin/python
# API Challenge 1
#
#Copyright 2013 Mark Lessel
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import pyrax
import os
import time

def wait_for_networking(server):
    while len(server.networks)==0 and server.status not in ['ACTIVE', 'ERROR']:
        time.sleep(5)
        server.get()

def main():
    pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
    cs = pyrax.cloudservers
    base_name = "apichallenge1_web"
    image = [img for img in cs.images.list() if "12.04" in img.name][0]
    flavor = [flavor for flavor in cs.flavors.list() if flavor.ram == 512][0]
    
    servers = []
    for i in xrange(1,4):
        server_name = base_name + str(i)
        print "Building %s..." % server_name
        server = cs.servers.create(server_name, image.id, flavor.id)
        servers.append(server)
    print "Waiting for IPs to be allocated...\n"
    for server in servers:
        #pyrax.utils.wait_until(server, "status", ['ACTIVE', 'ERROR'], interval=15, attempts=0)
        wait_for_networking(server)
        print "Name:", server.name
        if server.status not in ['ACTIVE','BUILD']:
            print "Status:", server.status
        print "Public IPs:", ", ".join(server.networks['public'])
        print "Username: root"
        print "Password:", server.adminPass
        print

if __name__ == '__main__':
    main()

