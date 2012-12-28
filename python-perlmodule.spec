%define modname	pyperl

# tried enabled again as perl build now provides threads again, but breaks...
%bcond_with	multi_perl

Summary:	Perl for python - use perl code in python
Name:		python-perlmodule
Version:	1.0.1d
Release:	14
Source0:	%{modname}-%{version}.tar.lzma
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
License:	Artistic
Group:		Development/Python
Url:		http://search.cpan.org/dist/%{modname}/
BuildRequires:	perl-devel >= 5.6
BuildRequires:	pkgconfig(python)
Provides:	%{modname} = %{EVRD}

%description
Perlmodule makes it possible to embed perl interpreters in any
python program. It can be used to invoke arbitrary perl code, load
any perl modules, and make calls directly into perl functions. The
perl code invoked can call back into python as it sees fit.

%if %{with multi_perl}
This package is built with MULTI_PERL enabled, each python thread
gets its own separate perl interpreter.
%endif

%prep
%setup -q -n %{modname}-%{version}
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
%if %{with multi_perl}
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


%changelog
* Fri Dec 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.1d-14
- always link against python (P10)
- use %bcond_with for multi_perl

* Wed Jan 25 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.1d-13
+ Revision: 768358
- svn commit -m mass rebuild of perl extension against perl 5.14.2
- cleanup junk

* Wed Jan 26 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.1d-11
+ Revision: 632818
- fix regresion tests
- don't compile with '-Wno-error=format-security'
- really drop dead patch..
- link against libdl (P9)
- fix api breakages with new perl

  + Jérôme Quelin <jquelin@mandriva.org>
    - perl 5.12 rebuild
    - rebuild for perl 5.12

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 1.0.1d-8mdv2010.0
+ Revision: 442351
- rebuild

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix some compile warnings (P8)
    - really enable threads with %%multi_perl (although broken...)

* Tue Mar 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.1d-7mdv2009.1
+ Revision: 347874
- workaround enforced usage format security build errors

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 1.0.1d-6mdv2009.0
+ Revision: 259740
- rebuild

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 1.0.1d-5mdv2009.0
+ Revision: 247584
- rebuild

* Wed Feb 27 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.1d-3mdv2008.1
+ Revision: 175754
- comment out dead perl functions (updates P7)
- fix build with new perl
- provide pyperl
- fix installation bug in setup.py which sets root to '' if not specific
  (P6 from  Pedro Algarvio aka s0undt3ch <ufs@ufsoft.org>)
- fix backwards compatibility with older python (P5 from Pedro Algarvio aka s0undt3ch <ufs@ufsoft.org>)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Oct 20 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.1d-2mdv2008.1
+ Revision: 100557
- add check stage
  cleanups
- fix code to work with python 2.5, fixes crashes as well as broken list function (P4)
- fix tests so that they run again without errors (P3)
- move some things from spec to setup.py with some new stuff added (P1)

* Fri Oct 19 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.1d-1mdv2008.1
+ Revision: 100500
- revert various changes due to misunderstandings of various stuff (I suck:p)
- 1.0.1d
- try fix linking of Python::Object
- really disable the rest of thread stuff (P0)
- don't rebuild Python-Object during install (P1)
- fix short circuitting

* Sat Sep 15 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.1-8mdv2008.0
+ Revision: 86303
- rebuild


* Mon Jan 16 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.0.1-7mdk
- Fix build on x86_64

* Thu May 19 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.0.1-6mdk
- Rebuild for new perl

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 1.0.1-5mdk
- Rebuild for new python

* Mon Nov 15 2004 Michael Scherer <misc@mandrake.org> 1.0.1-4mdk 
- fix my own error

* Mon Nov 15 2004 Michael Scherer <misc@mandrake.org> 1.0.1-3mdk
- Rebuild for new perl
- add a switch for enabling multi_perl, and remove the feature

* Sun Oct 24 2004 Michael Scherer <misc@mandrake.org> 1.0.1-2mdk
- Rebuild

* Wed Jul 09 2003 Austin Acton <aacton@yorku.ca> 1.0.1-1mdk 
- andi payn <payn@myrealbox.com> :
  - Initial specfile
- install in vendor, not site
- trick manpages into installing (doc_vendor_install missing from makefile)

