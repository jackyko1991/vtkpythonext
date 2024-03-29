#ifndef __yltkExceptionObject_h
#define __yltkExceptionObject_h

#include "yltkSmartPointer.h"

namespace yltk{
	/** \class ExceptionObject
	* \brief Standard exception handling object.
	*
	* ExceptionObject provides standard methods for throwing
	* and managing exceptions in itk. Specific exceptions should be
	* derived from this class. Note that this class is derived from
	* std::exception, so an application can catch ITK exceptions as
	* std::exception if desired.
	*
	* ExceptionObject maintains two types of information: a location
	* and description (both of which are strings). The location is the
	* point in the code where the exception was thrown; the description
	* is an error message that describes the exception. The ExceptionObject
	* can be thrown explicitly in code, or more conveniently, the 
	* itkExceptionMacro (found in Common/itkMacro.h) can be used.
	*
	* \ingroup YLTKSystemObjects 
	*/
	class ExceptionObject : public std::exception
	{
	public:
		typedef std::exception Superclass;
		/** Various types of constructors.  Note that these functions will be
		* called when children are instantiated.  The default constructor and
		* the copy constructor of ExceptionObject never throw an exception. */
		ExceptionObject();
		explicit ExceptionObject(const char *file, unsigned int lineNumber=0,
			const char *desc="None", const char *loc="Unknown");
		explicit ExceptionObject(const std::string& file, unsigned int lineNumber=0,
			const std::string& desc="None",
			const std::string& loc="Unknown");
		ExceptionObject( const ExceptionObject &orig );

		/** Virtual destructor needed for subclasses. Has to have empty throw(). */
		virtual ~ExceptionObject() throw();

		/** Assignment operator. */
		ExceptionObject &operator= ( const ExceptionObject &orig );

		/** Equivalence operator. */
		virtual bool operator==( const ExceptionObject &orig );

		virtual const char *GetNameOfClass() const 
		{return "ExceptionObject";}

		/** Print exception information.  This method can be overridden by
		* specific exception subtypes.  The default is to print out the
		* location where the exception was first thrown and any description
		* provided by the ``thrower''.   */
		virtual void Print(std::ostream& os) const;

		/** Methods to get and set the Location and Description fields. The Set
		* methods are overloaded to support both std::string and const char 
		* array types. Get methods return const char arrays. */
		virtual void SetLocation(const std::string& s);
		virtual void SetDescription(const std::string& s);
		virtual void SetLocation(const char * s);
		virtual void SetDescription (const char *s);
		virtual const char *GetLocation()    const;
		virtual const char *GetDescription() const;

		/** What file did the exception occur in? */
		virtual const char *GetFile()    const;

		/** What line did the exception occur in? */
		virtual unsigned int GetLine() const;

		/** Provide std::exception::what() implementation. */
		virtual const char* what() const throw();

	private:
		/** \class ReferenceCounterInterface
		*
		*  Exception data.  Location of the error and description of the error.
		*
		*  Class hierarchy
		*
		*
		*           ReferenceCounterInterface (Register/UnRegister)
		*                     ^
		*                     |
		*               ExceptionData       LightObject (Register/UnRegister)
		*                     ^                  ^
		*                     |                  |
		*                   ReferenceCountedExceptionData (Register/UnRegister)
		*
		*
		*
		*  The ReferenceCounterInterface is an abstract class providing
		*  the API interface expected by the SmartPointer. Its second derived
		*  class, the ReferenceCountedExceptionData, double inherits from LightObject
		*  and ExceptionData, and overloads the Register()/UnRegister() methods to
		*  delegate them to its second parent, the LightObject.
		*
		*/
		class ReferenceCounterInterface
		{
		public:
			virtual void Register() const = 0;
			virtual void UnRegister() const = 0;
			ReferenceCounterInterface() {}
			virtual ~ReferenceCounterInterface() {}
		};
		class ExceptionData;
		class ReferenceCountedExceptionData;
		SmartPointer<const ReferenceCounterInterface> m_ExceptionData;
		const ExceptionData * GetExceptionData() const;
	};

	/** Generic inserter operator for ExceptionObject and its subclasses. */
	inline std::ostream& operator<<(std::ostream& os, ExceptionObject &e)
	{
		(&e)->Print(os);
		return os;
	}

	/**
	* Specific exception types that are subclasses of ExceptionObject follow
	*/

	/** \class MemoryAllocationError
	* Exception thrown when image memory allocation fails.
	* \ingroup ITKSystemObjects
	*/
	class MemoryAllocationError : public ExceptionObject
	{
	public:
		/** Default constructor.  Needed to ensure the exception object can be
		* copied. */
		MemoryAllocationError() : ExceptionObject() {}

		/** Constructor. Needed to ensure the exception object can be copied. */
		MemoryAllocationError(const char *file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {}

		/** Constructor. Needed to ensure the exception object can be copied. */
		MemoryAllocationError(const std::string& file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {}  

		/** Constructor. Needed to ensure the exception object can be copied. */
		MemoryAllocationError(const std::string& file, unsigned int lineNumber, const std::string& desc, const std::string& loc) : ExceptionObject(file, lineNumber, desc, loc) {}  

		/** Virtual destructor needed for subclasses. Has to have empty throw(). */
		virtual ~MemoryAllocationError() throw() {}

		virtual const char* GetNameOfClass() const
		{ return "MemoryAllocationError"; }
	};

	/** \class RangeError
	* Exception thrown when accessing memory out of range.
	* \ingroup ITKSystemObjects 
	*/
	class RangeError : public ExceptionObject
	{
	public:
		/** Default constructor.  Needed to ensure the exception object can be
		* copied. */
		RangeError() : ExceptionObject() {}

		/** Constructor. Needed to ensure the exception object can be copied. */
		RangeError(const char *file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {}

		/** Constructor. Needed to ensure the exception object can be copied. */
		RangeError(const std::string& file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {}  

		/** Virtual destructor needed for subclasses. Has to have empty throw(). */
		virtual ~RangeError() throw() {}

		virtual const char *GetNameOfClass() const 
		{return "RangeError";}

	};

	/** \class InvalidArgumentError
	* Exception thrown when invalid argument is given to a method
	* or function.
	* \ingroup ITKSystemObjects 
	*/
	class InvalidArgumentError : public ExceptionObject
	{
	public:
		/**
		* Default constructor.  Needed to ensure the exception object can be
		* copied.
		*/
		InvalidArgumentError() : ExceptionObject() {}

		/**
		* Constructor. Needed to ensure the exception object can be copied.
		*/
		InvalidArgumentError(const char *file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {}

		/**
		* Constructor. Needed to ensure the exception object can be copied.
		*/
		InvalidArgumentError(const std::string& file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {}  

		/** Virtual destructor needed for subclasses. Has to have empty throw(). */
		virtual ~InvalidArgumentError() throw() {}

		virtual const char *GetNameOfClass() const 
		{return "InvalidArgumentError";}
	};

	/** \class IncompatibleOperandsError
	* Exception thrown when two operands are incompatible.
	* \ingroup ITKSystemObjects 
	*/
	class IncompatibleOperandsError : public ExceptionObject
	{
	public:
		/** Default constructor.  Needed to ensure the exception object can be
		* copied. */
		IncompatibleOperandsError() : ExceptionObject() {}

		/** Constructor. Needed to ensure the exception object can be copied. */
		IncompatibleOperandsError(const char *file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {}

		/** Constructor. Needed to ensure the exception object can be copied. */
		IncompatibleOperandsError(const std::string& file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {}  

		/** Virtual destructor needed for subclasses. Has to have empty throw(). */
		virtual ~IncompatibleOperandsError() throw() {}

		virtual const char *GetNameOfClass() const 
		{return "IncompatibleOperandsError";}
	};

	/** \class ProcessAborted
	* Exception thrown when a filter (actually a ProcessObject) has been aborted.
	* \ingroup ITKSystemObjects 
	*/
	class ProcessAborted : public ExceptionObject
	{
	public:
		/** Default constructor.  Needed to ensure the exception object can be
		* copied. */
		ProcessAborted() : ExceptionObject() {
			this->SetDescription("Filter execution was aborted by an external request"); }

		/** Constructor. Needed to ensure the exception object can be copied. */
		ProcessAborted(const char *file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {
			this->SetDescription("Filter execution was aborted by an external request"); }

		/** Constructor. Needed to ensure the exception object can be copied. */
		ProcessAborted(const std::string& file, unsigned int lineNumber) : ExceptionObject(file, lineNumber) {  
			this->SetDescription("Filter execution was aborted by an external request"); }

		/** Virtual destructor needed for subclasses. Has to have empty throw(). */
		virtual ~ProcessAborted() throw() {}

		virtual const char *GetNameOfClass() const 
		{return "ProcessAborted";}

	};
}
#endif
