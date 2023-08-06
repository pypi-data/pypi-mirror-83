Name: libpff
Version: 20200808
Release: 1
Summary: Library to access the Personal Folder File (OST, PAB and PST) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libpff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
                  
BuildRequires: gcc                  

%description -n libpff
Library to access the Personal Folder File (OST, PAB and PST) format

%package -n libpff-static
Summary: Library to access the Personal Folder File (OST, PAB and PST) format
Group: Development/Libraries
Requires: libpff = %{version}-%{release}

%description -n libpff-static
Static library version of libpff.

%package -n libpff-devel
Summary: Header files and libraries for developing applications for libpff
Group: Development/Libraries
Requires: libpff = %{version}-%{release}

%description -n libpff-devel
Header files and libraries for developing applications for libpff.

%package -n libpff-python2
Obsoletes: libpff-python < %{version}
Provides: libpff-python = %{version}
Summary: Python 2 bindings for libpff
Group: System Environment/Libraries
Requires: libpff = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libpff-python2
Python 2 bindings for libpff

%package -n libpff-python3
Summary: Python 3 bindings for libpff
Group: System Environment/Libraries
Requires: libpff = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libpff-python3
Python 3 bindings for libpff

%package -n libpff-tools
Summary: Several tools for reading Personal Folder Files (OST, PAB and PST)
Group: Applications/System
Requires: libpff = %{version}-%{release}

%description -n libpff-tools
Several tools for reading Personal Folder Files (OST, PAB and PST)

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libpff
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libpff-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libpff-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpff.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libpff-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libpff-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libpff-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Oct 26 2020 Joachim Metz <joachim.metz@gmail.com> 20200808-1
- Auto-generated

