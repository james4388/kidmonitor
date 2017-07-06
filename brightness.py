import ctypes


class Brightness(object):
    iokit = None
    cf = None
    kIOMasterPortDefault = None
    kCFAllocatorDefault = None
    kIOReturnSuccess = 0
    kCFStringEncodingMacRoman = 0
    IODisplayConnect = 'IODisplayConnect'
    kNilOptions = 0
    kIODisplayBrightnessKey = "brightness"

    def __init__(self):
        self.iokit = ctypes.cdll.LoadLibrary(
            ctypes.util.find_library('IOKit'))
        self.cf = ctypes.cdll.LoadLibrary(
            ctypes.util.find_library('CoreFoundation'))
        self.kIOMasterPortDefault = ctypes.c_void_p.in_dll(
            self.iokit, "kIOMasterPortDefault")
        self.iokit.IOServiceGetMatchingServices.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        self.iokit.IOServiceGetMatchingServices.restype = ctypes.c_void_p
        self.iokit.IOObjectRelease.argtypes = [ctypes.c_void_p]
        self.iokit.IOServiceMatching.restype = ctypes.c_void_p
        self.iokit.IOServiceGetMatchingServices.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        self.iokit.IODisplayGetFloatParameter.argtypes = [
            ctypes.c_void_p, ctypes.c_int32, ctypes.c_void_p,
            ctypes.c_void_p
        ]
        self.iokit.IODisplaySetFloatParameter.argtypes = [
            ctypes.c_void_p, ctypes.c_int32, ctypes.c_void_p,
            ctypes.c_float
        ]
        self.iokit.IOServiceGetMatchingServices.restype = ctypes.c_void_p
        self.cf.CFStringCreateWithCString.argtypes = [
            ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int32]
        self.cf.CFStringCreateWithCString.restype = ctypes.c_void_p
        self.kCFAllocatorDefault = ctypes.c_void_p.in_dll(
            self.cf, "kCFAllocatorDefault")

    def CFStr(self, string):
        return self.cf.CFStringCreateWithCString(
            self.kCFAllocatorDefault,
            string.encode("mac_roman"),
            self.kCFStringEncodingMacRoman)

    def get_brightness(self):
        level = ctypes.c_float(1.0)
        if self.iokit:
            iterator = ctypes.c_void_p()
            self.iokit.IOServiceGetMatchingServices(
                self.kIOMasterPortDefault,
                self.iokit.IOServiceMatching(
                    self.IODisplayConnect.encode('mac_roman')
                ), ctypes.byref(iterator))
            while self.iokit.IOIteratorIsValid(iterator):
                service = self.iokit.IOIteratorNext(iterator)
                self.iokit.IODisplayGetFloatParameter(
                    service, self.kNilOptions,
                    self.CFStr(self.kIODisplayBrightnessKey),
                    ctypes.byref(level)
                )
                self.iokit.IOObjectRelease(iterator)
        return level

    def set_brightness(self, level=1.0):
        level = ctypes.c_float(level)
        if self.iokit:
            iterator = ctypes.c_void_p()
            self.iokit.IOServiceGetMatchingServices(
                self.kIOMasterPortDefault,
                self.iokit.IOServiceMatching(
                    self.IODisplayConnect.encode('mac_roman')
                ), ctypes.byref(iterator))
            while self.iokit.IOIteratorIsValid(iterator):
                service = self.iokit.IOIteratorNext(iterator)
                self.iokit.IODisplaySetFloatParameter(
                    service, self.kNilOptions,
                    self.CFStr(self.kIODisplayBrightnessKey),
                    level
                )
                self.iokit.IOObjectRelease(iterator)
                return
