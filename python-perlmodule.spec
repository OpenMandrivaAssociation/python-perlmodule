%define oname	pyperl

# tried enabled again as perl build now provides threads again, but breaks...
%define multi_perl 0

Summary:	Perl for python - use perl code in python
Name:		python-perlmodule
Version:	1.0.1d
Release:	12
Source0:	%{oname}-%{version}.tar.lzma
Patch1:		pyperl-1.0.1d-improved-setup.py
Patch2:		pyperl-1.0.1d-makefile.pl-fixes.patch
Patch3:		pyperl-1.0.1d-fix-tests.patch
Patch4:		pyperl-1.0.1d-python2.5-fixes.patch
Patch5:		pyperl-1.0.1d-older-python-compat.patch
Patch6:		pyperl-1.0.1d-fix-setup-install.patch
Patch7:		pyperl-1.0.1d-new-perl-fix.patch
Patch8:		pyperl-1.0.1d-fix-format-warnings.patch
Patch9:		pyperl-1.0.1d-link-against-libdl.patch
License:	Artistic
Group:		Development/Python
Url:		http://search.cpan.org/dist/%{oname}/
BuildRequires:	perl-devel >= 5.6
BuildRequires:	python-devel >= 1.5.2
Provides:	%{oname} = %{EVRD}

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
%patch1 -p1 -b .improved~
%patch2 -p1 -b .makefixes~
%patch3 -p1 -b .fixtests~
%patch4 -p1 -b .python2.5~
%patch5 -p0 -b .oldpython~
%patch6 -p0 -b .fixsetup~
%patch7 -p1 -b .newperl~
%patch8 -p1 -b .format_warnings~
%patch9 -p1 -b .libdl~

%build
%if !%multi_perl
rm -f MULTI_PERL
%else
touch MULTI_PERL
%endif
python setup.py build

%check
python setup.py test

%install
python setup.py install --root %{buildroot}

%files
%doc README TODO MANIFEST Changes
%{perl_vendorarch}/auto/Python
%{perl_vendorarch}/Python.pm
%{perl_vendorarch}/Python
%{_mandir}/man3/*
%{python_sitearch}/*
