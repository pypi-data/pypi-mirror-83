/* Generated by Nim Compiler v1.4.0 */
/*   (c) 2020 Andreas Rumpf */
/* The generated code is subject to the original license. */
#define NIM_INTBITS 64

/* section: NIM_merge_HEADERS */

#include "nimbase.h"
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

/* section: NIM_merge_PROC_HEADERS */
N_LIB_PRIVATE N_NIMCALL(int, WTERMSIG__T7ZeAv6ofGPBA29bsuGG1ug)(int s);

/* section: NIM_merge_PROCS */
N_LIB_PRIVATE N_NIMCALL(NIM_BOOL, WIFSIGNALED__o9b5GK70QLj9ahJeczQ2LyRg)(int s) {
	NIM_BOOL result;
	result = (NIM_BOOL)0;
	result = (((NI8) 0) < (NI8)((NI64)(((NI8) ((NI32)((NI32)(s & ((NI32) 127)) + ((NI32) 1))))) >> (NU64)(((NI) 1))));
	return result;
}
N_LIB_PRIVATE N_NIMCALL(int, WTERMSIG__T7ZeAv6ofGPBA29bsuGG1ug)(int s) {
	int result;
	result = (int)0;
	result = (NI32)(s & ((NI32) 127));
	return result;
}
N_LIB_PRIVATE N_NIMCALL(int, WEXITSTATUS__T7ZeAv6ofGPBA29bsuGG1ug_2)(int s) {
	int result;
	result = (int)0;
	result = (NI32)((NI64)((NI32)(s & ((NI32) 65280))) >> (NU64)(((NI) 8)));
	return result;
}
N_LIB_PRIVATE N_NIMCALL(NIM_BOOL, WIFEXITED__o9b5GK70QLj9ahJeczQ2LyRg_2)(int s) {
	NIM_BOOL result;
	int T1_;
	result = (NIM_BOOL)0;
	T1_ = (int)0;
	T1_ = WTERMSIG__T7ZeAv6ofGPBA29bsuGG1ug(s);
	result = (T1_ == ((NI32) 0));
	return result;
}
