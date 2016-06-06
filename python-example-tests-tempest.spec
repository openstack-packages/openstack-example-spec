# This spec can be used for packaging of tempest plugin when residing in
# a separate project as designate-tempest-plugin. For tempest plugins included
# in main project git repo, it should be a sub-package of openstack-<service>.
%global service example
%global plugin example-tempest-plugin
%global module example_tempest_plugin

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of example
License:    ASL 2.0
URL:        https://github.com/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

Requires:   python-xxxxx >= a.b.c

%description
This package contains Tempest tests to cover the example project.
Additionally it provides a plugin to automatically load these tests into tempest.

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build

%install
%py2_install

%files
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%changelog
