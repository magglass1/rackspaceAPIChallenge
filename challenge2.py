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
    
    

if __name__ == '__main__':
    main()

