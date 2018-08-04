
BlenderExtenderps.dll: dlldata.obj BlenderExtender_p.obj BlenderExtender_i.obj
	link /dll /out:BlenderExtenderps.dll /def:BlenderExtenderps.def /entry:DllMain dlldata.obj BlenderExtender_p.obj BlenderExtender_i.obj \
		kernel32.lib rpcndr.lib rpcns4.lib rpcrt4.lib oleaut32.lib uuid.lib \
.c.obj:
	cl /c /Ox /DWIN32 /D_WIN32_WINNT=0x0400 /DREGISTER_PROXY_DLL \
		$<

clean:
	@del BlenderExtenderps.dll
	@del BlenderExtenderps.lib
	@del BlenderExtenderps.exp
	@del dlldata.obj
	@del BlenderExtender_p.obj
	@del BlenderExtender_i.obj
