import os
import imp
import zipfile

from dbnd import __version__ as version, relative_path


libs_list = ["dbnd", "dbnd_aws", "dbnd_spark", "dbnd_qubole"]


def build_source_zip(lib):
    zip_file_name = lib + ".zip"
    zip_file = zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED)
    entry_point_file = relative_path(__file__, "entry_points", lib, "entry_points.txt")
    dist_info_dir_name = "{}-{}.dist-info".format(lib, version)
    zip_file.write(dist_info_dir_name)
    zip_file.write(entry_point_file, os.path.join(dist_info_dir_name, entry_point_file))
    module_path = imp.find_module(lib)[1]
    zip_file.write(module_path)
    return zip_file_name


def build_databand_sources_zips():
    for lib in libs_list:
        build_source_zip(lib)



