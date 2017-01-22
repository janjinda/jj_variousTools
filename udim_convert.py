import os

path = raw_input("What directory do you want to convert? ")
path = path + "/" if not path.endswith("/") else path + ""
directory = os.listdir(path)
separator = "."

directory.remove('.DS_Store')


class UdimConvert(object):
    def uvToUdim(self):

        u = (self.coords.split("u")[-1])[0]
        v = (self.coords.split("v")[-1])[0]

        newU = int(u)

        newV = "%02d" % (int(v) - 1)

        udim = ("1%s%s" % (newV, newU))

        fileNew = ("%s.%s.%s" % (self.filename, udim, self.suffix))

        print ("%s -> %s" % (self.fileOld, fileNew))

        os.rename(path + self.fileOld, path + fileNew)

    def udimToUv(self):

        newU = self.coords[-1]

        newV = int(self.coords[1:3]) + 1

        uv = ("u%s_v%s" % (newU, newV))

        fileNew = ("%s%s%s.%s" % (self.filename, separator, uv, self.suffix))

        print ("%s -> %s" % (self.fileOld, fileNew))

        os.rename(path + self.fileOld, path + fileNew)

    def convertUV(self, type=None):

        for self.fileOld in directory:

            self.filename = self.fileOld.split(separator)[0]
            self.suffix = self.fileOld.split(".")[-1]
            self.coords = self.fileOld.split(separator)[-2]

            if type == 'from':
                self.udimToUv()
            elif type == 'to':
                self.uvToUdim()
            else:
                raise RuntimeError("No conversion type given")


udimConvert = UdimConvert()
user = raw_input("Do you want to convert 'from' or 'to' UDIM? ")
udimConvert.convertUV(type=user)
