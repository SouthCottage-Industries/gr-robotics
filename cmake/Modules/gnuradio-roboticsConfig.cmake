find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_ROBOTICS gnuradio-robotics)

FIND_PATH(
    GR_ROBOTICS_INCLUDE_DIRS
    NAMES gnuradio/robotics/api.h
    HINTS $ENV{ROBOTICS_DIR}/include
        ${PC_ROBOTICS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_ROBOTICS_LIBRARIES
    NAMES gnuradio-robotics
    HINTS $ENV{ROBOTICS_DIR}/lib
        ${PC_ROBOTICS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-roboticsTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_ROBOTICS DEFAULT_MSG GR_ROBOTICS_LIBRARIES GR_ROBOTICS_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_ROBOTICS_LIBRARIES GR_ROBOTICS_INCLUDE_DIRS)
