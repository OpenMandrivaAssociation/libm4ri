%define	snapshot		20130416
%define	name			libm4ri
%define major			0
%define	libm4ri			%mklibname m4ri %{major}
%define	libm4ri_devel		%mklibname m4ri -d

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	M4RI is a library for fast arithmetic with dense matrices over F2
Version:	0.%{snapshot}
Release:	3
URL:		http://m4ri.sagemath.org
Source:		http://m4ri.sagemath.org/downloads/m4ri-%{snapshot}.tar.gz
Source1:	%{name}.rpmlintrc

# This patch will not be sent upstream, as it is Fedora-specific.
# Permanently disable SSE3 and SSSE3 detection.  Without this patch, the
# config file tends to be regenerated at inconvenient times.
Patch0:         m4ri-no-sse3.patch
# Fix a format specifier.
Patch1:         m4ri-printf.patch

BuildRequires:  doxygen
BuildRequires:	gomp-devel
BuildRequires:  png-devel
BuildRequires:  texlive

%description
M4RI is a library for fast arithmetic with dense matrices over F_2.
The name M4RI comes from the first implemented algorithm: The "Method
of the Four Russians" inversion algorithm published by Gregory Bard.
M4RI is used by the Sage mathematics software and the PolyBoRi library.

%package	-n %{libm4ri}
Group:		System/Libraries
Summary:	M4RI runtime library
Provides:	m4ri = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description	-n %{libm4ri}
M4RI is a library for fast arithmetic with dense matrices over F2.
It was started by Gregory Bard, is maintained by Martin Albrecht.
Several people contributed to it (see below). The name M4RI comes
from the first implemented algorithm: The "Method of the Four Russians"
inversion algorithm published by Gregory Bard. This algorithm in turn
is named after the "Method of the Four Russians" multiplication algorithm
which is probably better referred to as Kronrod's method. M4RI is used by
the Sage mathematics software and the PolyBoRi library. M4RI is available
under the General Public License Version 2 or later (GPLv2+).

%package	-n %{libm4ri_devel}
Group:		Development/C
Summary:	M4RI development files
Provides:	m4ri-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libm4ri} = %{version}-%{release}

%description	-n %{libm4ri_devel}
M4RI is a library for fast arithmetic with dense matrices over F2.
M4RI is used by the Sage mathematics software and the PolyBoRi library.

%prep
%setup -q -n m4ri-%{snapshot}
%patch0
%patch1

# Remove an unnecessary direct library dependency from the pkgconfig file
sed -i -e "s/ -lm//" m4ri.pc.in

# Die, rpath, die!  Also workaround libtool reordering -Wl,--as-needed after
# all the libraries
sed -e "s|\(hardcode_libdir_flag_spec=\)'.*|\1|" \
    -e "s|\(runpath_var=\)LD_RUN_PATH|\1|" \
    -e 's|CC="g..|& -Wl,--as-needed|' \
    -i configure 

# Fix a couple of broken doxygen commands
sed -i.orig "s/\\\\output/\\\\return/;s/\\\\seealso/\\\\see/" m4ri/misc.h
touch -r m4ri/misc.h.orig m4ri/misc.h
rm -f m4ri/misc.h.orig

%build
%ifarch %ix86
# Build an SSE2-enabled version, 
%configure --disable-static --enable-openmp CFLAGS="$RPM_OPT_FLAGS -march=pentium4"
sed -e 's/^#undef HAVE_MMX/#define HAVE_MMX/' \
    -e 's/^#undef HAVE_SSE$/#define HAVE_SSE/' \
    -e 's/^#undef HAVE_SSE2/#define HAVE_SSE2/' \
    -i src/config.h
sed -e 's/^\(#define __M4RI_HAVE_SSE2[[:blank:]]*\)0/\11/' \
    -e 's/^\(#define __M4RI_SIMD_CFLAGS[[:blank:]]*\).*/\1" -mmmx -msse -msse2"/' \
    -i src/m4ri_config.h
sed -i 's/^SIMD_CFLAGS =.*/SIMD_CFLAGS = -mmmx -msse -msse2/' Makefile
%else
%configure --disable-static --enable-openmp
%endif

%make LIBS=-lm

%ifarch %ix86
# Build an SSE2-disabled version
cp -a .libs .libs.sse2
make clean
rm -fr .deps
%configure --disable-static --enable-openmp --disable-sse2
%make LIBS=-lm
%endif

# Build documentation
cd m4ri
doxygen

%install
make install DESTDIR=$RPM_BUILD_ROOT

%ifarch %ix86
mkdir -p %{buildroot}%{_libdir}/sse2
mv %{buildroot}%{_libdir}/libm4ri-*.so %{buildroot}%{_libdir}/sse2
mv .libs .libs.nosse2
mv .libs.sse2 .libs
make install DESTDIR=$RPM_BUILD_ROOT
%endif

%check
make check LD_LIBRARY_PATH=`pwd`/.libs

%files		-n %{libm4ri}
%doc COPYING README
%{_libdir}/libm4ri-*.so
%ifarch %ix86
%{_libdir}/sse2/libm4ri-*.so
%endif

%files		-n %{libm4ri_devel}
%doc doc/html
%{_includedir}/m4ri
%{_libdir}/libm4ri.so
%{_libdir}/pkgconfig/m4ri.pc
