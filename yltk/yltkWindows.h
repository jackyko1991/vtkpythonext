/** This file is used to create the smallest windows.h possible.
* Also it removes a few annoying #define's in windows.h. */
#ifndef __yltkWindows_h
#define __yltkWindows_h
#ifndef NOMINMAX
#define NOMINMAX
#endif
#ifdef WIN32_LEAN_AND_MEAN
#undef WIN32_LEAN_AND_MEAN
#endif
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <winbase.h>
#endif