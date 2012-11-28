%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name MDB2_Driver_mysqli
%global prever    b4

Name:           php-pear-mysqli
Version:        1.5.0
Release:        1.wp5
Summary:        MySQL Improved MDB2 driver

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/MDB2_Driver_mysqli
Source0:        http://pear.php.net/get/%{pear_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.1

Requires:       php-common >= 5.2.0
Requires:       php-mysqli
Requires:       php-pcre
Requires:       php-pear(PEAR)
Requires:       php-pear(MDB2) >= 2.5.0%{?prever}
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}%{?prever}

%description
This is the MySQL Improved MDB2 driver.


%prep
%setup -qc
cd %{pear_name}-%{version}%{?prever}
# package.xml is V2
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}%{?prever}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT docdir
cd %{pear_name}-%{version}%{?prever}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
install -d $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_testdir}/%{pear_name}
%{pear_phpdir}/MDB2/Driver/*/mysqli.php
%{pear_phpdir}/MDB2/Driver/mysqli.php
# packager stuff, not need, could probably be removed
%{pear_datadir}/%{pear_name}


%changelog
* Wed Oct 24 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.7.b4
- update to 1.5.0b4

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.6.b3
- rebuilt for new pear_datadir

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.5.b3
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-0.4.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-0.3.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-0.2.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.5.0-0.1.b3
- update to 1.5.0b3
- move MDB2_Driver_mysqli.xml to php-pear-MDB2-Driver-mysqli.xml

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 14 2007 Lubomir Kundrak <lkundrak@redhat.com> 1.4.1-3
- Add fix for CVE-2007-5934 MDB2 Data injection and disclosure

* Sat Sep 22 2007 Johan Cwiklinski <johan AT x-tnd DOT be> 1.4.1-2
- Requires MDB2 2.4.1 or newer

* Sun Sep 02 2007 Johan Cwiklinski <johan AT x-tnd DOT be> 1.4.1-1
- Initial Release
