/* Generated by Nim Compiler v1.4.0 */
/*   (c) 2020 Andreas Rumpf */
/* The generated code is subject to the original license. */
#define NIM_INTBITS 64

/* section: NIM_merge_HEADERS */

#include "nimbase.h"
#include <dlfcn.h>
#include <string.h>
#undef LANGUAGE_C
#undef MIPSEB
#undef MIPSEL
#undef PPC
#undef R3000
#undef R4000
#undef i386
#undef linux
#undef mips
#undef near
#undef far
#undef powerpc
#undef unix

/* section: NIM_merge_FRAME_DEFINES */
#define nimfr_(x, y)
#define nimln_(x, y)

/* section: NIM_merge_FORWARD_TYPES */
typedef struct NimStrPayload NimStrPayload;
typedef struct NimStringV2 NimStringV2;
typedef struct tySequence__sM4lkSb7zS6F7OVMvW9cffQ tySequence__sM4lkSb7zS6F7OVMvW9cffQ;
typedef struct tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content;
typedef struct tyObject_LibraryError__x1muge9crz9aAVqWWUrEL9aXg tyObject_LibraryError__x1muge9crz9aAVqWWUrEL9aXg;
typedef struct tyObject_OSError__BeJgrOdDsczOwEWOZbRfKA tyObject_OSError__BeJgrOdDsczOwEWOZbRfKA;
typedef struct tyObject_CatchableError__qrLSDoe2oBoAqNtJ9badtnA tyObject_CatchableError__qrLSDoe2oBoAqNtJ9badtnA;
typedef struct Exception Exception;
typedef struct RootObj RootObj;
typedef struct TNimTypeV2 TNimTypeV2;
typedef struct tySequence__uB9b75OUPRENsBAu4AnoePA tySequence__uB9b75OUPRENsBAu4AnoePA;
typedef struct tySequence__uB9b75OUPRENsBAu4AnoePA_Content tySequence__uB9b75OUPRENsBAu4AnoePA_Content;
typedef struct tyObject_StackTraceEntry__oLyohQ7O2XOvGnflOss8EA tyObject_StackTraceEntry__oLyohQ7O2XOvGnflOss8EA;

/* section: NIM_merge_TYPES */
struct NimStrPayload {
NI cap;
NIM_CHAR data[SEQ_DECL_SIZE];
};
struct NimStringV2 {
NI len;
NimStrPayload* p;
};
struct tySequence__sM4lkSb7zS6F7OVMvW9cffQ {
  NI len; tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content* p;
};
struct TNimTypeV2 {
void* destructor;
NI size;
NI align;
NCSTRING name;
void* traceImpl;
void* disposeImpl;
void* typeInfoV1;
};
struct RootObj {
TNimTypeV2* m_type;
};
struct tySequence__uB9b75OUPRENsBAu4AnoePA {
  NI len; tySequence__uB9b75OUPRENsBAu4AnoePA_Content* p;
};
struct Exception {
  RootObj Sup;
Exception* parent;
NCSTRING name;
NimStringV2 message;
tySequence__uB9b75OUPRENsBAu4AnoePA trace;
Exception* up;
};
struct tyObject_CatchableError__qrLSDoe2oBoAqNtJ9badtnA {
  Exception Sup;
};
struct tyObject_OSError__BeJgrOdDsczOwEWOZbRfKA {
  tyObject_CatchableError__qrLSDoe2oBoAqNtJ9badtnA Sup;
NI32 errorCode;
};
struct tyObject_LibraryError__x1muge9crz9aAVqWWUrEL9aXg {
  tyObject_OSError__BeJgrOdDsczOwEWOZbRfKA Sup;
};


#ifndef tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content_PP
#define tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content_PP
struct tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content { NI cap; NimStringV2 data[SEQ_DECL_SIZE];};
#endif

      

#ifndef tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content_PP
#define tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content_PP
struct tySequence__sM4lkSb7zS6F7OVMvW9cffQ_Content { NI cap; NimStringV2 data[SEQ_DECL_SIZE];};
#endif

      struct tyObject_StackTraceEntry__oLyohQ7O2XOvGnflOss8EA {
NCSTRING procname;
NI line;
NCSTRING filename;
};


#ifndef tySequence__uB9b75OUPRENsBAu4AnoePA_Content_PP
#define tySequence__uB9b75OUPRENsBAu4AnoePA_Content_PP
struct tySequence__uB9b75OUPRENsBAu4AnoePA_Content { NI cap; tyObject_StackTraceEntry__oLyohQ7O2XOvGnflOss8EA data[SEQ_DECL_SIZE];};
#endif

      
/* section: NIM_merge_PROC_HEADERS */
N_LIB_PRIVATE N_NIMCALL(tySequence__sM4lkSb7zS6F7OVMvW9cffQ, newSeq__q7W9bxIQ7BrFLngLO9cYelsA)(NI len);
N_LIB_PRIVATE N_NIMCALL(void, libCandidates__TEY9aqiaMWVK2l0NzZy7BwQ)(NimStringV2 s, tySequence__sM4lkSb7zS6F7OVMvW9cffQ* dest);
N_LIB_PRIVATE N_NIMCALL(NI, nsuFindChar)(NimStringV2 s, NIM_CHAR sub, NI start, NI last);
N_LIB_PRIVATE N_NIMCALL(NimStringV2, substr__2yh9cer0ymNRHlOOg8P7IuA)(NimStringV2 s, NI first, NI last);
N_LIB_PRIVATE N_NIMCALL(NimStringV2, substr__iGg0RIKceRvsmvq8FUHOEw)(NimStringV2 s, NI first);
N_LIB_PRIVATE N_NIMCALL(void, eqsink___aBBXmHFBEivKqERloP6zmA)(NimStringV2* dest, NimStringV2 src);
static N_INLINE(void, appendString)(NimStringV2* dest, NimStringV2 src);
static N_INLINE(void, copyMem__i80o3k0SgEI5gTRCzYdyWAsystem)(void* dest, void* source, NI size);
static N_INLINE(void, nimCopyMem)(void* dest, void* source, NI size);
N_LIB_PRIVATE N_NIMCALL(NimStringV2, rawNewString)(NI space);
N_LIB_PRIVATE N_NIMCALL(void, eqdestroy___dS1BF3Vxjg9aJMmmhVJKSpQ)(NimStringV2* dest);
N_LIB_PRIVATE N_NIMCALL(void, add__dK9ajFgX5RSWQx0eHjjpjSQ)(tySequence__sM4lkSb7zS6F7OVMvW9cffQ* x, NimStringV2 value);
static N_INLINE(NIM_BOOL*, nimErrorFlag)(void);
N_LIB_PRIVATE N_NIMCALL(void*, loadLib__Yq5XYz2ycX5V5B9bUM4Uyiw)(NimStringV2 path, NIM_BOOL globalSymbols);
static N_INLINE(NCSTRING, nimToCStringConv)(NimStringV2 s);
N_LIB_PRIVATE N_NIMCALL(void, eqdestroy___0RiuPw9cXhtLB9a2rQ2jA69cg)(tySequence__sM4lkSb7zS6F7OVMvW9cffQ* dest);
N_LIB_PRIVATE N_NIMCALL(void*, nimNewObj)(NI size);
N_LIB_PRIVATE N_NIMCALL(NimStringV2, cstrToNimstr)(NCSTRING str);
N_LIB_PRIVATE N_NIMCALL(void, raiseExceptionEx)(Exception* e, NCSTRING ename, NCSTRING procname, NCSTRING filename, NI line);

/* section: NIM_merge_DATA */
extern TNimTypeV2 NTIv2__x1muge9crz9aAVqWWUrEL9aXg_;
static const struct {
  NI cap; NIM_CHAR data[23+1];
} TM__Vbi6rBBOqdMySprhH3iUcg_2 = { 23 | NIM_STRLIT_FLAG, "could not find symbol: " };
static const NimStringV2 TM__Vbi6rBBOqdMySprhH3iUcg_3 = {23, (NimStrPayload*)&TM__Vbi6rBBOqdMySprhH3iUcg_2};

/* section: NIM_merge_VARS */
extern NIM_BOOL nimInErrorMode__759bT87luu8XGcbkw13FUjA;

/* section: NIM_merge_PROCS */
N_LIB_PRIVATE N_NIMCALL(void*, symAddr__ALH9bdNwXEzg7MPq4PA9csvw)(void* lib, NCSTRING name) {
	void* result;
	result = (void*)0;
	result = dlsym(lib, name);
	return result;
}
N_LIB_PRIVATE N_NIMCALL(void*, loadLib__3W0xEugBG13TxVu4hk9b9b5g)(void) {
	void* result;
	result = (void*)0;
	result = dlopen(NIM_NIL, ((int) 2));
	return result;
}
static N_INLINE(void, nimCopyMem)(void* dest, void* source, NI size) {
	void* T1_;
	T1_ = (void*)0;
	T1_ = memcpy(dest, source, ((size_t) (size)));
}
static N_INLINE(void, copyMem__i80o3k0SgEI5gTRCzYdyWAsystem)(void* dest, void* source, NI size) {
	nimCopyMem(dest, source, size);
}
static N_INLINE(void, appendString)(NimStringV2* dest, NimStringV2 src) {
	{
		void* T5_;
		void* T6_;
		if (!(((NI) 0) < src.len)) goto LA3_;
		T5_ = (void*)0;
		T5_ = ((void*) ((&(*(*dest).p).data[(*dest).len])));
		T6_ = (void*)0;
		T6_ = ((void*) ((&(*src.p).data[((NI) 0)])));
		copyMem__i80o3k0SgEI5gTRCzYdyWAsystem(T5_, T6_, ((NI) ((NI)(src.len + ((NI) 1)))));
		(*dest).len += src.len;
	}
	LA3_: ;
}
static N_INLINE(NIM_BOOL*, nimErrorFlag)(void) {
	NIM_BOOL* result;
	result = (NIM_BOOL*)0;
	result = (&nimInErrorMode__759bT87luu8XGcbkw13FUjA);
	return result;
}
N_LIB_PRIVATE N_NIMCALL(void, libCandidates__TEY9aqiaMWVK2l0NzZy7BwQ)(NimStringV2 s, tySequence__sM4lkSb7zS6F7OVMvW9cffQ* dest) {
	NI le;
	NI ri;
NIM_BOOL* nimErr_;
{nimErr_ = nimErrorFlag();
	le = nsuFindChar(s, 40, ((NI) 0), ((NI) 0));
	ri = nsuFindChar(s, 41, ((NI) ((NI)(le + ((NI) 1)))), ((NI) 0));
	{
		NIM_BOOL T4_;
		NimStringV2 prefix;
		NimStringV2 suffix;
		T4_ = (NIM_BOOL)0;
		T4_ = (((NI) 0) <= le);
		if (!(T4_)) goto LA5_;
		T4_ = (le < ri);
		LA5_: ;
		if (!T4_) goto LA6_;
		prefix.len = 0; prefix.p = NIM_NIL;
		suffix.len = 0; suffix.p = NIM_NIL;
		prefix = substr__2yh9cer0ymNRHlOOg8P7IuA(s, ((NI) 0), (NI)(le - ((NI) 1)));
		suffix = substr__iGg0RIKceRvsmvq8FUHOEw(s, (NI)(ri + ((NI) 1)));
		{
			NimStringV2 middle;
			NimStringV2 colontmp_;
			NI lastX60gensym26_;
			NI splitsX60gensym26_;
			middle.len = 0; middle.p = NIM_NIL;
			colontmp_.len = 0; colontmp_.p = NIM_NIL;
			colontmp_ = substr__2yh9cer0ymNRHlOOg8P7IuA(s, (NI)(le + ((NI) 1)), (NI)(ri - ((NI) 1)));
			lastX60gensym26_ = ((NI) 0);
			splitsX60gensym26_ = ((NI) -1);
			{
				while (1) {
					NI firstX60gensym26_;
					NimStringV2 T21_;
					NimStringV2 T22_;
					if (!(lastX60gensym26_ <= colontmp_.len)) goto LA12;
					firstX60gensym26_ = lastX60gensym26_;
					{
						while (1) {
							NIM_BOOL T15_;
							T15_ = (NIM_BOOL)0;
							T15_ = (lastX60gensym26_ < colontmp_.len);
							if (!(T15_)) goto LA16_;
							T15_ = !(((NU8)(colontmp_.p->data[lastX60gensym26_]) == (NU8)(124)));
							LA16_: ;
							if (!T15_) goto LA14;
							lastX60gensym26_ += ((NI) 1);
						} LA14: ;
					}
					{
						if (!(splitsX60gensym26_ == ((NI) 0))) goto LA19_;
						lastX60gensym26_ = colontmp_.len;
					}
					LA19_: ;
					T21_.len = 0; T21_.p = NIM_NIL;
					T21_ = substr__2yh9cer0ymNRHlOOg8P7IuA(colontmp_, firstX60gensym26_, (NI)(lastX60gensym26_ - ((NI) 1)));
					eqsink___aBBXmHFBEivKqERloP6zmA((&middle), T21_);
					T22_.len = 0; T22_.p = NIM_NIL;
					T22_ = rawNewString(prefix.len + middle.len + suffix.len + 0);
appendString((&T22_), prefix);
appendString((&T22_), middle);
appendString((&T22_), suffix);
					libCandidates__TEY9aqiaMWVK2l0NzZy7BwQ(T22_, dest);
					{
						if (!(splitsX60gensym26_ == ((NI) 0))) goto LA25_;
						goto LA11;
					}
					LA25_: ;
					splitsX60gensym26_ -= ((NI) 1);
					lastX60gensym26_ += ((NI) 1);
				} LA12: ;
			} LA11: ;
			{
				LA10_:;
			}
			{
				eqdestroy___dS1BF3Vxjg9aJMmmhVJKSpQ((&colontmp_));
				eqdestroy___dS1BF3Vxjg9aJMmmhVJKSpQ((&middle));
			}
			if (NIM_UNLIKELY(*nimErr_)) goto LA8_;
		}
		{
			LA8_:;
		}
		{
			eqdestroy___dS1BF3Vxjg9aJMmmhVJKSpQ((&suffix));
			eqdestroy___dS1BF3Vxjg9aJMmmhVJKSpQ((&prefix));
		}
		if (NIM_UNLIKELY(*nimErr_)) goto LA1_;
	}
	goto LA2_;
	LA6_: ;
	{
		NimStringV2 blitTmp;
		blitTmp = s;
		s.len = 0; s.p = NIM_NIL;
		add__dK9ajFgX5RSWQx0eHjjpjSQ((&(*dest)), blitTmp);
	}
	LA2_: ;
	{
		LA1_:;
	}
	{
		eqdestroy___dS1BF3Vxjg9aJMmmhVJKSpQ((&s));
	}
	if (NIM_UNLIKELY(*nimErr_)) goto BeforeRet_;
	}BeforeRet_: ;
}
static N_INLINE(NCSTRING, nimToCStringConv)(NimStringV2 s) {
	NCSTRING result;
	result = (NCSTRING)0;
	{
		if (!(s.len == ((NI) 0))) goto LA3_;
		result = "";
	}
	goto LA1_;
	LA3_: ;
	{
		result = ((NCSTRING) ((*s.p).data));
	}
	LA1_: ;
	return result;
}
N_LIB_PRIVATE N_NIMCALL(void*, loadLib__Yq5XYz2ycX5V5B9bUM4Uyiw)(NimStringV2 path, NIM_BOOL globalSymbols) {
	void* result;
	NI32 colontmpD_;
	int colontmpD__2;
	NI32 flags;
	result = (void*)0;
	colontmpD_ = (NI32)0;
	colontmpD__2 = (int)0;
	{
		if (!globalSymbols) goto LA3_;
		colontmpD_ = ((NI32) 258);
		flags = colontmpD_;
	}
	goto LA1_;
	LA3_: ;
	{
		colontmpD__2 = ((int) 2);
		flags = colontmpD__2;
	}
	LA1_: ;
	result = dlopen(nimToCStringConv(path), flags);
	return result;
}
N_LIB_PRIVATE N_NIMCALL(void*, loadLibPattern__b9aH5C9aWbfFKSp3nIx1lqTA)(NimStringV2 pattern, NIM_BOOL globalSymbols) {
	void* result;
	tySequence__sM4lkSb7zS6F7OVMvW9cffQ candidates;
	NimStringV2 blitTmp;
NIM_BOOL* nimErr_;
{nimErr_ = nimErrorFlag();
	result = (void*)0;
	candidates.len = 0; candidates.p = NIM_NIL;
	candidates = newSeq__q7W9bxIQ7BrFLngLO9cYelsA(((NI) 0));
	blitTmp = pattern;
	libCandidates__TEY9aqiaMWVK2l0NzZy7BwQ(blitTmp, (&candidates));
	{
		NimStringV2* c;
		NI i;
		NI L;
		NI T3_;
		c = (NimStringV2*)0;
		i = ((NI) 0);
		T3_ = candidates.len;
		L = T3_;
		{
			while (1) {
				if (!(i < L)) goto LA5;
				c = (&candidates.p->data[i]);
				result = loadLib__Yq5XYz2ycX5V5B9bUM4Uyiw((*c), globalSymbols);
				{
					if (!!((result == 0))) goto LA8_;
					goto LA2;
				}
				LA8_: ;
				i += ((NI) 1);
			} LA5: ;
		}
	} LA2: ;
	{
		LA1_:;
	}
	{
		eqdestroy___0RiuPw9cXhtLB9a2rQ2jA69cg((&candidates));
	}
	if (NIM_UNLIKELY(*nimErr_)) goto BeforeRet_;
	}BeforeRet_: ;
	return result;
}
N_LIB_PRIVATE N_NOINLINE(void, raiseInvalidLibrary__TnaNIb4lz2PqhpvzfjxuWw)(NCSTRING name) {
	NimStringV2 colontmpD_;
	tyObject_LibraryError__x1muge9crz9aAVqWWUrEL9aXg* T2_;
	NimStringV2 T3_;
NIM_BOOL* nimErr_;
{nimErr_ = nimErrorFlag();
	colontmpD_.len = 0; colontmpD_.p = NIM_NIL;
	T2_ = (tyObject_LibraryError__x1muge9crz9aAVqWWUrEL9aXg*)0;
	T2_ = (tyObject_LibraryError__x1muge9crz9aAVqWWUrEL9aXg*) nimNewObj(sizeof(tyObject_LibraryError__x1muge9crz9aAVqWWUrEL9aXg));
	(*T2_).Sup.Sup.Sup.Sup.m_type = (&NTIv2__x1muge9crz9aAVqWWUrEL9aXg_);
	(*T2_).Sup.Sup.Sup.name = "LibraryError";
	T3_.len = 0; T3_.p = NIM_NIL;
	colontmpD_ = cstrToNimstr(name);
	T3_ = rawNewString(colontmpD_.len + 23);
appendString((&T3_), TM__Vbi6rBBOqdMySprhH3iUcg_3);
appendString((&T3_), colontmpD_);
	(*T2_).Sup.Sup.Sup.message = T3_;
	(*T2_).Sup.Sup.Sup.parent = NIM_NIL;
	raiseExceptionEx((Exception*)T2_, "LibraryError", "raiseInvalidLibrary", "dynlib.nim", 75);
	goto LA1_;
	{
		LA1_:;
	}
	{
		eqdestroy___dS1BF3Vxjg9aJMmmhVJKSpQ((&colontmpD_));
	}
	if (NIM_UNLIKELY(*nimErr_)) goto BeforeRet_;
	}BeforeRet_: ;
}
