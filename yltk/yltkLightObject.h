#ifndef __yltkLightObject_h
#define __yltkLightObject_h

#include "yltkSmartPointer.h"
#include "yltkTimeStamp.h"
#include "yltkIndent.h"
#include "yltkSimpleFastMutexLock.h"
#include "yltkMacros.h"

#include <iostream>
#include <typeinfo>

#if defined(_WIN32)
	// To get LONG defined
	#include "yltkWindows.h"
#elif defined(__APPLE__)
	// To get MAC_OS_X_VERSION_MIN_REQUIRED defined
	#include <AvailabilityMacros.h>
#endif

namespace yltk{
	/** \class LightObject
	* \brief Light weight base class for most itk classes.
	* 
	* LightObject is the highest level base class for most itk objects. It
	* implements reference counting and the API for object printing.
	* It can be used as a lightweight base class in preference to Object.
	* (LightObject does not support callbacks or modified time as Object
	* does.) All ITK objects should be a subclass of LightObject or Object
	* with few exceptions (due to performance concerns).
	*
	* \sa Object
	* \ingroup YLTKSystemObjects
	* \ingroup DataRepresentation
	*/
	class LightObject{
	public:
		/** Standard clas typedefs. */
		typedef LightObject               Self;
		typedef SmartPointer<Self>        Pointer;
		typedef SmartPointer<const Self>  ConstPointer;

		/** Method for creation through the object factory. */
		static Pointer New();

		/** Create an object from an instance, potentially deferring to a
		* factory.  This method allows you to create an instance of an
		* object that is exactly the same type as the referring object.
		* This is useful in cases where an object has been cast back to a
		* base class. */
		virtual Pointer CreateAnother() const;

		/** Delete an yltk object.  This method should always be used to delete an
		* object when the new operator was used to create it. Using the C
		*  delete method will not work with reference counting.  */
		virtual void Delete();

		/** Return the name of this class as a string. Used by the object factory
		* (implemented in New()) to instantiate objects of a named type. Also
		* used for debugging and other output information.  */
		virtual const char *GetNameOfClass() const {return "LightObject";}


#ifdef _WIN32
		/** Used to avoid dll boundary problems.  */
		void* operator new(size_t);
		void* operator new[](size_t);
		void operator delete(void*);
		void operator delete[](void*, size_t);
#endif
		/** Cause the object to print itself out. */
		void Print(std::ostream& os, Indent indent=0) const;

		/** This method is called when itkExceptionMacro executes. It allows 
		* the debugger to break on error.  */
		static void BreakOnError();

		/** Increase the reference count (mark as used by another object).  */
		virtual void Register() const;

		/** Decrease the reference count (release by another object).  */
		virtual void UnRegister() const;

		/** Gets the reference count on this object. */
		virtual int GetReferenceCount() const {return static_cast<int>(m_ReferenceCount);}

		/** Sets the reference count on this object. This is a dangerous
		* method, use it with care. */
		virtual void SetReferenceCount(int);

	protected:
		LightObject():m_ReferenceCount(1) {}
		virtual ~LightObject(); 

		/** Methods invoked by Print() to print information about the object
		* including superclasses. Typically not called by the user (use Print()
		* instead) but used in the hierarchical print process to combine the
		* output of several classes.  */
		virtual void PrintSelf(std::ostream& os, Indent indent) const;
		virtual void PrintHeader(std::ostream& os, Indent indent) const;
		virtual void PrintTrailer(std::ostream& os, Indent indent) const;

		/** Define the type of the reference count according to the
		target. This allows the use of atomic operations */
#if (defined(WIN32) || defined(_WIN32))
		typedef LONG InternalReferenceCountType;
#elif defined(__APPLE__) && (MAC_OS_X_VERSION_MIN_REQUIRED >= 1050)
#if defined (__LP64__) && __LP64__
		typedef volatile int64_t InternalReferenceCountType;
#else
		typedef volatile int32_t InternalReferenceCountType;
#endif
#elif defined(__GLIBCPP__) || defined(__GLIBCXX__)
		typedef _Atomic_word InternalReferenceCountType;
#else
		typedef int InternalReferenceCountType;
#endif
		
		/** Number of uses of this object by other objects. */
		mutable InternalReferenceCountType m_ReferenceCount;

		/** Mutex lock to protect modification to the reference count */
		mutable SimpleFastMutexLock m_ReferenceCountLock;
		
	private:
		LightObject(const Self&);	//purposely not implemented
		void operator=(const Self&);	//purposely not implemented

	};
}

#endif