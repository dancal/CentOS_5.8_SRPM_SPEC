Summary: Gearman Server and C Library
Name: gearmand
Version: 1.1.3
Release: 1.wp5
License: BSD
Group: System Environment/Libraries
BuildRequires: bison
URL: http://launchpad.net/gearmand
Requires: sqlite, libevent >= 1.4, boost-program-options >=  1.39

Packager: Brian Aker <brian@tangent.org>

Source: http://launchpad.net/gearmand/trunk/%{version}/+download/gearmand-%{version}.tar.gz
Source1: support/gearmand.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gearman provides a generic framework to farm out work to other machines, dispatching function calls to machines that are better suited to do work, to do work in parallel, to load balance processing, or to call functions between languages.

This package provides the client utilities.

%package server
Summary: Gearmand Server
Group: Applications/Databases
Requires: sqlite, libevent >= 1.4, boost-program-options >=  1.39

%description server
Gearman provides a generic framework to farm out work to other machines, dispatching function calls to machines that are better suited to do work, to do work in parallel, to load balance processing, or to call functions between languages.

This package provides the Gearmand Server.

%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.

%prep
%setup -q

%configure --disable-libpq --disable-libtokyocabinet --disable-libdrizzle --disable-libmemcached --enable-jobserver=yes


%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""
mkdir -p $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/var/log/gearmand
mkdir -p $RPM_BUILD_ROOT/var/run/gearmand
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/gearmand

%check

%clean
%{__rm} -rf %{buildroot}

%pre server
if ! /usr/bin/id -g gearmand &>/dev/null; then
    /usr/sbin/groupadd -r gearmand
fi
if ! /usr/bin/id gearmand &>/dev/null; then
    /usr/sbin/useradd -M -r -g gearmand -d /var/lib/gearmand -s /bin/false \
	-c "Gearman Server" gearmand > /dev/null 2>&1
fi

%post server
if test $1 = 1
then
  /sbin/chkconfig --add gearmand
fi

%preun server
if test $1 = 0
then
  /sbin/chkconfig --del gearmand
fi

%postun server
if test $1 -ge 1
then
  /sbin/service gearmand condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
%{_bindir}/gearadmin
%{_bindir}/gearman
%{_libdir}/libgearman.la
%{_libdir}/libgearman.so.8
%{_libdir}/libgearman.so.8.0.0

%files server
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
%{_sbindir}/gearmand
/etc/rc.d/init.d/gearmand
%attr(0755,gearmand,gearmand) %dir /var/log/gearmand
%attr(0755,gearmand,gearmand) %dir /var/run/gearmand

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
%{_includedir}/libgearman/gearman.h
%{_includedir}/libgearman-1.0/actions.h
%{_includedir}/libgearman-1.0/aggregator.h
%{_includedir}/libgearman-1.0/allocator.h
%{_includedir}/libgearman-1.0/argument.h
%{_includedir}/libgearman-1.0/client.h
%{_includedir}/libgearman-1.0/client_callbacks.h
%{_includedir}/libgearman-1.0/configure.h
%{_includedir}/libgearman-1.0/connection.h
%{_includedir}/libgearman-1.0/constants.h
%{_includedir}/libgearman-1.0/core.h
%{_includedir}/libgearman-1.0/execute.h
%{_includedir}/libgearman-1.0/function.h
%{_includedir}/libgearman-1.0/gearman.h
%{_includedir}/libgearman-1.0/interface/status.h
%{_includedir}/libgearman-1.0/interface/task.h
%{_includedir}/libgearman-1.0/interface/client.h
%{_includedir}/libgearman-1.0/interface/worker.h
%{_includedir}/libgearman-1.0/job.h
%{_includedir}/libgearman-1.0/job_handle.h
%{_includedir}/libgearman-1.0/kill.h
%{_includedir}/libgearman-1.0/limits.h
%{_includedir}/libgearman-1.0/ostream.hpp
%{_includedir}/libgearman-1.0/parse.h
%{_includedir}/libgearman-1.0/priority.h
%{_includedir}/libgearman-1.0/protocol.h
%{_includedir}/libgearman-1.0/result.h
%{_includedir}/libgearman-1.0/return.h
%{_includedir}/libgearman-1.0/signal.h
%{_includedir}/libgearman-1.0/status.h
%{_includedir}/libgearman-1.0/strerror.h
%{_includedir}/libgearman-1.0/string.h
%{_includedir}/libgearman-1.0/task.h
%{_includedir}/libgearman-1.0/task_attr.h
%{_includedir}/libgearman-1.0/util.h
%{_includedir}/libgearman-1.0/version.h
%{_includedir}/libgearman-1.0/visibility.h
%{_includedir}/libgearman-1.0/worker.h
%{_libdir}/pkgconfig/gearmand.pc
%{_libdir}/libgearman.so


%changelog
* Wed Jan 7 2009 Brian Aker <brian@tangent.org> - 0.1-1
- Initial package
