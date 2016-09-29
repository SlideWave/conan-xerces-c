from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "slidewavellc")


class ReuseConan(ConanFile):
    settings = {
        "os": ["Windows"],
        "compiler": ["Visual Studio"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86", "x86_64"]
    }
    requires = "xerces-c/3.4.1@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        self.run(os.sep.join([".","bin","test"]))
