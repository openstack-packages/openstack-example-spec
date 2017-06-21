# This spec can be used for packaging of tempest plugin when residing in
# a separate project as designate-tempest-plugin. For tempest plugins included
# in main project git repo, it should be a sub-package of openstack-<service>.
%global service example
%global plugin example-tempest-plugin
%global module example_tempest_plugin
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of example
License:    ASL 2.0
URL:        https://github.com/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{version}.tar.gz

BuildArch:  noarch

%description
This package contains Tempest tests to cover the example project.
Additionally it provides a plugin to automatically load these tests into tempest.


%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

Requires:   python-xxxxx >= a.b.c

%description -n python2-%{service}-tests-tempest
This package contains Tempest tests to cover the example project.
Additionally it provides a plugin to automatically load these tests into tempest.

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the example tempest tests.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-xxxxx >= a.b.c

%description -n python3-%{service}-tests-tempest
This package contains Tempest tests to cover the example project.
Additionally it provides a plugin to automatically load these tests into tempest.
%endif


%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# remove requirements
%py_req_cleanup
# Remove bundled egg-info
rm -rf *.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
# Use the test command required by the plugin
ostestr --whitelist-file test-whitelist.txt

%files -n python2-%{service}-tests-tempest
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}-tests-tempest
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
