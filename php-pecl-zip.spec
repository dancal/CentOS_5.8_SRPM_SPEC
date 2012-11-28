%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

Name:           php-pecl-zip
Version:        1.10.2
Release:        1.wp5
Summary:        A zip management extension

Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/zip
Source0:        http://pecl.php.net/package/zip/zip-1.10.2.tgz
Source1:		zip.ini
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  php-devel
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_apiver}

%description
Zip is an extension to create, modify and read zip files.

%prep
%setup -q -n zip-1.10.2

%build
%{_bindir}/phpize
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# install configuration
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%{__cp} %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/zip.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CREDITS
%config(noreplace) %{_sysconfdir}/php.d/zip.ini
%{php_extdir}/zip.so

