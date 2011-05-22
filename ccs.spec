Summary:	Cluster configuration system to manage the cluster config file
Summary(pl.UTF-8):	System konfiguracji klastra do zarządzania jego plikiem konfiguracyjnym
Name:		ccs
Version:	2.03.10
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	379b560096e315d4b52e238a5c72ba4a
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://sources.redhat.com/cluster/ccs/
BuildRequires:	cman-devel >= 2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
Cluster configuration system to manage the cluster config file.

%description -l pl.UTF-8
System konfiguracji klastra do zarządzania jego plikiem
konfiguracyjnym.

%package devel
Summary:	Header files and static library for ccs
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteka statyczna ccs
Group:		Development/Libraries
# doesn't require base

%description devel
Header files and static library for ccs.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteka statyczna ccs.

%prep
%setup -q -n cluster-%{version}

%build
./configure \
	--cc="%{__cc}" \
	--cflags="%{rpmcflags} -Wall" \
	--ldflags="%{rpmldflags}" \
	--incdir=%{_includedir} \
	--ncursesincdir=%{_includedir}/ncurses \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--without_gfs \
	--without_gfs2 \
	--without_gnbd \
	--without_kernel_modules
%{__make} -C %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} -C %{name} install \
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
%attr(755,root,root) %{_sbindir}/ccs_test
%attr(755,root,root) %{_sbindir}/ccs_tool
%attr(755,root,root) %{_sbindir}/ccsd
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
