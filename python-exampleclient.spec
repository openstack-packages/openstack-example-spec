%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%global default_python 3
%else
%global default_python 2
%endif


%global client python-exampleclient
%global sclient exampleclient
# If a executable is provided by the package uncomment following line
#%global executable example

Name:       %{client}
Version:    XXX
Release:    XXX
Summary:    OpenStack Example client
License:    ASL 2.0
URL:        http://launchpad.net/%{client}/

Source0:    http://tarballs.openstack.org/%{client}/%{client}-master.tar.gz

BuildArch:  noarch

%package -n python2-%{sclient}
Summary:    OpenStack Example client
%{?python_provide:%python_provide python2-%{sclient}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
# Test requirements should be added here as BuildRequires for tests in %check

Requires:   python-oslo-config >= 2:3.4.0

%description -n python2-%{sclient}
OpenStack example client


%package -n python2-%{sclient}-tests
Summary:    OpenStack example client tests
Requires:   python2-%{sclient} = %{version}-%{release}

# Test requirements should be added here as Requires.

%description -n python2-%{sclient}-tests
OpenStack example client tests

This package contains the example client test files.


%package -n python-%{sclient}-doc
Summary:    OpenStack example client documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{sclient}-doc
OpenStack example client documentation

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{sclient}
Summary:    OpenStack Example client
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git
# Test requirements should be added here as BuildRequires if adding tests in %check

Requires:   python3-oslo-config >= 2:3.4.0

%description -n python3-%{sclient}
OpenStack example client


%package -n python3-%{sclient}-tests
Summary:    OpenStack example client tests
Requires:   python3-%{sclient} = %{version}-%{release}

# Test requirements should be added here as Requires.

%description -n python3-%{sclient}-tests
OpenStack example client tests

This package contains the example client test files.

%endif # with_python3


%description
OpenStack example library.


%prep
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build -b html doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

# If the client has man page uncomment following line
# sphinx-build -b man doc/source man

%install

%py2_install
# If the client has man page uncomment following line
# install -p -D -m 644 man/%{executable}.1 %{buildroot}%{_mandir}/man1/%{executable}.1

%if 0%{?with_python3}
# If a executable is provided by the package uncomment following line
#mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/python2-%{executable}
%py3_install
# If a executable is provided by the package uncomment following lines
#mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/python3-%{executable}
#%if 0%{?default_python} >= 3
#ln -s %{_bindir}/python3-%{executable} %{buildroot}%{_bindir}/%{executable}
#%else
#ln -s %{_bindir}/python2-%{executable} %{buildroot}%{_bindir}/%{executable}
#%endif
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{sclient}
%license LICENSE
%{python2_sitelib}/%{sclient}
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/%{sclient}/tests
# If the client has man page uncomment
#%{_mandir}/man1/%{executable}.1
# If a executable is provided by the package uncomment following lines
#%{_bindir}/python2-%{executable}
#%if 0%{?default_python} <= 2
#%{_bindir}/%{executable}
#%endif

%files -n python2-%{sclient}-tests
%license LICENSE
%{python2_sitelib}/%{sclient}/tests

%files -n python-%{sclient}-doc
%license LICENSE
%doc html README.rst

%if 0%{?with_python3}
%files python3-%{sclient}
%license LICENSE
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sclient}/tests
# If the client has man page uncomment
#%{_mandir}/man1/%{executable}.1
# If a executable is provided by the package uncomment following lines
#%{_bindir}/python3-%{executable}
#%if 0%{?default_python} >= 3
#%{_bindir}/%{executable}
#%endif

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{sclient}/tests
%endif # with_python3

%changelog
