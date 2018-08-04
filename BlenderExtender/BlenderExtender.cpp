// BlenderExtender.cpp : Defines the initialization routines for the DLL.
//

#include "stdafx.h"
#include "BlenderExtender.h"
#include <initguid.h>

// TODO: Only need one of these nippers:
#include <atlimage.h> 
#include <gdiplus.h>

#include "BlenderExtender_i.c"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

#define MAX_PATH 512


// This is pretty much an ASSERT().
#define ERRIF(c) if(!c) { fprintf(pOutputLog,"ERR: " #c); fflush(pOutputLog); return -1;}
class Application
{
private:
	int pid;
	HANDLE hOutputRead; // Includes stdout and stderr
	HANDLE hInputWrite;
	BOOL bRunThread;
	FILE *pOutputLog;

public:
	Application():
		pid (0),
		hOutputRead (NULL),
		hInputWrite (NULL),
		bRunThread (TRUE),
		pOutputLog (NULL)
	{
	}

	int run (const char *pszCommand, FILE *pOutputLog, bool bHidden)
	{
		HANDLE hOutputWrite;
		HANDLE hInputRead;
		HANDLE hErrorWrite;


		this->pOutputLog=pOutputLog;
		// Set up the security attributes struct.
		SECURITY_ATTRIBUTES sa;
		sa.nLength= sizeof(SECURITY_ATTRIBUTES);
		sa.lpSecurityDescriptor = NULL;
		sa.bInheritHandle = TRUE;

		// Create the pipes we need for wrting stdin and reading both stdout and stderr.
		{
			HANDLE hOutputReadTmp, hInputWriteTmp;
			ERRIF (CreatePipe(&hOutputReadTmp,&hOutputWrite,&sa,0));
			ERRIF (CreatePipe(&hInputRead,&hInputWriteTmp,&sa,0));
			ERRIF (DuplicateHandle(GetCurrentProcess(),hOutputWrite,GetCurrentProcess(),&hErrorWrite,0,TRUE,DUPLICATE_SAME_ACCESS));
			ERRIF (DuplicateHandle(GetCurrentProcess(),hOutputReadTmp,GetCurrentProcess(),&hOutputRead,0,FALSE,DUPLICATE_SAME_ACCESS));
			ERRIF (DuplicateHandle(GetCurrentProcess(),hInputWriteTmp,GetCurrentProcess(),&hInputWrite,0,FALSE,DUPLICATE_SAME_ACCESS));
			ERRIF (CloseHandle(hOutputReadTmp));
			ERRIF (CloseHandle(hInputWriteTmp));
		}

		// Set up the program startup settings
		PROCESS_INFORMATION pi;
		STARTUPINFO si;
		ZeroMemory(&si,sizeof(STARTUPINFO));
		si.cb = sizeof(STARTUPINFO);
		si.dwFlags = STARTF_USESTDHANDLES;
		si.hStdOutput = hOutputWrite;
		si.hStdInput  = hInputRead;
		si.hStdError  = hErrorWrite;
		if (bHidden)
		{
			si.dwFlags |= STARTF_USESHOWWINDOW;
			si.wShowWindow = SW_HIDE;
		}

		// letter rip!
		TCHAR *pszwCommand = new TCHAR[strlen (pszCommand) + 1];
		wsprintf (pszwCommand, _T("%S"), pszCommand);
		ERRIF (CreateProcess(NULL,pszwCommand,NULL,NULL,TRUE,CREATE_NEW_CONSOLE,NULL,NULL,&si,&pi));
		pid=pi.dwProcessId;
		delete[] pszwCommand;

		// Close all unnecessary handles (for our side).
		ERRIF (CloseHandle(pi.hThread));
		ERRIF (CloseHandle(hOutputWrite));
		ERRIF (CloseHandle(hInputRead ));
		ERRIF (CloseHandle(hErrorWrite));

		// Launch the thread that watches standard out.
		DWORD dwThreadId;
		HANDLE hThread = CreateThread(NULL,0,Application::_stdoutReadThread,this,0,&dwThreadId);
		ERRIF (hThread != NULL);

		// Wait until child process exits.
		WaitForSingleObject (pi.hProcess, INFINITE);

		// Tell the read thread to exit and wait for thread to die.
		bRunThread = FALSE;
		WaitForSingleObject(hThread,INFINITE);

		// clean up
		ERRIF (CloseHandle(hOutputRead));
		ERRIF (CloseHandle(hInputWrite));

		// get process exit code
		DWORD dwExitCode;
		ERRIF (GetExitCodeProcess(pi.hProcess,&dwExitCode));
		ERRIF (CloseHandle(pi.hProcess));
		return dwExitCode;
	}

	static DWORD WINAPI _stdoutReadThread(LPVOID lpParameter)
	{
		CHAR lpBuffer[256];
		DWORD nBytesRead;
		DWORD nCharsWritten;
		Application *pThis = (Application*)lpParameter;
		while (pThis->bRunThread)
		{
			if (!ReadFile(pThis->hOutputRead,lpBuffer,sizeof(lpBuffer), &nBytesRead,NULL) || !nBytesRead)
			{
				if (GetLastError() == ERROR_BROKEN_PIPE)
				{
					break; // Process exited and shut down its pipe.
				}
				continue;
			}
			fwrite(lpBuffer,1,nBytesRead,pThis->pOutputLog);
			fflush(pThis->pOutputLog);
		}
		return 0;
	}


};


//
//TODO: If this DLL is dynamically linked against the MFC DLLs,
//		any functions exported from this DLL which call into
//		MFC must have the AFX_MANAGE_STATE macro added at the
//		very beginning of the function.
//
//		For example:
//
//		extern "C" BOOL PASCAL EXPORT ExportedFunction()
//		{
//			AFX_MANAGE_STATE(AfxGetStaticModuleState());
//			// normal function body here
//		}
//
//		It is very important that this macro appear in each
//		function, prior to any calls into MFC.  This means that
//		it must appear as the first statement within the 
//		function, even before any object variable declarations
//		as their constructors may generate calls into the MFC
//		DLL.
//
//		Please see MFC Technical Notes 33 and 58 for additional
//		details.
//


// CBlenderExtenderApp


class CBlenderExtenderModule :
	public CAtlMfcModule
{
public:
	DECLARE_LIBID(LIBID_BlenderExtenderLib);
	DECLARE_REGISTRY_APPID_RESOURCEID(IDR_BLENDEREXTENDER, "{1C645451-545F-475E-9EAA-0057CB6092D7}");};

CBlenderExtenderModule _AtlModule;

BEGIN_MESSAGE_MAP(CBlenderExtenderApp, CWinApp)
END_MESSAGE_MAP()


// CBlenderExtenderApp construction

CBlenderExtenderApp::CBlenderExtenderApp()
{
	// TODO: add construction code here,
	// Place all significant initialization in InitInstance
}


// The one and only CBlenderExtenderApp object

CBlenderExtenderApp theApp;


// CBlenderExtenderApp initialization

BOOL CBlenderExtenderApp::InitInstance()
{
	COleObjectFactory::RegisterAll();
	CWinApp::InitInstance();

	return TRUE;
}


#define BUF_SIZE 512
HBITMAP CBlenderExtenderApp::Render(const TCHAR *szSettingsIni, LPCTSTR lpFileName, int width, int height, int frame)
{
	HBITMAP hBitmap = NULL;

	// Read info from the .ini file
	TCHAR szScriptPath[MAX_PATH];
	GetPrivateProfileString(_T("BlenderExtender"),_T("renderThis"),_T("k_renderThis.py"),szScriptPath,MAX_PATH,szSettingsIni);
	TCHAR szRenderPath[MAX_PATH];
	GetPrivateProfileString(_T("BlenderExtender"),_T("outdir"),_T("renders"),szRenderPath,MAX_PATH,szSettingsIni);

	// figger out the output filename
	int fnPos;
	for (fnPos = wcslen (lpFileName); fnPos > 0; --fnPos)
	{
		if (lpFileName[fnPos] == '\\')
		{
			++fnPos;
			break;
		}
	}
	TCHAR *szOutputPath = new TCHAR[wcslen (szRenderPath) + 1 + wcslen (&lpFileName[fnPos]) + 4 + 3];
	wsprintf (szOutputPath, _T("%s\\%s.png"), szRenderPath, &lpFileName[fnPos]);

	// build up a command line
	char *pszCommandLine=new char[8 + wcslen (szScriptPath) + 28 + wcslen (lpFileName) + 9 + wcslen (szOutputPath) + 1 + 1];
	sprintf(pszCommandLine,"python \"%S\" --w=96 --h=96 --filename=\"%S\" --out=\"%S\"", szScriptPath, lpFileName, szOutputPath);

	// run that puppy!
	char *szLogFilename = new char[wcslen (szOutputPath) + 5];
	sprintf (szLogFilename, "%S.log", szOutputPath);
	FILE *pLogFile = fopen (szLogFilename, "w");
	fprintf (pLogFile, "Executing:\n\t%s\n",pszCommandLine);
#if 1
#if 1
	Application a;
	int returnCode = a.run (pszCommandLine, pLogFile, true);
	bool bFailed = false;
#else
	int returnCode = system(pszCommandLine);
	bool bFailed=false;
#endif
#else
	FILE *pPipe = _popen (pszCommandLine, "rt");
	bool bFailed=false;
	int returnCode=-1;
	if (pPipe)
	{
		char szResultBuffer[BUF_SIZE];

		// Scan the stdout
		while(fgets (szResultBuffer, BUF_SIZE, pPipe))
		{
			printf ("%s", szResultBuffer);
			for (int i=0; szResultBuffer[i]; ++i)
				if (szResultBuffer[i]=='E' && 0==strncmp (&szResultBuffer[i], "[ERR]", 5))
					bFailed=true;

				fputs (szResultBuffer, pLogFile);
		}
		returnCode=_pclose (pPipe);
		fprintf (pLogFile, "Return code %d\n", returnCode);
	}
	else
	{
			fprintf (pLogFile, "[ERR] Unable to run \"%S\"\n", pszCommandLine);
	}
#endif

	CImage *poImage = NULL;
	if (returnCode != 0 || bFailed)
	{
		bFailed = true;
	}
	else
	{
		// Open the rendered image!
		CImage *poImage=new CImage ();
		if (S_OK != poImage->Load (szOutputPath))
		{
			fprintf (pLogFile, "ERR>> Image load failed \"%S\"\b", szOutputPath);
		}
		else
		{	
			COLORREF cr = GetSysColor (COLOR_WINDOW);
			HDC dcFinal = CreateCompatibleDC (NULL);
			hBitmap = CreateBitmap (96,96,1,32,NULL);
			SelectObject (dcFinal, hBitmap);
			HBRUSH hBrush = CreateSolidBrush (cr);
			RECT rect = {0,0,96,96};
			FillRect (dcFinal, &rect, hBrush);
			DeleteObject (hBrush);
			poImage->AlphaBlend (dcFinal, 0, 0);
			DeleteDC (dcFinal);

			DeleteFile (szOutputPath);
			DeleteFileA (szLogFilename);
		}
		delete poImage;

	}

	fclose (pLogFile);

	delete[] szOutputPath;
	delete[] pszCommandLine;
	delete[] szLogFilename;

	return hBitmap;
}
#undef BUF_SIZE


HBITMAP CBlenderExtenderApp::CreateThumbnail(LPCTSTR lpFileName, const SIZE bmSize)
{
	// TODO: http://www.codeproject.com/KB/GDI-plus/LovelyGoldFishDeskPet.aspx ??
	
	// figure out .ini file
	int nLen = wcslen (m_pszHelpFilePath);
	TCHAR *szSettingsIni = new TCHAR[nLen + 20];
	wcscpy (szSettingsIni, m_pszHelpFilePath);
	for (;szSettingsIni[nLen]!='\\';--nLen);
	wsprintf (&szSettingsIni[nLen + 1], _T("settings.ini"));

	// Try and render a bitmap
	HBITMAP hThumb = Render (szSettingsIni, lpFileName, bmSize.cx, bmSize.cy);
	
	if (hThumb == NULL)
	{
		CBitmap* pBmpThumb;
		CBitmap bmpStatic;
		CImage image;
		bool bWorked = false;

		// Load up an "unrenderable" indicator bitmap
		CImage *poImage=new CImage ();

		TCHAR szBrokenImagePath[MAX_PATH];
		GetPrivateProfileString(_T("BlenderExtender"),_T("brokenImage"),_T(""),szBrokenImagePath,MAX_PATH,szSettingsIni);
	
		try{
			// Try and get the user-specified image first
			if (szBrokenImagePath && szBrokenImagePath[0] && (S_OK == poImage->Load (szBrokenImagePath)))
			{	
				COLORREF cr = GetSysColor (COLOR_WINDOW);
				HDC dcFinal = CreateCompatibleDC (NULL);
				hThumb = CreateBitmap (96,96,1,32,NULL);
				SelectObject (dcFinal, hThumb);
				HBRUSH hBrush = CreateSolidBrush (cr);
				RECT rect = {0,0,96,96};
				FillRect (dcFinal, &rect, hBrush);
				DeleteObject (hBrush);
				poImage->AlphaBlend (dcFinal, 0, 0);
				DeleteDC (dcFinal);

				bWorked = (hThumb!=NULL);
			}
		} catch(...) {
			bWorked = false;
		}
		delete poImage;
		if (!bWorked)
		{
			// No user-specified image?  Use our own internal bitmap.
			bmpStatic.LoadBitmapW (IDB_NOTFOUND);
			pBmpThumb = &bmpStatic;

			// Scale the bitmap to the correct size
			CDC dcOriginal;
			CDC dcResult;
			dcOriginal.CreateCompatibleDC (NULL);
			dcResult.CreateCompatibleDC (&dcOriginal);
			CBitmap* pOldBitmap = dcOriginal.SelectObject(pBmpThumb);
			dcOriginal.StretchBlt (0,0,bmSize.cx,bmSize.cy,&dcResult,0,0,pBmpThumb->GetBitmapDimension().cx,pBmpThumb->GetBitmapDimension().cy,SRCCOPY);
			dcOriginal.SelectObject (pOldBitmap);

			// Convret the CBitmap to an HBITMAP
			hThumb = (HBITMAP)pBmpThumb->Detach();
		}
	}

	delete[] szSettingsIni;
	szSettingsIni = NULL;

    return hThumb;
}


// DllCanUnloadNow - Allows COM to unload DLL
#ifndef _WIN32_WCE
#pragma comment(linker, "/EXPORT:DllCanUnloadNow=_DllCanUnloadNow@0,PRIVATE")
#pragma comment(linker, "/EXPORT:DllGetClassObject=_DllGetClassObject@12,PRIVATE")
#pragma comment(linker, "/EXPORT:DllRegisterServer=_DllRegisterServer@0,PRIVATE")
#pragma comment(linker, "/EXPORT:DllUnregisterServer=_DllUnregisterServer@0,PRIVATE")
#else
#ifdef _X86_
#pragma comment(linker, "/EXPORT:DllCanUnloadNow=_DllCanUnloadNow,PRIVATE")
#pragma comment(linker, "/EXPORT:DllGetClassObject=_DllGetClassObject,PRIVATE")
#pragma comment(linker, "/EXPORT:DllRegisterServer=_DllRegisterServer,PRIVATE")
#pragma comment(linker, "/EXPORT:DllUnregisterServer=_DllUnregisterServer,PRIVATE")
#else
#pragma comment(linker, "/EXPORT:DllCanUnloadNow,PRIVATE")
#pragma comment(linker, "/EXPORT:DllGetClassObject,PRIVATE")
#pragma comment(linker, "/EXPORT:DllRegisterServer,PRIVATE")
#pragma comment(linker, "/EXPORT:DllUnregisterServer,PRIVATE")
#endif // _X86_
#endif // !_WIN32_WCE

STDAPI DllCanUnloadNow(void)
{
	AFX_MANAGE_STATE(AfxGetStaticModuleState());
	if (_AtlModule.GetLockCount() > 0)
		return S_FALSE;
	return S_OK;
}

// DllGetClassObject - Returns class factory
STDAPI DllGetClassObject(REFCLSID rclsid, REFIID riid, LPVOID* ppv)
{
	AFX_MANAGE_STATE(AfxGetStaticModuleState());
	if (S_OK == _AtlModule.GetClassObject(rclsid, riid, ppv))
		return S_OK;
	return AfxDllGetClassObject(rclsid, riid, ppv);
}

// DllRegisterServer - Adds entries to the system registry
STDAPI DllRegisterServer(void)
{
	AFX_MANAGE_STATE(AfxGetStaticModuleState());
	_AtlModule.UpdateRegistryAppId(TRUE);
	HRESULT hRes2 = _AtlModule.RegisterServer(TRUE);
	if (hRes2 != S_OK)
		return hRes2;
	if (!COleObjectFactory::UpdateRegistryAll(TRUE))
		return ResultFromScode(SELFREG_E_CLASS);
	return S_OK;
}

// DllUnregisterServer - Removes entries from the system registry
STDAPI DllUnregisterServer(void)
{
	AFX_MANAGE_STATE(AfxGetStaticModuleState());
	_AtlModule.UpdateRegistryAppId(FALSE);
	HRESULT hRes2 = _AtlModule.UnregisterServer(TRUE);
	// TODO: Set the registry key HKLM/.blend/shellex/{BB2E617C-0920-11d1-9A0B-00C04FC2D6C1} = {AE7B2720-60D0-48FC-958A-7CAD029A7CF5}
	if (hRes2 != S_OK)
		return hRes2;
	if (!COleObjectFactory::UpdateRegistryAll(FALSE))
		return ResultFromScode(SELFREG_E_CLASS);
	return S_OK;
}


