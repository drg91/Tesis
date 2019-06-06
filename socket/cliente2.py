import socket

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/demo_socket")
print "Sending..."
s.send("Hello C from Python!")
data = s.recv(1024)
s.close()
print 'Received', repr(data)