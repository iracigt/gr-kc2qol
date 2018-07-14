INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_KC2QOL kc2qol)

FIND_PATH(
    KC2QOL_INCLUDE_DIRS
    NAMES kc2qol/api.h
    HINTS $ENV{KC2QOL_DIR}/include
        ${PC_KC2QOL_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    KC2QOL_LIBRARIES
    NAMES gnuradio-kc2qol
    HINTS $ENV{KC2QOL_DIR}/lib
        ${PC_KC2QOL_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(KC2QOL DEFAULT_MSG KC2QOL_LIBRARIES KC2QOL_INCLUDE_DIRS)
MARK_AS_ADVANCED(KC2QOL_LIBRARIES KC2QOL_INCLUDE_DIRS)

