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

/* section: NIM_merge_PROCS */
N_LIB_PRIVATE N_NIMCALL(NI, nextPowerOfTwo__v2qC0V55wqa9bmqc7eHTz8A)(NI x) {
	NI result;
	result = (NI)0;
	result = (NI)(x - ((NI) 1));
	result = (NI)(result | (NI)((NI64)(result) >> (NU64)(((NI) 32))));
	result = (NI)(result | (NI)((NI64)(result) >> (NU64)(((NI) 16))));
	result = (NI)(result | (NI)((NI64)(result) >> (NU64)(((NI) 8))));
	result = (NI)(result | (NI)((NI64)(result) >> (NU64)(((NI) 4))));
	result = (NI)(result | (NI)((NI64)(result) >> (NU64)(((NI) 2))));
	result = (NI)(result | (NI)((NI64)(result) >> (NU64)(((NI) 1))));
	result += (NI)(((NI) 1) + (x <= ((NI) 0)));
	return result;
}
