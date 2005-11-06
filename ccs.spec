Summary:	Cluster configuration system to manage the cluster config file
Summary(pl):	System konfiguracji klastra do zarz±dzania jego plikiem konfiguracyjnym
Name:		ccs
Version:	1.01.00
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	e98551b02ee8ed46ae0ab8fca193d751
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://sources.redhat.com/cluster/ccs/
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	magma-devel >= 1.0
BuildRequires:	perl-base
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
cd %{name}
%{__perl} -pi -e 's/-O2/%{rpmcflags}/' {ccs_tool,ccs_test,lib,daemon}/Makefile

%build
cd %{name}
./configure \
	--incdir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}"

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
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/%{name} start\" to start %{name}" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop >&2
        fi
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
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/ccs.h
%{_libdir}/libccs.a
