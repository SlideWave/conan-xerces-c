from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="slidewavellc")
    builder.add({"arch": "x86", "build_type": "Debug"})
    builder.add({"arch": "x86", "build_type": "Release"})
    builder.add({"arch": "x86_64", "build_type": "Debug"})
    builder.add({"arch": "x86_64", "build_type": "Release"})
    builder.run()
