# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "/home/cameron/Documents/Projects/Programming/esp/v5.4/esp-idf/components/bootloader/subproject")
  file(MAKE_DIRECTORY "/home/cameron/Documents/Projects/Programming/esp/v5.4/esp-idf/components/bootloader/subproject")
endif()
file(MAKE_DIRECTORY
  "/home/cameron/Documents/Projects/Programming/GUI/Waveshare/Projects/Template-waveshare_esp32s3_7_inch/build/bootloader"
  "/home/cameron/Documents/Projects/Programming/GUI/Waveshare/Projects/Template-waveshare_esp32s3_7_inch/build/bootloader-prefix"
  "/home/cameron/Documents/Projects/Programming/GUI/Waveshare/Projects/Template-waveshare_esp32s3_7_inch/build/bootloader-prefix/tmp"
  "/home/cameron/Documents/Projects/Programming/GUI/Waveshare/Projects/Template-waveshare_esp32s3_7_inch/build/bootloader-prefix/src/bootloader-stamp"
  "/home/cameron/Documents/Projects/Programming/GUI/Waveshare/Projects/Template-waveshare_esp32s3_7_inch/build/bootloader-prefix/src"
  "/home/cameron/Documents/Projects/Programming/GUI/Waveshare/Projects/Template-waveshare_esp32s3_7_inch/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/cameron/Documents/Projects/Programming/GUI/Waveshare/Projects/Template-waveshare_esp32s3_7_inch/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/cameron/Documents/Projects/Programming/GUI/Waveshare/Projects/Template-waveshare_esp32s3_7_inch/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
