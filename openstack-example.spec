%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global service example

Name:		openstack-%{service}
Version:    XXX
Release:    XXX
Summary:	OpenStack Example Service
License:	ASL 2.0
URL:		http://launchpad.net/%{service}/

Source0:	http://tarballs.openstack.org/%{service}/%{service}-master.tar.gz
Source1:	%{service}.logrotate
Source2:	openstack-example-server.service
Source3:    %{service}-dist.conf

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-pbr
BuildRequires:	python-setuptools
BuildRequires:  git
BuildRequires:	systemd
BuildRequires:	systemd-units
# Required to compile translation files
BuildRequires:  python-babel

Requires:	openstack-%{service}-common = %{version}-%{release}

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This is the description of an example service for OpenStack.


%package -n python-%{service}
Summary:	Example Python libraries

Requires:	python-oslo-db >= 2.0

%description -n python-%{service}
This is the description of an example service for OpenStack.

This package contains the Example Python library.


%package -n python-%{service}-tests
Summary:	Example tests
Requires:	python-%{service} = %{version}-%{release}

%description -n python-%{service}-tests
This is the description of an example service for OpenStack.

This package contains the Example test files.


%package common
Summary:	Example common files
Requires:	python-%{service} = %{version}-%{release}

%description common
This is the description of an example service for OpenStack.

This package contains Example common files.

%package doc
Summary:	Example documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
This is the description of an example service for OpenStack.

This package contains the documentation.

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt


%build
%py2_build
# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/%{service}/locale

%install
%py2_install

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}/usr/etc/%{service}/* %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini %{buildroot}%{_datadir}/%{service}/api-paste.ini

# Install dist conf
install -p -D -m 640 %{SOURCE3} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{service}

# Install systemd units
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-example-server.service

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
getent passwd %{service} >/dev/null || \
    useradd -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
    -c "OpenStack Example Daemons" %{service}
exit 0


%post
%systemd_post openstack-example-server.service

%preun
%systemd_preun openstack-example-server.service

%postun
%systemd_postun_with_restart openstack-example-server.service

%files
%license LICENSE
%{_bindir}/openstack-example-server
%{_unitdir}/openstack-example-server.service
%attr(-, root, %{service}) %{_datadir}/%{service}/api-paste.ini


%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests


%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%files common -f %{service}.lang
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{service}
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{service}
%dir %{_datadir}/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%dir %{_sharedstatedir}/%{service}
%dir %{_localstatedir}/log/%{service}

%files doc
%license LICENSE
%doc html README.rst

%changelog

