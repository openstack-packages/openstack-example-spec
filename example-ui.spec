Name:         openstack-app-catalog-ui
Version:      XXX
Release:      XXX
Summary:      The UI component for the OpenStack App Catalog

License:      ASL 2.0
URL:          https://github.com/stackforge/apps-catalog-ui
Source0:      https://pypi.python.org/packages/source/a/app-catalog-ui/app-catalog-ui-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-flake8
BuildRequires: openstack-dashboard

Requires: pytz
Requires: openstack-dashboard
Requires: python-scss
Requires: python-pbr
Requires: python-oslo-config


%description
app-catalog-ui is an OpenStack Horizon user interface plugin to provide easy access to the OpenStack App Catalog.

%prep
%setup -q -n app-catalog-ui-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
export OSLO_PACKAGE_VERSION=%{version}
%{__python2} setup.py build

%install
export OSLO_PACKAGE_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Move config to horizon
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
mv enabled/_80_project_catalog_panel_group.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_80_project_catalog_panel_group.py
mv enabled/_90_project_app_catalog_panel.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_90_project_app_catalog_panel.py
mv enabled/_91_project_component_catalog_panel.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_91_project_component_catalog_panel.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_80_project_catalog_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_80_project_catalog_panel_group.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_90_project_app_catalog_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_90_project_app_catalog_panel.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_91_project_component_catalog_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_91_project_component_catalog_panel.py

# Move static files to horizon. These require that you compile them again
# post install { python manage.py compress }
mkdir -p  %{buildroot}%{python2_sitelib}/app_catalog/static
mkdir -p  %{buildroot}%{python2_sitelib}/app_catalog/templates
mkdir -p  %{buildroot}%{python2_sitelib}/component_catalog/templates
cp -r app_catalog/static/* %{buildroot}%{python2_sitelib}/app_catalog/static/
cp -r app_catalog/templates/* %{buildroot}%{python2_sitelib}/app_catalog/templates/
cp -r component_catalog/templates/* %{buildroot}%{python2_sitelib}/component_catalog/templates/

%check
# no upstream tests

%files
%doc README.rst
%license LICENSE
%dir %{python2_sitelib}/app_catalog
%dir %{python2_sitelib}/component_catalog
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/app_catalog/*.py*
%{python2_sitelib}/app_catalog/templates
%{python2_sitelib}/app_catalog/static
%{python2_sitelib}/component_catalog/*.py*
%{python2_sitelib}/component_catalog/templates
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_80_project_catalog_panel_group.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_90_project_app_catalog_panel.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_91_project_component_catalog_panel.py*
%{_sysconfdir}/openstack-dashboard/enabled/_80_project_catalog_panel_group.py*
%{_sysconfdir}/openstack-dashboard/enabled/_90_project_app_catalog_panel.py*
%{_sysconfdir}/openstack-dashboard/enabled/_91_project_component_catalog_panel.py*

%changelog

