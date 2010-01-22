%define	snapshot		20091120
%define	name			libm4ri
%define major			0
%define	libm4ri			%mklibname m4ri %{major}
%define	libm4ri_devel		%mklibname m4ri -d
%define	libm4ri_static_devel	%mklibname m4ri -d -s

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	M4RI is a library for fast arithmetic with dense matrices over F2
Version:	0.%{snapshot}
Release:	%mkrel 2
# sagemath 4.3 spkg renamed
Source:		libm4ri-%{snapshot}.tar.bz2
URL:		http://m4ri.sagemath.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
M4RI is a library for fast arithmetic with dense matrices over F2.
It was started by Gregory Bard, is maintained by Martin Albrecht.
Several people contributed to it (see below). The name M4RI comes
from the first implemented algorithm: The "Method of the Four Russians"
inversion algorithm published by Gregory Bard. This algorithm in turn
is named after the "Method of the Four Russians" multiplication algorithm
which is probably better referred to as Kronrod's method. M4RI is used by
the Sage mathematics software and the PolyBoRi library. M4RI is available
under the General Public License Version 2 or later (GPLv2+).

%package	-n %{libm4ri}
Group:		System/Libraries
Summary:	M4RI runtime library
Requires:	%{libm4ri} = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}

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
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libm4ri} = %{version}-%{release}

%description	-n %{libm4ri_devel}
M4RI is a library for fast arithmetic with dense matrices over F2.
M4RI is used by the Sage mathematics software and the PolyBoRi library.

%package	-n %{libm4ri_static_devel}
Group:		Development/C
Summary:	M4RI static library
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Requires:	%{libm4ri_devel} = %{version}-%{release}

%description	-n %{libm4ri_static_devel}
M4RI is a library for fast arithmetic with dense matrices over F2.
M4RI is used by the Sage mathematics software and the PolyBoRi library.

%prep
%setup -q -n libm4ri-%{snapshot}.p0

%build
pushd src
    autoreconf
    %configure
    %make
popd

%install
pushd src
    %makeinstall_std
popd

%clean
rm -rf %{buildroot}

%files		-n %{libm4ri}
%defattr(-,root,root)
%{_libdir}/libm4ri-0.0.20091101.so

%files		-n %{libm4ri_devel}
%defattr(-,root,root)
%dir %{_includedir}/m4ri
%{_includedir}/m4ri/*
%{_libdir}/libm4ri.la
%{_libdir}/libm4ri.so

%files		-n %{libm4ri_static_devel}
%defattr(-,root,root)
%dir %{_includedir}/m4ri
%{_libdir}/libm4ri.a
