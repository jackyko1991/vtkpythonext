#include "yltkSimpleFastMutexLock.h"

namespace yltk{
	// Construct a new SimpleMutexLock
	SimpleFastMutexLock::SimpleFastMutexLock()
	{
		#ifdef YLTK_USE_SPROC
				init_lock( &m_FastMutexLock );
		#endif

		#if defined(_WIN32) && !defined(YLTK_USE_PTHREADS)
				//this->MutexLock = CreateMutex( NULL, FALSE, NULL );
				InitializeCriticalSection(&m_FastMutexLock);
		#endif

		#ifdef YLTK_USE_PTHREADS
		#ifdef YLTK_HP_PTHREADS
				pthread_mutex_init(&(m_FastMutexLock), pthread_mutexattr_default);
		#else
				pthread_mutex_init(&(m_FastMutexLock), NULL);
		#endif
		#endif
	}

	// Destruct the SimpleMutexVariable
	SimpleFastMutexLock::~SimpleFastMutexLock()
	{
		#if defined(_WIN32) && !defined(YLTK_USE_PTHREADS)
			//CloseHandle(this->MutexLock);
			DeleteCriticalSection(&m_FastMutexLock);
		#endif

		#ifdef YLTK_USE_PTHREADS
			pthread_mutex_destroy( &m_FastMutexLock);
		#endif
	}

	// Lock the FastMutexLock
	void SimpleFastMutexLock::Lock() const
	{
		#ifdef YLTK_USE_SPROC
			spin_lock( &m_FastMutexLock );
		#endif

		#if defined(_WIN32) && !defined(YLTK_USE_PTHREADS)
			//WaitForSingleObject( this->MutexLock, INFINITE );
			EnterCriticalSection(&m_FastMutexLock);
		#endif

		#ifdef YLTK_USE_PTHREADS
			pthread_mutex_lock( &m_FastMutexLock);
		#endif
	}

	// Unlock the FastMutexLock
	void SimpleFastMutexLock::Unlock() const
	{
		#ifdef YLTK_USE_SPROC
			release_lock( &m_FastMutexLock );
		#endif

		#if defined(_WIN32) && !defined(YLTK_USE_PTHREADS)
			//ReleaseMutex( this->MutexLock );
			LeaveCriticalSection(&m_FastMutexLock);
		#endif

		#ifdef YLTK_USE_PTHREADS
				pthread_mutex_unlock( &m_FastMutexLock);
		#endif
	}
}