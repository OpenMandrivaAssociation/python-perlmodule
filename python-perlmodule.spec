%define oname	pyperl

# tried enabled again as perl build now provides threads again, but breaks...
%bcond_with	multi_perl

Summary:	Perl for python - use perl code in python
Name:		python-perlmodule
Version:	1.0.1d
Release:	21
License:	Artistic
Group:		Development/Python
Url:		http://search.cpan.org/dist/%{oname}/
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
Patch10:	pyperl-1.0.1d-link-against-python.patch
BuildRequires:	perl-devel >= 5.6
BuildRequires:	pkgconfig(python2)
Provides:	%{oname} = %{EVRD}

%description
Perlmodule makes it possible to embed perl interpreters in any
python program. It can be used to invoke arbitrary perl code, load
any perl modules, and make calls directly into perl functions. The
perl code invoked can call back into python as it sees fit.

%if %{with multi_perl}
This package is built with MULTI_PERL enabled--each python thread
gets its own separate perl interpreter.
%endif

%prep
%setup -qn %{oname}-%{version}
%patch1 -p1 -b .improved~
%patch2 -p1 -b .makefixes~
%patch3 -p1 -b .fixtests~
%patch4 -p1 -b .python2.5~
%patch5 -p0 -b .oldpython~
%patch6 -p0 -b .fixsetup~
%patch7 -p1 -b .newperl~
%patch8 -p1 -b .format_warnings~
%patch9 -p1 -b .libdl~
%patch10 -p1 -b .py_link~

%build
%if !%{with multi_perl}
rm -f MULTI_PERL
%else
touch MULTI_PERL
%endif
%{__python2} setup.py build

%check
%{__python2} setup.py test

%install
%{__python2} setup.py install --root %{buildroot}

%files
%doc README TODO MANIFEST Changes
%{perl_vendorarch}/auto/Python
%{perl_vendorarch}/Python.pm
%{perl_vendorarch}/Python
%{_mandir}/man3/*
%{py2_platsitedir}/*

