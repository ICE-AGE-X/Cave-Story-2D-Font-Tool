import struct


def writeInt1(file, value):
    file.write(value.to_bytes(1, "little"))


def writeInt2(file, value):
    file.write(value.to_bytes(2, "little"))

def writeInt4(file, value):
    file.write(value.to_bytes(4, "little"))
    
def writeInt2BE(file, value):
    file.write(value.to_bytes(2, "big"))


def readIntN(file, n):
    return struct.unpack('i', file.read(n))[0]


def readInt4(file):
    return readIntN(file, 4)


def readInt2(file):
    return readIntN(file, 2)


def readInt1(file):
    return readIntN(file, 1)


def readStr(file, size):
    name = file.read(size)
    pos = findEndPos(name)
    return str(name[:pos], encoding="utf-8")


def findEndPos(data):
    idx = 0
    while data[idx] != 0:
        idx += 1
    return idx


def fillByteN(wf, size):
    for i in range(size):
        wf.write(b'\x00')


def padSize128(wf, len):
    padSizeN(wf, len, 128)


def padSizeN(wf, len, n):
    len = len % n
    if len > 0:
        len = n-len
    else:
        return
    for i in range(len):
        wf.write(b'\x00')
    return


def calFixLen(len):
    len = len % 128
    if len > 0:
        return 128-len
    return 0
