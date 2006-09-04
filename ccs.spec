Summary:	Cluster configuration system to manage the cluster config file
Summary(pl):	System konfiguracji klastra do zarz±dzania jego plikiem konfiguracyjnym
Name:		ccs
Version:	1.03.00
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	8eea23df70d2007c4fb8c234cfea49cf
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-optflags.patch
URL:		http://sources.redhat.com/cluster/ccs/
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	magma-devel >= 0:1.01
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	magma >= 0:1.01
Requires:	rc-scripts
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
# doesn't require base

%description devel
Header files and static library for ccs.

%description devel -l pl
Pliki nag³ówkowe i biblioteka statyczna ccs.

%prep
%setup -q -n cluster-%{version}
%patch0 -p1

%build
cd %{name}
./configure \
	--incdir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	OPTCFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/cluster
touch $RPM_BUILD_ROOT%{_sysconfdir}/cluster/cluster.xml

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/cluster
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cluster/cluster.xml
%{_mandir}/man5/cluster.conf.5*
%{_mandir}/man7/ccs.7*
%{_mandir}/man8/ccs*.8*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/ccs.h
%{_libdir}/libccs.a
