# Process this file with autoconf to produce a configure script.

# AC_PREREQ(2.59)
AC_INIT([qore-glut-module], [0.0.3],
        [David Nichols <nicholsman@gmail.com>],
        [qore-glut-module])
AM_INIT_AUTOMAKE
AC_CONFIG_HEADER([config.h])

AC_LANG(C++)
AC_PROG_CXX
AC_PROG_CC
AC_DISABLE_STATIC
AC_LIBTOOL_DLOPEN
AM_PROG_LIBTOOL
AC_PROG_INSTALL

# fix for building with older autotools
if test ! -d m4; then mkdir m4; fi

AC_CONFIG_MACRO_DIR([m4])

# set system variables
OS=`uname -s`
if test "$OS" = "HP-UX"; then
   if test "$host_cpu" = "ia64"; then
      ARCH=itanium
   else
      ARCH=PA-RISC
   fi
else
   ARCH=`uname -p`
   if test "$ARCH" = unknown; then
      ARCH=`uname -m`
   fi
   if test $ARCH = i686 -o $ARCH = i586 -o $ARCH = athlon ; then
      ARCH=i386
   fi
fi

# set find prefix
if test -n "$prefix" -a "$prefix" != "NONE"; then
   find_prefix="$prefix"
fi

#AC_CANONICAL_HOST
# get CPU family
case "${host_cpu}" in
   i[[3456]]86) cpu_family=i386 ;;
   amd64)       cpu_family=x86_64 ;;
   *)           cpu_family=${host_cpu} ;;
esac

# set OS-specific variables
SHLIB_SUFFIX=so
#echo host_os=${host_os}sss
case "${host_os}" in
     *linux*)   # set compile flags for Linux
		CPPFLAGS="${CPPFLAGS} -D_GNU_SOURCE"
		SHLIB_SUFFIX=so
		AC_DEFINE(LINUX, 1, if compiling on Linux)
		;;
     *solaris*) # set compile flags for Solaris
		CPPFLAGS="${CPPFLAGS} -D_POSIX_C_SOURCE=199506L -D_XPG4_2 -D_XPG5 -D__EXTENSIONS__"
		# for checking for some network functions on Solaris
		LDFLAGS="$LDFLAGS -lnsl"
		# assume we are using CC if not using g++, add -norunpath to link flags in this case
		if test "$GXX" != "yes"; then
		   CXXFLAGS="${CXXFLAGS} -mt"
		   LDFLAGS="$LDFLAGS -norunpath -mt"
		fi
		AC_DEFINE(SOLARIS, 1, if compiling on Solaris)
		# add -ldl to libs if on Solaris 8
		if test "${host_os}" = "solaris2.8"; then
		   OTHER_LIBS="$OTHER_LIBS -ldl"
		fi
		solaris=yes
	        ;;
     *darwin*)  SHLIB_SUFFIX=dylib
		# libtool 1.5.* is creating modules on Darwin 8.* (OS/X 10.4.*) with a .so suffix for some reason
		MODULE_SUFFIX=so
		AC_DEFINE(DARWIN, 1, [if compiling on Darwin])
		# use gnutar on darwin to avoid getting those pesky resource files
		AMTAR=gnutar
		darwin=true
		;;
     *hpux*)    if test "$host_cpu" = "ia64"; then
     		   SHLIB_SUFFIX=so
		else  # assume hppa (PA-RISC)
     		   SHLIB_SUFFIX=sl
		   AC_DEFINE(SHLIB_SUFFIX, "sl", shared library suffix)
		fi
		# add "-AA" and -D__STDC_EXT__ to aCC commandline to enable a clean compile
		if test -n "`echo $CXX|grep aCC`"; then
		   CXXFLAGS="$CXXFLAGS -AA -D__STDC_EXT__ -D_RWSTD_MULTI_THREAD"
		fi
		AC_DEFINE(HPUX, 1, if compiling on HP-UX)
		;;
esac
AC_SUBST(SHLIB_SUFFIX)
if test -z "$MODULE_SUFFIX" ; then
   MODULE_SUFFIX=$SHLIB_SUFFIX
fi
AC_SUBST(MODULE_SUFFIX)

AC_ARG_ENABLE([64bit],
  [AS_HELP_STRING([--enable-64bit],
		  [enable 64bit support (default: auto)])],
  [case "${enable_64bit}" in
       yes|no) ;;
       *)      AC_MSG_ERROR(bad value ${enable_64bit} for --enable-64bit) ;;
      esac],
  [enable_64bit=auto])

if test "$enable_64bit" = "auto"; then
   # turn on 64-bit by default if compiling on itanium or x86_64
   if test "$host_cpu" = "ia64" -o "$host_cpu" = "x86_64" -o "$host_cpu" = "amd64"; then
      enable_64bit=yes
   else
      case "${host_os}" in
          darwin*)   mv=`uname -r|cut -f1 -d.`
     	   	     if test $mv -ge 10 -a "${host_cpu}" = "i386"; then
		         enable_64bit=yes
		     fi
		     ;;
	  solaris*)  if test "${host_cpu}" = "i386"; then
			 # if we are running on a 64-bit machine, then enable a 64-bit build
			 if test -n "`isainfo -v 2>/dev/null| grep 64-bit`"; then
			     enable_64bit=yes
			 fi
		     fi
		     ;;
      esac
      if test "$enable_64bit" = "auto"; then
	  enable_64bit=no
      fi
   fi
fi

# allow users to explicitly set libsuffix
AC_ARG_WITH([libsuffix],
  [AS_HELP_STRING([--with-libsuffix@<:@=LIBSUFFIX@:>@],
                  [explitily set libsuffix])],
  [LIBSUFFIX=$with_libsuffix; LIBSUFFIX_SET=yes;AC_SUBST(LIBSUFFIX)],
  [])

# see if we know how to set flags properly for different hosts and architectures
# FIXME: add test on HP-UX if the compiler can generate the appropriate binaries
if test "$enable_64bit" = "yes"; then
   case "${host_os}" in
      *linux*)	if test "$GXX" = "yes" -a "$ARCH" != "aarch64"; then
		   CXXFLAGS="$CXXFLAGS -m64"
		fi
		# only set LIBSUFFIX=64 if /usr/lib64 exists
		if test "$LIBSUFFIX_SET" != "yes"; then
		  if test -d /usr/lib64; then
		     LIBSUFFIX=64
                  fi
		  target="${host_cpu}-${host_os}"
		  if test -d /usr/lib/$target; then
		     LIBSUFFIX=/$target
                  fi
		  AC_SUBST(LIBSUFFIX)
		fi
		;;
      *hpux*)	if test "$host_cpu" = "ia64"; then
                    if test -n "`echo $CXX|grep aCC`"; then
                        CXXFLAGS="$CXXFLAGS +DD64"
                    elif test "$GXX" = "yes"; then
                        CXXFLAGS="$CXXFLAGS -mlp64"
                    fi
                else
		    if test -n "`echo $CXX|grep aCC`"; then
		        CXXFLAGS="$CXXFLAGS +DA2.0W"
		    elif test "$GXX" = "yes"; then
			CXXFLAGS="$CXXFLAGS -march=2.0"
		    fi
		fi
		;;
     *solaris*) if test "$GXX" = "yes"; then
		    if test "$host_cpu" = "sparc"; then
		        CXXFLAGS="$CXXFLAGS -mcpu=ultrasparc3 -m64"  # NOTE we compile for minimum ultrasparc 3 in 64-bit mode
		    else
		        CXXFLAGS="$CXXFLAGS -m64"
		    fi
		else
		    CC_MAJOR=`$CXX -V 2>&1 | head -1| cut -f1 -d.|cut -d\  -f4`
		    CC_MINOR=`$CXX -V 2>&1 | head -1| cut -f2 -d.|cut -d\  -f1`
		    if test "$CC_MAJOR" -gt 5 -o \( "$CC_MAJOR" -eq 5 -a "$CC_MINOR" -ge 10 \); then
		        CXXFLAGS="$CXXFLAGS -m64"
		    else
			CXXFLAGS="$CXXFLAGS -xarch=generic64"
		    fi
		fi
		;;
     *darwin*)	if test "$GXX" = "yes"; then
		   CXXFLAGS="$CXXFLAGS -m64"
		fi
		# set ARCH to x86_64 to be consistent with other intel 64-bit builds
		if test "$host_cpu" = "i386"; then
		   ARCH=x86_64
		fi
		;;
   esac
   SYBLIBSUFFIX=64
   RVLIBSUFFIX=64
   bits=64
else
   case "${host_os}" in
     *linux*)	if test "$GXX" = "yes"; then
		   CXXFLAGS="$CXXFLAGS -m32"
		fi
                # multiarch
		if test "$LIBSUFFIX_SET" != "yes"; then
                  if test -a "$host_cpu" = "x86_64" -a -d /usr/lib32; then
                     LIBSUFFIX=32
                  fi
                  AC_SUBST(LIBSUFFIX)
		fi
		;;
     *darwin*)  if test "$GXX" = "yes"; then
                   CXXFLAGS="$CXXFLAGS -m32"
                fi
                ;;
     *hpux*)	if test "$host_cpu" != "ia64"; then
		    if test "$GXX" = "yes"; then
		        CXXFLAGS="$CXXFLAGS -march=2.0"
		    elif test -n "`echo $CXX|grep aCC`" -a "$host_cpu" != "ia64"; then
		        CXXFLAGS="$CXXFLAGS +DA2.0N"   # NOTE we compile for PA-RISC 2.0 32-bit, not PA-RISC 1.1
		    fi
		fi
		;;
     *solaris*) if test "$GXX" = "yes"; then
		    if test "$host_cpu" = "sparc"; then
		        CXXFLAGS="$CXXFLAGS -mcpu=v8 -m32"
		    else
		        CXXFLAGS="$CXXFLAGS -m32"
		    fi
		else
		    CXXFLAGS="$CXXFLAGS -xarch=generic"
		fi
		;;
   esac
   if test "$host_cpu" = "x86_64"; then
      cpu_family=i386
   fi
   bits=32
fi

# test for C++11
AX_CXX_COMPILE_STDCXX_11([noext], [mandatory])
if test "$HAVE_CXX11" = "1"; then
    AM_CXXFLAGS=-std=gnu++11
fi

# checks for how to build threads
ACX_PTHREAD
if test "$acx_pthread_ok" = "no"; then
   AC_MSG_ERROR(POSIX threads do not seem to be supported on this platform, aborting)
fi
CXXFLAGS="$CXXFLAGS $PTHREAD_CFLAGS"
#LDFLAGS="$LDFLAGS $PTHREAD_LIBS"

AC_ARG_ENABLE([single-compilation-unit],
  [AS_HELP_STRING([--enable-single-compilation-unit],
                  [enable compilation as a single unit (default: on)])],
  [case "${enable_single_compilation_unit}" in
       yes|no) ;;
       *)      AC_MSG_ERROR(bad value ${enable_single_compilation_unit} for --enable-single-compilation-unit) ;;
      esac],
  [enable_single_compilation_unit=yes])


set_qore_cppflags() {
    QORE_INC_DIR=$1
    if test "$1" != "/usr/include"; then
        QORE_CPPFLAGS=-I$1
    fi
}

find_qore() {
    a="$1"
    if test \( "$a" = "/" -o -z "$a" \) -a -h "$a/lib${LIBSUFFIX}"; then
        a=/usr
    fi
    lib=$a/lib${LIBSUFFIX}

    # if we only want the static qore libraries
    if test -n "$qore_static"; then
        if test -f "$lib/libqore.a"; then
            QORE_LDFLAGS="$lib/libqore.a"
            AC_MSG_RESULT([$lib (forced static)])
        fi
    else
        if test -f "$lib/libqore.${SHLIB_SUFFIX}"; then
            if test "$lib" != "/lib" -a "$lib" != "/usr/lib"; then
                QORE_LDFLAGS="-L$lib"
            fi
            QORE_LDFLAGS="$QORE_LDFLAGS -lqore"
            AC_MSG_RESULT([$lib (shared)])
        elif test -f "$lib/libqore.a"; then
            if test "$lib" != "/lib" -a "$lib" != "/usr/lib"; then
                QORE_LDFLAGS="-L$lib"
            fi
            QORE_LDFLAGS="$QORE_LDFLAGS -lqore"
            AC_MSG_RESULT([$lib (static)])
        fi
    fi
    if test -z "$QORE_LDFLAGS"; then
        return
    fi

    AC_MSG_CHECKING([for qore include files])
    # try to find include files
    if test "$a" = "/"; then
        inc=/usr/include
    else
        inc=$a/include
    fi
    if test -f "$inc/qore/Qore.h"; then
        AC_MSG_RESULT([found: $inc])
        set_qore_cppflags $inc
    else
        AC_MSG_ERROR([not found])
    fi

    AC_SUBST(QORE_LDFLAGS)
    AC_SUBST(QORE_CPPFLAGS)
}

# see if we can figure out where the qore library is
AC_ARG_WITH([qore-dir],
  [AS_HELP_STRING([--with-qore-dir@<:@=DIR@:>@],
                  [Qore directory])],
  [if test ! -d "${with_qore_dir}"; then AC_MSG_ERROR(bad value ${with_qore_dir} for --with-qore-dir); unset with_qore_dir; fi],
  [with_qore_dir="$QORE_DIR"])

AC_MSG_CHECKING([for qore libraries and header files])
for dir in "${with_qore_dir}" "${find_prefix}" /usr / /usr/local /opt/gnu /opt/qore /usr/local/qore /opt/local /sw /usr/sfw /opt/sfw; do
    find_qore $dir
    if test -n "$QORE_LDFLAGS"; then
        break
    fi
done
if test -z "$QORE_LDFLAGS"; then
    AC_MSG_ERROR([no qore library found])
else
   # test qore version
   AC_MSG_CHECKING([qore library version])

   # get qore version code
   qvc=`grep QORE_VERSION_CODE $QORE_INC_DIR/qore/qore-version.h|cut -f3 -d\  2>/dev/null`

   # get qore version string
   qore_version=`grep QORE_VERSION.\" $QORE_INC_DIR/qore/qore-version.h|cut -f3 -d\ |sed s/\"//g 2>/dev/null`

   # if version code not present, may be qore 0.7.0 or earlier
   if test -z "$qvc"; then
      qv_major=`grep QORE_VERSION_MAJOR $QORE_INC_DIR/qore/qore-version.h|cut -f3 -d\  2>/dev/null`
      if test -z "$qv_major"; then
         AC_MSG_ERROR([cannot determine; check Qore header files in $QORE_INC_DIR])
      fi

      qv_minor=`grep QORE_VERSION_MINOR $QORE_INC_DIR/qore/qore-version.h|cut -f3 -d\  2>/dev/null`
      qv_sub=`grep QORE_VERSION_SUB $QORE_INC_DIR/qore/qore-version.h|cut -f3 -d\  2>/dev/null`

      if test "$qv_major" -gt 0; then
         qvc=`printf "%d%02d%02d" $qv_major $qv_minor $qv_sub`
      else
         qvc=`printf "%d%02d" $qv_major $qv_minor $qv_sub`
      fi
      AC_DEFINE_UNQUOTED([QORE_VERSION_CODE], $qvc, [define when missing in Qore headers])
   fi

   if test $qvc -lt 812; then
      AC_MSG_ERROR([found $qore_version; this module requires at least version 0.8.12])
   fi

   AC_MSG_RESULT([${qore_version} OK])

   MODULE_API=`qore --module-api`
   AC_SUBST(MODULE_API)

   if test -z "${prefix}" -o "${prefix}" = "NONE"; then
      libdir=`qore --module-dir`
   else
      libdir="$prefix/lib${LIBSUFFIX}/qore-modules"
      qlibdir=`qore --module-dir`
      if test "$libdir" != "$qlibdir"; then
         AC_MSG_WARN([warning, installed qore's module dir is $qlibdir, this module will be installed in $libdir])
      fi
   fi
fi

AC_ARG_ENABLE([profile],
     [AS_HELP_STRING([--enable-profile],
		     [turn on profiling support (default=no)])],
     [case "${enable_profile}" in
       yes|no) ;;
       *)      AC_MSG_ERROR(bad value ${enable_profile} for --enable-profile) ;;
      esac],
     [enable_profile=no])

AC_ARG_ENABLE([debug],
     [AS_HELP_STRING([--enable-debug],
		     [turn on debugging (default=no)])],
     [case "${enable_debug}" in
       yes|no) ;;
       *)      AC_MSG_ERROR(bad value ${enable_debug} for --enable-debug) ;;
      esac],
     [enable_debug=yes])

if test "${enable_debug}" = yes; then
   AC_DEFINE(DEBUG, 1, Define if debugging support should be included)
   # remove -O2 from CXXFLAGS so valgrind can report properly
   CXXFLAGS=`echo $CXXFLAGS | sed 's/\-O2//'`
else
   AC_DEFINE(NDEBUG, 1, Define if assert() declarations should be suppressed)
fi

if test "${enable_profile}" = yes; then
   AC_DEFINE(PROFILE, 1, Define if profiling support should be included)
fi

AC_ARG_ENABLE([optimization],
     [AS_HELP_STRING([--enable-optimization],
		     [turn on optimization (default=auto (yes unless debugging is enabled)])],
     [case "${enable_optimization}" in
       yes|no) ;;
       *)      AC_MSG_ERROR(bad value ${enable_optimization} for --enable-optimization) ;;
      esac],
     [enable_optimization=auto])

if test "$enable_optimization" = "auto"; then
   if test "${enable_debug}" = yes; then
      enable_optimization=no
   else
      enable_optimization=yes
   fi
fi

# check for gcc visibility support
AC_MSG_CHECKING([for gcc visibility support])
if test "$GXX" = "yes"; then
   gcc_version=`$CXX -dumpversion`
   if test "$gcc_version" \> "4"; then
      AC_DEFINE(HAVE_GCC_VISIBILITY, 1, if compiling with g++ and visibility support is available)
      AC_MSG_RESULT([yes, $CXX $gcc_version])
      # we no longer set visibility to hidden by default because it makes RTTI symbols invisible
      # all functions in the library are tagged anyway
      #CXXFLAGS="$CXXFLAGS -fvisibility=hidden"
   else
      AC_MSG_RESULT([no, gcc $gcc_version])
   fi
else
   AC_MSG_RESULT([no, $CXX])
fi

AC_ARG_WITH([glut],
    [AS_HELP_STRING([--with-glut@<:@=DIR@:>@],
                    [glut base directory])],
    [if test "${with_glut}" != "no" -a ! -d "${with_glut}"; then AC_MSG_ERROR(directory ${with_glut} does not exist for --with-glut); unset with_glut; fi])

AC_ARG_WITH([glut-libs],
    [AS_HELP_STRING([--with-glut-libs@<:@=DIR@:>@],
                    [glut library directory])],
    [if test ! -d "${with_glut_libs}"; then AC_MSG_ERROR(directory ${with_glut_libs} does not exist for --with-glut-libs); unset with_glut_libs; fi])

AC_ARG_WITH([glut-includes],
    [AS_HELP_STRING([--with-glut-includes@<:@=DIR@:>@],
                    [glut include file parent directory])],
    [if test ! -d "${with_glut_includes}"; then AC_MSG_ERROR(directory ${with_glut_includes} does not exist for --with-glut-includes); unset with_glut_includes; fi])

check_glut_include() {
    if test -f "$1/glut.h"; then
       found_glut_includes=$1
    elif test -f "$1/GL/glut.h"; then
       found_glut_includes=$1/GL
    elif test -f "$1/glut/glut.h"; then
       found_glut_includes=$1/glut
    elif test "$2" = "err"; then
       AC_MSG_ERROR([$1 is not a valid glut parent include directory])
    fi
}

check_glut_lib() {
    if test -f "$1/libglut.${SHLIB_SUFFIX}"; then
       found_glut_libs=$lib
    elif test "$2" = "err"; then
    	AC_MSG_ERROR([$1 is not a valid glut library directory])
    fi
}

check_glut() {
    a="$1"
    if test \( "$a" = "/" -o -z "$a" \) -a -h "$a/lib${LIBSUFFIX}"; then
        a=/usr
    fi

    if test -z "$with_glut_includes"; then
        inc="$a/include"
        if test "$a" = "/"; then
       	    inc=/usr/include
        fi
	check_glut_include $inc

	if test -z "$found_glut_includes"; then
	    #echo DBG: glut $a $inc includes not found
       	    return
    	fi
	with_glut_includes="$found_glut_includes"
	unset found_glut_includes
    fi

    if test -z "$with_glut_libs"; then
        lib="$a/lib${LIBSUFFIX}"

	check_glut_lib $lib
    	if test -z "$found_glut_libs"; then
       	    #echo DBG: glut $a $lib libs not found
       	    unset with_glut_includes
       	    return
    	fi
	with_glut_libs="$found_glut_libs"
    fi
    if test "$with_glut_libs" != "/lib${LIBSUFFIX}"; then
        glut_app_libs=true
    fi
}

# see if we can figure out where the glut include files and libraries are
if test "${with_glut}" != "no"; then
   AC_MSG_CHECKING([for glut includes and libraries])

   if test -n "$with_glut_includes" -a -n "$with_glut_libs"; then
      check_glut_includes "$with_glut_includes" err
      check_glut_libs "$with_glut_libs" err
   else
      if test -n "$with_glut"; then
      	 check_glut "$with_glut"
      	 if test -z "$with_glut_includes"; then
	    AC_MSG_ERROR([not found in $with_glut])
      	 fi
      else
         # check for frameworks on darwin
	 if test -n "$darwin" -a -d /System/Library/Frameworks/GLUT.framework; then
	    glut_framework="/System/Library/Frameworks"
	    GLUT_INCLUDES="-I /System/Library/Frameworks/GLUT.framework/Headers"
	    GLUT_LIBS="-framework GLUT"
	 else
	    for dir in $GLUT_DIR / /usr /usr/X11 /usr/X11R6 /usr/openwin /usr/local /opt/glut /usr/glut /sw /opt/local /opt/sfw /usr/sfw /opt/gnu; do
      	       check_glut $dir
      	       if test -n "$with_glut_includes"; then
	          break;
      	       fi
   	    done
         fi
      fi
   fi

   if test -n "$glut_framework"; then
      AC_MSG_RESULT([using Darwin frameworks in $glut_framework])
      with_glut=yes
   else
      if test -n "$with_glut_includes"; then
         if test -n "$glut_static"; then
	    AC_MSG_RESULT([includes=$with_glut_includes, libs=$with_glut_libs (static)])
      	 else
	    AC_MSG_RESULT([includes=$with_glut_includes, libs=$with_glut_libs (shared)])
      	 fi
      	 with_glut=yes
      else
	 AC_MSG_ERROR([not found])
         unset with_glut
      fi
   fi
fi

if test "${with_glut}" = yes; then
  if test -n "$with_glut_includes" -o -n "$glut_framework"; then
     if test -z "$GLUT_INCLUDES"; then
        GLUT_INCLUDES="-I$with_glut_includes"
     fi
     if test -z "$GLUT_LIBS"; then
	GLUT_LIBS="-lglut"
	if test -n "$glut_app_libs"; then
	   GLUT_LIBS="-L$with_glut_libs $GLUT_LIBS"
	fi
     fi

     # check if C++ compiler can link with GLUT libs
     SAVE_CXXFLAGS="$CXXFLAGS"
     SAVE_LDFLAGS="$LDFLAGS"
     CXXFLAGS="$CXXFLAGS $GLUT_INCLUDES"
     LDFLAGS="$LDFLAGS $GLUT_LIBS"
     AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[
#include <glut.h>
	 ]],[[
   glutInit(0, 0);
	]])], glut_links=yes, glut_links=no)

     CXXFLAGS="$SAVE_CXXFLAGS"
     LDFLAGS="$SAVE_LDFLAGS"

     if test "$glut_links" = "no"; then
        AC_MSG_ERROR([could not compile a test glut program])
     else
        AC_SUBST(GLUT_INCLUDES)
	AC_SUBST(GLUT_LIBS)
        with_glut=yes
     fi
  else
     AC_MSG_WARN([no glut libraries or includes found, disabling glut support])
     unset with_glut
  fi
fi

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_CONST
AC_C_INLINE
AC_TYPE_PID_T
AC_TYPE_SIZE_T
AC_CHECK_MEMBERS([struct stat.st_blksize])
AC_STRUCT_ST_BLOCKS
AC_CHECK_MEMBERS([struct stat.st_rdev])
AC_HEADER_TIME
AC_STRUCT_TM
AC_C_VOLATILE

# turn on optimizations if we know how
if test "$enable_optimization" = "yes"; then
    if test "$GXX" = "yes"; then
        CXXFLAGS="$CXXFLAGS -O3"  # gcc
    elif test "$CXX" = "CC" -a "`echo $host_os|cut -b-7`" = "solaris"; then
        # remove -g with Solaris CC as it reduces optimization levels
	CXXFLAGS="`echo $CXXFLAGS| sed s/-g//` -xO5" # Solaris CC
    elif test -n "`echo $CXX|grep aCC`"; then 
        # remove -g with HP-UX aCC as it reduces optimization levels
	CXXFLAGS="`echo $CXXFLAGS| sed s/-g//` +O4" # HP-UX aCC
    fi
else
    if test "$GXX" = "yes"; then
        CXXFLAGS="`echo $CXXFLAGS| sed s/-O2//`"  # gcc
    fi
fi

# turn on some build flags for non-debugging, non-profiling builds
#if test "$enable_debug" = "no" -a "$enable_profile" = "no" -a "$enable_optimization" = "yes" ; then
    # we can no longer strip binaries and libraries with non-debugging, non-profiling builds on Darwin with -Wl,-x because it breaks linking :(
#fi

# turn on warnings if we know how
if test "$GXX" = "yes"; then
   CXXFLAGS="$CXXFLAGS -Wall"  # gcc
else
   if test "$solaris" = yes; then
      # turn on all warnings for the oracle sun studio compiler
      CXXFLAGS="$CXXFLAGS +w"
   fi
fi

AC_SUBST(OTHER_LIBS)

# save more version information in config.h
MODULE_VERSION_MAJOR=`echo $PACKAGE_VERSION | cut -f3 -d\  | sed s/\"//g | cut -f1 -d.`
MODULE_VERSION_MINOR=`echo $PACKAGE_VERSION | cut -f3 -d\  | sed s/\"//g | cut -f2 -d.`
MODULE_VERSION_SUB=`echo $PACKAGE_VERSION | cut -f3 -d\  | sed s/\"//g | cut -f3 -d.`

# set version information
AC_DEFINE_UNQUOTED([MODULE_VERSION_MAJOR], $MODULE_VERSION_MAJOR, [major version number])
AC_DEFINE_UNQUOTED([MODULE_VERSION_MINOR], $MODULE_VERSION_MINOR, [minor version number])
AC_DEFINE_UNQUOTED([MODULE_VERSION_SUB], $MODULE_VERSION_SUB, [sub version number])
AC_DEFINE_UNQUOTED([MODULE_TARGET_ARCH], "$ARCH", [host type])
AC_DEFINE_UNQUOTED([MODULE_TARGET_OS], "$OS", [host type])
AC_DEFINE_UNQUOTED([MODULE_TARGET_BITS], $bits, [32 or 64 bit build])

AM_CONDITIONAL([COND_DEBUG],      [test "$enable_debug" = yes])
AM_CONDITIONAL([COND_PROFILE],    [test "$enable_profile" = yes])
AM_CONDITIONAL([COND_SINGLE_COMPILATION_UNIT], [test "$enable_single_compilation_unit" = yes])

AC_CONFIG_FILES([Makefile src/Makefile])
AC_OUTPUT

echo "*** MODULE FEATURES ***"
printf "%-24s: %s %s" module "$OS" "$cpu_family"
if test "$enable_64bit" = "yes"; then
   printf " (64-bit)\n"
else
   printf " (32-bit)\n"
fi

show_library_feature() {
   printf "%-24s: " "$1"
   if test "$2" = "yes"; then
      printf "%-8s" yes
   else
      printf disabled
   fi
   if test -n "$3"; then
      printf " (%s)" $3
   fi
   echo
}

show_library_feature optimizations $enable_optimization
show_library_feature debug $enable_debug
show_library_feature profiling $enable_profile
