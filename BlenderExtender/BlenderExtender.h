// BlenderExtender.h : main header file for the BlenderExtender DLL
//

#pragma once

#ifndef __AFXWIN_H__
	#error "include 'stdafx.h' before including this file for PCH"
#endif

#include "resource.h"		// main symbols
#include "BlenderExtender_i.h"


// CBlenderExtenderApp
// See BlenderExtender.cpp for the implementation of this class
//

class CBlenderExtenderApp : public CWinApp
{
public:
	CBlenderExtenderApp();

	HBITMAP CreateThumbnail(LPCTSTR lpFileName, const SIZE bmSize);
	HBITMAP Render(const TCHAR *szSettingsIni, LPCTSTR lpFileName, int width, int height, int frame = 0);

// Overrides
public:
	virtual BOOL InitInstance();

	DECLARE_MESSAGE_MAP()
public:
	int Run(bool bSilent);
};
