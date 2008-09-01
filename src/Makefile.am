if COND_SINGLE_COMPILATION_UNIT
GLUT_SOURCES = single-compilation-unit.cc
else
GLUT_SOURCES = glut.cc glut-constants.cc GlutVoidPtrType.cc
endif

lib_LTLIBRARIES = glut.la
glut_la_SOURCES = $(GLUT_SOURCES)
glut_la_LDFLAGS = -module -avoid-version ${GLUT_LIBS}

INCLUDES = -I$(top_srcdir)/include $(GLUT_INCLUDES)

AM_CXXFLAGS = ${PTHREAD_CFLAGS}

if COND_PROFILE
AM_CXXFLAGS += -g -pg
else
if COND_DEBUG
AM_CXXFLAGS += -g
endif
endif

install-exec-hook:
	mv $(libdir)/glut.$(MODULE_SUFFIX) $(libdir)/glut.qmod
	rm -f $(libdir)/glut.la $(libdir)/glut.a

