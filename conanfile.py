from conans import ConanFile
import os


class XercesConan(ConanFile):
    name = "xerces-c"
    version = "3.1.4"
    url = "https://github.com/slidewavellc/conan-xerces-c"
    src_dir = "xerces-c"
    license="http://www.apache.org/licenses/LICENSE-2.0.html"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86", "x86_64"]
    }
    options = {
        "with_icu": [True, False],
        "shared": [True, False]
    }
    default_options = "with_icu=False", "shared=False"
    exports = "%s/*" % src_dir


    def config(self):
        del self.settings.compiler.libcxx


    def build(self):
        if self.settings.compiler == "Visual Studio":
            self.build_with_vs()
        else:
            self.build_with_make()

    def package(self):
        build_dir = "{source}/Build/{arch}/{compiler}/{build_type}".format(
                source=self.src_dir,
                arch="x64" if self.settings.arch == "x86_64" else "Win32",
                compiler=self.settings.compiler.version,
                build_type=self.settings.build_type
            )
        self.copy("*.hpp", dst="include", src="%s/src" % self.src_dir)
        self.copy("*.lib", dst="lib", src=self.src_dir, keep_path=False)
        self.copy("*.dll", dst="lib", src=self.src_dir, keep_path=False)
        self.copy("*.a", dst="lib", src=self.src_dir, keep_path=False)
        self.copy("*.so", dst="lib", src=self.src_dir, keep_path=False)


    def package_info(self):
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.includedirs = ['include']
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["xerces-c_3"]
        elif self.settings.os == "Linux":
            self.cpp_info.libs = ["libxerces-c.a"] if not self.options.shared else ['libxerces-c.so']


    def build_with_vs(self):
        solution_path = "xerces-c\\projects\\Win32\\VC{0}\\xerces-all\\xerces-all.sln".format(str(self.settings.compiler.version))
        solution_path = os.path.join(os.path.dirname(__file__), solution_path)
        config_name = str(self.settings.build_type)  # *TODO: other options 
        platform = "x64" if self.settings.arch == "x86_64" else "Win32"
        runtime_map = {
            "MDd": "MultiThreadedDebugDLL",
            "MD": "MultiThreadedDLL",
            "MTd": "MultiThreadedDebug",
            "MT": "MultiThreaded"
        }
        runtime = runtime_map[str(self.settings.compiler.runtime)]
        vs_version = self.settings.compiler.version

        build_cmd = "msbuild \"{solution}\" \"/p:Configuration={config}\" \"/p:Platform={platform}\" \"/p:VisualStudioVersion={vs_version}\" /m".format(
            solution=solution_path,
            config=config_name,
            platform=platform,
            vs_version=vs_version
        )
        self.run(build_cmd)

    # *WARNING: untested!
    def build_with_make(self):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        self.run("cd %s && %s" % (self.src_dir, 'chmod u+x configure'))
        self.run("cd %s/config && %s" % (self.src_dir, 'chmod u+x pretty-make'))
        self.run("cd %s && %s %s" % (self.src_dir, env.command_line, './configure'))
        self.run("cd %s && %s %s" % (self.src_dir, env.command_line, 'make'))

    