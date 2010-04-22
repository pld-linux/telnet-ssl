# TODO:
# - telnetd:
#   - fix (or maybe not?) path to SSL certs
#   - provide inetd entry for both telnet and telnets ?
Summary:	Client for the telnet remote login protocol with support for SSL
Summary(pl.UTF-8):	Klient protokołu telnet ze wsparciem dla SSL
Name:		telnet-ssl
Version:	0.17.24
Release:	0.1
License:	GPL
Group:		Networking
# based on debian (netkit-)telnet-ssl package
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

%description -l pl.UTF-8
Polecenie telnet jest wykorzystywane do interaktywnej komunikacji z
innym komputerem przy użyciu protokołu TELNET.

Telnet(d)-SSL zastępuje telnet(d) dostarczając wersję rozszerzoną o
możliwość uwierzytelniania i szyfrowania SSL. Telnet(d)-SSL w pełni
współpracuje ze standardowym telnet(d) - sprawdza czy aplikacja po
drugiej stronie wspiera SSL, jeśli nie przełącza się do standardowego
protokołu TELNET.

Korzyści względem klasycznego telnet(d): hasła i dane nie będą wysłane
czystym tekstem. Nikt nie będzie mógł ich zobaczyć korzystając z
aplikacji takich jak tcpdump. Przy użyciu telnet-ssl możliwe jest
także połączenie się z serwerem www (n.p. https://www.netscape.com)
przy użyciu SSL.

%package -n telnetd-ssl
Summary:	Server for the telnet-ssl remote login protocol
Summary(pl.UTF-8):	Serwer usługi telnet-ssl
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

%description -n telnetd-ssl -l pl.UTF-8
Polecenie telnet jest wykorzystywane do interaktywnej komunikacji z
innym komputerem przy użyciu protokołu TELNET.

Telnet(d)-SSL zastępuje telnet(d) dostarczając wersję rozszerzoną o
możliwość uwierzytelniania i szyfrowania SSL. Telnet(d)-SSL w pełni
współpracuje ze standardowym telnet(d) - sprawdza czy aplikacja po
drugiej stronie wspiera SSL, jeśli nie przełącza się do standardowego
protokołu TELNET.

Korzyści względem klasycznego telnet(d): hasła i dane nie będą wysłane
czystym tekstem. Nikt nie będzie mógł ich zobaczyć korzystając z
aplikacji takich jak tcpdump. Przy użyciu telnet-ssl możliwe jest
także połączenie się z serwerem www (n.p. https://www.netscape.com)
przy użyciu SSL.

Ten pakiet dostarcza serwer telnet-ssl.

%prep
%setup -q -n netkit-%{name}-%{version}+0.1.orig
%patch0 -p1
%patch1 -p1

sed -i -e "s|/usr/lib/telnetlogin|%{_sbindir}/telnetlogin|" telnetd/Makefile

%build
CFLAGS="%{rpmcflags} -D_GNU_SOURCE"
CXXFLAGS="%{rpmcflags} -D_GNU_SOURCE"
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
