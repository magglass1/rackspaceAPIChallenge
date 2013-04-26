#!/usr/bin/python
# API Challenge 2
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

def wait_for_networking(server):
    while len(server.networks)==0 and server.status not in ['ACTIVE', 'ERROR']:
        time.sleep(5)
        server.get()

def main():
    pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))
    cs = pyrax.cloudservers
    servers = cs.servers.list()
    srv_dict = {}
    print "Select a server to clone:"
    for pos, srv in enumerate(servers):
        print "%s: %s" % (pos, srv.name)
        srv_dict[str(pos)] = srv.id
    selection = None
    while selection not in srv_dict:
        if selection is not None:
            print " -- Invalid choice"
        selection = raw_input("Enter the number for your choice: ")

    server_id = srv_dict[selection]
    print

    print "Taking image of server..."
    img_id = cs.servers.create_image(server_id, "server_clone_temp")
    print "Image ID:", img_id
    print "Waiting for image to complete..."
    image = cs.images.get(img_id)
    server = cs.servers.get(server_id)
    
    pyrax.utils.wait_until(image, "status", "ACTIVE")
    
    server_name = server.name + "_clone"
    print "Building server...\n"
    server = cs.servers.create(server_name, img_id, server.flavor)

    wait_for_networking(server)
    print "Name:", server.name
    if server.status not in ['ACTIVE','BUILD']:
        print "Status:", server.status
    print "Public IPs:", ", ".join(server.networks['public'])
    print "Username: root"
    print "Password:", server.adminPass
    print
    print "Waiting for server to become ACTIVE..."
    pyrax.utils.wait_until(server, "status", ['ACTIVE','BUILD'])
    print "Server status:", server.status
    print "Deleting image..."
    cs.images.delete(img_id)
    print "Done!"
    

if __name__ == '__main__':
    main()

