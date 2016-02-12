%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library example-library
%global module example_library

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Example library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-master.tar.gz

BuildArch:  noarch

%package -n python2-%{library}
Summary:    OpenStack Example library
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

Requires:   python-oslo-config >= 2:3.4.0

%description -n python2-%{library}
OpenStack example library.


%package -n python2-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python2-%{library} = %{version}-%{release}

%description -n python2-%{library}-tests
OpenStack example library.

This package contains the example library test files.


%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{library}-doc
OpenStack example library.

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    OpenStack Example library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git

Requires:   python3-oslo-config >= 2:3.4.0

%description -n python3-%{library}
OpenStack example library.


%package -n python3-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
OpenStack example library.

This package contains the example library test files.

%endif # with_python3


%description
OpenStack example library.


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc html README.rst

%if 0%{?with_python3}
%files python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
