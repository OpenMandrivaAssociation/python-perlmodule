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
#Patch0:	pyperl-1.0.1d-disable-threads.patch
Patch1:		pyperl-1.0.1d-dont-rebuild-perl-object-at-install.patch
Patch2:		pyperl-1.0.1d-makefile.pl-fixes.patch
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
#%patch0 -p1 -b .nothreads
%patch1 -p1 -b .norebuild
%patch2 -p1 -b .makefixes

%build
%if !%multi_perl
rm -f MULTI_PERL
%endif

cd Python-Object
perl Makefile.PL INSTALLDIRS=vendor \
%if %multi_perl
	-DMULTI_PERL
%endif

%make
cd ..

ln -s Python-Object/blib/arch/auto/Python ./
python setup.py build

%install
rm -rf %{buildroot}
cd Python-Object
%makeinstall_std
cd ..
python setup.py install --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README TODO MANIFEST Changes
%{perl_vendorarch}/auto/Python
%{perl_vendorarch}/Python.pm
%{perl_vendorarch}/Python
%{_mandir}/man3/*
%{python_sitearch}/*

