# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.2

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/martin/Repos/SafePet/backend/c++

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/martin/Repos/SafePet/backend/c++/build

# Include any dependencies generated for this target.
include CMakeFiles/lbp.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/lbp.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/lbp.dir/flags.make

CMakeFiles/lbp.dir/main.cpp.o: CMakeFiles/lbp.dir/flags.make
CMakeFiles/lbp.dir/main.cpp.o: ../main.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/martin/Repos/SafePet/backend/c++/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/lbp.dir/main.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/lbp.dir/main.cpp.o -c /home/martin/Repos/SafePet/backend/c++/main.cpp

CMakeFiles/lbp.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/lbp.dir/main.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/martin/Repos/SafePet/backend/c++/main.cpp > CMakeFiles/lbp.dir/main.cpp.i

CMakeFiles/lbp.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/lbp.dir/main.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/martin/Repos/SafePet/backend/c++/main.cpp -o CMakeFiles/lbp.dir/main.cpp.s

CMakeFiles/lbp.dir/main.cpp.o.requires:
.PHONY : CMakeFiles/lbp.dir/main.cpp.o.requires

CMakeFiles/lbp.dir/main.cpp.o.provides: CMakeFiles/lbp.dir/main.cpp.o.requires
	$(MAKE) -f CMakeFiles/lbp.dir/build.make CMakeFiles/lbp.dir/main.cpp.o.provides.build
.PHONY : CMakeFiles/lbp.dir/main.cpp.o.provides

CMakeFiles/lbp.dir/main.cpp.o.provides.build: CMakeFiles/lbp.dir/main.cpp.o

CMakeFiles/lbp.dir/lbp.cpp.o: CMakeFiles/lbp.dir/flags.make
CMakeFiles/lbp.dir/lbp.cpp.o: ../lbp.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/martin/Repos/SafePet/backend/c++/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/lbp.dir/lbp.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/lbp.dir/lbp.cpp.o -c /home/martin/Repos/SafePet/backend/c++/lbp.cpp

CMakeFiles/lbp.dir/lbp.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/lbp.dir/lbp.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/martin/Repos/SafePet/backend/c++/lbp.cpp > CMakeFiles/lbp.dir/lbp.cpp.i

CMakeFiles/lbp.dir/lbp.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/lbp.dir/lbp.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/martin/Repos/SafePet/backend/c++/lbp.cpp -o CMakeFiles/lbp.dir/lbp.cpp.s

CMakeFiles/lbp.dir/lbp.cpp.o.requires:
.PHONY : CMakeFiles/lbp.dir/lbp.cpp.o.requires

CMakeFiles/lbp.dir/lbp.cpp.o.provides: CMakeFiles/lbp.dir/lbp.cpp.o.requires
	$(MAKE) -f CMakeFiles/lbp.dir/build.make CMakeFiles/lbp.dir/lbp.cpp.o.provides.build
.PHONY : CMakeFiles/lbp.dir/lbp.cpp.o.provides

CMakeFiles/lbp.dir/lbp.cpp.o.provides.build: CMakeFiles/lbp.dir/lbp.cpp.o

CMakeFiles/lbp.dir/histogram.cpp.o: CMakeFiles/lbp.dir/flags.make
CMakeFiles/lbp.dir/histogram.cpp.o: ../histogram.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/martin/Repos/SafePet/backend/c++/build/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/lbp.dir/histogram.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/lbp.dir/histogram.cpp.o -c /home/martin/Repos/SafePet/backend/c++/histogram.cpp

CMakeFiles/lbp.dir/histogram.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/lbp.dir/histogram.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/martin/Repos/SafePet/backend/c++/histogram.cpp > CMakeFiles/lbp.dir/histogram.cpp.i

CMakeFiles/lbp.dir/histogram.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/lbp.dir/histogram.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/martin/Repos/SafePet/backend/c++/histogram.cpp -o CMakeFiles/lbp.dir/histogram.cpp.s

CMakeFiles/lbp.dir/histogram.cpp.o.requires:
.PHONY : CMakeFiles/lbp.dir/histogram.cpp.o.requires

CMakeFiles/lbp.dir/histogram.cpp.o.provides: CMakeFiles/lbp.dir/histogram.cpp.o.requires
	$(MAKE) -f CMakeFiles/lbp.dir/build.make CMakeFiles/lbp.dir/histogram.cpp.o.provides.build
.PHONY : CMakeFiles/lbp.dir/histogram.cpp.o.provides

CMakeFiles/lbp.dir/histogram.cpp.o.provides.build: CMakeFiles/lbp.dir/histogram.cpp.o

# Object files for target lbp
lbp_OBJECTS = \
"CMakeFiles/lbp.dir/main.cpp.o" \
"CMakeFiles/lbp.dir/lbp.cpp.o" \
"CMakeFiles/lbp.dir/histogram.cpp.o"

# External object files for target lbp
lbp_EXTERNAL_OBJECTS =

lbp: CMakeFiles/lbp.dir/main.cpp.o
lbp: CMakeFiles/lbp.dir/lbp.cpp.o
lbp: CMakeFiles/lbp.dir/histogram.cpp.o
lbp: CMakeFiles/lbp.dir/build.make
lbp: /usr/lib64/libopencv_videostab.so.2.4.11
lbp: /usr/lib64/libopencv_ts.so.2.4.11
lbp: /usr/lib64/libopencv_superres.so.2.4.11
lbp: /usr/lib64/libopencv_stitching.so.2.4.11
lbp: /usr/lib64/libopencv_ocl.so.2.4.11
lbp: /usr/lib64/libopencv_gpu.so.2.4.11
lbp: /usr/lib64/libopencv_contrib.so.2.4.11
lbp: /usr/lib64/libopencv_photo.so.2.4.11
lbp: /usr/lib64/libopencv_legacy.so.2.4.11
lbp: /usr/lib64/libopencv_video.so.2.4.11
lbp: /usr/lib64/libopencv_objdetect.so.2.4.11
lbp: /usr/lib64/libopencv_ml.so.2.4.11
lbp: /usr/lib64/libopencv_calib3d.so.2.4.11
lbp: /usr/lib64/libopencv_features2d.so.2.4.11
lbp: /usr/lib64/libopencv_highgui.so.2.4.11
lbp: /usr/lib64/libopencv_imgproc.so.2.4.11
lbp: /usr/lib64/libopencv_flann.so.2.4.11
lbp: /usr/lib64/libopencv_core.so.2.4.11
lbp: CMakeFiles/lbp.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable lbp"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/lbp.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/lbp.dir/build: lbp
.PHONY : CMakeFiles/lbp.dir/build

CMakeFiles/lbp.dir/requires: CMakeFiles/lbp.dir/main.cpp.o.requires
CMakeFiles/lbp.dir/requires: CMakeFiles/lbp.dir/lbp.cpp.o.requires
CMakeFiles/lbp.dir/requires: CMakeFiles/lbp.dir/histogram.cpp.o.requires
.PHONY : CMakeFiles/lbp.dir/requires

CMakeFiles/lbp.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/lbp.dir/cmake_clean.cmake
.PHONY : CMakeFiles/lbp.dir/clean

CMakeFiles/lbp.dir/depend:
	cd /home/martin/Repos/SafePet/backend/c++/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/martin/Repos/SafePet/backend/c++ /home/martin/Repos/SafePet/backend/c++ /home/martin/Repos/SafePet/backend/c++/build /home/martin/Repos/SafePet/backend/c++/build /home/martin/Repos/SafePet/backend/c++/build/CMakeFiles/lbp.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/lbp.dir/depend

