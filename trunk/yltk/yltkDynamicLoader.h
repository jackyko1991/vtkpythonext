#ifndef __yltkDynamicLoader_h
#define	__yltkDynamicLoader_h

#include "yltkObject.h"
#include "yltkObjectFactory.h"

namespace yltk{
	/** \class DynamicLoader
	* \brief Portable loading of dynamic libraries or dll's.
	*
	* DynamicLoader provides a portable interface to loading dynamic
	* libraries or dll's into a process.
	*
	* \ingroup OSSystemObjects
	*/

	// Ugly stuff for library handles
	// They are different on several different OS's
#if defined(__hpux)
	typedef shl_t LibraryHandle;
#elif defined(_WIN32) && !defined(__CYGWIN__)
	typedef HMODULE LibraryHandle;
#elif defined(__APPLE__)
#if MAC_OS_X_VERSION_MAX_ALLOWED < 1030
	typedef NSModule LibraryHandle;
#else
	typedef void* LibraryHandle;
#endif
#elif defined(__BEOS__)
	typedef image_id LibraryHandle;
#else  // POSIX
	typedef void* LibraryHandle;
#endif

typedef LibraryHandle LibHandle;

// Cannot use this as this is a void (*)() but YLTK old API used to be void*
// Return type from DynamicLoader::GetSymbolAddress.
typedef void (*SymbolPointer)();

	class DynamicLoader: public Object{
	public:
		/** Standard class typedefs. */
		typedef DynamicLoader               Self;
		typedef Object                      Superclass;
		typedef SmartPointer<Self>          Pointer;
		typedef SmartPointer<const Self>    ConstPointer;

		/** Method for creation through the object factory. */
		yltkNewMacro(Self);

		/** Run-time type information (and related methods). */
		yltkTypeMacro(DynamicLoader,Object);

		/** Load a dynamic library into the current process.
		* The returned LibHandle can be used to access the symbols in the
		* library. */
		static LibHandle OpenLibrary(const char*);

		/** Attempt to detach a dynamic library from the
		* process.  A value of true is returned if it is sucessful. */
		static int CloseLibrary(LibHandle);

		/** Find the address of the symbol in the given library. */
		static void* GetSymbolAddress(LibHandle, const char*);

		/** Return the library prefix for the given architecture */
		static const char* LibPrefix();

		/** Return the library extension for the given architecture. */
		static const char* LibExtension();

		/** Return the last error produced from a calls made on this class. */
		static const char* LastError();

	protected:
		DynamicLoader();
		~DynamicLoader();
	private:
		DynamicLoader(const Self&); //purposely not implemented
		void operator=(const Self&); //purposely not implemented

	};

}
#endif