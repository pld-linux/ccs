#
# Conditional build:
Summary:	cluster configuration system to manage the cluster config file
Name:		ccs
%define	snap	20040625
Version:	0.0.0.%{snap}.1
Release:	1
License:	GPL
Group:		Applications/System
Source0:	%{name}.tar.gz
# Source0-md5:	9c119853aac17437bf0b05cbb8a37117
URL:		http://sources.redhat.com/cluster/
BuildRequires:	libxml-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
cluster configuration system to manage the cluster config file.

%package devel
Summary:        Header files and development documentation for %{name}
Group:          Development/Libraries

%description devel
Header files and development documentation for %{name}.

%prep
%setup -q -n %{name}

%build
./configure \
	--incdir=%{_includedir} \
	--kernel_src=%{_kernelsrcdir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/*.a
