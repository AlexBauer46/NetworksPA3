'''
Created on Oct 12, 2016

@author: mwittie
'''

import network_3 as network
import link_3 as link
import threading
from time import sleep
from rprint import print


## configuration parameters
router_queue_size = 0  # 0 means unlimited
simulation_time = 10  # give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
	object_L = []  # keeps track of objects, so we can kill their threads
	
	# create network nodes
	client1 = network.Host(1)
	object_L.append(client1)
	client2 = network.Host(2)
	object_L.append(client2)
	router_a = network.Router(name='A', intf_count=2, max_queue_size=router_queue_size, r_table=[[3,0],[4,1]])
	object_L.append(router_a)
	router_b = network.Router(name='B', intf_count=1, max_queue_size=router_queue_size, r_table=[[3,0]])
	object_L.append(router_b)
	router_c = network.Router(name='C', intf_count=1, max_queue_size=router_queue_size, r_table=[[4,0]])
	object_L.append(router_c)
	router_d = network.Router(name='D', intf_count=2, max_queue_size=router_queue_size, r_table=[[3,0],[4,1]])
	object_L.append(router_d)
	server1 = network.Host(3)
	object_L.append(server1)
	server2 = network.Host(4)
	object_L.append(server2)
	
	# create a Link Layer to keep track of links between network nodes
	link_layer = link.LinkLayer()
	object_L.append(link_layer)
	
	# add all the links
	# link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
	link_layer.add_link(link.Link(client1, 0, router_a, 0, 50))
	link_layer.add_link(link.Link(client2, 0, router_a, 1, 50))
	link_layer.add_link(link.Link(router_a, 0, router_b, 0, 50))
	link_layer.add_link(link.Link(router_a, 1, router_c, 0, 50))
	link_layer.add_link(link.Link(router_b, 0, router_d, 0, 50))
	link_layer.add_link(link.Link(router_c, 0, router_d, 1, 50))
	link_layer.add_link(link.Link(router_d, 0, server1, 0, 50))
	link_layer.add_link(link.Link(router_d, 1, server2, 0, 50))
	
	# start all the objects
	thread_L = [threading.Thread(name=object.__str__(), target=object.run) for object in object_L]
	for t in thread_L:
		t.start()
	
	# create some send events
	for i in range(3):
		client1.udt_send(3, 'Hello Host 3 from Host 1 %d' % i)
	for i in range(3,6):
		client2.udt_send(4, 'Hello Host 4 from Host 2 %d' % i)
	
	# give the network sufficient time to transfer all packets before quitting
	sleep(simulation_time)
	
	# join all threads
	for o in object_L:
		o.stop = True
	for t in thread_L:
		t.join()
	
	print("All simulation threads joined")
