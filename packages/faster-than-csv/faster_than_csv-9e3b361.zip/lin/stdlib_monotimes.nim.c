/* Generated by Nim Compiler v1.4.0 */
/*   (c) 2020 Andreas Rumpf */
/* The generated code is subject to the original license. */
#define NIM_INTBITS 64

/* section: NIM_merge_HEADERS */

#include "nimbase.h"
#include <string.h>
#include <time.h>
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
typedef struct tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w;
typedef struct tyObject_Duration__lj9ar6Co3fgk6NgGnVaNpJw tyObject_Duration__lj9ar6Co3fgk6NgGnVaNpJw;

/* section: NIM_merge_TYPES */
struct tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w {
NI64 ticks;
};
struct tyObject_Duration__lj9ar6Co3fgk6NgGnVaNpJw {
NI64 seconds;
NI nanosecond;
};

/* section: NIM_merge_PROC_HEADERS */
static N_INLINE(void, nimZeroMem)(void* p, NI size);
static N_INLINE(void, nimSetMem__zxfKBYntu9cBapkhrCOk1fgmemory)(void* a, int v, NI size);
N_LIB_PRIVATE N_NIMCALL(tyObject_Duration__lj9ar6Co3fgk6NgGnVaNpJw, initDuration__wcR3zetvspAUsyuvWZ07Xg)(NI64 nanoseconds, NI64 microseconds, NI64 milliseconds, NI64 seconds, NI64 minutes, NI64 hours, NI64 days, NI64 weeks);

/* section: NIM_merge_PROCS */
static N_INLINE(void, nimSetMem__zxfKBYntu9cBapkhrCOk1fgmemory)(void* a, int v, NI size) {
	void* T1_;
	T1_ = (void*)0;
	T1_ = memset(a, v, ((size_t) (size)));
}
static N_INLINE(void, nimZeroMem)(void* p, NI size) {
	nimSetMem__zxfKBYntu9cBapkhrCOk1fgmemory(p, ((int) 0), size);
}
N_LIB_PRIVATE N_NIMCALL(tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w, getMonoTime__QkEugs2Q2iFK9b83sl2B6wA)(void) {
	tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w result;
	struct timespec ts;
	int T1_;
	nimZeroMem((void*)(&result), sizeof(tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w));
	nimZeroMem((void*)(&ts), sizeof(struct timespec));
	T1_ = (int)0;
	T1_ = clock_gettime(((int) 1), (&ts));
	(void)(T1_);
	nimZeroMem((void*)(&result), sizeof(tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w));
	result.ticks = (NI64)((NI64)(((NI64) (ts.tv_sec)) * IL64(1000000000)) + ((NI64) (ts.tv_nsec)));
	return result;
}
N_LIB_PRIVATE N_NIMCALL(tyObject_Duration__lj9ar6Co3fgk6NgGnVaNpJw, minus___p9cBm7joedh4BwcboQ3HMVQ)(tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w a, tyObject_MonoTime__FEvFMlkqJiSSGVO6HgTv8w b) {
	tyObject_Duration__lj9ar6Co3fgk6NgGnVaNpJw result;
	nimZeroMem((void*)(&result), sizeof(tyObject_Duration__lj9ar6Co3fgk6NgGnVaNpJw));
	result = initDuration__wcR3zetvspAUsyuvWZ07Xg((NI64)(a.ticks - b.ticks), IL64(0), IL64(0), IL64(0), IL64(0), IL64(0), IL64(0), IL64(0));
	return result;
}
