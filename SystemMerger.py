#!/usr/bin/env python
"""
Copyright (C) 2013 TeamHackLG Cybojenix <anthonydking@slimroms.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# concept taken from thecubed's guide on xda
# http://forum.xda-developers.com/showpost.php?p=46486167&postcount=8

from __future__ import print_function
from os import listdir, name, path, remove

print(
      "System Image Merger Copyright (C) 2013 Cybojenix@TeamHackLG\n"
      "This program comes with ABSOLUTELY NO WARRANTY\n"
      "This is free software, and you are welcome to redistribute it\n"
      "under certain conditions\n"
     )

if not name == "posix":
    print("This script is designed for Linux, it may not work on Windows")

def ddrep_write_zero(length, dd_of="system.img"):
    with open(dd_of, "w") as f:
        f.seek((length * 512) - 1)
        f.write("\0")

def dd_replacement(dd_if, offset, dd_of="system.img"):
    with open(dd_if, "r") as f_bin:
        with open(dd_of, "r+b") as f_img:
            f_img.seek(offset*512)
            f_img.write(f_bin.read())


def find_files():
    """
        returns: a list of files found that match the form "system_.*\.bin"
    """
    listing = listdir(".")
    found = []
    for bin_file in listing:
        if bin_file.startswith("system_") and bin_file.endswith(".bin"):
             found.append(bin_file)
    return found


def order_files(system_bins):
    """
        system_bins: a list of the system bins found
                     ex- ["system_455.bin", "system_342.bin"]
        returns: an ordered list with turples based on the numerical data in the file name
                 ex- [("system_342.bin", 342), (system_455.bin", 455)]
    """
    ordered_list = []
    for system_bin in system_bins:
        try:
            x = system_bin.strip("system_").strip(".bin")
        except ValueError:
            raise Exception("the file formatting has changed. Please contact me")
        ordered_list.append(x)
    ordered_list.sort(key=int)

    final_list = []
    for x in ordered_list:
        temp_turple = (int(x), "".join(["system_", x, ".bin"]))
        final_list.append(temp_turple)
    return final_list


def start_image(file_list, offset):
    """
        file_list: a list with turples of the files and numerical data they hold
        offset: the amount of bytes that the system.img is offset by
        returns: nothing
    """
    last = file_list[-1:][0][0]
    size = last # - offset # fudge factor to extend the system image more. allows for mounting
    print("writing zero's to the base of the image. this can take a while")
    ddrep_write_zero(size)


def bin_to_image(file_list, offset):
    """
        file_list: a list with turples of the files and numerical data they hold
        returns: nothing
    """
    for system_bin in file_list:#[1:]:
        seek = str(system_bin[0] - offset)
        print("writing %s to system.img" % system_bin[1])
        dd_replacement(system_bin[1], int(seek))


def print_after():
    if name == "posix":
        print(
              "the system image has been made. to mount it, run\n"
              "...\n"
              "sudo mkdir -p /mnt/lgimg && mount system.img /mnt/lgimg\n"
             )
    else:
        print(
              "the system image has been made. to explore it\n"
              "open it up in ex2explorer\n"
             )
    print(
          "thank you for using a product, brought to you by TeamHackLG.\n"
          "If you have any questions, join is on freenode at #TeamHackLG"
         )
          


def main():
    if path.isfile("system.img"):
        remove("system.img")
    system_files = find_files()
    ordered = order_files(system_files)
    offset = ordered[0][0]
    start_image(ordered, offset)
    bin_to_image(ordered, offset)
    print_after()



if __name__ == '__main__':
    main()
