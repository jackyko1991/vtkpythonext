#ifndef __yltkSimpleFastMutexLock_h
#define __yltkSimpleFastMutexLock_h

#include "yltkMacros.h"

#ifdef YLTK_USE_SPROC
#include <abi_mutex.h>
#endif

#ifdef YLTK_USE_PTHREADS
#include <pthread.h>
#endif

#if defined(_WIN32) && !defined(YLTK_USE_PTHREADS)
	#include "yltkWindows.h"
#endif

namespace yltk{

#ifdef YLTK_USE_SPROC
	#include <abi_mutex.h>
	typedef abilock_t FastMutexType;
#endif

#ifdef YLTK_USE_PTHREADS
	#include <pthread.h>
	typedef pthread_mutex_t FastMutexType;
#endif

#if defined(_WIN32) && !defined(YLTK_USE_PTHREADS)
	#include <winbase.h>
	typedef CRITICAL_SECTION FastMutexType;
#endif

#ifndef YLTK_USE_SPROC
#ifndef YLTK_USE_PTHREADS
#ifndef _WIN32
	typedef int FastMutexType;
#endif
#endif
#endif
	
	//Critical Section object that is not a itkObject.
	class SimpleFastMutexLock{
	public:
		/** Standard class typedefs.  */
		typedef SimpleFastMutexLock       Self;

		/** Constructor and destructor left public purposely because of stack allocation. */
		SimpleFastMutexLock();
		~SimpleFastMutexLock();

		/** Lock access. */
		void Lock() const;

		/** Unlock access. */
		void Unlock() const;

	protected:
		mutable FastMutexType m_FastMutexLock;
	};


}

#endif