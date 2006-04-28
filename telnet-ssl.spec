# TODO:
# - telnetd:
#   - fix path to telnetlogin
#   - fix (or maybe not?) path to SSL certs
#   - provide inetd entry for both telnet and telnets ?
Summary:	Client for the telnet remote login protocol with support for SSL
Summary(pl):	Klient protoko³u telnet ze wsparciem dla SSL
Name:		telnet-ssl
Version:	0.17.24
Release:	0.1
License:	GPL
Group:		Networking
# based on debian telnet-ssl package
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	43a402139ed6b86434fdb83256feaad8
Source1:	telnetd-ssl.inetd
Patch0:		%{name}-debian.patch
Patch1:		%{name}-install.patch
# better url?
URL:		http://packages.debian.org/telnet-ssl
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The telnet command is used for interactive communication with another
host using the TELNET protocol.

SSL telnet(d) replaces normal telnet(d) using SSL authentication and
encryption. It interoperates with normal telnet(d) in both directions.
It checks if the other side is also talking SSL, if not it falls back
to normal telnet protocol.

Advantages over normal telnet(d): Your passwords and the data you send
will not go in cleartext over the line. Nobody can get it with tcpdump
or similar tools. With SSLtelnet you can also connect to https-server
like https://www.netscape.com.

%description -l pl
Polecenie telnet jest wykorzystywane do interaktywnej komunikacji z
innym komputerem przy u¿yciu protoko³u TELNET.

Telnet(d)-SSL zastêpuje telnet(d) dostarczaj±c wersjê rozszerzon± o
mo¿liwo¶æ autentykacji i szyfrowania SSL. Telnet(d)-SSL w pe³ni
wspó³pracuje ze standardowym telnet(d) - sprawdza czy aplikacja po
drugiej stronie wspiera SSL, je¶li nie prze³±cza siê do standardowego
protoko³u TELNET.

Korzy¶ci wzglêdem klasycznego telnet(d): has³a i dane nie bêd± wys³ane
czystym tekstem. Nikt nie bêdzie móg³ ich zobaczyæ korzystaj±c z
aplikacji takich jak tcpdump. Przy u¿yciu telnet-ssl mo¿liwe jest
tak¿e po³±czenie siê z serwerem www (n.p. https://www.netscape.com)
przy u¿yciu SSL.

%package -n telnetd-ssl
Summary:	Server for the telnet-ssl remote login protocol
Summary(pl):	Serwer us³ugi telnet-ssl
Group:		Networking
Requires:	inetdaemon
Requires:	login
Requires:	rc-inetd >= 0.8
Obsoletes:	inetutils-telnetd
Obsoletes:	telnet-server

%description -n telnetd-ssl
The telnet command is used for interactive communication with another
host using the TELNET protocol.

SSL telnet(d) replaces normal telnet(d) using SSL authentication and
encryption. It interoperates with normal telnet(d) in both directions.
It checks if the other side is also talking SSL, if not it falls back
to normal telnet protocol.

Advantages over normal telnet(d): Your passwords and the data you send
will not go in cleartext over the line. Nobody can get it with tcpdump
or similar tools. With SSLtelnet you can also connect to https-server
like https://www.netscape.com. Just do 'telnet www.netscape.com 443'.

This package provides server for the telnet-ssl.

%description -n telnetd-ssl -l pl
Polecenie telnet jest wykorzystywane do interaktywnej komunikacji z
innym komputerem przy u¿yciu protoko³u TELNET.

Telnet(d)-SSL zastêpuje telnet(d) dostarczaj±c wersjê rozszerzon± o
mo¿liwo¶æ autentykacji i szyfrowania SSL. Telnet(d)-SSL w pe³ni
wspó³pracuje ze standardowym telnet(d) - sprawdza czy aplikacja po
drugiej stronie wspiera SSL, je¶li nie prze³±cza siê do standardowego
protoko³u TELNET.

Korzy¶ci wzglêdem klasycznego telnet(d): has³a i dane nie bêd± wys³ane
czystym tekstem. Nikt nie bêdzie móg³ ich zobaczyæ korzystaj±c z
aplikacji takich jak tcpdump. Przy u¿yciu telnet-ssl mo¿liwe jest
tak¿e po³±czenie siê z serwerem www (n.p. https://www.netscape.com)
przy u¿yciu SSL.

Ten pakiet dostarcza serwer telnet-ssl.

%prep
%setup -q -n netkit-%{name}-%{version}+0.1.orig
%patch0 -p1
%patch1 -p1

%build
CFLAGS="%{rpmcflags} -D_GNU_SOURCE -DLOGIN_WRAPPER=\"/usr/bin/telnetlogin\""
CXXFLAGS="%{rpmcflags} -D_GNU_SOURCE -DLOGIN_WRAPPER=\"/usr/bin/telnetlogin\""
export CFLAGS CXXFLAGS
./configure \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--installroot=$RPM_BUILD_ROOT \
	--with-c-compiler="%{__cc}" \
	--with-c++-compiler="%{__cxx}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR="%{_mandir}" \
	SUB="telnet telnetd telnetlogin"

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/telnetd

%clean
rm -rf $RPM_BUILD_ROOT

%post -n telnetd-ssl
%service -q rc-inetd reload

%postun -n telnetd-ssl
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/telnet-ssl
%{_mandir}/man1/telnet-ssl*

%files -n telnetd-ssl
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/telnetd
%attr(755,root,root) %{_sbindir}/in.telnetd
%attr(755,root,root) %{_sbindir}/telnetlogin
%{_mandir}/man8/*
