%define module_api %(qore --module-api 2>/dev/null)
%define module_dir %{_libdir}/qore-modules

%if 0%{?sles_version}

%define dist .sles%{?sles_version}

%else
%if 0%{?suse_version}

# get *suse release major version
%define os_maj %(echo %suse_version|rev|cut -b3-|rev)
# get *suse release minor version without trailing zeros
%define os_min %(echo %suse_version|rev|cut -b-2|rev|sed s/0*$//)

%if %suse_version > 1010
%define dist .opensuse%{os_maj}_%{os_min}
%else
%define dist .suse%{os_maj}_%{os_min}
%endif

%endif
%endif

Summary: GLUT Module for Qore
Name: qore-glut-module
Version: 0.0.3
Release: 1%{dist}
License: LGPL
Group: Development/Languages
URL: http://www.qoretechnologies.com/qore
Source: http://prdownloads.sourceforge.net/qore/%{name}-%{version}.tar.gz
#Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: /usr/bin/env
Requires: qore-module-api-%{module_api}
Requires: qore-opengl-module
BuildRequires: gcc-c++
BuildRequires: qore-devel
%if 0%{?mdkversion}
%ifarch x86_64 ppc64 x390x ia64
BuildRequires: lib64mesaglut3-devel
%else
BuildRequires: libmesaglut3-devel
%endif
%else
BuildRequires: freeglut-devel
%endif
BuildRequires: qore

%description
This module provides functionality enabling qore scripts/programs to use GLUT
functionality and therefore implement platform-independent OpenGL GUIs.


%if 0%{?suse_version}
%debug_package
%endif

%prep
%setup -q
%ifarch x86_64 ppc64 x390x ia64
c64=--enable-64bit
%endif
./configure RPM_OPT_FLAGS="$RPM_OPT_FLAGS" --prefix=/usr --disable-debug $c64

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{module_dir}
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/qore-glut-module/examples
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{module_dir}
%doc COPYING README RELEASE-NOTES ChangeLog AUTHORS

%changelog
* Tue Jan 6 2009 David Nichols <david_nichols@users.sourceforge.net>
- updated version to 0.0.3

* Tue Sep 2 2008 David Nichols <david_nichols@users.sourceforge.net>
- initial spec file for separate glut release
