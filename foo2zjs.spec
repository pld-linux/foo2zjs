Summary:	Linux printer driver for ZjStream protocol
Summary(pl.UTF-8):	Linuksowy sterownik drukarek dla protokołu ZjStream
Name:		foo2zjs
Version:	20080418
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://foo2zjs.rkkda.com/%{name}.tar.gz
# Source0-md5:	d86f589c37166420afe9122a2538420b
Source1:	http://foo2zjs.rkkda.com/firmware/sihp1000.tar.gz
# Source1-md5:	8c7028d4be5b5b12ed19a59969b3911a
Source2:	http://foo2zjs.rkkda.com/firmware/sihp1005.tar.gz
# Source2-md5:	59cc9f6a2c1657be8d5070e4ec97b06a
Source3:	http://foo2zjs.rkkda.com/firmware/sihp1018.tar.gz
# Source3-md5:	0d4abf6091aa28a98b9993fbe2dbbaa2
Source4:	http://foo2zjs.rkkda.com/firmware/sihp1020.tar.gz
# Source4-md5:	02b19c047be9a6fed84dc53327c116fc
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
- HP LaserJet 1000, 1005, 1018, 1020

%description firmware -l pl.UTF-8
Firmware dla drukarek HP LaserJet 10xx:
- HP LaserJet 1000, 1005, 1018, 1020

%package udev-rules
Summary:	udev rules for HP LaserJet 10xx printers
Summary(pl.UTF-8):	Reguły udev dla drukarek HP LaserJet 10xx
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-firmware = %{version}-%{release}
Requires:	udev-core

%description udev-rules
udev rules for printers:
- HP LaserJet 1000, 1005, 1018, 1020

%description udev-rules -l pl.UTF-8
Reguły udev dla drukarek:
- HP LaserJet 1000, 1005, 1018, 1020

%prep
%setup -q -n %{name}
%patch0 -p0
%patch1 -p0

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{firmware,crd}
install -d $RPM_BUILD_ROOT/etc/udev/rules.d
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install {arm2hpdl,foo2zjs,foo2zjs-wrapper,foo2zjs-pstops{,.sh},zjsdecode,usb_printerid} \
	$RPM_BUILD_ROOT%{_bindir}
install hplj1000 $RPM_BUILD_ROOT%{_bindir}/hplj10xx
install hplj10xx.rules $RPM_BUILD_ROOT/etc/udev/rules.d/11-hplj10xx.rules

install %{SOURCE1} .
install %{SOURCE2} .
install %{SOURCE3} .
install %{SOURCE4} .
for i in sihp1000 sihp1005 sihp1018 sihp1020; do
	tar -xf $i.tar.gz --use=gzip
	rm $i.tar.gz
	./arm2hpdl $i.img > $i.dl
	install $i.dl $RPM_BUILD_ROOT%{_datadir}/%{name}/firmware
done
install *.ps $RPM_BUILD_ROOT%{_datadir}/%{name}
install crd/zjs/*.{crd,ps} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/crd
install {foo2zjs,foo2zjs-wrapper,zjsdecode}.1 \
	$RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q cups restart

%files
%defattr(644,root,root,755)
%doc ChangeLog README manual.pdf
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.ps
%{_datadir}/%{name}/crd
%{_mandir}/man1/*.1*

%files firmware
%defattr(644,root,root,755)
%{_datadir}/%{name}/firmware

%files udev-rules
%defattr(644,root,root,755)
/etc/udev/rules.d/11-hplj10xx.rules
