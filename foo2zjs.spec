Summary:	Linux printer driver for ZjStream protocol
Summary(pl.UTF-8):	Linuksowy sterownik drukarek dla protokołu ZjStream
Name:		foo2zjs
Version:	20120504
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://foo2zjs.rkkda.com/foo2zjs.tar.gz#/%{name}-%{version}.tar.gz
# Source0-md5:	88fd5a0982001cfc17a58885802f37d7
Source1:	http://foo2zjs.rkkda.com/firmware/sihp1000.tar.gz
# Source1-md5:	eb7f6e1edfec313e6ca23abd27a0d1c2
Source2:	http://foo2zjs.rkkda.com/firmware/sihp1005.tar.gz
# Source2-md5:	04f7bd2eec09131371e27403626f38b5
Source3:	http://foo2zjs.rkkda.com/firmware/sihpP1006.tar.gz
# Source3-md5:	df4b0b84c6feb0d45f64d7fc219895a5
Source4:	http://foo2zjs.rkkda.com/firmware/sihp1018.tar.gz
# Source4-md5:	bf61f2ce504b233f999bc358f5a79499
Source5:	http://foo2zjs.rkkda.com/firmware/sihp1020.tar.gz
# Source5-md5:	1d408fa44fb43f2f5f8c8f7eabcc70c6
Patch0:		%{name}-udev-rules.patch
Patch1:		%{name}-hplj1000.patch
URL:		http://foo2zjs.rkkda.com/
BuildRequires:	cups-filter-foomatic
BuildRequires:	ghostscript
BuildRequires:	groff
Requires:	foomatic-db
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
foo2zjs is an open source printer driver for printers that use the
Zenographics ZjStream wire protocol for their print data. With
foo2zjs, you can print to some HP and Minolta/QMS ZjStream printers,
such as these:

- HP LaserJet 1000 B/W
- HP LaserJet 1005 B/W
- HP LaserJet 1006 B/W
- HP LaserJet 1018 B/W
- HP LaserJet 1020 B/W
- Konica Minolta magicolor 2430 DL B/W and color
- Minolta/QMS 2300 DL B/W and color
- Minolta/QMS 2200 DL B/W and color

%description -l pl.UTF-8
foo2zjs to otwarty sterownik dla drukarek używających do druku
protokołu Zenographics ZjStream. Dzięki foo2zjs można drukować na
drukarkach HP oraz Minolta/QMS ZjStream takich jak:

- HP LaserJet 1000 B/W
- HP LaserJet 1005 B/W
- HP LaserJet 1006 B/W
- HP LaserJet 1018 B/W
- HP LaserJet 1020 B/W
- Konica Minolta magicolor 2430 DL B/W and color
- Minolta/QMS 2300 DL B/W and color
- Minolta/QMS 2200 DL B/W and color

%package firmware
Summary:	Firmware for HP LaserJet 10xx printers
Summary(pl.UTF-8):	Firmware dla drukarek HP LaserJet 10xx
License:	distributable
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	cups-foomatic-db-HP

%description firmware
Firmware for HP LaserJet 10xx printers:
- HP LaserJet 1000, 1005, 1006, 1018, 1020

%description firmware -l pl.UTF-8
Firmware dla drukarek HP LaserJet 10xx:
- HP LaserJet 1000, 1005, 1006, 1018, 1020

%package udev-rules
Summary:	udev rules for HP LaserJet 10xx printers
Summary(pl.UTF-8):	Reguły udev dla drukarek HP LaserJet 10xx
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-firmware = %{version}-%{release}
Requires:	udev-core

%description udev-rules
udev rules for printers:
- HP LaserJet 1000, 1005, 1006, 1018, 1020

%description udev-rules -l pl.UTF-8
Reguły udev dla drukarek:
- HP LaserJet 1000, 1005, 1006, 1018, 1020

%prep
%setup -qc -a1 -a2 -a3 -a4 -a5
mv %{name}/* .; rmdir %{name}
%patch -P0 -p1
%patch -P1 -p1

%build
%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_datadir}/%{name}/{firmware,crd},/lib/udev/rules.d}

%{__make} install-prog \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	UDEVBIN=$RPM_BUILD_ROOT%{_bindir}

%{__make} install-man \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install -p hplj1000 $RPM_BUILD_ROOT%{_bindir}/hplj10xx
cp -p hplj10xx.rules $RPM_BUILD_ROOT/lib/udev/rules.d/11-hplj10xx.rules

for i in sihp1000 sihp1005 sihpP1006 sihp1018 sihp1020; do
	./arm2hpdl $i.img > $i.dl
	cp -p $i.dl $RPM_BUILD_ROOT%{_datadir}/%{name}/firmware
done
cp -p *.ps $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p crd/zjs/*.{crd,ps} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/crd

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q cups restart

%files
%defattr(644,root,root,755)
%doc ChangeLog README manual.pdf
%attr(755,root,root) %{_bindir}/arm2hpdl
%attr(755,root,root) %{_bindir}/command2foo2lava-pjl
%attr(755,root,root) %{_bindir}/foo2hiperc
%attr(755,root,root) %{_bindir}/foo2hiperc-wrapper
%attr(755,root,root) %{_bindir}/foo2hp
%attr(755,root,root) %{_bindir}/foo2hp2600-wrapper
%attr(755,root,root) %{_bindir}/foo2lava
%attr(755,root,root) %{_bindir}/foo2lava-wrapper
%attr(755,root,root) %{_bindir}/foo2oak
%attr(755,root,root) %{_bindir}/foo2oak-wrapper
%attr(755,root,root) %{_bindir}/foo2qpdl
%attr(755,root,root) %{_bindir}/foo2qpdl-wrapper
%attr(755,root,root) %{_bindir}/foo2slx
%attr(755,root,root) %{_bindir}/foo2slx-wrapper
%attr(755,root,root) %{_bindir}/foo2xqx
%attr(755,root,root) %{_bindir}/foo2xqx-wrapper
%attr(755,root,root) %{_bindir}/foo2zjs
%attr(755,root,root) %{_bindir}/foo2zjs-pstops
%attr(755,root,root) %{_bindir}/foo2zjs-wrapper
%attr(755,root,root) %{_bindir}/gipddecode
%attr(755,root,root) %{_bindir}/hbpldecode
%attr(755,root,root) %{_bindir}/hipercdecode
%attr(755,root,root) %{_bindir}/hplj10xx
%attr(755,root,root) %{_bindir}/lavadecode
%attr(755,root,root) %{_bindir}/oakdecode
%attr(755,root,root) %{_bindir}/opldecode
%attr(755,root,root) %{_bindir}/printer-profile
%attr(755,root,root) %{_bindir}/qpdldecode
%attr(755,root,root) %{_bindir}/slxdecode
%attr(755,root,root) %{_bindir}/usb_printerid
%attr(755,root,root) %{_bindir}/xqxdecode
%attr(755,root,root) %{_bindir}/zjsdecode
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.ps
%{_datadir}/%{name}/crd
%{_mandir}/man1/*.1*

%files firmware
%defattr(644,root,root,755)
%{_datadir}/%{name}/firmware

%files udev-rules
%defattr(644,root,root,755)
/lib/udev/rules.d/11-hplj10xx.rules
