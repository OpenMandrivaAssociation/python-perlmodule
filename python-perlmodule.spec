%define oname	pyperl
%define name	python-perlmodule
%define version 1.0.1d
%define release %mkrel 1

# removed as perl build no longer provides thread
%define multi_perl 0

Summary:	Perl for python - use perl code in python
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{oname}-%{version}.tar.lzma
Patch0:		pyperl-1.0.1d-disable-threads.patch
Patch1:		pyperl-1.0.1d-dont-rebuild-perl-object-at-install.patch
License:	Artistic
Group:		Development/Python
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url:		http://search.cpan.org/dist/%{oname}/
BuildRequires:	perl-devel >= 5.6
BuildRequires:	python-devel >= 1.5.2

%description
Perlmodule makes it possible to embed perl interpreters in any
python program. It can be used to invoke arbitrary perl code, load
any perl modules, and make calls directly into perl functions. The
perl code invoked can call back into python as it sees fit.

%if %multi_perl
This package is built with MULTI_PERL enabled--each python thread
gets its own separate perl interpreter.
%endif

%prep
%setup -q -n %{oname}-%{version}
%build
%if !%multi_perl
rm -f MULTI_PERL
%endif

cd Python-Object
CFLAGS="$RPM_OPT_FLAGS"
perl Makefile.PL  INSTALLDIRS=vendor\
%if %multi_perl
	-DMULTI_PERL \
%endif
	PREFIX=$RPM_BUILD_ROOT%{_prefix}
perl -pi -e 's/MAN3EXT = 3pm/MAN3EXT = 3/' Makefile
%make
cd ..
ln -sf Python-Object/blib/arch/auto/Python ./
python setup.py build
#for i in  Python-Object/blib/man3/*3pm ; do
#    mv -f $i ${i%%pm}
#done;

#python test.py

%install
rm -rf $RPM_BUILD_ROOT
cd Python-Object
make install_vendor
#mkdir -p $RPM_BUILD_ROOT/%_mandir/man3pm
#cp blib/man3/*.3pm $RPM_BUILD_ROOT/%_mandir/man3pm
cd ..
python setup.py install --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO MANIFEST Changes
%perl_vendorarch/auto/Python
%perl_vendorarch/Python.pm
%perl_vendorarch/Python
%{_mandir}/man3/*
%{_libdir}/python*/site-packages/*

