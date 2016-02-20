import struct

file = open( "/dev/input/event5", "rb" );

def getMouseEvent():
        buf = file.read(20);
        print len(buf)
#        pInfo,deviceId,deviceType,serial,x,y,buttons,pressuretx,ty,tx = struct.unpack( "iiiiiiiiii", buf[0:40] );
        #print ("%-10u  %-10u  %-10u  %-10u  %-10u  %-10u  %-10u  %-10u  %-10u  %-10u\n" % (pInfo,deviceId,deviceType,serial,x,y,buttons,pressuretx,ty,tx) );
        pInfo,deviceId,Time,serial,x,y,buttons,pressuretx,ty,tx = struct.unpack( "hhhhhhhhhh", buf);
#        print ("%-10u %-10u\n" % (Time,buttons));
        print ("%-10u %-10u\n" % (deviceId,y));
        # return stuffs

while( 1 ):
        getMouseEvent();
file.close();
