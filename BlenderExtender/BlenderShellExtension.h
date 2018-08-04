// BlenderShellExtension.h : Declaration of the CBlenderShellExtension

#pragma once
#include "resource.h"       // main symbols

#include "BlenderExtender.h"

#if defined(_WIN32_WCE) && !defined(_CE_DCOM) && !defined(_CE_ALLOW_SINGLE_THREADED_OBJECTS_IN_MTA)
#error "Single-threaded COM objects are not properly supported on Windows CE platform, such as the Windows Mobile platforms that do not include full DCOM support. Define _CE_ALLOW_SINGLE_THREADED_OBJECTS_IN_MTA to force ATL to support creating single-thread COM object's and allow use of it's single-threaded COM object implementations. The threading model in your rgs file was set to 'Free' as that is the only threading model supported in non DCOM Windows CE platforms."
#endif



// CBlenderShellExtension

class ATL_NO_VTABLE CBlenderShellExtension :
	public CComObjectRootEx<CComSingleThreadModel>,
	public CComCoClass<CBlenderShellExtension, &CLSID_BlenderShellExtension>,
	public IPersistFile,
    public IExtractImage2
{
public:
	SIZE m_bmSize;
	CString m_szFile;

	CBlenderShellExtension()
	{
	}

	virtual HRESULT STDMETHODCALLTYPE Extract(HBITMAP* phBmpThumbnail);
	virtual HRESULT STDMETHODCALLTYPE GetLocation(LPWSTR pszPathBuffer,
		DWORD cchMax, DWORD *pdwPriority,
		const SIZE *prgSize, DWORD dwRecClrDepth,
		DWORD *pdwFlags);
	virtual HRESULT STDMETHODCALLTYPE Load(LPCOLESTR wszFile, DWORD dwMode);
	virtual HRESULT STDMETHODCALLTYPE GetClassID(CLSID *);
	virtual HRESULT STDMETHODCALLTYPE IsDirty(void);
	virtual HRESULT STDMETHODCALLTYPE Save(LPCOLESTR,BOOL);
	virtual HRESULT STDMETHODCALLTYPE SaveCompleted(LPCOLESTR);
	virtual HRESULT STDMETHODCALLTYPE GetCurFile(LPOLESTR *);
	virtual HRESULT STDMETHODCALLTYPE GetDateStamp(FILETIME *ftModified);

DECLARE_REGISTRY_RESOURCEID(IDR_BLENDERSHELLEXTENSION)


BEGIN_COM_MAP(CBlenderShellExtension)
	//COM_INTERFACE_ENTRY(IBlenderShellExtension)
	COM_INTERFACE_ENTRY(IPersistFile)
	COM_INTERFACE_ENTRY(IExtractImage)
	COM_INTERFACE_ENTRY(IExtractImage2)
END_COM_MAP()



	DECLARE_PROTECT_FINAL_CONSTRUCT()

	HRESULT FinalConstruct()
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}

public:

};

OBJECT_ENTRY_AUTO(__uuidof(BlenderShellExtension), CBlenderShellExtension)
