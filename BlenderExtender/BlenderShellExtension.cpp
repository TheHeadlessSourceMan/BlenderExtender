// BlenderShellExtension.cpp : Implementation of CBlenderShellExtension

#include "stdafx.h"
#include "BlenderShellExtension.h"

extern CBlenderExtenderApp theApp;


HRESULT CBlenderShellExtension::Load(LPCOLESTR wszFile, DWORD dwMode)
{
	m_szFile = CString(wszFile);
	return S_OK;	
};


HRESULT CBlenderShellExtension::GetLocation(LPWSTR pszPathBuffer,
		DWORD cchMax, DWORD *pdwPriority,
		const SIZE *prgSize, DWORD dwRecClrDepth,
		DWORD *pdwFlags)
{
	m_bmSize = *prgSize;
	*pdwFlags |= IEIFLAG_REFRESH;
	if (*pdwFlags & IEIFLAG_ASYNC )	return E_PENDING;
	return NOERROR;
}


HRESULT CBlenderShellExtension::Extract(HBITMAP* phBmpThumbnail)
{
    AFX_MANAGE_STATE(AfxGetStaticModuleState());

    HBITMAP m_hPreview = theApp.CreateThumbnail(m_szFile, m_bmSize);
    *phBmpThumbnail = m_hPreview;
    return NOERROR;
}


HRESULT CBlenderShellExtension::GetClassID(CLSID *)
{
    return NOERROR;
}


HRESULT CBlenderShellExtension::IsDirty(void)
{
    return NOERROR;
}


HRESULT CBlenderShellExtension::Save(LPCOLESTR,BOOL)
{
    return NOERROR;
}


HRESULT CBlenderShellExtension::SaveCompleted(LPCOLESTR)
{
    return NOERROR;
}


HRESULT CBlenderShellExtension::GetCurFile(LPOLESTR *)
{
    return NOERROR;
}


HRESULT CBlenderShellExtension::GetDateStamp(FILETIME *ftModified)
{
	HANDLE hFile = CreateFile (m_szFile, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if(hFile == INVALID_HANDLE_VALUE)
    {
        return E_FAIL;
    }

    if (!GetFileTime (hFile, NULL, NULL, ftModified))
	{
		CloseHandle (hFile);
        return E_FAIL;
	}
	CloseHandle(hFile);

    return NOERROR;
}


// CBlenderShellExtension

