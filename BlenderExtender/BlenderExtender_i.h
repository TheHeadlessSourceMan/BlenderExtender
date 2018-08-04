

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 7.00.0500 */
/* at Fri May 22 16:32:30 2009
 */
/* Compiler settings for .\BlenderExtender.idl:
    Oicf, W1, Zp8, env=Win32 (32b run)
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
//@@MIDL_FILE_HEADING(  )

#pragma warning( disable: 4049 )  /* more than 64k source lines */


/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 475
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif // __RPCNDR_H_VERSION__

#ifndef COM_NO_WINDOWS_H
#include "windows.h"
#include "ole2.h"
#endif /*COM_NO_WINDOWS_H*/

#ifndef __BlenderExtender_i_h__
#define __BlenderExtender_i_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __IBlenderShellExtension_FWD_DEFINED__
#define __IBlenderShellExtension_FWD_DEFINED__
typedef interface IBlenderShellExtension IBlenderShellExtension;
#endif 	/* __IBlenderShellExtension_FWD_DEFINED__ */


#ifndef __BlenderShellExtension_FWD_DEFINED__
#define __BlenderShellExtension_FWD_DEFINED__

#ifdef __cplusplus
typedef class BlenderShellExtension BlenderShellExtension;
#else
typedef struct BlenderShellExtension BlenderShellExtension;
#endif /* __cplusplus */

#endif 	/* __BlenderShellExtension_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"

#ifdef __cplusplus
extern "C"{
#endif 


#ifndef __IBlenderShellExtension_INTERFACE_DEFINED__
#define __IBlenderShellExtension_INTERFACE_DEFINED__

/* interface IBlenderShellExtension */
/* [unique][helpstring][nonextensible][dual][uuid][object] */ 


EXTERN_C const IID IID_IBlenderShellExtension;

#if defined(__cplusplus) && !defined(CINTERFACE)
    
    MIDL_INTERFACE("575D1DBB-037C-4EA4-BF77-312224A7995A")
    IBlenderShellExtension : public IDispatch
    {
    public:
    };
    
#else 	/* C style interface */

    typedef struct IBlenderShellExtensionVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            IBlenderShellExtension * This,
            /* [in] */ REFIID riid,
            /* [iid_is][out] */ 
            __RPC__deref_out  void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            IBlenderShellExtension * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            IBlenderShellExtension * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            IBlenderShellExtension * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            IBlenderShellExtension * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            IBlenderShellExtension * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [range][in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            IBlenderShellExtension * This,
            /* [in] */ DISPID dispIdMember,
            /* [in] */ REFIID riid,
            /* [in] */ LCID lcid,
            /* [in] */ WORD wFlags,
            /* [out][in] */ DISPPARAMS *pDispParams,
            /* [out] */ VARIANT *pVarResult,
            /* [out] */ EXCEPINFO *pExcepInfo,
            /* [out] */ UINT *puArgErr);
        
        END_INTERFACE
    } IBlenderShellExtensionVtbl;

    interface IBlenderShellExtension
    {
        CONST_VTBL struct IBlenderShellExtensionVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define IBlenderShellExtension_QueryInterface(This,riid,ppvObject)	\
    ( (This)->lpVtbl -> QueryInterface(This,riid,ppvObject) ) 

#define IBlenderShellExtension_AddRef(This)	\
    ( (This)->lpVtbl -> AddRef(This) ) 

#define IBlenderShellExtension_Release(This)	\
    ( (This)->lpVtbl -> Release(This) ) 


#define IBlenderShellExtension_GetTypeInfoCount(This,pctinfo)	\
    ( (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo) ) 

#define IBlenderShellExtension_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    ( (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo) ) 

#define IBlenderShellExtension_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    ( (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId) ) 

#define IBlenderShellExtension_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    ( (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr) ) 


#endif /* COBJMACROS */


#endif 	/* C style interface */




#endif 	/* __IBlenderShellExtension_INTERFACE_DEFINED__ */



#ifndef __BlenderExtenderLib_LIBRARY_DEFINED__
#define __BlenderExtenderLib_LIBRARY_DEFINED__

/* library BlenderExtenderLib */
/* [helpstring][version][uuid] */ 


EXTERN_C const IID LIBID_BlenderExtenderLib;

EXTERN_C const CLSID CLSID_BlenderShellExtension;

#ifdef __cplusplus

class DECLSPEC_UUID("AE7B2720-60D0-48FC-958A-7CAD029A7CF5")
BlenderShellExtension;
#endif
#endif /* __BlenderExtenderLib_LIBRARY_DEFINED__ */

/* Additional Prototypes for ALL interfaces */

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


