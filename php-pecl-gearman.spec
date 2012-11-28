%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name gearman

Name:           php-pecl-gearman
Version:        0.7.0
Release:        1.wp5
Summary:        PECL package for gearmand

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/gearman
Source0:        http://pecl.php.net/get/gearman-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  automake php-devel php-pear
BuildRequires:  libgearman-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(Gearman) = %{version}

%if 0%{?php_zend_api}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
Requires:       php-api = %{php_apiver}
%endif

Requires: gearmand

%description
The Gearman extension uses libgearman library to provide API for communicating
with gearmand, and writing clients and workers.

%prep
%setup -qcn %{pecl_name}-%{version}
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pecl_name}-%{version}/%{pecl_name}.xml
cd %{pecl_name}-%{version}

%build
cd %{pecl_name}-%{version}
phpize
%configure --enable-%{pecl_name}
%{__make}

%install
cd %{pecl_name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

# install config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# install doc files
install -d docs
install -pm 644 CREDITS LICENSE README docs

# Install XML package description
install -d $RPM_BUILD_ROOT%{pecl_xmldir}
install -pm 644 %{pecl_name}.xml $RPM_BUILD_ROOT%{pecl_xmldir}/%{name}.xml


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/docs/*
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Mon Sep 27 2010 Andy Thompson <athompson@ibuildings.com> 0.7.0-1
- Initial release
