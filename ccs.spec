Summary:	Cluster configuration system to manage the cluster config file
Summary(pl):	System konfiguracji klastra do zarz±dzania jego plikiem konfiguracyjnym
Name:		ccs
Version:	0.24
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://people.redhat.com/cfeist/cluster/tgz/%{name}-%{version}.tar.gz
# Source0-md5:	1df515f83510b4f5d9c0c5f70e8503cf
URL:		http://sources.redhat.com/cluster/ccs/
BuildRequires:	libxml-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
Cluster configuration system to manage the cluster config file.

%description -l pl
System konfiguracji klastra do zarz±dzania jego plikiem
konfiguracyjnym.

%package devel
Summary:	Header files and static library for ccs
Summary(pl):	Pliki nag³ówkowe i biblioteka statyczna ccs
Group:		Development/Libraries

%description devel
Header files and static library for ccs.

%description devel -l pl
Pliki nag³ówkowe i biblioteka statyczna ccs.

%prep
%setup -q

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

install -d $RPM_BUILD_ROOT%{_sysconfdir}/cluster
touch $RPM_BUILD_ROOT%{_sysconfdir}/cluster/cluster.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/cluster
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cluster/cluster.xml

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/*.a
