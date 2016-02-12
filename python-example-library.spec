%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

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

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

Requires:   python-oslo-config >= 2:3.4.0


%description
OpenStack example library.


%package tests
Summary:    OpenStack example library tests
Requires:   python-%{library} = %{version}-%{release}

%description tests
OpenStack example library.

This package contains the example library test files.


%package doc
Summary:    OpenStack example library documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
OpenStack example library.

This package contains the documentation.

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install

%files
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files doc
%license LICENSE
%doc html README.rst

%changelog
