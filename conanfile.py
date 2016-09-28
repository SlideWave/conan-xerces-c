from conans import ConanFile
import os


class XercesConan(ConanFile):
    name = "xerces-c"
    version = "3.4.1"
    settings = {
        "os": ["Windows"],
        "compiler": ["Visual Studio"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86", "x86_64"]
    }
    options = {
        "shared": [True, False]
    }
    default_options = "shared=True"
    exports = "xerces-c/*"


    def build(self):
        if self.settings.compiler == "Visual Studio":
            self.build_with_vs()
        else:
            self.build_with_make()

    def package(self):
        self.copy("*.h", dst="include")
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)
        self.copy("*.so", dst="lib", src="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = ["xerces-c"]


    def build_with_vs(self):
        solution_path = "xerces-c\\projects\\Win32\\VC{0}\\xerces-all\\xerces-all.sln".format(str(self.settings.compiler.version))
        solution_path = os.path.join(os.path.dirname(__file__), solution_path)
        config_name = str(self.settings.build_type)
        platform = "x64" if self.settings.arch == "x86_64" else "Win32"
        runtime_map = {
            "MDd": "MultiThreadedDebugDLL",
            "MD": "MultiThreadedDLL",
            "MTd": "MultiThreadedDebug",
            "MT": "MultiThreaded"
        }
        runtime = runtime_map[str(self.settings.compiler.runtime)]
        vs_version = self.settings.compiler.version

        build_cmd = "msbuild \"{solution}\" /t:XercesLib:Build \"/p:Configuration={config}\" \"/p:Platform={platform}\" \"/p:VisualStudioVersion={vs_version}\" /m".format(
            solution=solution_path,
            config=config_name,
            platform="Win32",
            vs_version=vs_version
        )
        self.run(build_cmd)

    def build_with_make(self):
        pass
    