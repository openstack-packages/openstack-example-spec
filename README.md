# Templates for openstack rpm packaging

This is a set of example files that can be use to create rpm packages for openstack. 

**Notes**

- puppet-example.spec: file is only for reference. In RDO, spec files are created automatically from metadata.json file.
- python-exampleclient: all required content for executable included in RPMs has been commented as most clients should be provided as osc plugins for openstackclient. For client packages including executable files, read the spec file and uncomment what needed.
- spec file for openstack-example includes compilation and installation of translation files. If the project doesn't contain translation files, lines with references to locale or lang mut be removed or commented.
