\def\fileversion{0.1}
\def\filedate{2021/09/15}

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\typeout{^^J  ***  LaTeX class for IACR Communications on Cryptology v\fileversion\space ***^^J}
\ProvidesClass{iacrcc}[\filedate]

% IACR Communications in Cryptology DOCUMENT CLASS
% Authoritative source is github.com/IACR/latex/iacrcc
% This is originally based on
%   iacrtrans: github.com/Cryptosaurus/iacrtrans
%   acmart: github.com/borisveytsman/acmart
%
% To the extent possible under law, the author(s) have dedicated all
% copyright and related and neighboring rights to this software to the
% public domain worldwide. This software is distributed without any
% warranty.
%
% You should have received a copy of the CC0 Public Domain Dedication
% along with this software. If not, see
% <http://creativecommons.org/publicdomain/zero/1.0/>.
%
%
%%% Class options:
%
%% Document mode
% [preprint]      Preprint (no copyright info) -- default mode
% [submission]    Anonymous submission
% [notanonymous]  Keep author names in submission mode
% [final]         Final version
%% Package options
% [floatrow]      Load floatrow package with correct captions
% [nohyperref]    Disable automatic loading of hyperref
% [nolastpage]    Disable automatic loading of lastpage
% [xcolor=xxx]    Pass xxx to xcolor package
% [hyperref=xxx]  Pass xxx to hyperref package
%
%%% HOWTO use this class
%
%% Title
% This should look like:
% \title[running={The iacrcc class},onclick={https://github.com/IACR/latex},subtitle={LaTeX Class Documentation}]{How to Use the IACR Communications in Cryptology Class}
% Where the options in square brackets “[ ]”are optional and control the following:
% running: the running title displayed in the headers
% onclick: define what to do when clicking on the title. This could be used to point to a webpage associated with this paper. 
% subtitle: provide a subtitle
%
%% Authors are listed individually using the \addauthor tag followed by a list of affiliations.
% The idea is that every author makes a separate call to this command.
% This should look like:
% \addauthor[inst={1,2},orcid=0000-0000-0000-0000,onclick={www.test.com},footnote={I would like to thanks my mom for the support.}]{Alice Accomplished}
% Where the options in square brackets “[ ]”are optional and control the following:
%  inst: a numerical list pointing to the index of the institutaion in the affiliation array.
%  orcid: create a small clickable orcid logo next to the authors name linking to the authors ORCID iD see: orcid.org.
%  footnote: create an author-specific footnote.
%  onclick: define what to do when clicking on the author name: e.g.,~can point to the academic webpage.
%
%& Affiliations are listed individually using the \affiliations command *after* the (list of) authors using \addauthor
% This should look like:
% \affiliation[ror=05f950310,onclick={http://www.kuleuven.be/english}]{KU Leuven}
% Where the options in square brackets “[ ]”are optional and control the following:
%  ror: provide the Research Organization Registry (ROR) indetifier for this affiliation (see: ror.org). This is used for meta-data collection only.
%  onclick: define what to do when clicking on the affiliation name: e.g., can point to the affiliation webpage.
%
% A footnote can be placed on the front page without a symbol / numbering using:
% \genericfootnote{This is the full version of our paper published at XX}
%
% \begin{abstract}
% Lorem ipsum dolor sit amet...
% \end{abstract}
%
%% Warnings
% - please don't use any \pagestyle or \thispagestyle command
% - if you have proof with explicit \qed inside, you should either
%   remove \qed symbols or replace them by \qedhere

% Common definitions
\RequirePackage{xkeyval}
\def\publname{IACR Communications on Cryptology}
\def\IACR@vol{0}
\def\IACR@no{0}
\def\IACR@fp{1}
\def\IACR@lp{\if@loadhr\pageref*{LastPage}\else\pageref{LastPage}\fi}
\def\IACR@ISSN{XXXX-XXXX}
\def\IACR@DOI{XXXXXXXX}
\def\IACR@Received{20XX-XX-XX}
\def\IACR@Revised{20XX-XX-XX}
\def\IACR@Accepted{20XX-XX-XX}
\def\IACR@Published{20XX-XX-XX}
\newif\if@IACR@Received \@IACR@Receivedfalse
\newif\if@IACR@Revised \@IACR@Revisedfalse
\newif\if@IACR@Accepted \@IACR@Acceptedfalse
\newif\if@IACR@Published \@IACR@Publishedfalse

\newcommand{\setfirstpage}[1]{\def\IACR@fp{#1}\setcounter{page}{#1}}
\newcommand{\setlastpage}[1]{\def\IACR@lp{#1}}
\newcommand{\setvolume}[1]{\def\IACR@vol{#1}}
\newcommand{\setnumber}[1]{\def\IACR@no{#1}}
\newcommand{\setISSN}[1]{\def\IACR@ISSN{#1}}
\newcommand{\setDOI}[1]{\def\IACR@DOI{#1}}

\newcommand{\setReceived}[1]{\@IACR@Receivedtrue\def\IACR@Received{#1}}
\newcommand{\setRevised}[1]{\@IACR@Revisedtrue\def\IACR@Revised{#1}}
\newcommand{\setAccepted}[1]{\@IACR@Acceptedtrue\def\IACR@Accepted{#1}}
\newcommand{\setPublished}[1]{\@IACR@Publishedtrue\def\IACR@Published{#1}}

% Options
\newif\if@loadhr
\@loadhrtrue
\newif\if@hyperxmp@doi
\@hyperxmp@doifalse
\define@key{IACR}{nohyperref}[]{\@loadhrfalse}
\newif\if@floatrow
\@floatrowfalse
\define@key{IACR}{floatrow}[]{\@floatrowtrue}
\newif\if@submission
\@submissionfalse
\newif\if@anonymous
\@anonymousfalse
\newif\if@preprint
\@preprinttrue
\define@key{IACR}{final}[]{\PassOptionsToClass{\CurrentOption}{article}\@preprintfalse}
\define@key{IACR}{preprint}[]{\@preprinttrue}      % Default
\define@key{IACR}{submission}[]{\@submissiontrue\@anonymoustrue}
\define@key{IACR}{notanonymous}[]{\@anonymousfalse}
\newif\if@IACR@lastpage
\@IACR@lastpagetrue
\define@key{IACR}{nolastpage}[]{\@IACR@lastpagefalse}

\define@key{IACR}{xcolor}{\PassOptionsToPackage{#1}{xcolor}}
\define@key{IACR}{hyperref}{\PassOptionsToPackage{#1}{hyperref}}

\DeclareOptionX*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptionsX<IACR>\relax

% article class with a4paper
\LoadClass[10pt,twoside]{article}[2007/10/19]

% Hyperref must be loaded last, but before other AtEndPreamble hooks
\if@loadhr
  \RequirePackage{xcolor}
  \RequirePackage{etoolbox}
  % Make robust some counters that are made fragile by `calc` needed for orcidlink
  \robustify\setcounter
  \robustify\addtocounter
  \robustify\setlength
  \robustify\addtolength
  \RequirePackage{xstring} % for IfSubStr
  
  \AtEndPreamble{
    \@ifpackageloaded{hyperref}{}{\RequirePackage{hyperref}}
    \hypersetup{pdflang=en}
    \hypersetup{urlcolor=cyan}
    \hypersetup{colorlinks=true,
      citecolor=black!70!green,
      linkcolor=black!70!red}
    % Disable latexdiff commands in PDF links
    \pdfstringdefDisableCommands{%
      \def\DIFadd#1{#1}%
      \def\DIFdel#1{}%
    }
    % Old versions of hyperxmp do not support DOI
    \@ifpackagelater{hyperxmp}{2019/03/14}{\@hyperxmp@doitrue\hypersetup{keeppdfinfo=true}}{}
  }
  \RequirePackage{hyperxmp} % hyperxmp 5.x has issues with AtEndPreamble
  \setcounter{tocdepth}{2}
\fi

% Geometry
\RequirePackage[a4paper,hscale=0.65,vscale=0.75,marginratio=1:1,marginparwidth=2.7cm]{geometry}
\RequirePackage{afterpage}
% Title fonts: bf+sf
\RequirePackage{sectsty}
\allsectionsfont{\sffamily\boldmath}
% Also for descriptions
\renewcommand*\descriptionlabel[1]{\hspace\labelsep
                                   \normalfont\bfseries\sffamily\boldmath #1}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This copies over definition of the orcidlink from the orcidlink style file
% by by Leo C. Stein which in turn is a package around Milo's code on TeX.SE,
% see https://tex.stackexchange.com/a/445583/34063

\RequirePackage{tikz}
\ProcessOptions\relax
\usetikzlibrary{svg.path}

\definecolor{orcidlogocol}{HTML}{A6CE39}
\tikzset{
  orcidlogo/.pic={
    \fill[orcidlogocol] svg{M256,128c0,70.7-57.3,128-128,128C57.3,256,0,198.7,0,128C0,57.3,57.3,0,128,0C198.7,0,256,57.3,256,128z};
    \fill[white] svg{M86.3,186.2H70.9V79.1h15.4v48.4V186.2z}
                 svg{M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5c34.9,0,42.9-26.5,42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7V172.4z}
                 svg{M88.7,56.8c0,5.5-4.5,10.1-10.1,10.1c-5.6,0-10.1-4.6-10.1-10.1c0-5.6,4.5-10.1,10.1-10.1C84.2,46.7,88.7,51.3,88.7,56.8z};
  }
}

% Reciprocal of the height of the svg whose source is above.  The
% original generates a 256pt high graphic; this macro holds 1/256.
\newcommand{\@OrigHeightRecip}{0.00390625}

% We will compute the current X height to make the logo the right height
\newlength{\@curXheight}

\DeclareRobustCommand\orcidlink[1]{%
\texorpdfstring{%
\setlength{\@curXheight}{\fontcharht\font`X}%
\href{https://orcid.org/#1}{\XeTeXLinkBox{\mbox{%
\begin{tikzpicture}[yscale=-\@OrigHeightRecip*\@curXheight,
xscale=\@OrigHeightRecip*\@curXheight,transform shape]
\pic{orcidlogo};
\end{tikzpicture}%
}}}}{}}

% End of macros for orcidlink
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Add support for keys
\RequirePackage{pgfkeys}

\pgfkeys{/IACR-author/entities/.cd,
  inst/.initial=\@empty,
  orcid/.initial=\@empty,
  footnote/.initial=\@empty,
  onclick/.initial=\@empty,
  running/.initial=\@empty,
  }
\def\IACR@author@params@set@keys#1{%%
  \pgfkeys{/IACR-author/entities/.cd,#1}}
\def\IACR@author@params@get#1{%%
  \pgfkeysvalueof{/IACR-author/entities/#1}}
\newcommand\IACR@author@params@clearkeys{%
  \IACR@author@params@set@keys{inst=\@empty,orcid=\@empty,footnote=\@empty,onclick=\@empty,running=\@empty}%
}

\pgfkeys{/IACR-affiliation/entities/.cd,
  ror/.initial=\@empty,
  onclick/.initial=\@empty,
  department/.initial=\@empty,
  street/.initial=\@empty,
  city/.initial=\@empty,
  state/.initial=\@empty,
  zip/.initial=\@empty,
  country/.initial=\@empty,
  }
\def\IACR@affiliation@params@set@keys#1{%%
  \pgfkeys{/IACR-affiliation/entities/.cd,#1}}
\def\IACR@affiliation@params@get#1{%%
  \pgfkeysvalueof{/IACR-affiliation/entities/#1}}
\newcommand\IACR@affiliation@params@clearkeys{%
  \IACR@affiliation@params@set@keys{ror=\@empty,onclick=\@empty,department=\@empty,street=\@empty,city=\@empty,state=\@empty,zip=\@empty,country=\@empty}%
}

\pgfkeys{/IACR-title/entities/.cd,
  running/.initial=\@empty,
  onclick/.initial=\@empty,
  subtitle/.initial=\@empty,
  }
\def\IACR@title@params@set@keys#1{%%
  \pgfkeys{/IACR-title/entities/.cd,#1}}
\def\IACR@title@params@get#1{%%
  \pgfkeysvalueof{/IACR-title/entities/#1}}
\newcommand\IACR@title@params@clearkeys{%
  \IACR@title@params@set@keys{running=\@empty,onclick=\@empty,subtitle=\@empty}%
}

% Title/Author/affiliations
\global\let\IACR@runningauthors\@empty
\global\let\@author\@empty
\global\let\@affiliation\@empty

\newcounter{IACR@author@cnt}
\newcounter{IACR@inst@cnt}
\newif\if@IACR@autoinst
\@IACR@autoinsttrue
\def\IACR@author@last{0}

\newwrite\meta
\immediate\openout\meta=\jobname.meta
\RequirePackage{pgfplots}
\newcount\num@authors
\num@authors=0\relax
\newcount\num@affil
\num@affil=0\relax

\AtEndDocument{\immediate\closeout\meta}

\renewcommand\maketitle{\par
  \immediate\write\meta{title: \@plaintitle}%
  \ifx\@subtitle\@empty\else
    \immediate\write\meta{\IACRSS subtitle: \@subtitle}%
  \fi
  %  
  \begingroup
    \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
    \long\def\@makefntext##1{\parindent 1em\noindent
            \hb@xt@1.8em{%
                \hss\@textsuperscript{\normalfont\@thefnmark}}##1}%
    \newpage
    \global\@topnum\z@   % Prevents figures from going at top of page.
    \@maketitle
    \thispagestyle{title}\@thanks
  \endgroup
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@date\@empty
  \global\let\title\relax
  \global\let\date\relax
  \global\let\and\relax
  \global\let\email\relax
  % Adjust header size for title page
  \addtolength{\headheight}{\baselineskip}%
  \addtolength{\headsep}{-\baselineskip}%
  \afterpage{%
    \global\advance\headheight by -\baselineskip%
    \global\advance\headsep by \baselineskip%
  }%
}

% Add support for a footnote without symbol on the front page
\gdef\@genericfootnote{\@empty}
\newcommand\genericfootnote[1]{\gdef\@genericfootnote{\renewcommand\thefootnote{}\footnotetext{#1}}}

\def\@maketitle{%
  % Count authors and affiliations
  \setcounter{IACR@author@cnt}{1}%
  \setcounter{IACR@inst@cnt}{1}%
  \setbox0\hbox{\def\thanks##1{\global\@IACR@autoinstfalse}\def\inst##1{\global\@IACR@autoinstfalse}\def\and{\stepcounter{IACR@author@cnt}}\@author}%
  \setbox0\hbox{\def\and{\stepcounter{IACR@inst@cnt}}\@affiliation}%
  \xdef\IACR@author@last{\theIACR@author@cnt}%
  \edef\IACR@inst@last{\theIACR@inst@cnt}%
  \ifnum\IACR@author@last=\IACR@inst@last\else\@IACR@autoinstfalse\fi
  \ifnum\IACR@author@last=1 \@IACR@autoinstfalse\fi
  \newpage
  \null
  \vskip 2em%
  \begin{center}%
  \let \footnote \thanks
    {\def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
      {\LARGE \bfseries\sffamily\boldmath \@title\@genericfootnote\par}
    \ifdefined\@subtitle\vskip .5em{\large\sffamily\bfseries\@subtitle\par}\fi}%
    \vskip 1.5em%
    {\large
      \lineskip .5em%
        \if@anonymous
        Anonymous Submission
        \else
        \setcounter{IACR@author@cnt}{1}%
        \def\and{\if@IACR@autoinst\inst{\theIACR@author@cnt} \fi
          \stepcounter{IACR@author@cnt}%
          \ifnum\theIACR@author@cnt=\IACR@author@last\unskip\space and \ignorespaces\else\unskip, \ignorespaces\fi}
        \@author\if@IACR@autoinst\inst{\theIACR@author@cnt}\fi
        \vskip 1em\par
        \small
        \setcounter{IACR@author@cnt}{1}%        
        % When there is only one author with one or more affiliations
        % do not display the affiliation counter
        \def\and{\par\ifnum\num@authors=1\relax\else\stepcounter{IACR@author@cnt}$^\theIACR@author@cnt$~\fi}
        \ifnum\num@authors=1\relax\else
          \ifnum\IACR@inst@last>1 $^1$~\fi\ignorespaces%
        \fi
        \@affiliation
        \fi
      }%
  \end{center}%
  \par
  \vskip 1.5em}

% This is for indentation in meta file.
\newcommand{\IACRSS}{\space\space}

\renewcommand\author[2][]{\ClassError{iacrcc}{%
  Do not use the \string\author\space macro: use the \string\addauthor\space macro instead}{}%
}

\newcommand\surname[1]{#1}

\newcommand\addauthor[2][]{%    
  % Some very basic checking if addauthor is used correctly
  % Check if the name contains an "," this might be correct (e.g., Alice, Jr)
  \IfSubStr{\detokenize{#2}}{,}{\ClassWarning{iacrcc}{%
      Do not put several authors in the same \string\addauthor\space macro!}}{}%
  % Affiliations should be defined *after* addauthor
  \ifnum\num@affil>0\relax
    \ClassError{iacrcc}{affiliations must follow authors}{}%
  \fi
  % Do not use " and " in your author name: this might indicate incorrect usage
  % The usage of "\and" will not and throw an error.
  \IfSubStr{#2}{ and }{\ClassError{iacrcc}{%
      Do not put several authors in the same \string\addauthor\space macro!}{}}{}%   
  \global\advance\num@authors by 1\relax%
  %
  % Write out the author in the meta file.
  \immediate\write\meta{author:}%
  \immediate\write\meta{\IACRSS name: \unexpanded{#2}}%
  \renewcommand\surname[1]{##1}%
  \IACR@author@params@set@keys{#1}%
  \immediate\write\meta{\IACRSS affil: \IACR@author@params@get{inst}}%
  \edef\@IACRorcid{\IACR@author@params@get{orcid}}%
  \edef\@IACRfootnote{\IACR@author@params@get{footnote}}%
  \edef\@IACRonclick{\IACR@author@params@get{onclick}}%
  \edef\@IACRinst{\IACR@author@params@get{inst}}%
  \edef\@IACRrunningauthor{\IACR@author@params@get{running}}%
  % Author name + optionally clickable
  \ifx\@author\@empty
    \ifx\@IACRonclick\@empty
	  \def\@author{#2}%
	\else
	  \edef\@author{\noexpand\href{\@IACRonclick}{\noexpand\color{black}{#2}}}%
	\fi
  \else
    \ifx\@IACRonclick\@empty
	  \appto\@author{\and#2}%
	\else
	  \eappto\@author{\noexpand\and\noexpand\href{\@IACRonclick}{\noexpand\color{black}{#2}}}%
	\fi
  \fi
  % Add the footnote text if present
  \ifx\@IACRfootnote\@empty\else
    \eappto\@author{\noexpand\footnote{\@IACRfootnote}}%
  \fi
  \ifx\@IACRorcid\@empty\else
    \eappto\@author{~\noexpand\orcidlink{\@IACRorcid}}%
    \immediate\write\meta{\IACRSS orcid: \@IACRorcid}%
  \fi
  \ifx\@IACRinst\@empty\else
    \eappto\@author{\noexpand\inst{\@IACRinst}}%
  \fi
  \ifx\@IACRrunningauthor\@empty
    \ifx\IACR@runningauthors\@empty
	  \edef\IACR@runningauthors{#2}%
	\else
	  \eappto\IACR@runningauthors{, #2}%
	\fi
  \else
    \ifx\IACR@runningauthors\@empty
      \edef\IACR@runningauthors{\@IACRrunningauthor}%
	\else
	  \eappto\IACR@runningauthors{, \@IACRrunningauthor}%
	\fi
  \fi
  \IACR@author@params@clearkeys%
}

% Provide the title of the paper
\renewcommand\title[2][]{%
  \IACR@title@params@set@keys{#1}%
  \edef\@IACRrunning{\IACR@title@params@get{running}}%
  \edef\@IACRonclick{\IACR@title@params@get{onclick}}%
  \edef\@IACRsubtitle{\IACR@title@params@get{subtitle}}%
  \gdef\@plaintitle{#2}
  \ifx\@IACRrunning\@empty
    \gdef\IACR@runningtitle{#2}%
  \else
    \gdef\IACR@runningtitle{\@IACRrunning}%
  \fi
  \ifx\@IACRonclick\@empty
    \edef\@title{#2}%
  \else
    \edef\@title{\noexpand\href{\@IACRonclick}{\noexpand\color{black}{#2}}}%
  \fi
  \ifx\@IACRsubtitle\@empty
    \gdef\@subtitle{\@empty}%
  \else
    \gdef\@subtitle{\@IACRsubtitle}%
  \fi
  \IACR@title@params@clearkeys%
}

\newcommand{\email}[2][\mailto]{%
  \def\mailto{#2}%
  , \href{mailto:#1}{\nolinkurl{#2}}%
}

\newcommand\affiliation[2][]{%
  \global\advance\num@affil by 1\relax% 
  \immediate\write\meta{affiliation:}%
  \immediate\write\meta{\IACRSS name: \unexpanded{#2}}%  
  \IACR@affiliation@params@set@keys{#1}%%
  \edef\@IACRror{\IACR@affiliation@params@get{ror}}%
  \edef\@IACRonclick{\IACR@affiliation@params@get{onclick}}%
  \edef\@IACRdepartment{\IACR@affiliation@params@get{department}}%
  \edef\@IACRstreet{\IACR@affiliation@params@get{street}}%
  \edef\@IACRcity{\IACR@affiliation@params@get{city}}%
  \edef\@IACRstate{\IACR@affiliation@params@get{state}}%
  \edef\@IACRzip{\IACR@affiliation@params@get{zip}}%
  \edef\@IACRcountry{\IACR@affiliation@params@get{country}}%
  \ifx\@IACRror\@empty\else
    \immediate\write\meta{\IACRSS ror: \@IACRror}%
  \fi  
  \ifx\@IACRdepartment\@empty\else
    \immediate\write\meta{\IACRSS department: \@IACRdepartment}%
  \fi
  \ifx\@IACRstreet\@empty\else
    \immediate\write\meta{\IACRSS street: \@IACRstreet}%
  \fi
  \ifx\@IACRcity\@empty\else
    \immediate\write\meta{\IACRSS city: \@IACRcity}%
  \fi
  \ifx\@IACRstate\@empty\else
    \immediate\write\meta{\IACRSS state: \@IACRstate}%
  \fi
  \ifx\@IACRzip\@empty\else
    \immediate\write\meta{\IACRSS zip: \@IACRzip}%
  \fi
  \ifx\@IACRcountry\@empty\else
    \immediate\write\meta{\IACRSS country: \@IACRcountry}%
  \fi
  \ifx\@IACRonclick\@empty
    \ifx\@affiliation\@empty
      \gdef\@affiliation{\unexpanded{#2}}%
    \else
      \appto\@affiliation{\and\unexpanded{#2}}%
    \fi
  \else
    \ifx\@affiliation\@empty
      \edef\@affiliation{\noexpand\href{\@IACRonclick}{\noexpand\color{black}{\unexpanded{#2}}}}%
    \else
      \eappto\@affiliation{\noexpand\and{\noexpand\href{\@IACRonclick}{\noexpand\color{black}{\unexpanded{#2}}}}}%
    \fi
  \fi	
  \IACR@affiliation@params@clearkeys%
}

\if@anonymous
\gdef\@author{Anonymous Submission to \publname}
\renewcommand{\addauthor}[2][]{}
\renewcommand{\authorrunning}[1]{}
\renewcommand{\affiliation}[2][]{}
\fi

\newcommand{\inst}[1]{%
  \ifnum\num@authors=1\relax\else
    \ifnum\num@affil=1\relax\else
      \unskip$^{#1}$%
    \fi
  \fi}
  
\def\fnmsep{\unskip$^,$}

% Head/foot
\RequirePackage{fancyhdr}
\RequirePackage{graphicx}

\if@submission
\else
  \if@preprint
  \else
    % recent versions of hyperxmp load totpages, which conflicts with lastpage
    \@ifpackageloaded{totpages}{
      \def\IACR@lp{\if@loadhr\pageref*{TotPages}\else\pageref{TotPages}\fi}
    }{
      \if@IACR@lastpage
        \RequirePackage{lastpage}
      \else
        \typeout{IACR Trans: not loading lastpage, please use \@backslashchar setlastpage}
      \fi%!lastpage
    }
  \fi%!preprint
\fi%!submission

\fancypagestyle{title}{%
\fancyhf{} % clear all header and footer fields
\if@submission
\else
  \if@preprint
  \else
    \fancyhead[L]{%
      \small%
      \publname{}\\
      ISSN~\IACR@ISSN, Vol.~\IACR@vol, No.~\IACR@no, pp.~\IACR@fp--\IACR@lp. \hfill{}%
      \if@loadhr{\href{https://doi.org/\IACR@DOI}{DOI:\IACR@DOI}}\else{DOI:\IACR@DOI}\fi%
    }
    \fancyfoot[L]{%
      \small%
      Licensed under %
      \if@loadhr{\href{http://creativecommons.org/licenses/by/4.0/}{Creative Commons License CC-BY 4.0.}}%
      \else{Creative Commons License CC-BY 4.0.}%
      \fi%
      \hfill{}%
      \includegraphics[clip,height=2ex]{CC-by}\\[.1em]%
      \if@IACR@Received Received: \IACR@Received \hfill{} \fi%
      \if@IACR@Revised Revised: \IACR@Revised \hfill{} \fi%
      \if@IACR@Accepted Accepted: \IACR@Accepted \hfill{} \fi%
      \if@IACR@Published Published: \IACR@Published \fi%
    }%
    \if@loadhr
      \hypersetup{pdfcopyright={Licensed under Creative Commons License CC-BY 4.0.}}
      \hypersetup{pdflicenseurl={http://creativecommons.org/licenses/by/4.0/}}
      \hypersetup{pdfsubject={\publname{}, DOI:\IACR@DOI}}
    \fi
  \fi%!preprint
\fi%!submission

\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
}%fancypagestyle

\fancyhf{}
\fancyhead[RO,LE]{\thepage}
\fancyhead[RE]{%
  \ifdefined\IACR@runningtitle\IACR@runningtitle%
  \else%
    \def\thanks##1{}%
    \def\fnmsep{}%
    \def\\{}%
    \def\footnote##1{}%
    \@title%
  \fi}
\fancyhead[LO]{%
  \ifx\IACR@runningauthors\@empty
    \def\thanks##1{}%
    \def\inst##1{}%
    \def\fnmsep{}%
    \def\\{}%
    \def\footnote##1{}%
    \setcounter{IACR@author@cnt}{1}%
    \def\and{\stepcounter{IACR@author@cnt}%
      \ifnum\theIACR@author@cnt=\IACR@author@last\unskip\space and \ignorespaces \else\unskip, \ignorespaces\fi}
    \@author%
  \else
    \IACR@runningauthors%
  \fi}

\renewcommand{\markboth}[2]{}
\pagestyle{fancy}

%Abstract style, keywords
\def\@IACR@keywords{No keywords given.}

\def\keywords{\@ifnextchar[{\IACR@@@keywords}{\IACR@@keywords}}
\def\IACR@@@keywords[#1]#2{\gdef\@IACR@PDFkeywords{#1}\gdef\@IACR@keywords{#2}}
\def\IACR@@keywords#1{\gdef\@IACR@keywords{#1}}

\renewenvironment{abstract}{%
  \def\and{,\space}\edef\@writekeywords{\@IACR@keywords}%
  \immediate\write\meta{keywords: \@writekeywords}%
  \small\quotation\setlength{\parindent}{0pt}\noindent
  \textbf{\textsf{Abstract.}}}
  {\smallskip\par\textbf{\textsf{Keywords:}}
    \def\and{\unskip\space\textperiodcentered\space\ignorespaces}\@IACR@keywords
  \endquotation%
  \if@loadhr
    %% PDF keywords
    \def\and{, }%
    \def\thanks##1{}%
    \def\footnote##1{}%
    \def\inst##1{}%
    \def\fnmsep{}%
    \def\\{}%
    \def\zap@first@space ##1{##1}
    \def\insert@last@space##1,##2{%
      ##1%
      \ifx##2\@empty\space\else, \expandafter\insert@last@space##2\fi}
    \def\zap@comma@space##1 ,##2{%
      ##1%
      \ifx##2\@empty\else, \expandafter\zap@comma@space##2\fi}
    \def\zap@dbl@space##1 ##2{%
      ##1%
      \ifx##2\@empty\else\space\expandafter\zap@dbl@space##2\fi}
    \ifdefined\@IACR@PDFkeywords
      \hypersetup{pdfkeywords=\@IACR@PDFkeywords}
    \else
      \protected@edef\@tmp{\expandafter\@IACR@keywords}
      \protected@edef\@tmp{\expandafter\insert@last@space\@tmp,\@empty}
      \protected@edef\@tmp{\expandafter\zap@comma@space\@tmp ,\@empty}
      \protected@edef\@tmp{\expandafter\insert@last@space\@tmp,\@empty}
      \protected@edef\@tmp{\expandafter\zap@dbl@space\@tmp \@empty}
      \protected@edef\@tmp{\expandafter\zap@first@space \@tmp}
      \hypersetup{pdfkeywords=\@tmp}
    \fi
    %% PDF author
    \def\zap@one##1,##2{##1}
    \def\zap@last##1,##2{\ifx##1\@empty\else\space and \expandafter\zap@one##1\fi}
    \def\zap@last@comma##1,##2,##3{%
      ##1%
      \ifx##3\@empty%
      \expandafter\zap@last\else
      ,\expandafter\zap@last@comma\fi%
      ##2,##3}
    \ifx\IACR@runningauthors\@empty
	  \protected@edef\@tmp{\expandafter\@author}
      \protected@edef\@tmp{\expandafter\insert@last@space\@tmp,\@empty}
      \protected@edef\@tmp{\expandafter\zap@comma@space\@tmp ,\@empty}
      \protected@edef\@tmp{\expandafter\insert@last@space\@tmp,\@empty}
      \protected@edef\@tmp{\expandafter\zap@dbl@space\@tmp \@empty}
      \ifx\@tmp\empty\else
        \protected@edef\@tmp{\expandafter\zap@first@space \@tmp}
        \typeout{IACR@AUTHOR: \@tmp}
        \hypersetup{pdfauthor=\@tmp}
      \fi
	\else
	  \hypersetup{pdfauthor=\IACR@runningauthors}
      \typeout{IACR@AUTHOR: \IACR@runningauthors}
    \fi
    %% PDF title
    \ifdefined\IACR@runningtitle
      \hypersetup{pdftitle=\IACR@runningtitle}
      \typeout{IACR@TITLE: \IACR@runningtitle^^J}
    \else
      \protected@edef\@tmp{\expandafter\@title}
      \protected@edef\@tmp{\expandafter\insert@last@space\@tmp,\@empty}
      \protected@edef\@tmp{\expandafter\zap@dbl@space\@tmp \@empty}
      \ifx\@tmp\empty\else
        \protected@edef\@tmp{\expandafter\zap@first@space \@tmp}
        \hypersetup{pdftitle=\@tmp}
        \typeout{IACR@TITLE: \@tmp^^J}
      \fi
    \fi
    % PDF metadata
    \if@submission\else
      \if@preprint\else
        \if@hyperxmp@doi{
          \hypersetup{%
            pdfdoi=\IACR@DOI,%
            pdfissn=\IACR@ISSN,%
            pdfpubtype=journal,%
            pdfpublication=\publname,%
            pdfvolumenum=\IACR@vol,%
            pdfissuenum=\IACR@no,%
            pdfpagerange={\IACR@fp-\IACR@lp},%
        }}
      \fi
    \fi
  \fi
}


% autoref: capitals for Sections, and adding Algorithm
\def\equationautorefname{Equation}%
\def\footnoteautorefname{footnote}%
\def\itemautorefname{item}%
\def\figureautorefname{Figure}%
\def\tableautorefname{Table}%
\def\partautorefname{Part}%
\def\appendixautorefname{Appendix}%
\def\chapterautorefname{Chapter}%
\def\sectionautorefname{Section}%
\def\subsectionautorefname{Subsection}%
\def\subsubsectionautorefname{Subsubsection}%
\def\paragraphautorefname{paragraph}%
\def\subparagraphautorefname{subparagraph}%
\def\FancyVerbLineautorefname{line}%
\def\theoremautorefname{Theorem}%
\def\pageautorefname{page}%

\def\algorithmautorefname{Algorithm}

\def\definitionautorefname{Definition}
\def\exampleautorefname{Example}
\def\exerciseautorefname{Exercise}
\def\propertyautorefname{Property}
\def\questionautorefname{Question}
\def\solutionautorefname{Solution}
\def\propositionautorefname{Proposition}
\def\problemautorefname{Problem}
\def\lemmaautorefname{Lemma}
\def\conjectureautorefname{Conjecture}
\def\corollaryautorefname{Corollary}
\def\claimautorefname{Claim}
\def\remarkautorefname{Remark}
\def\noteautorefname{Note}
\def\caseautorefname{Case}

% AMS math
\RequirePackage{amsmath,amssymb,amsthm}
\RequirePackage{mathtools}
\theoremstyle{definition}
\newtheorem{definition}{Definition}
\newtheorem{example}{Example}
\newtheorem{exercise}{Exercise}
\newtheorem{property}{Property}
\newtheorem{question}{Question}
\newtheorem{solution}{Solution}

\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\newtheorem{problem}{Problem}
\newtheorem{lemma}{Lemma}
\newtheorem{conjecture}{Conjecture}
\newtheorem{corollary}{Corollary}
\newtheorem*{claim}{Claim}

\theoremstyle{remark}
\newtheorem{remark}{Remark}
\newtheorem{note}{Note}
\newtheorem{case}{Case}

\theoremstyle{plain}

% Floats and captions
\if@floatrow
\RequirePackage{floatrow}
\floatsetup[table]{style=Plaintop}
\RequirePackage{caption}
\captionsetup{labelfont={sf,bf}}
\else
\RequirePackage{float}
\newcommand\fs@iacrabove{%
  % Swap \abovecaptionskip and \belowcaptionskip
  \addtolength\abovecaptionskip{-\belowcaptionskip}
  \addtolength\belowcaptionskip{\abovecaptionskip}
  \addtolength\abovecaptionskip{-\belowcaptionskip}
  \setlength\abovecaptionskip{-\abovecaptionskip}
  \fs@plaintop%
  \def\@fs@cfont{\sffamily\bfseries}}
\newcommand\fs@iacrbelow{%
  \fs@plain%
  \def\@fs@cfont{\sffamily\bfseries}}
\floatstyle{iacrabove}
\restylefloat{table}
\floatstyle{iacrbelow}
\restylefloat{figure}
\fi

% Line # for submission
\newcommand\linenomathWithnumbersforAMS{%
  \ifLineNumbers
%%  \ifx\@@par\@@@par\else
    \ifnum\interlinepenalty>-\linenopenaltypar
      \global\holdinginserts\thr@@
      \advance\interlinepenalty \linenopenalty
     \ifhmode                                   % v4.3
      \advance\predisplaypenalty \linenopenalty
     \fi
%%      \advance\postdisplaypenalty \linenopenalty
      \advance\interdisplaylinepenalty \linenopenalty
    \fi
  \fi
  \ignorespaces
  }

\if@submission
\RequirePackage[mathlines]{lineno}
\RequirePackage{xcolor}
\linenumbers
\def\linenumberfont{\normalfont\tiny\sffamily\color{gray}}

% Taken from http://phaseportrait.blogspot.fr/2007/08/lineno-and-amsmath-compatibility.html
\newcommand*\patchAmsMathEnvironmentForLineno[1]{%
  \expandafter\let\csname old#1\expandafter\endcsname\csname #1\endcsname
  \expandafter\let\csname oldend#1\expandafter\endcsname\csname end#1\endcsname
  \renewenvironment{#1}%
     {\linenomathWithnumbersforAMS\csname old#1\endcsname}%
     {\csname oldend#1\endcsname\endlinenomath}}%
\newcommand*\patchBothAmsMathEnvironmentsForLineno[1]{%
  \patchAmsMathEnvironmentForLineno{#1}%
  \patchAmsMathEnvironmentForLineno{#1*}}%
\AtBeginDocument{%
\patchAmsMathEnvironmentForLineno{equation*}%
\patchBothAmsMathEnvironmentsForLineno{align}%
\patchBothAmsMathEnvironmentsForLineno{flalign}%
\patchBothAmsMathEnvironmentsForLineno{alignat}%
\patchBothAmsMathEnvironmentsForLineno{gather}%
\patchBothAmsMathEnvironmentsForLineno{multline}%
}
\fi

% Microtype
\RequirePackage{microtype}

% Fonts
\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}
\endinput
%end of file iacrcc.cls
