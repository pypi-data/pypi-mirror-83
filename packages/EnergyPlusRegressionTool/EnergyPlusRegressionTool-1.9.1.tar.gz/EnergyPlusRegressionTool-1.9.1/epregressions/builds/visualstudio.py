import os

from epregressions.builds.base import BaseBuildDirectoryStructure


class CMakeCacheVisualStudioBuildDirectory(BaseBuildDirectoryStructure):
    """
    A Visual Studio based build directory class
    This tries to use a "Release" folder, but if it does not exist it tries to fall back to a "Debug" folder
    """

    def __init__(self):
        super(CMakeCacheVisualStudioBuildDirectory, self).__init__()
        self.source_directory = None
        self.build_mode = 'Release'

    def set_build_mode(self, debug):
        self.build_mode = 'Debug' if debug else 'Release'

    def set_build_directory(self, build_directory):
        """
        This method takes a build directory, and updates any dependent member variables, in this case the source dir.
        This method *does* allow an invalid build_directory, as could happen during program initialization

        :param build_directory:
        :return:
        """
        self.build_directory = build_directory
        if not os.path.exists(self.build_directory):
            self.source_directory = 'unknown - invalid build directory?'
            return
        cmake_cache_file = os.path.join(self.build_directory, 'CMakeCache.txt')
        with open(cmake_cache_file, 'r') as f_cache:
            for this_line in f_cache.readlines():
                if 'CMAKE_HOME_DIRECTORY:INTERNAL=' in this_line:
                    tokens = this_line.strip().split('=')
                    self.source_directory = tokens[1]
                    break
            else:
                raise Exception('Could not find source directory spec in the CMakeCache file')

    def get_idf_directory(self):
        if not self.build_directory:
            raise Exception('Build directory has not been set with set_build_directory()')
        return os.path.join(self.source_directory, 'testfiles')

    def verify(self):
        results = []
        if not self.build_directory:
            raise Exception('Build directory has not been set with set_build_directory()')
        build_dir = self.build_directory
        exists = os.path.exists(build_dir)
        results.append(
            ["Case %s Build Directory Exists? ", build_dir, exists]
        )
        cmake_cache_file = os.path.join(build_dir, 'CMakeCache.txt')
        exists = os.path.exists(cmake_cache_file)
        results.append(
            ["Case %s Build CMake Cache? ", cmake_cache_file, exists]
        )
        source_dir = self.source_directory
        exists = os.path.exists(source_dir)
        results.append(
            ["Case %s Source Directory Exists? ", source_dir, exists]
        )
        test_files_dir = os.path.join(self.source_directory, 'testfiles')
        exists = os.path.exists(test_files_dir)
        results.append(
            ["Case %s Test Files Directory Exists? ", test_files_dir, exists]
        )
        data_sets_dir = os.path.join(self.source_directory, 'datasets')
        exists = os.path.exists(data_sets_dir)
        results.append(
            ["Case %s Data Sets Directory Exists? ", data_sets_dir, exists]
        )
        products_dir = os.path.join(self.build_directory, 'Products')
        exists = os.path.exists(products_dir)
        results.append(
            ["Case %s Products Directory Exists? ", products_dir, exists]
        )
        build_mode_folder = 'Release'
        release_folder = os.path.join(self.build_directory, 'Products', build_mode_folder)
        release_folder_exists = os.path.exists(release_folder)
        if release_folder_exists:
            self.set_build_mode(debug=False)
        else:
            self.set_build_mode(debug=True)
        energy_plus_exe = os.path.join(self.build_directory, 'Products', self.build_mode, 'energyplus.exe')
        exists = os.path.exists(energy_plus_exe)
        results.append(
            ["Case %s EnergyPlus Binary Exists? ", energy_plus_exe, exists]
        )
        basement_exe = os.path.join(self.build_directory, 'Products', 'Basement.exe')
        exists = os.path.exists(basement_exe)
        results.append(
            ["Case %s Basement (Fortran) Binary Exists? ", basement_exe, exists]
        )
        return results

    def get_build_tree(self):
        if not self.build_directory:
            raise Exception('Build directory has not been set with set_build_directory()')
        return {
            'build_dir': self.build_directory,
            'source_dir': self.source_directory,
            'energyplus': os.path.join(self.build_directory, 'Products', self.build_mode, 'energyplus.exe'),
            'basement': os.path.join(self.build_directory, 'Products', 'Basement.exe'),
            'idd_path': os.path.join(self.build_directory, 'Products', 'Energy+.idd'),
            'slab': os.path.join(self.build_directory, 'Products', 'Slab.exe'),
            'basementidd': os.path.join(self.build_directory, 'Products', 'BasementGHT.idd'),
            'slabidd': os.path.join(self.build_directory, 'Products', 'SlabGHT.idd'),
            'expandobjects': os.path.join(self.build_directory, 'Products', 'ExpandObjects.exe'),
            'epmacro': os.path.join(self.source_directory, 'bin', 'EPMacro', 'Linux', 'EPMacro.exe'),
            'readvars': os.path.join(self.build_directory, 'Products', 'ReadVarsESO.exe'),
            'parametric': os.path.join(self.build_directory, 'Products', 'ParametricPreprocessor.exe'),
            'test_files_dir': os.path.join(self.source_directory, 'testfiles'),
            'weather_dir': os.path.join(self.source_directory, 'weather'),
            'data_sets_dir': os.path.join(self.source_directory, 'datasets')
        }
