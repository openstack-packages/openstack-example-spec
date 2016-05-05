# NOTE: Reference only.
# spec files for puppet modules are automatically created from metadata.json file
# in RDO project. 

Name:           puppet-example
Version:        XXX
Release:        XXX
Summary:        Puppet module for example
License:        ASL 2.0

URL:            https://launchpad.net/puppet-example

Source0:        https://github.com/openstack/puppet-example/archive/%{version}.tar.gz

BuildArch:      noarch

Requires:       puppet-inifile
Requires:       puppet-stdlib
Requires:       puppet >= 2.7.0

%description
Example puppet module 

%prep
%setup -q -n %{name}-%{version}

find . -type f -name ".*" -exec rm {} +
find . -size 0 -exec rm {} +
find . \( -name "*.pl" -o -name "*.sh"  \) -exec chmod +x {} +
find . \( -name "*.pp" -o -name "*.py"  \) -exec chmod -x {} +
find . \( -name "*.rb" -o -name "*.erb" \) -exec chmod -x {} +
find . \( -name spec -o -name ext \) | xargs rm -rf

%build


%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}/%{_datadir}/openstack-puppet/modules/example/
cp -rp * %{buildroot}/%{_datadir}/openstack-puppet/modules/example/


%files
%{_datadir}/openstack-puppet/modules/example/


%changelog


