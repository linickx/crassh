%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global srcname CraSSH
Name:           python-crassh
Version:        2.03
Release:        1%{?dist}
Summary:        Cisco IOS SSH library for python
Group:          Development/Libraries
License:        GPLv2
URL:            https://github.com/linickx/crassh/
Source0:        https://pypi.python.org/packages/source/p/CraSSH/CraSSH-%{version}.tar.gz

BuildArch:      noarch
BuildRequires: python-setuptools
BuildRequires: python-paramiko 

Requires:      python-paramiko

%description
C.R.A.SSH (crassh) stands for Cisco Remote Automation via SSH, it is a python script for automating commands on Cisco devices.
Crassh can be used in two ways:
* a stand alone script that users (Network Admins) can run to perform actions on Cisco devices
* a module developers can import and leverage in their own scripts

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}
install -d $RPM_BUILD_ROOT{%{_bindir}/crassh}

%files
%doc LICENSE PKG-INFO README.rst
%{python_sitelib}/*
%attr(0755,root,root) %{_bindir}/crassh

%changelog
* Sat Feb 20 2016 Nick Bettison <linickx gmail com> - 2.03-1
- First Draft SPEC