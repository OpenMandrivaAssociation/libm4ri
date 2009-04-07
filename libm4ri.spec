%define		snapshot	20090105

Name:		libm4ri
Group:		Sciences/Mathematics
License:	GPL
Summary:	M4RI is a library for fast arithmetic with dense matrices over F2
Version:	0.%{snapshot}
Release:	%mkrel 1
Source:		http://m4ri.sagemath.org/downloads/m4ri-%{snapshot}.tar.gz
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

%package	devel
Group:		Development/Other
Summary:	M4RI runtime library

%description	devel
M4RI is a library for fast arithmetic with dense matrices over F2.
M4RI is used by the Sage mathematics software and the PolyBoRi library.

%prep
%setup -q -n m4ri-%{snapshot}

%build
autoreconf
%configure
%make

%install
%makeinstall_std

%clean
rm -rf %{buildroot}

%files		devel
%defattr(-,root,root)
%dir %{_includedir}/m4ri
%{_includedir}/m4ri/*
%{_libdir}/libm4ri*
