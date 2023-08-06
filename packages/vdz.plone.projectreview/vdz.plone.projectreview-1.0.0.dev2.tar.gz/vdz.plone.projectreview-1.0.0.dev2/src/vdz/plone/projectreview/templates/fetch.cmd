@echo off
setlocal
set mydir=%~dp0
set mydrv=%~d0
cd /d S:\WiTraBau\07 Entwurf\Prototypen || goto error
hg branch plone
cd /d %mydir%
echo on
@rem Verbundprojekte auflisten, anlegen, bearbeiten:
copy s:pr_main.pt
@rem Teilprojekte eines Verbundprojekts:
copy s:pr_subprojects.pt
@rem Reviewstellen eines Verbundprojekts:
copy s:pr_reviewers.pt
@rem Ergebnisbogen eines Projekts:
copy s:pr_result.pt
@rem Ergebnis der Evaluation:
copy s:pr_report.pt
copy s:css\witrabau.css ..\static\

goto ende

:error
echo Ooops! >&2
:ende
