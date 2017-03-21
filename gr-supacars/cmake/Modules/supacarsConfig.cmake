INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SUPACARS supacars)

FIND_PATH(
    SUPACARS_INCLUDE_DIRS
    NAMES supacars/api.h
    HINTS $ENV{SUPACARS_DIR}/include
        ${PC_SUPACARS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SUPACARS_LIBRARIES
    NAMES gnuradio-supacars
    HINTS $ENV{SUPACARS_DIR}/lib
        ${PC_SUPACARS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SUPACARS DEFAULT_MSG SUPACARS_LIBRARIES SUPACARS_INCLUDE_DIRS)
MARK_AS_ADVANCED(SUPACARS_LIBRARIES SUPACARS_INCLUDE_DIRS)

