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

