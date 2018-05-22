import smbus
import math

class Gyro():

    def read_byte(adr):
        return bus.read_byte_data(address, adr)

    def read_word(adr):
        high = bus.read_byte_data(address, adr)
        low = bus.read_byte_data(address, adr+1)
        val = (high << 8) + low
        return val

    #Reads a two complement value and converts it for integer
    def read_word_2c(adr):
        val = read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(a,b):
        return math.sqrt((a*a)+(b*b))

    #Convert tilt angle in radians to degrees at y axis
    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)

    #Convert tilt angle in radians to degrees at x axis
    def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)

    def rotation():

        # Power management registers
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
        
        bus = smbus.SMBus(0) # or bus = smbus.SMBus(1) for Revision 2 boards
        address = 0x68       # This is the address value read via the i2cdetect command

        # Now wake the 6050 up as it starts in sleep mode
        bus.write_byte_data(address, power_mgmt_1, 0)

        #Default rotation scaling value of MPU6050
        #Rotation values in degrees per second
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)

        gyro_xout_scaled = gyro_xout / 131
        gyro_yout_scaled = gyro_yout / 131
        gyro_zout_scaled = gyro_zout / 131

        #Registers which holds the data in 16-bit two-complement format
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)

        #Default scaling value of MPU6050
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        #Rotation angle in degrees for x and y axis     
        x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        y_rotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

        result = [x_rotation, y_rotation]

        return result

        
    def print_values():
        print "Gyroscope Data"
        print "Values in degrees per second"
        print "---------"
        print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout_scaled),"°/sec"
        print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout_scaled),"°/sec"
        print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout_scaled),"°/sec"

        print
        print "Accelerometer data"
        print "Values in degrees"
        print "------------------"

        print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled,
        print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled,
        print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled,

        print
        print "x rotation: ",x_rotation,"°"
        print "y rotation: " ,y_rotation,"°"
