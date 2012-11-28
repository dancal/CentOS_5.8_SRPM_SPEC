%define default_extdir  %{_libdir}/php/modules
%define default_apiver  20090626
%define default_version 5.3.18

%define module_version 2.0.0
%define php_name php

%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{default_extdir})
%{!?php_version:%define php_version %(php-config --version 2>/dev/null || echo %{default_version})}

# This is the apache userid, only used for sysvipc semaphores which is the
# default on ppc since spinlock is not detected
%define userid         48

Summary: PHP accelerator, optimizer, encoder and dynamic content cacher
Name: %{php_name}-xcache
Version: %{php_version}_%{module_version}
Release: 1.wp5
License: GPL
Group: Development/Languages
URL: http://xcache.lighttpd.net/
Packager: Builder <umask@yandex.ru>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: %{php_name} = %{php_version}
Provides: php-zend_extension
BuildRequires: %{php_name}, %{php_name}-devel, sed
# Required by phpize
BuildRequires: autoconf, automake, libtool
Conflicts: php-mmcache, php-eaccelerator, php-pecl-xdebug, php-pecl-apc
Conflicts: %{php_name}-mmcache, %{php_name}-eaccelerator, %{php_name}-pecl-xdebug, %{php_name}-pecl-apc

Source0: xcache-%{module_version}.tar.gz
Source1: xcache.ini

%description
XCache is a fast, stable PHP opcode cacher that has been tested and is now
running on production servers under high load. It is tested (on linux) and
supported on all of the latest PHP cvs branches such as PHP_4_3 PHP_4_4
PHP_5_1 PHP_5_2 HEAD(6.x). ThreadSafe/Windows is also supported.

%prep
%setup -n xcache-%{module_version}

%build
phpize
%configure --enable-xcache

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# The cache directory where pre-compiled files will reside
%{__mkdir_p} %{buildroot}%{_var}/cache/php-xcache
%{__mkdir_p} %{buildroot}%{_var}/www/html/xcache/

# Drop in the bit of configuration
%{__install} -D -m 0644 $RPM_SOURCE_DIR/xcache.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xcache.ini
sed -i -e 's|/REPLACEME|%{php_extdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xcache.ini
%{__install} -D -m 0644 admin/* $RPM_BUILD_ROOT%{_var}/www/html/xcache/


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc xcache.ini admin/
%config(noreplace) %{_sysconfdir}/php.d/xcache.ini
%{php_extdir}/xcache.so
%{_var}/www/html/xcache/*

%changelog
* Sun Jan 23 2011 Builder <umask00@gmail.com> - 1.3.1-umask.8
- new branch for php53

* Wed Jan 12 2011 Builder <umask00@gmail.com> - 1.3.1-umask.7
- update to 1.3.1

* Wed Jun 24 2009 Builder <umask00@gmail.com> - 1.2.2-umask.6
- rebuild against php-5.2.10

* Fri Apr 17 2009 Builder <umask00@gmail.com> - 1.2.2-umask.5
- rebuild against php-5.2.9

* Tue Dec  9 2008 Builder <umask00@gmail.com> - 1.2.2-umask.4
- rebuild against php-5.2.8

* Sun Dec  7 2008 Builder <umask00@gmail.com> - 1.2.2-umask.3
- rebuild against php-5.2.7

* Thu May  8 2008 Builder <umask@yandex.ru> - 1.2.2-umask.2
- update conflicts

* Thu May  8 2008 Builder <umask@yandex.ru> - 1.2.2-umask.1
- build for umask repo

* Tue Jul  3 2007 Jason Litka <http://www.jasonlitka.com/> 1.2.1-jason.2
- Changed the config file back to "noreplace"
- Removed the check for # of CPU cores since it couldn't tell the difference
  between real cores and virtual ones
- Changed the php requirement for install to the same version found during
  the build

* Tue Jul  3 2007 Jason Litka <http://www.jasonlitka.com/> 1.2.1-jason.1
- Updated sources to 1.2.1
- Changed naming convention to match my other packages

* Thu Dec 28 2006 Jason Litka <http://www.jasonlitka.com/> 1.2.0_0.2
- Removed the PHP API check so that the package would build on PHP 4.

* Wed Dec 20 2006 Jason Litka <http://www.jasonlitka.com/> 1.2.0_0.1
- Initial build
- Has Cache, Optimizer, and Coverager modules built but only the first two
  are enabled

